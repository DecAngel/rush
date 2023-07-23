import os
from typing import Dict

import torch
import torchvision.transforms as tt

from models.fire_classification.fc.models import create_model
from settings import fire_detection_model_dir, fire_device


class FireDetector:
    def __init__(self) -> None:
        stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.cfg = {
            'model_root': fire_detection_model_dir,
            'ckpt': 'model_epoch7.ckpt',
            'pretrained_model': 'efficientnet_b3a',
            'model': 'TimmFC3CLF',
            'pretrained': False,
            'device': torch.device(f'cuda:{fire_device}'),
            'valid_transform': tt.Compose([tt.Resize([256, 256]), tt.ToTensor(), tt.Normalize(*stats)])
        }
        self.classes = ['safe', 'fire']
        self.model = self.init_model()

    @torch.no_grad()
    def one_step(self, data: Dict[str, object]):
        image = self.cfg['valid_transform'](data['image'])
        image = torch.unsqueeze(image, 0).to(self.cfg['device'])

        output = self.model(image)
        _, pred = torch.max(output, dim=1)
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
        model = create_model(self.cfg, 2).to(self.cfg['device'])
        model_ckpt = torch.load(os.path.join(self.cfg['model_root'], self.cfg['ckpt']))
        model.load_state_dict(model_ckpt)
        model.eval()

        return model
