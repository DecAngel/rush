from typing import Iterable, Iterator, Dict, Any

import cv2
import numpy as np
from PIL import Image

from rush.configs import demo_path
from rush.utils.logger import rush_logger


class _DemoSource(Iterable[Dict[str, Any]]):
    def __init__(self):
        self.data = self.get_data()
        rush_logger.info(f'{self.__class__} loading complete!')

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        while True:
            yield self.data

    def get_data(self) -> Dict[str, Any]:
        raise NotImplementedError()


class CrowdCounterDemoSource(_DemoSource):
    def get_data(self) -> Dict[str, Any]:
        return {
            'image': Image.open(str(demo_path.joinpath('crowd_counter.jpg'))).convert('RGB'),
            'sensor': 'crowd counter demo image',
            'anomaly': True,
        }


class FireDetectorDemoSource(_DemoSource):
    def get_data(self) -> Dict[str, Any]:
        return {
            'image': Image.open(str(demo_path.joinpath('fire_detector.jpg'))),
            'label': int(demo_path.joinpath('fire_detector.txt').read_text()),
            'sensor': 'fire detector demo image',
            'anomaly': True,
        }


class PVCDetectorDemoSource(_DemoSource):
    def get_data(self) -> Dict[str, Any]:
        video = []
        for file in sorted(demo_path.joinpath('vad_detector').iterdir()):
            image = cv2.imread(str(file))
            image = cv2.resize(image, (256, 256))
            image = image.astype(dtype=np.float32)
            video.append(image)
        return {
            'video': video,
            'sensor': 'pvc detector demo video',
            'anomaly': True,
        }
