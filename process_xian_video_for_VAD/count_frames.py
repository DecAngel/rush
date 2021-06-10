"""
The count_frames.py is used to create count_frames.txt.
"""
import os


def count_frames(video_path, save_path):
    save_file = os.path.join(save_path, 'count_frames.txt')
    with open(save_file, 'w') as f:
        for i, video in enumerate(os.listdir(video_path)):
            frames = os.listdir(os.path.join(video_path, video))
            line = video + ',' + str(len(frames))
            if  i != 0 : line = '\n' + line
            f.write(line)


if __name__ == '__main__':
    video_path = 'Dataset/test/pictures'
    save_path = 'Dataset/test'
    count_frames(video_path, save_path)
    print('Done!')
