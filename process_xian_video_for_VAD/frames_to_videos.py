"""
The frames_to_videos.py is used to convert frames to videos by using multipocessing and cv2.

The structure of frames is shown below:

dataset_name:
|------------|frames(pictures):
|------------------|video1:
|------------------------|: frame1(picture1)
|------------------------|: frame2(picture2) ...
|------------------|video2:
|------------------------|: frame1(picture1)
|------------------------|: frame2(picture2) ...

The structure of videos is shown below:

dataset_name:
|------------|videos_from_frames:
|------------------|: video1
|------------------|: video2
|------------------|: video3
|------------------|: video4 ...

"""
import os
import cv2
import imageio
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool


def frames2videos(frame_list, target_video, four_cc, fps, start, end, target_shape):
    if len(frame_list) < 1: return

    if target_shape == None:
        f_height, f_width, _ = frame_list[0].shape
    else:
        f_height, f_width = int(target_shape[0]), int(target_shape[1])

    start = int(len(frame_list) * start)
    end = int(len(frame_list) * end)
    video_writer = cv2.VideoWriter(target_video, four_cc, fps, (f_width, f_height))

    while start < end:
        frame = cv2.resize(frame_list[start], (f_width, f_height), interpolation=cv2.INTER_LINEAR)
        video_writer.write(frame)
        start += 1


def frames_to_videos(args):
    video_name, frames_path, save_path, file_type, start, end, target_shape = args
    video_path = os.path.join(frames_path, video_name)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    rgb_list, flow_list, flow_x_list, flow_y_list = [], [], [], []
    for frame_name in os.listdir(video_path):
        frame = cv2.imread(os.path.join(video_path, frame_name))
        if 'flow_x' in frame_name:
            flow_x_list.append(frame[..., 0])
        elif 'flow_y' in frame_name:
            flow_y_list.append(frame[..., 0])
        else:
            rgb_list.append(frame)

    for i in range(len(flow_x_list)):
        flow_frame = np.zeros_like(rgb_list[0])
        flow_frame[..., 2] = flow_x_list[i]
        flow_frame[..., 0] = flow_y_list[i]
        flow_frame[..., 1] = 255 // 2
        flow_list.append(flow_frame)

    if file_type == 'avi':
        four_cc = cv2.VideoWriter_fourcc(*'H264')

    rgb_video = os.path.join(save_path, '{}.{}'.format(video_name, file_type))
    flow_video = os.path.join(save_path, '{}_flow.{}'.format(video_name, file_type))
    frames2videos(rgb_list, rgb_video, four_cc, 25)
    frames2videos(flow_list, flow_video, four_cc, 25)


if __name__ == '__main__':
    frames_path = 'Dataset/test/frames'
    save_path = 'Dataset/test/videos_from_frames'
    videos_name = os.listdir(frames_path)
    videos_num = len(videos_name)
    file_type = 'avi'
    start = 0
    end = 1
    target_shape = None
    mode = 'run'

    if mode == 'run':
        args = zip(videos_name, [frames_path] * videos_num, [save_path] * videos_num, [file_type] * videos_num, 
                    [start] * videos_num, [end] * videos_num, [target_shape] * videos_num)
        with Pool(processes=4) as p:
            with tqdm(total=videos_num) as pbar:
                for i, _ in tqdm(enumerate(p.imap_unordered(frames_to_videos, args))):
                    pbar.update()
    else:
        args = (videos_name[0], frames_path, save_path, file_type, start, end, target_shape)
        frames_to_videos(args)

    print("Done!")
