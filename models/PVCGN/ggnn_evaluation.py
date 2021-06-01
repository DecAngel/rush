import argparse
import yaml
import numpy as np
import torch
from models.PVCGN.ggnn.multigraph import Net
from models.PVCGN.ggnn_train import evaluate
from models.PVCGN.lib import utils
from models.PVCGN.lib.utils import collate_wrapper
torch.cuda.set_device(2)
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def read_cfg_file(filename):
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=Loader)
    return cfg


def main(args):
    import tempfile

    cfg = read_cfg_file(args.config_filename)
    log_dir = tempfile.gettempdir()
    log_level = cfg.get('log_level', 'INFO')

    logger = utils.get_logger(log_dir, __name__, 'info.log', level=log_level)

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    #  all edge_index in same dataset is same
    # edge_index = adjacency_to_edge_index(adj_mx)  # alreay added self-loop
    logger.info(cfg)
    batch_size = cfg['data']['batch_size']
    test_batch_size = cfg['data']['test_batch_size']
    # edge_index = utils.load_pickle(cfg['data']['edge_index_pkl_filename'])
    hz = cfg['data'].get('name', 'nothz') == 'hz'
    nj = cfg['data'].get('name', 'nothz') == 'nj'

    adj_mx_list = []
    graph_pkl_filename = cfg['data']['graph_pkl_filename']

    if not isinstance(graph_pkl_filename, list):
        graph_pkl_filename = [graph_pkl_filename]

    src = []
    dst = []
    for g in graph_pkl_filename:
        if hz:
            adj_mx = utils.load_graph_data_hz(g)
        elif nj:
            adj_mx = utils.load_graph_data_nj(g)
        else:
            _, _, adj_mx = utils.load_graph_data(g)

        for i in range(len(adj_mx)):
            adj_mx[i, i] = 0
        adj_mx_list.append(adj_mx)

    adj_mx = np.stack(adj_mx_list, axis=-1)
    if cfg['model'].get('norm', False):
        print('row normalization')
        adj_mx = adj_mx / (adj_mx.sum(axis=0) + 1e-18)
    src, dst = adj_mx.sum(axis=-1).nonzero()
    edge_index = torch.tensor([src, dst], dtype=torch.long, device=device)
    edge_attr = torch.tensor(adj_mx[adj_mx.sum(axis=-1) != 0],
                             dtype=torch.float,
                             device=device)

    output_dim = cfg['model']['output_dim']
    for i in range(adj_mx.shape[-1]):
        logger.info(adj_mx[..., i])

    #  print(adj_mx.shape) (207, 207)

    if hz:
        dataset = utils.load_dataset_hz(**cfg['data'],
                                        scaler_axis=(0,
                                                     1,
                                                     2,
                                                     3))
    else:
        dataset = utils.load_dataset_nj(**cfg['data'])

    for k, v in dataset.items():
        if hasattr(v, 'shape'):
            logger.info((k, v.shape))

    model = Net(cfg).to(device)
    model.load_state_dict(torch.load(cfg['model']['save_path']), strict=False)

    evaluate(model=model,
             dataset=dataset,
             dataset_type='test',
             edge_index=edge_index,
             edge_attr=edge_attr,
             device=device,
             output_dim=output_dim,
             logger=logger,
             cfg=cfg,
             format_result=True, save_res=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_filename',
                        default='trained/xian.yaml',
                        type=str,
                        help='Configuration filename for restoring the model.')
    args = parser.parse_args()
    main(args)
