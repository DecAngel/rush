"""
The videos_to_frames.py is used to convert videos to frames by using multipocessing and cv2.

The structure of videos is shown below:

dataset_name:
|------------|videos:
|------------------|: video1
|------------------|: video2
|------------------|: video3
|------------------|: video4 ...

The structure of frames is shown below:

dataset_name:
|------------|frames:
|------------------|video1:
|------------------------|: flow_x_00001 ...
|------------------------|: flow_y_00001 ...
|------------------------|: img_00001 ...
|------------------|video2:
|------------------------|: flow_x_00001 ...
|------------------------|: flow_y_00001 ...
|------------------------|: img_00001 ...

"""
import os
import cv2
import imageio
import argparse
import skvideo.io
import numpy as np
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool


def get_data_list():
    data_list = []
    for cls_names in os.listdir(data_path):
        data_list.append(cls_names)
    data_list.sort()
    return data_list, len(data_list)


def ToImg(raw_flow, bound):
    '''
    this function scale the input pixels to 0-255 with bi-bound
    :param raw_flow: input raw pixel value (not in 0-255)
    :param bound: upper and lower bound (-bound, bound)
    :return: pixel value scale from 0 to 255
    '''
    flow = raw_flow
    flow[flow > bound] = bound
    flow[flow < -bound] = -bound
    flow -= -bound
    flow *= (255 / float(2 * bound))
    return flow.astype(np.uint8)


def save_flows(*args):
    '''
    To save the optical flow images and raw images
    :param save_path: save_path name (always equal to the video id)
    :param num: the save id, which belongs one of the extracted frames
    :param image: raw image
    :param flows: contains flow_x and flow_y
    :param bound: set the bi-bound to flow images
    :return: return 0
    '''
    save_path, num, image = args[0], args[1], args[2]
    if not os.path.exists(os.path.join(save_path)):
        os.makedirs(os.path.join(save_path))

    # save the image
    save_img = os.path.join(save_path, 'img_{:05d}.jpg'.format(num))
    imageio.imsave(save_img, image)

    if (len(args) > 3):
        flows, bound = args[3], args[4]
        # rescale to 0~255 with the bound setting
        flow_x = ToImg(flows[..., 0], bound)
        flow_y = ToImg(flows[..., 1], bound)

        # save the flows
        save_x = os.path.join(save_path, 'flow_x_{:05d}.jpg'.format(num))
        save_y = os.path.join(save_path, 'flow_y_{:05d}.jpg'.format(num))
        flow_x_img = Image.fromarray(flow_x)
        flow_y_img = Image.fromarray(flow_y)
        imageio.imsave(save_x, flow_x_img)
        imageio.imsave(save_y, flow_y_img)

    return 0


def dense_flow_videos(args):
    '''
    To extract dense_flow images
    '''
    data_name, save_path, data_path, step, bound, processor, compute_flow = args
    video_path = os.path.join(data_path, data_name)

    try:
        videocapture = skvideo.io.vread(video_path)
    except Exception as e:
        print('{} read error!'.format(data_name))
        print(e)
        return

    loop_num, frame_num = 0, 0
    len_frame = len(videocapture)
    if compute_flow:
        dtvl1 = cv2.optflow.createOptFlow_DualTVL1()

    while True:
        if loop_num >= len_frame: break
        frame = videocapture[loop_num]
        loop_num += 1

        if frame_num == 0:
            if compute_flow:
                pre_image = cv2.UMat(frame) if processor == 'gpu' else frame
                pre_gray = cv2.cvtColor(pre_image, cv2.COLOR_RGB2GRAY)
            frame_num += 1
            # to pass the out of stepped frames
            step_t = step
            while step_t > 1:
                loop_num += 1
                step_t -= 1
            continue

        if compute_flow:
            cur_image = cv2.UMat(frame) if processor == 'gpu' else frame
            cur_gray = cv2.cvtColor(cur_image, cv2.COLOR_RGB2GRAY)
            flowDTVL1 = dtvl1.calc(pre_gray, cur_gray, None)
            flowDTVL1 = cv2.UMat.get(flowDTVL1) if processor == 'gpu' else flowDTVL1
            save_flows(save_path, frame_num, frame, flowDTVL1, bound)
            pre_gray = cur_gray
            pre_image = cur_image
        else:
            save_flows(save_path, frame_num, frame)

        frame_num += 1
        # to pass the out of stepped frames
        step_t = step
        while step_t > 1:
            loop_num += 1
            step_t -= 1


