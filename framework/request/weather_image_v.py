import os
import glob

import numpy
from PIL import Image

from framework.request.utils import np_load_frame
# fire_image_dir = '/home/yuanyu/projects/rush/models/fire_classification/data/testingsamples'
from models.weather_classification.wcyy.data import create_full_dataset, log_dateset_info
from urls import wc_classes, wc_image_dir


class WeatherImageResource:
    def __init__(self) -> None:
        self.cfg = {
            'classes': wc_classes,
            'data_dir': wc_image_dir,
            'transform': 'tt_none'
        }
        self.dataset = create_full_dataset(self.cfg)
        num_classes = len(self.dataset.classes)
        print('wc dataset'.center(100, '-'))
        log_dateset_info(self.dataset)
        # valid_dl = DeviceDataLoader(
        #     DataLoader(valid_ds, 1, num_workers=2, pin_memory=True),
        #     cfg['device'])
        # self.imgs = glob.glob(os.path.join(fire_image_dir, '*.jpg'))
        # self.imgs.sort()
        self.cur_idx = 0
        # self.length = len(self.imgs)
        self.length = len(self.dataset)

    def next(self):
        # img_path = self.imgs[self.cur_idx]
        # img = Image.open(img_path)
        img, label = self.dataset[self.cur_idx]
        self.cur_idx = (self.cur_idx + 1) % self.length

        return img, label


weatherImageResource = WeatherImageResource()


def get_weather_image_v() -> Image.Image:
    image, label = weatherImageResource.next()
    return {
        'image': image,
        'label': label,
        'sensor': 'virtual image'
    }