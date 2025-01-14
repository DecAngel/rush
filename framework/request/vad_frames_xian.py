import os
import glob
from pathlib import Path
from collections import OrderedDict
from typing import Dict, Any

import numpy as np
import pandas as pd

from framework.request.utils import np_load_frame
from settings import vad_xian_videos_dir, vad_xian_label_df_path


class VADFramesResource:
    def __init__(self, train=False) -> None:
        self.dir = Path(vad_xian_videos_dir)
        self.label_df = self.label_df = pd.read_csv(
            vad_xian_label_df_path, index_col=0)
        self.cfg = {
            'resized_height': 256,
            'resized_width': 256
        }
        # split train n test
        self.train = train
        self.video_path_list = glob.glob(str(self.dir / '*'))

        self.train_video_path_list, self.test_video_path_list = self.split_train_n_test(
            self.video_path_list, self.label_df)

        self.video_path_list = self.train_video_path_list if self.train else self.test_video_path_list
        self.video_dict = OrderedDict()
        self.setup()

        self.cur_idx = 0
        self.length = len(self.video_path_list)

    def next(self):
        video_name = self.video_name_list[self.cur_idx]

        frames = list(map(
            lambda img_path: np_load_frame(img_path, (self.cfg['resized_width'], self.cfg['resized_height'])),
            self.video_dict[video_name]['frame'])
        )

        self.cur_idx = (self.cur_idx + 1) % self.length
        return np.array(frames)

    def setup(self):
        self.video_name_list = list()
        for video in sorted(self.video_path_list):
            video_name = video.split('/')[-1]
            self.video_name_list.append(video_name)
            self.video_dict[video_name] = {}
            self.video_dict[video_name]['path'] = video
            self.video_dict[video_name]['frame'] = glob.glob(os.path.join(video, '*.jpg'))
            self.video_dict[video_name]['frame'].sort()
            self.video_dict[video_name]['length'] = len(self.video_dict[video_name]['frame'])

    def get_all_samples(self):
        videos = self.train_video_path_list if self.train else self.test_video_path_list
        frames = []
        for video in sorted(videos):
            video_name = video.split('/')[-1]
            for i in range(len(self.videos[video_name]['frame'])-self._time_step-self._num_pred):
                frames.append(self.videos[video_name]['frame'][i])

        return frames

    def split_train_n_test(self, video_path_list, label_df):
        train_list, test_list = list(), list()

        anomal_video_path_set = set(label_df.new_video)
        # print(anomal_video_path_set)
        for video_path in video_path_list:
            if str(video_path).split('/')[-1] in anomal_video_path_set:
                # print(str(video_path).split('/')[-1])
                test_list.append(video_path)
            else:
                train_list.append(video_path)

        return train_list, test_list


def get_vad_frames_xian() -> Dict[str, Any]:
    try:
        frame_array = get_vad_frames_xian.resource.next()
    except AttributeError:
        get_vad_frames_xian.resource = VADFramesResource()
        frame_array = get_vad_frames_xian.resource.next()
    return {
        'frames': frame_array,
        'sensor': 'virtual video'
    }
