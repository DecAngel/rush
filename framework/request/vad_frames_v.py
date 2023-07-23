import os
import glob
from collections import OrderedDict
from typing import Dict, Any

import numpy as np

from framework.request.utils import np_load_frame
from settings import vad_videos_dir


class VADFramesResource:
    def __init__(self) -> None:
        self.data_dir = vad_videos_dir
        self.cfg = {
            'resized_height': 256,
            'resized_width': 256
        }
        self.video_path_list = list()
        self.video_dict = OrderedDict()
        self.setup()

        self.cur_idx = 0
        self.length = len(self.video_path_list)

    def next(self):
        video_name = self.video_path_list[self.cur_idx]
        frames = list(map(
            lambda img_path: np_load_frame(img_path, (self.cfg['resized_width'], self.cfg['resized_height'])),
            self.video_dict[video_name]['frame'])
        )
        self.cur_idx = (self.cur_idx + 1) % self.length
        return np.array(frames)

    def setup(self):
        self.video_path_list = glob.glob(os.path.join(self.data_dir, '*'))
        self.video_path_list.sort()
        for video_path in sorted(self.video_path_list):
            self.video_dict[video_path] = {}
            self.video_dict[video_path]['path'] = video_path
            self.video_dict[video_path]['frame'] = glob.glob(os.path.join(video_path, '*.jpg'))
            self.video_dict[video_path]['frame'].sort()
            self.video_dict[video_path]['length'] = len(self.video_dict[video_path]['frame'])


def get_vad_frames_v() -> Dict[str, Any]:
    try:
        frame_array = get_vad_frames_v.resource.next()
    except AttributeError:
        get_vad_frames_v.resource = VADFramesResource()
        frame_array = get_vad_frames_v.resource.next()
    return {
        'frames': frame_array,
        'sensor': 'virtual video'
    }
