import os
from typing import Dict

import numpy as np
import torch
import torch.nn as nn
from torch.utils import data
import torchvision.transforms as tt

from models.fire_classification.fc.utils.device import to_device, get_default_device
from models.MNAD.utils import (
    psnr,
    # anomaly_score_list
    anomaly_score_list_inv
)
from urls import (
    vad_model_dir,
    vad_mitems_dir
)


class VideoAnomalyDetector:
    def __init__(self) -> None:
        stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.cfg = {
            'model_dir': vad_model_dir,
            'mitems_dir': vad_mitems_dir,
            'device': get_default_device(),
            'valid_transform': tt.Compose([tt.ToTensor()]),
            'loss_func_mse': nn.MSELoss(reduction='none'),
            'th': 0.8
        }
        self.model, self.m_items=self.init_model()

    @torch.no_grad()
    def one_step(self, data: Dict[str, object]):
        dataset = FramesDataset(data['frames'], self.cfg['valid_transform'], 256, 256)
        psnr_list = list()
        anomaly_score_total_list = list()
        mse_imgs = list()
        for frames in dataset:
            frames = frames.unsqueeze(0).to(self.cfg['device'])
            
            outputs, feas, updated_feas, self.m_items, softmax_score_query, softmax_score_memory, _, _, _, compactness_loss=self.model.forward(
                frames[:, 0:3*4], self.m_items, False)
            mse_img=self.cfg['loss_func_mse'](
                (outputs[0]+1)/2, (frames[0, 3*4:]+1)/2)

            mse_loss=torch.mean(mse_img).item()
            # mse_feas=compactness_loss.item()
            psnr_list.append(psnr(mse_loss))
            mse_imgs.append(mse_img.permute(1, 2, 0).cpu().numpy())
        anomaly_score_total_list = anomaly_score_list_inv(psnr_list)

        # mse_imgs = torch.stack(mse_imgs, 0)
        # print(mse_imgs.shape)
        # print(mse_imgs[0])
        # import matplotlib.pyplot as plt
        # from torchvision.utils import make_grid
        # fig, ax = plt.subplots(figsize=(12, 12))
        # ax.set_xticks([])
        # ax.set_yticks([])
        # ax.imshow(make_grid(mse_imgs.cpu()[:], nrow=32, normalize=True).permute(1, 2, 0))
        # fig2, ax2 = plt.subplots(figsize=(12, 12))
        # ax2.plot(anomaly_score_total_list, color='r')
        # plt.show()

        # print(len(data['frames']))
        # print(len(mse_imgs))
        return {
            'type': 'vad',
            'anomaly': bool(np.max(anomaly_score_total_list) > self.cfg['th']),
            'frames': data['frames'][4:, ...],
            'pred': anomaly_score_total_list,
            'mse_imgs': mse_imgs,
            # 'label': data['label'].item(),
            'sensors': data['sensors']
        }

    def init_model(self):
        model=to_device(torch.load(self.cfg['model_dir']), self.cfg['device'])
        model.eval()
        m_items=to_device(torch.load(
            self.cfg['mitems_dir']), self.cfg['device'])

        return model, m_items


class FramesDataset(data.Dataset):
    def __init__(self, frames, transform, resize_height, resize_width, time_step=4, num_pred=1):
        self.frames = frames
        self.transform = transform
        self._resize_height = resize_height
        self._resize_width = resize_width
        self._time_step = time_step
        self._num_pred = num_pred
        # print('VAD', self.frames.shape, type(self.frames.shape))
        self.length = self.frames.shape[0] - self._time_step - self._num_pred

    def __getitem__(self, index):
        frames = list()

        for i in range(self._time_step+self._num_pred):
            image = self.frames[index + i]
            image = (image / 127.5) - 1.0

            if self.transform is not None:
                frames.append(self.transform(image))

        return torch.Tensor(np.concatenate(frames, axis=0))

    def __len__(self):
        return self.length
