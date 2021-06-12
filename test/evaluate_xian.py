import os
import sys
import math
from collections import OrderedDict
import copy
import random
import glob
import time
from easydict import EasyDict
os.chdir('/home/yuanyu/projects/rush')

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torch.nn.init as init
import torch.utils.data as data
import torch.utils.data.dataset as dataset
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.autograd import Variable
from sklearn.metrics import roc_auc_score
import torchvision.utils as v_utils
import matplotlib.pyplot as plt

from models.MNAD.model.utils import CustomDataLoader
from models.MNAD.model.final_future_prediction_with_memory_spatial_sumonly_weight_ranking_top1 import *
from models.MNAD.model.Reconstruction import *
from models.MNAD.utils import *
import urls

id = 51
cfg = EasyDict(
    # dataset
    video_folder='/home/yuanyu/projects/data/DaYanTa_2/8_C' + str(id) + '/frames',
    label_file_path='/home/yuanyu/projects/rush/process_xian_video_for_VAD/label_dyt_' + str(id) + '_0429.csv',
    transform=transforms.Compose([transforms.ToTensor()]),
    resized_height=256,
    resized_width=256,
    time_step=4,
    num_pred=1,

    # model
    method='pred',
    t_length=5,
    fdim=512,
    mdim=512,
    msize=10,

    # test
    model_path='./models/MNAD/exp/Xian/pred/log' + str(id) + '/model.pth',
    m_items_path='./models/MNAD/exp/Xian/pred/log' + str(id) + '/keys.pt',
    log_dir='./xian_results/' + str(id),
    gpus='1,2,3',
    batch_size=1,
    num_workers=1,

    alpha=1,
    th=0.01,
    loss_func_mse=nn.MSELoss(reduction='none'),
)


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = cfg.gpus
# make sure to use cudnn for computational performance
torch.backends.cudnn.enabled = True
if not os.path.exists(cfg.log_dir):
    os.mkdir(cfg.log_dir)


# init dataloader
test_dataset = CustomDataLoader(
    cfg.video_folder,
    transforms.Compose([
        transforms.ToTensor(),
    ]),
    label_file_path=cfg.label_file_path,
    resize_height=cfg.resized_height, resize_width=cfg.resized_width,
    time_step=cfg.t_length-1,
    train=False
)

test_loader = data.DataLoader(test_dataset, batch_size=cfg.batch_size,
                              shuffle=False, num_workers=cfg.num_workers, drop_last=False)


# init model
model = torch.load(cfg.model_path)
model.cuda()
model.eval()
m_items = torch.load(cfg.m_items_path)


# Init result savers
results = dict()

video_name_list = list()

mse_imgs_list = list()
mse_loss_list = list()
psnr_list = list()


for i, imgs in enumerate(test_loader):
    imgs = imgs.cuda()
    outputs, feas, updated_feas, m_items, softmax_score_query, softmax_score_memory, _, _, _, compactness_loss = model.forward(
        imgs[:, 0:3*4], m_items, False
    )
    mse_imgs = cfg.loss_func_mse((outputs[0]+1)/2, (imgs[0, 3*4:]+1)/2)
    mse_loss = torch.mean(mse_imgs).item()
    mse_feas = compactness_loss.item()
    psnr_ = psnr(mse_loss)

    print(i, mse_loss)
    torch.save({
        'mse_imgs': mse_imgs,
        'mse_loss': mse_loss,
        'psnr': psnr_
    }, f'{cfg.log_dir}/result_{i}.pt')
    # mse_imgs_list.append(mse_imgs)
    # mse_loss_list.append(mse_loss)
    # psnr_list.append(psnr_)


# torch.save({
#     'mse_imgs_list': mse_imgs_list,
#     'mse_loss_list': mse_loss_list,
#     'psnr_list': psnr_list
# }, 'xian_test_results.pt')
