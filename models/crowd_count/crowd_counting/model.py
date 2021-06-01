import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from torch.autograd import Variable

from models.crowd_count.crowd_counting.misc.layer import Conv2d
from models.crowd_count.crowd_counting.misc.utils import *
# import pdb


class VGG(nn.Module):
    def __init__(self, pretrained=True):
        super(VGG, self).__init__()
        vgg = models.vgg16(pretrained=pretrained)
        # if pretrained:
        #     vgg.load_state_dict(torch.load(model_path))
        features = list(vgg.features.children())
        self.features4 = nn.Sequential(*features[0:23])

        self.de_pred = nn.Sequential(Conv2d(512, 128, 1, same_padding=True, NL='relu'),
                                     Conv2d(128, 1, 1, same_padding=True, NL='relu'))

    def forward(self, x):
        x = self.features4(x)
        x = self.de_pred(x)

        x = F.interpolate(x, scale_factor=8)

        return x


class net(nn.Module):
    def __init__(self, gpus):
        super(net, self).__init__()
        self.CCN = VGG()
        if len(gpus) > 1:
            self.CCN = torch.nn.DataParallel(self.CCN, device_ids=gpus).cuda()
        else:
            self.CCN = self.CCN.cuda()
        self.loss_mse_fn = nn.MSELoss().cuda()

    @property
    def loss(self):
        return self.loss_mse

    def forward(self, img, gt_map):

        den = self.CCN(img)
        self.loss_mse = self.build_loss(den.squeeze(), gt_map.squeeze())
        return den

    def build_loss(self, den, gt_data):
        loss_mse = self.loss_mse_fn(den, gt_data)
        return loss_mse

    def test_forward(self, img):
        density_map = self.CCN(img)
        return density_map
