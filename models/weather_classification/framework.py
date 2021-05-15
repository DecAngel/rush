import os
from typing import Dict

import torch
import torchvision.transforms as tt

from models.weather_classification.wcyy.utils.device import to_device, get_default_device
from models.weather_classification.wcyy.models import create_model
from urls import (
    wc_model_root,
    wc_classes
)


class WeatherClassifier:
    def __init__(self) -> None:
        stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.cfg = {
            'model_root': wc_model_root,
            'ckpt': 'model.ckpt',
            'pretrained_model': 'efficientnet_b3a',
            'model': 'TimmFC3CLF',
            'pretrained': True,
            'device': get_default_device(),
            'valid_transform': tt.Compose([tt.Resize([320, 320]), tt.ToTensor(), tt.Normalize(*stats)])
        }
        self.classes = wc_classes
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
            'type': 'weather',
            'anomaly': pred in [0, 1, 2],
            'pred': self.classes[pred],
            'label': self.classes[data.get('label', None)],
            'sensors': data['sensors']
        }

    def init_model(self):
        model = to_device(create_model(
            self.cfg, len(self.classes)), self.cfg['device'])
        model_ckpt = torch.load(os.path.join(
            self.cfg['model_root'], self.cfg['ckpt']))
        model.load_state_dict(model_ckpt)
        model.eval()

        return model
