from typing import Dict, Any

import torch
import torchvision.transforms as tt

from .timm_clf import TimmFC3CLF
from rush.configs import weights_path, fire_detector_device


class FireDetector:
    def __init__(self):
        stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.valid_transform = tt.Compose([tt.Resize([256, 256]), tt.ToTensor(), tt.Normalize(*stats)])
        self.classes = ['safe', 'fire']
        self.device = torch.device(f'cuda:{fire_detector_device}')
        self.model = TimmFC3CLF(2, 'efficientnet_b3a', False)
        self.model.load_state_dict(torch.load(str(weights_path.joinpath('fire_detector.ckpt'))))
        self.model = self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def one_step(self, data: Dict[str, Any]):
        image = self.valid_transform(data['image'])
        image = torch.unsqueeze(image, 0).to(self.device)

        output = self.model(image)
        _, pred = torch.max(output, dim=1)
        pred = pred.item()

        return {
            'type': 'fire',
            'anomaly': pred == 1,
            'pred': pred,
            'label': data['label'],
            'sensors': data['sensors'],
            'data': data
        }
