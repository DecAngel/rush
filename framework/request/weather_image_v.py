from typing import Dict, Any

from models.weather_classification.wcyy.data import create_full_dataset, log_dateset_info
from settings import wc_classes, wc_image_dir


class WeatherImageResource:
    def __init__(self) -> None:
        self.cfg = {
            'classes': wc_classes,
            'data_dir': wc_image_dir,
            'transform': 'tt_none'
        }
        self.dataset = create_full_dataset(self.cfg)
        print('wc dataset'.center(100, '-'))
        log_dateset_info(self.dataset)
        self.cur_idx = 0
        self.length = len(self.dataset)

    def next(self):
        img, label = self.dataset[self.cur_idx]
        self.cur_idx = (self.cur_idx + 1) % self.length

        return img, label


def get_weather_image_v() -> Dict[str, Any]:
    try:
        image, label = get_weather_image_v.resource.next()
    except AttributeError:
        get_weather_image_v.resource = WeatherImageResource()
        image, label = get_weather_image_v.resource.next()
    return {
        'image': image,
        'label': label,
        'sensor': 'virtual image'
    }
