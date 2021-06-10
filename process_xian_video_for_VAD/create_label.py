"""
The create_label.py is used to create frames label.
Before running create_label.py, please run count_frames.py and point out the abnormal frames.

The content of count_frames.txt is shown below:

dataset_name:
|------------|count_frames.txt:
 video_name, len_frame, start_frame, end_frame
------------------------------------------------
|test3     , 133      , 5          , 15        |
|test4     , 139      , 20         , 30        |
|test5 ...                                     |
------------------------------------------------

"""
import os
import numpy as np


def create_label(label_file, save_path):
    with open(label_file, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            try:
                video_name, len_frame, start_frame, end_frame = line.split(',')
            except:
                print('The range of abnormal frames has not been pointed out!')
                exit(0)
            label = np.zeros(int(len_frame))
            label[int(start_frame) : int(end_frame)] = 1
            if not os.path.exists(save_path): os.makedirs(save_path)
            np.save(os.path.join(save_path, video_name + '.npy'), label.astype(np.uint8))


if __name__ == '__main__':
    label_file = 'Dataset/test/count_frames.txt'
    save_path = 'Dataset/test/frames_label'
    create_label(label_file, save_path)
    print('Done!')
