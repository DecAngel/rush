import os
from typing import Dict

import torch
import torchvision.transforms as tt

from models.fire_classification.fc.utils.device import to_device, get_default_device
from models.fire_classification.fc.models import create_model
from urls import fire_detection_model_root

class FireDetector:
    def __init__(self) -> None:
        stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.cfg = {
            'model_root': fire_detection_model_root,
            'ckpt': 'model_epoch7.ckpt',
            'pretrained_model': 'efficientnet_b3a',
            'model': 'TimmFC3CLF',
            'pretrained': True,
            'device': get_default_device(),
            'valid_transform': tt.Compose([tt.Resize([256, 256]), tt.ToTensor(), tt.Normalize(*stats)])
        }
        self.classes = ['safe', 'fire']
        self.model = self.init_model()

    @torch.no_grad()
    def one_step(self, data: Dict[str, object]):
        image = self.cfg['valid_transform'](data['image'])
        image = torch.unsqueeze(image, 0).to(self.cfg['device'])

        # import matplotlib.pyplot as plt
        # from torchvision.utils import make_grid
        # fig, ax = plt.subplots(figsize=(12, 12))
        # ax.set_xticks([])
        # ax.set_yticks([])
        # ax.imshow(make_grid(image.cpu()[:], nrow=1).permute(1, 2, 0))
        # plt.show()

        output = self.model(image)
        _, pred = torch.max(output, dim=1)
        # print(f'output: {output}, pred: {pred}')
        pred = pred.item()

        return {
            'type': 'fire',
            'anomaly': pred == 1,
            'pred': pred,
            'label': data['label'].item(),
            'sensors': data['sensors'],
            'data': data
        }

    def init_model(self):
        model = to_device(create_model(self.cfg, 2), self.cfg['device'])
        model_ckpt = torch.load(os.path.join(
            self.cfg['model_root'], self.cfg['ckpt']))
        model.load_state_dict(model_ckpt)
        model.eval()

        return model
