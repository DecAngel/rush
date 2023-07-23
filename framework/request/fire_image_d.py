from typing import Dict, Any

from models.fire_classification.fc.data import create_dataset
from settings import fire_image_dir


class FireImageResourceD:
    def __init__(self) -> None:
        self.data_dir = fire_image_dir
        self.cfg = {
            'train': False,
            'train_ann_file_path': self.data_dir + '/annotation_for_train.txt',
            'valid_ann_file_path': self.data_dir + '/annotation_for_valid.txt',
            'train_transform': 'tt_none',
            'valid_transform': 'tt_none'
        }
        self.valid_ds = create_dataset(self.cfg, train=False)
        self.cur_idx = 0
        self.length = len(self.valid_ds)

    def next(self):
        img, label = self.valid_ds[self.cur_idx]
        self.cur_idx = (self.cur_idx + 1) % self.length
        return img, label


def get_fire_image_d() -> Dict[str, Any]:
    try:
        image, label = get_fire_image_d.resource.next()
    except AttributeError:
        get_fire_image_d.resource = FireImageResourceD()
        image, label = get_fire_image_d.resource.next()
    return {
        'image': image,
        'label': label,
        'sensors': [
            'virtual image',
            'virtual Thermo',
            'CO2'
        ]
    }
