from easydict import EasyDict

from torchvision import transforms


config_8_C51 = EasyDict(
    video_folder='/home/yuanyu/projects/data/DaYanTa_2/8_C51/frames',
    label_file_path='/home/yuanyu/projects/dyt_VAD/label2.csv',
    transform=transforms.Compose([transforms.ToTensor()]),
    resize_height=256,
    resize_width=256,
    time_step=4,
    num_pred=1,
    log_dir='/home/yuanyu/projects/rush/models/MNAD/exp/Xian/pred/log2'
)