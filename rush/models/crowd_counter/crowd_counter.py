import numpy as np
import torch
import torchvision.transforms as standard_transforms

from .model import CrowdCountingNet
from rush.configs import weights_path, crowd_counter_device


class CrowdCounter:
    def __init__(self):
        self.mean_std = (
            [0.49254346, 0.47839335, 0.50212276],
            [0.20278716, 0.19684295, 0.2028682]
        )
        self.cfg = {
            'device': torch.device(f'cuda:{crowd_counter_device}'),
            'img_transform': standard_transforms.Compose([
                standard_transforms.ToTensor(),
                standard_transforms.Normalize(*self.mean_std)
            ]),
            'model_path': str(weights_path.joinpath('crowd_counter.pth')),
        }
        self.crowd_counter_model = CrowdCountingNet(pretrained=False)
        self.crowd_counter_model.load_state_dict(
            {k.replace('CCN.module', 'cnn'): v for k, v in torch.load(self.cfg['model_path']).items()}, True
        )
        self.crowd_counter_model.to(self.cfg['device'])
        self.crowd_counter_model.eval()

    @torch.no_grad()
    def one_step(self, data):
        img = self.cfg['img_transform'](data['image'])[None, ...]
        img = img.to(self.cfg['device'])
        pred_map = self.crowd_counter_model.test_forward(img)
        pred_map = pred_map.cpu().data.numpy()[0, 0, :, :]
        pred = np.sum(pred_map)/100.0
        pred_map = pred_map/np.max(pred_map+1e-20)
        return {
            'type': 'crowd',
            'anomaly': False,
            'pred': (pred, pred_map),
            'sensors': data['sensors']
        }
