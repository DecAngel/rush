import torch.nn.functional as F
from torchvision import models

from .layer import Conv2d
from .utils import *


class VGG(nn.Module):
    def __init__(self, pretrained=True):
        super(VGG, self).__init__()
        vgg = models.vgg16(pretrained=pretrained)
        features = list(vgg.features.children())
        self.features4 = nn.Sequential(*features[0:23])

        self.de_pred = nn.Sequential(Conv2d(512, 128, 1, same_padding=True, NL='relu'),
                                     Conv2d(128, 1, 1, same_padding=True, NL='relu'))

    def forward(self, x):
        x = self.features4(x)
        x = self.de_pred(x)

        x = F.interpolate(x, scale_factor=8)

        return x


class CrowdCountingNet(nn.Module):
    def __init__(self, pretrained=True):
        super(CrowdCountingNet, self).__init__()
        self.cnn = VGG(pretrained=pretrained)
        self.loss_mse_fn = nn.MSELoss()

    @property
    def loss(self):
        return self.loss_mse

    def forward(self, img, gt_map):
        den = self.cnn(img)
        self.loss_mse = self.build_loss(den.squeeze(), gt_map.squeeze())
        return den

    def build_loss(self, den, gt_data):
        loss_mse = self.loss_mse_fn(den, gt_data)
        return loss_mse

    def test_forward(self, img):
        density_map = self.cnn(img)
        return density_map
