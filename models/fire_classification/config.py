import torch
import torchvision.transforms as tt
from timm.data.random_erasing import RandomErasing
from timm.data import Mixup


data_dir = './data'

stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

tt1 = tt.Compose([
    tt.RandomResizedCrop([200, 200]),
    tt.RandomHorizontalFlip(),
    tt.RandomVerticalFlip(),
    tt.RandomRotation(90),
    tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

tt2 = tt.Compose([
    tt.RandomResizedCrop([200, 200]),
    tt.RandomHorizontalFlip(),
    tt.RandomRotation(30),
    tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

tt3 = tt.Compose([
    tt.RandomResizedCrop([200, 200]),
    tt.RandomHorizontalFlip(),
    tt.RandomRotation(30),
    # tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

tt4 = tt.Compose([
    tt.Resize([256, 256]),
    tt.RandomCrop([200, 200]),
    tt.RandomHorizontalFlip(),
    tt.RandomRotation(30),
    # tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

tt5 = tt.Compose([
    tt.Resize([400, 400]),
    tt.RandomCrop([320, 320]),
    tt.RandomHorizontalFlip(),
    tt.RandomRotation(30),
    # tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

tt6 = tt.Compose([
    tt.Resize([400, 400]),
    tt.RandomCrop([256, 256]),
    tt.RandomHorizontalFlip(),
    tt.RandomRotation(30),
    # tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

tt7 = tt.Compose([
    tt.Resize([400, 400]),
    tt.RandomCrop([320, 320]),
    tt.RandomHorizontalFlip(),
    tt.RandomRotation(30),
    # tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    tt.ToTensor(),
    tt.Normalize(*stats),
    RandomErasing(device="cpu")
])

tt8 = tt.Compose([
    tt.Resize([400, 400]),
    tt.RandomCrop([320, 320]),
    tt.RandomHorizontalFlip(),
    tt.RandomRotation(30),
    # tt.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
    Mixup(num_classes=6),
    tt.ToTensor(),
    tt.Normalize(*stats)
])


vt1 = tt.Compose([tt.Resize([200, 200]), tt.ToTensor(), tt.Normalize(*stats)])
vt2 = tt.Compose([tt.Resize([320, 320]), tt.ToTensor(), tt.Normalize(*stats)])
vt3 = tt.Compose([tt.Resize([256, 256]), tt.ToTensor(), tt.Normalize(*stats)])
vt4 = tt.Compose([tt.Resize([400, 400]), tt.ToTensor(), tt.Normalize(*stats)])


efficientnet_b3a_e8_b16_tt6_vt3_explr_timmfc3clf_freeze_Adam = {
    'train_ann_file_path': data_dir + '/annotation_for_train.txt',
    'valid_ann_file_path': data_dir + '/annotation_for_valid.txt',
    'epochs': 11,
    'batch_size': 16,
    'max_lr': 3e-4,
    'grad_clip': 0.1,
    'weight_decay': 1e-4,
    'pretrained_model': 'efficientnet_b3a',
    'pretrained': True,
    'train_transform': 'tt6',
    'valid_transform': 'vt3',
    'model': 'TimmFC3CLF',
    'freeze': True,
    'opt_func': 'Adam',
    'save_p': 1,
}
