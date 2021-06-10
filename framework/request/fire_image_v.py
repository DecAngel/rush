from typing import Dict

from models.fire_classification.fc.data import create_dataset, DeviceDataLoader, log_dateset_info
from urls import fire_image_dir


class FireImageResource:
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
        num_classes = len(self.valid_ds.classes)
        print('test_ds'.center(100, '-'))
        log_dateset_info(self.valid_ds)
        # valid_dl = DeviceDataLoader(
        #     DataLoader(valid_ds, 1, num_workers=2, pin_memory=True),
        #     cfg['device'])
        # self.imgs = glob.glob(os.path.join(fire_image_dir, '*.jpg'))
        # self.imgs.sort()
        self.cur_idx = 0
        # self.length = len(self.imgs)
        self.length = len(self.valid_ds)

    def next(self):
        # img_path = self.imgs[self.cur_idx]
        # img = Image.open(img_path)
        img, label = self.valid_ds[self.cur_idx]
        self.cur_idx = (self.cur_idx + 1) % self.length

        return img, label


fireImageResource = FireImageResource()


def get_fire_image_v() -> Dict[str, object]:
    image, label = fireImageResource.next()
    return {
        'image': image,
        'label': label,
        'sensors': [
            'virtual image',
            'virtual Thermo',
            'CO2'
        ]
    }