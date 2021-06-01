# part of this code are copied from DCRNN
import numpy as np
import torch
from torch import nn


class MAPE1(nn.Module):

    def __init__(self, size_average=None, reduce=None, reduction: str = 'mean'):
        super(MAPE1, self).__init__()

    def forward(self, preds, targets, null_val=np.nan):

        if np.isnan(null_val):
            mask = ~torch.isnan(targets)
        else:
            mask = (targets != null_val)
        mask = mask.float()
        mask /= torch.mean((mask))
        mask = torch.where(torch.isnan(mask), torch.zeros_like(mask), mask)
        loss = torch.abs((preds - targets) / (targets + 1))
        loss = loss * mask
        loss = torch.where(torch.isnan(loss), torch.zeros_like(loss), loss)

        return torch.mean(loss)


class MAPE2(nn.Module):

    def __init__(self):
        super(MAPE2, self).__init__()

    def forward(self, preds, targets, value, device):
        targets = torch.tensor(data=targets, dtype=torch.float, device=device)
        mask = targets > value
        return torch.abs((targets[mask] - preds[mask]) / targets[mask]).mean()


class MAPE3(nn.Module):

    def __init__(self):
        super(MAPE2, self).__init__()

    def forward(self, preds, targets, value=0):
        mask = targets > value
        return np.fabs((targets[mask] - preds[mask]) / targets[mask]).mean()


def masked_rmse_np(preds, labels, null_val=np.nan):
    return np.sqrt(masked_mse_np(preds=preds, labels=labels, null_val=null_val))


def masked_mse_np(preds, labels, null_val=np.nan):
    with np.errstate(divide='ignore', invalid='ignore'):
        if np.isnan(null_val):
            mask = ~np.isnan(labels)
        else:
            # mask = np.not_equal(labels, null_val)
            mask = (labels > 109)
        mask = mask.astype('float32')
        mask /= np.mean(mask)
        rmse = np.square(np.subtract(preds, labels)).astype('float32')
        rmse = np.nan_to_num(rmse * mask)
        return np.mean(rmse)


def masked_mae_np(preds, labels, null_val=np.nan, mode='dcrnn'):
    with np.errstate(divide='ignore', invalid='ignore'):
        if np.isnan(null_val):
            mask = ~np.isnan(labels)
        else:
            # mask = np.not_equal(labels, null_val)
            mask = (labels > 109)
        mask = mask.astype('float32')
        mask /= np.mean(mask)
        mae = np.abs(np.subtract(preds, labels)).astype('float32')
        mae = np.nan_to_num(mae * mask)
        if mode == 'dcrnn':
            return np.mean(mae)
        else:
            return np.mean(mae, axis=(0, 1))


def masked_mape_np(preds, labels, null_val=np.nan):
    with np.errstate(divide='ignore', invalid='ignore'):
        if np.isnan(null_val):
            mask = ~np.isnan(labels)
        else:
            # mask = np.not_equal(labels, null_val)
            mask = (labels > 109)
        mask = mask.astype('float32')
        mask /= np.mean(mask)
        mape = np.abs(np.divide(np.subtract(preds, labels).astype('float32'), labels))
        mape = np.nan_to_num(mask * mape)
        return np.mean(mape)


