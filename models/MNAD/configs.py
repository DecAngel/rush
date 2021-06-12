from easydict import EasyDict

from torchvision import transforms


config_8_C51 = EasyDict(
    video_folder='/home/yuanyu/projects/data/DaYanTa_2/8_C51/frames',
    label_file_path='/home/yuanyu/projects/rush/process_xian_video_for_VAD/label_dyt_51_0429.csv',
    transform=transforms.Compose([transforms.ToTensor()]),
    resize_height=256,
    resize_width=256,
    time_step=4,
    num_pred=1,
    log_dir='/home/yuanyu/projects/rush/models/MNAD/exp/Xian/pred/log51'
)

config_8_C31 = EasyDict(
    video_folder='/home/yuanyu/projects/data/DaYanTa_2/8_C31/frames',
    label_file_path='/home/yuanyu/projects/rush/process_xian_video_for_VAD/label_dyt_31_0429.csv',
    transform=transforms.Compose([transforms.ToTensor()]),
    resize_height=256,
    resize_width=256,
    time_step=4,
    num_pred=1,
    log_dir='/home/yuanyu/projects/rush/models/MNAD/exp/Xian/pred/log31'
)

config_8_C32 = EasyDict(
    video_folder='/home/yuanyu/projects/data/DaYanTa_2/8_C32/frames',
    label_file_path='/home/yuanyu/projects/rush/process_xian_video_for_VAD/label_dyt_32_0429.csv',
    transform=transforms.Compose([transforms.ToTensor()]),
    resize_height=256,
    resize_width=256,
    time_step=4,
    num_pred=1,
    log_dir='/home/yuanyu/projects/rush/models/MNAD/exp/Xian/pred/log32'
)

config_8_C33 = EasyDict(
    video_folder='/home/yuanyu/projects/data/DaYanTa_2/8_C33/frames',
    label_file_path='/home/yuanyu/projects/rush/process_xian_video_for_VAD/label_dyt_33_0429.csv',
    transform=transforms.Compose([transforms.ToTensor()]),
    resize_height=256,
    resize_width=256,
    time_step=4,
    num_pred=1,
    log_dir='/home/yuanyu/projects/rush/models/MNAD/exp/Xian/pred/log33'
)