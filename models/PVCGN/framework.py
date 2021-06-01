import os
from typing import Dict

import numpy as np
import torch
import torchvision.transforms as tt

from models.fire_classification.fc.utils.device import get_default_device
from models.PVCGN.ggnn.multigraph import Net
from models.PVCGN.lib.utils import collate_wrapper
from models.PVCGN.ggnn_train import read_cfg_file
from models.PVCGN.lib import utils
from urls import PV_cfg_path


class PVCDetector:
    def __init__(self) -> None:
        self.cfg = {
            'config_filename': PV_cfg_path,
            'model_cfg': read_cfg_file(PV_cfg_path),
            'device': get_default_device()
        }
        self.model = self.init_model()

    @torch.no_grad()
    def one_step(self, data: Dict[str, object]):
        (x, y, xtime, ytime) = data['od']
        scaler = data['scaler']
        y = y[..., :self.output_dim]
        sequences, y = collate_wrapper(x=x, y=y,
                                       edge_index=self.edge_index,
                                       edge_attr=self.edge_attr,
                                       device=self.cfg['device'])
        # (T, N, num_nodes, num_out_channels)
        y_pred = self.model(sequences)
        # y_preds = np.concatenate(y_preds, axis=0)  # concat in batch_size dim.
        y_pred_list = list()

        for horizon_i in range(self.horizon):
            inversed_y_pred = torch.clamp_min(scaler.inverse_transform(
                y_pred[:, horizon_i, :, :self.output_dim]), 0)
            y_pred_list.append(inversed_y_pred)
        # print(y_pred_list)
        return {
            'type': 'od',
            'anomaly': False,
            'pred': y_pred_list,
            'sensors': data['sensors']
        }

    def init_model(self):
        cfg = self.cfg['model_cfg']
        device = self.cfg['device']

        adj_mx_list = []
        graph_pkl_filename = cfg['data']['graph_pkl_filename']

        if not isinstance(graph_pkl_filename, list):
            graph_pkl_filename = [graph_pkl_filename]

        src = []
        dst = []
        for g in graph_pkl_filename:
            adj_mx = utils.load_graph_data_nj(g)

            for i in range(len(adj_mx)):
                adj_mx[i, i] = 0
            adj_mx_list.append(adj_mx)

        adj_mx = np.stack(adj_mx_list, axis=-1)
        if cfg['model'].get('norm', False):
            print('row normalization')
            adj_mx = adj_mx / (adj_mx.sum(axis=0) + 1e-18)
        src, dst = adj_mx.sum(axis=-1).nonzero()
        self.edge_index = torch.tensor(
            [src, dst], dtype=torch.long, device=device)
        self.edge_attr = torch.tensor(adj_mx[adj_mx.sum(axis=-1) != 0],
                                      dtype=torch.float,
                                      device=device)

        self.output_dim = cfg['model']['output_dim']
        self.horizon = cfg['model']['horizon']

        model = Net(cfg).to(device)
        model.load_state_dict(torch.load(
            cfg['model']['save_path']), strict=False)
        model.eval()

        return model
