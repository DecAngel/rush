import os
from copy import copy
from argparse import ArgumentParser
from collections import defaultdict

import numpy as np
import torch
from torch.utils.data import DataLoader
import torchvision.transforms as tt
from tensorboardX import SummaryWriter

from models.fire_classification.fc.data import create_dataset, DeviceDataLoader, log_dateset_info
from models.fire_classification.fc.models import create_model
from models.fire_classification.fc.utils.device import to_device, get_default_device
from models.fire_classification.fc.utils.exp import get_exp_ID
from models.fire_classification import config


def predict_full(args):
    if args.gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)

    cfg = getattr(config, args.cfg)
    cfg['ckpt'] = args.ckpt
    cfg['device'] = get_default_device()
    # cfg['device'] = torch.device('cpu')
    if cfg.get('exp_id', None) is None:
        cfg['exp_id'] = get_exp_ID(cfg)

    exps_root = 'runs'
    exp_id = cfg['exp_id']
    writer = SummaryWriter(os.path.join(exps_root, exp_id))

    # Create datasets
    # stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    # test_transform = tt.Compose(
    #     [tt.Resize([200, 200]),
    #         tt.ToTensor(),
    #         tt.Normalize(*stats)])
    # set the batch size
    batch_size = cfg['batch_size']
    train_ds = create_dataset(cfg, train=True)
    valid_ds = create_dataset(cfg, train=False)
    num_classes = len(train_ds.classes)
    print('train_ds'.center(100, '-'))
    log_dateset_info(train_ds)
    print('test_ds'.center(100, '-'))
    log_dateset_info(valid_ds)

    print(f'train_ds size: {len(train_ds)}')
    print(f'valid_ds size: {len(valid_ds)}')

    # test_ds = valid_ds
    train_dl = DeviceDataLoader(
        DataLoader(train_ds,
                   batch_size,
                   shuffle=True,
                   num_workers=3,
                   pin_memory=True), cfg['device'])
    valid_dl = DeviceDataLoader(
        DataLoader(valid_ds, batch_size, num_workers=2, pin_memory=True),
        cfg['device'])

    # show_batch(valid_dl)
    model = to_device(create_model(cfg, 2), cfg['device'])
    model_ckpt = torch.load(os.path.join(writer.logdir, cfg['ckpt']))
    model.load_state_dict(model_ckpt)

    train_ds_out, valid_ds_out = dict(), dict()
    train_ds_out['result'], train_ds_out['outputs_dict'] = predict(
        model, train_dl)
    valid_ds_out['result'], valid_ds_out['outputs_dict'] = predict(
        model, valid_dl)
    torch.save({
        'train_ds_out': train_ds_out,
        'valid_ds_out': valid_ds_out
    }, args.save_path)
    return train_ds_out, valid_ds_out


@torch.no_grad()
def predict(model, dataloader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in dataloader]
    outputs_dict = defaultdict(list)
    for mini_dict in outputs:
        for key, value in mini_dict.items():
            tmp = outputs_dict[key]
            tmp.append(value)
            outputs_dict[key] = tmp
    return model.validation_epoch_end(outputs), outputs_dict


def eval_outputs(outputs_dict):
    pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--precomputed_outputs', '-p', type=str, default=None)
    parser.add_argument(
        '--cfg',
        type=str,
        default='efficientnet_b3a_e8_b16_tt6_vt3_explr_timmfc3clf_freeze_Adam')
    parser.add_argument('--gpu', type=str, default=None)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--ckpt', type=str, default='model.ckpt')
    parser.add_argument('--save_path',
                        type=str,
                        default='./predict_outputs.out')
    args = parser.parse_args()

    # load or compute outputs
    if args.precomputed_outputs is not None:
        ckpt = torch.load(args.precomputed_outputs)
        train_ds_out, valid_ds_out = ckpt['train_ds_out'], ckpt['valid_ds_out']
    else:
        train_ds_out, valid_ds_out = predict_full(args)

    # from utils import plt_confusion_matrix
    # import matplotlib.pyplot as plt
    # classes = 6
    # for ds_out in [train_ds_out, valid_ds_out]:
    #     result, outputs_dict = ds_out['result'], ds_out['outputs_dict']
    #     f = plt_confusion_matrix(outputs_dict['y_pred'],
    #                              outputs_dict['y_true'], classes)
    #     plt.show()
    #     print(result)
