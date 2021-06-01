import numpy as np
import torch
from torch.autograd import Variable
import torchvision.transforms as standard_transforms

from models.crowd_count.crowd_counting.model import net
from models.weather_classification.wcyy.utils.device import get_default_device
from urls import crowd_count_model_path, crowd_count_gpus


class CrowdCounter():
    def __init__(self):
        # torch.cuda.set_device(0)
        self.mean_std = ([0.49254346, 0.47839335, 0.50212276], [
                         0.20278716, 0.19684295, 0.2028682])
        self.cfg = {
            'device': get_default_device(),
            'img_transform': standard_transforms.Compose([
                standard_transforms.ToTensor(),
                standard_transforms.Normalize(*self.mean_std)
            ]),
            'model_path': crowd_count_model_path,
            'gpus': crowd_count_gpus
        }
        torch.backends.cudnn.benchmark = True
        self.crowd_counter_model = net(gpus=self.cfg['gpus'])
        self.crowd_counter_model.load_state_dict(
            torch.load(self.cfg['model_path']), False)
        self.crowd_counter_model.to(self.cfg['device'])
        self.crowd_counter_model.eval()

    def one_step(self, data):
        img = self.cfg['img_transform'](data['image'])
        with torch.no_grad():
            img = Variable(img[None, :, :, :]).to(self.cfg['device'])
            pred_map = self.crowd_counter_model.test_forward(img)
        pred_map = pred_map.cpu().data.numpy()[0, 0, :, :]
        pred = np.sum(pred_map)/100.0
        pred_map = pred_map/np.max(pred_map+1e-20)
        # pred 人数 pred_map 密度图
        # torch.set_printoptions(profile="full")
        # print(pred)
        # print(pred_map.shape)
        # print(pred_map)
        return {
            'type': 'crowd',
            'anomaly': False,
            'pred': (pred, pred_map),
            'sensors': data['sensors']
        }