def dense_flow_pictures(args):
    '''
    To extract dense_flow images
    '''
    data_name, save_path, data_path, step, bound, processor, compute_flow = args
    picture_path = os.path.join(data_path, data_name)

    frame_num, step_t = 0, step
    if compute_flow:
        dtvl1 = cv2.optflow.createOptFlow_DualTVL1()

    for frame_name in os.listdir(picture_path):
        frame = imageio.imread(os.path.join(picture_path, frame_name))

        if frame_num == 0:
            if compute_flow:
                pre_image =  cv2.UMat(frame) if processor == 'gpu' else frame
                pre_gray = cv2.cvtColor(pre_image, cv2.COLOR_RGB2GRAY)
            frame_num += 1
            continue

        # to pass the out of stepped frames
        if step_t > 1:
            step_t -= 1
            continue
        else:
            step_t = step

        if compute_flow:
            cur_image = cv2.UMat(frame) if processor == 'gpu' else frame
            cur_gray = cv2.cvtColor(cur_image, cv2.COLOR_RGB2GRAY)
            flowDTVL1 = dtvl1.calc(pre_gray, cur_gray, None)
            flowDTVL1 = cv2.UMat.get(flowDTVL1) if processor == 'gpu' else flowDTVL1
            save_flows(save_path, frame_num, frame, flowDTVL1, bound)
            pre_gray = cur_gray
            pre_image = cur_image
        else:
            save_flows(save_path, frame_num, frame)

        frame_num += 1


def parse_args():
    cfg = {
        'data_path': '/home/yuanyu/projects/data/DaYanTa_2/8_C51/tmp',
        'data_type': 'videos',
        'compute_flow': False
    }
    parser = argparse.ArgumentParser(description='densely extract the video frames and optical flows')
    parser.add_argument('--data_path', default=cfg['data_path'], type=str)
    parser.add_argument('--data_type', default=cfg['data_type'], type=str, help='set \'videos\' if process video, otherwise, set \'pictures\'')
    parser.add_argument('--num_workers', default=4, type=int, help='num of workers to act multi-process')
    parser.add_argument('--step', default=1, type=int, help='gap frames')
    parser.add_argument('--bound', default=20, type=int, help='set the maximum of optical flow')
    parser.add_argument('--s_', default=0, type=int, help='start id')
    parser.add_argument('--e_', default=1000, type=int, help='end id')
    parser.add_argument('--mode', default='run', type=str, help='set \'run\' if debug done, otherwise, set \'debug\'')
    parser.add_argument('--processor', default='gpu', type=str, help='set \'gpu\' if use gpu, otherwise, set \'cpu\'')
    parser.add_argument('--compute_flow', default=cfg['compute_flow'], type=bool, help='set \'True\' if compute flow, otherwise, set \'False\'')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    data_path = args.data_path
    data_type = args.data_type
    num_workers = args.num_workers
    step = args.step
    bound = args.bound
    s_ = args.s_
    e_ = args.e_
    mode = args.mode
    processor = args.processor
    compute_flow = args.compute_flow

    data_list, videos_num = get_data_list()
    data_list = data_list[s_ : e_]
    videos_num = min(len(data_list), e_ - s_)

    data_name = data_path.split('/')[-1]
    save_root = data_path.replace(data_name, 'frames')
    save_paths = [os.path.join(save_root, video.split('.')[0]) for video in data_list]

    if processor == 'gpu' and not cv2.ocl.haveOpenCL():
        print('GPU is not available! use CPU!')
        processor = 'cpu'

    print('find {} videos.'.format(videos_num))
    print('get ' + data_type + ' list done!')
    print('processor: {}'.format(processor))

    if data_type == 'videos':
        func = dense_flow_videos
    else:
        func = dense_flow_pictures

    if mode == 'run':
        args = zip(data_list, save_paths, [data_path] * videos_num, [step] * videos_num, 
                    [bound] * videos_num, [processor] * videos_num, [compute_flow] * videos_num)
        with Pool(processes=4) as p:
            with tqdm(total=videos_num) as pbar:
                for i, _ in tqdm(enumerate(p.imap_unordered(func, args))):
                    pbar.update()
    else:
        args = (data_list[0], save_paths[0], data_path, step, bound, processor, compute_flow)
        func(args)

    print("done!")
