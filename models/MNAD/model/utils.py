from collections import OrderedDict
from pathlib import Path
import os
import glob
import cv2

import numpy as np
import pandas as pd
import torch.utils.data as data


rng = np.random.RandomState(2020)


def np_load_frame(filename, resize_height, resize_width):
    """
    Load image path and convert it to numpy.ndarray. Notes that the color channels are BGR and the color space
    is normalized from [0, 255] to [-1, 1].

    :param filename: the full path of image
    :param resize_height: resized height
    :param resize_width: resized width
    :return: numpy.ndarray
    """
    image_decoded = cv2.imread(filename)
    image_resized = cv2.resize(image_decoded, (resize_width, resize_height))
    image_resized = image_resized.astype(dtype=np.float32)
    image_resized = (image_resized / 127.5) - 1.0
    return image_resized


class CustomDataLoader(data.Dataset):
    def __init__(self, video_folder, transform, resize_height, resize_width, time_step=4, num_pred=1):
        self.dir = video_folder
        self.transform = transform
        self.videos = OrderedDict()
        self._resize_height = resize_height
        self._resize_width = resize_width
        self._time_step = time_step
        self._num_pred = num_pred
        self.setup()
        self.samples = self.get_all_samples()
        print('samples:')
        print(len(self.samples))
        # print(self.samples )

    def setup(self):
        videos = glob.glob(os.path.join(self.dir, '*'))
        for video in sorted(videos):
            video_name = video.split('/')[-1]
            self.videos[video_name] = {}
            self.videos[video_name]['path'] = video
            self.videos[video_name]['frame'] = glob.glob(
                os.path.join(video, '*.jpg'))
            self.videos[video_name]['frame'].sort()
            self.videos[video_name]['length'] = len(
                self.videos[video_name]['frame'])

    def get_all_samples(self):
        frames = []
        videos = glob.glob(os.path.join(self.dir, '*'))
        for video in sorted(videos):
            video_name = video.split('/')[-1]
            for i in range(len(self.videos[video_name]['frame'])-self._time_step-self._num_pred):
                frames.append(self.videos[video_name]['frame'][i])

        return frames

    def __getitem__(self, index):
        # try:
        video_name = self.samples[index].split('/')[-2]
        frame_name = int(self.samples[index].split('/')[-1].split('.')[-2])

        batch = []
        for i in range(self._time_step+self._num_pred):
            image = np_load_frame(
                self.videos[video_name]['frame'][frame_name+i], self._resize_height, self._resize_width)
            if self.transform is not None:
                batch.append(self.transform(image))
        # except Exception as e:
        #     print(e)
        #     print(index, video_name, self.videos[video_name]['length'], frame_name+i, self.videos[video_name]['frame'][frame_name+i-1])

        return np.concatenate(batch, axis=0)

    def __len__(self):
        return len(self.samples)


class CustomDataLoader(data.Dataset):
    def __init__(self, video_folder, transform, resize_height, resize_width, label_file_path, time_step=4, num_pred=1, train=True):
        # split train n test
        self.train = train
        self.dir = Path(video_folder)
        self.video_path_list = sorted(glob.glob(str(self.dir / '*')))
        self.label_df = pd.read_csv(label_file_path, index_col=0)
        self.train_video_path_list, self.test_video_path_list = self.split_train_n_test(self.video_path_list, self.label_df)

        self.transform = transform
        self.videos = OrderedDict()
        self._resize_height = resize_height
        self._resize_width = resize_width
        self._time_step = time_step
        self._num_pred = num_pred
        self.setup()
        self.samples = self.get_all_samples()
        # print('samples:')
        # print(len(self.samples))
        # print(self.samples)

    def setup(self):
        videos = self.train_video_path_list if self.train else self.test_video_path_list
        for video in sorted(videos):
            video_name = video.split('/')[-1]
            self.videos[video_name] = {}
            self.videos[video_name]['path'] = video
            self.videos[video_name]['frame'] = glob.glob(
                os.path.join(video, '*.jpg'))
            self.videos[video_name]['frame'].sort()
            self.videos[video_name]['length'] = len(
                self.videos[video_name]['frame'])

    # TO DO
    def get_all_samples(self):
        videos = self.train_video_path_list if self.train else self.test_video_path_list
        frames = []
        for video in sorted(videos):
            video_name = video.split('/')[-1]
            for i in range(len(self.videos[video_name]['frame'])-self._time_step-self._num_pred):
                frames.append(self.videos[video_name]['frame'][i])

        # frames.sort()
        return frames
    
    def split_train_n_test(self, video_path_list, label_df):
        train_list, test_list = list(), list()

        anomal_video_path_set = set(label_df.new_video)
        # print(anomal_video_path_set)
        for video_path in video_path_list:
            # if str(video_path).split('/')[-1] in anomal_video_path_set:
            #     # print(str(video_path).split('/')[-1])
            #     test_list.append(video_path)
            # else:
            #     train_list.append(video_path)
            test_list.append(video_path)
        print(len(train_list), len(test_list))
        return train_list, test_list

    def __getitem__(self, index):
        # try:
        video_name = self.samples[index].split('/')[-2]
        frame_idx = int(self.samples[index].split('/')[-1].split('.')[-2].split('_')[-1])

        batch = []
        for i in range(self._time_step+self._num_pred):
            image = np_load_frame(
                self.videos[video_name]['frame'][frame_idx+i], self._resize_height, self._resize_width)
            if self.transform is not None:
                image = self.transform(image)
            batch.append(image)
        # except Exception as e:
        #     print(e)
        #     print(index, video_name, self.videos[video_name]['length'], frame_name+i, self.videos[video_name]['frame'][frame_name+i-1])

        return np.concatenate(batch, axis=0)

    def __len__(self):
        return len(self.samples)