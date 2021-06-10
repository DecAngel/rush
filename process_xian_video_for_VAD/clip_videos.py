"""
The clip_videos.py is used to clip videos by using multipocessing and cv2.

The structure of videos is shown below:

dataset_name:
|------------|videos:
|------------------|: video1
|------------------|: video2
|------------------|: video3
|------------------|: video4 ...

The structure of clips is shown below:

dataset_name:
|------------|clips:
|------------------|: video1_001
|------------------|: video1_002 ...
|------------------|: video2_001
|------------------|: video2_002 ...

"""
import os
import cv2
from tqdm import tqdm
from multiprocessing import Pool
from argparse import ArgumentParser


def clip_video_according_to_range(video_name, video_path, save_path, video_num, start_time, end_time, 
                                    target_fps=None, target_shape=None):
    cap = cv2.VideoCapture(os.path.join(video_path, video_name))
    if not cap.isOpened():
        print('Video is not opened!')
        return

    if target_shape == None:
        success, frame = cap.read()
        f_height, f_width = frame.shape[0], frame.shape[1]
    else:
        f_height, f_width = int(target_shape[0]), int(target_shape[1])
    target_fps = cap.get(5) if target_fps == None else target_fps

    # four_cc = cv2.VideoWriter_fourcc(*'H264')
    four_cc = cv2.VideoWriter_fourcc(*'mp4v')
    target_video = os.path.join(save_path, video_name.split('.')[0] + '_{:03d}.avi'.format(video_num))
    video_writer = cv2.VideoWriter(target_video, four_cc, target_fps, (f_width, f_height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_time)
    while start_time <= end_time:
        success, frame = cap.read()
        if not success: break
        frame = cv2.resize(frame, (f_width, f_height), interpolation=cv2.INTER_LINEAR)
        video_writer.write(frame)
        start_time += 1
    cap.release()


def clip_videos(args):
    video_name, video_path, save_path, clip_length, start, end, target_fps, target_shape = args
    cap = cv2.VideoCapture(os.path.join(video_path, video_name))
    if not cap.isOpened():
        print('Video is not opened!')
        return

    fps = cap.get(5)
    frame_number = cap.get(7) # the number of frames in the video 
    video_length = frame_number / fps
    start_time = int(fps * start * video_length)
    end_time = int(fps * end * video_length)
    offset = int(fps * clip_length)
    cap.release()

    video_num = 0
    for i in range(start_time, end_time, offset):
        clip_video_according_to_range(video_name, video_path, save_path, video_num, 
                                        i, i + offset, target_fps, target_shape)
        video_num += 1


if __name__ == '__main__':
    cfg = {
        'src': '/home/yuanyu/projects/data/DaYanTa/8_C51/2021-04-29',
        'target': '/home/yuanyu/projects/data/DaYanTa_2/8_C51/tmp'
    }
    parser = ArgumentParser()
    parser.add_argument('--src', '-s', type=str, default=cfg['src'])
    parser.add_argument('--target', '-t', type=str, default=cfg['target'])
    args = parser.parse_args()

    video_path = args.src
    save_path = args.target
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    videos_name = os.listdir(video_path)
    videos_name.sort()

    # don't foget it !!!!
    videos_name = [videos_name[-12:]]
    # don't forget above !!!!
    
    videos_num = len(videos_name)
    print(videos_name)

    mode = 'run'
    clip_length = 10 # the time length of clip (second)
    start = 0 # start splitting the video at this point (from 0 to 1)
    end = 1 # stop splitting the video at this point (from 0 to 1)
    target_fps = None
    target_shape = None

    if mode == 'run':
        args = zip(videos_name, [video_path] * videos_num, [save_path] * videos_num, 
                [clip_length] * videos_num, [start] * videos_num, [end] * videos_num, 
                [target_fps] * videos_num, [target_shape] * videos_num)
        with Pool(processes=4) as p:
            with tqdm(total=videos_num) as pbar:
                for i, _ in tqdm(enumerate(p.imap_unordered(clip_videos, args))):
                    pbar.update()
    else:
        args = (videos_name[0], video_path, save_path, clip_length, start, end, target_fps, target_shape)
        clip_videos(args)

    print("Done!")
