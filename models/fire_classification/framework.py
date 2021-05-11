import os

import torch

from models.fire_classification.fc.utils.device import to_device, get_default_device
from models.fire_classification.fc.models import create_model
import models.fire_classification.config as config


class FireDetector:
    def __init__(self) -> None:
        self.cfg = {
            'model_root': '/home/yuanyu/projects/rush/models/fire_classification/runs/exp-efficientnet_b3a_e11_b16_tt6_vt3_explr_TimmFC3CLF_freeze_Adam',
            'ckpt': 'model.ckpt',
            'pretrained_model': 'efficientnet_b3a',
            'model': 'TimmFC3CLF',
            'device': get_default_device(),
            'valid_transform': getattr(config, 'vt3'),
        }
        self.model = self.init_model()

    def one_step(self, data):
        pass

    def init_model(self):
        model = to_device(create_model(self.cfg, 2), self.cfg['device'])
        model_ckpt = torch.load(os.path.join(self.cfg['model_root'], self.cfg['ckpt']))
        model.load_state_dict(model_ckpt)
