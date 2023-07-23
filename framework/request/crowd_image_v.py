from typing import Dict, Any

from PIL import Image

from settings import crowd_img_path_v


class CrowdCountImageResourceV:
    def __init__(self):
        self.img_path = crowd_img_path_v
        self.img = Image.open(self.img_path).convert('RGB')

    def next(self) -> Image.Image:
        return self.img


def get_crowd_image_v() -> Dict[str, Any]:
    try:
        image = get_crowd_image_v.resource.next()
    except AttributeError:
        get_crowd_image_v.resource = CrowdCountImageResourceV()
        image = get_crowd_image_v.resource.next()
    return {
        'image': image,
        'sensor': 'virtual image'
    }
