from typing import Dict

from PIL import Image

from urls import crowd_img_path, mode


class CrowdCountImageResource:
    def __init__(self) -> None:
        self.img_path = crowd_img_path
        self.img = Image.open(self.img_path).convert('RGB')

        # self.cur_idx = 0
        # self.length = len(self.valid_ds)

    def next(self):
        return self.img


if mode == 'run':
    crowd_count_img_resource = CrowdCountImageResource()


def get_crowd_image_v() -> Dict[str, object]:
    image = crowd_count_img_resource.next()
    return {
        'image': image,
        'sensor': 'virtual image'
    }
