import os
from typing import Dict, Any

import numpy as np
import torch
import torch.nn as nn
from torch.utils import data
import torchvision.transforms as tt

from .final_future_prediction_with_memory_spatial_sumonly_weight_ranking_top1 import convAE
from .utils import (
    psnr,
    anomaly_score_list_inv
)
from rush.configs import weights_path, vad_detector_device


class VADDetector:
    def __init__(self):
        self.valid_transform = tt.ToTensor()
        self.loss_func_mse = nn.MSELoss(reduction='none')
        self.threshold = 0.8
        self.device = torch.device(f'cuda:{vad_detector_device}')
        self.model = convAE()
        self.model.load_state_dict(torch.load(str(weights_path.joinpath('vad_detector.pth')), map_location=self.device))
        self.m_items = torch.load(str(weights_path.joinpath('vad_detector_keys.pt')), map_location=self.device)

    @torch.no_grad()
    def one_step(self, data: Dict[str, Any]):
        dataset = FramesDataset(data['video'], self.valid_transform, 256, 256)
        psnr_list = list()
        mse_imgs = list()
        for frames in dataset:
            frames = frames.unsqueeze(0).to(self.device)
            (
                outputs, feas, updated_feas, self.m_items, softmax_score_query, softmax_score_memory,
                _, _, _, compactness_loss
            ) = self.model.forward(frames[:, 0:3*4], self.m_items, False)
            mse_img = self.loss_func_mse(
                (outputs[0]+1)/2, (frames[0, 3*4:]+1)/2)

            mse_loss=torch.mean(mse_img).item()
            psnr_list.append(psnr(mse_loss))
            mse_imgs.append(mse_img.permute(1, 2, 0).cpu().numpy())
        anomaly_score_total_list = anomaly_score_list_inv(psnr_list)

        return {
            'type': 'vad',
            'anomaly': bool(np.max(anomaly_score_total_list) > self.threshold),
            'frames': data['frames'][4:, ...],
            'pred': anomaly_score_total_list,
            'mse_imgs': mse_imgs,
            'sensors': data['sensors']
        }


class FramesDataset(data.Dataset):
    def __init__(self, frames, transform, resize_height, resize_width, time_step=4, num_pred=1):
        self.frames = frames
        self.transform = transform
        self._resize_height = resize_height
        self._resize_width = resize_width
        self._time_step = time_step
        self._num_pred = num_pred
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
