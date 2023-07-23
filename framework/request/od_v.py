from models.PVCGN.lib import utils
from models.PVCGN.ggnn_train import read_cfg_file
from settings import pv_cfg_path


class ODResource:
    def __init__(self):
        self.cfg = read_cfg_file(pv_cfg_path)['data']

        dataset = utils.load_dataset_nj(**self.cfg)
        self.dataloader = dataset['test_loader'].get_iterator()
        self.scaler = dataset['scaler']
        self.iter = self._init_iter()
        self.cur_idx = 0

    def next(self):
        return next(self.iter)

    def _init_iter(self):
        while True:
            for od in self.dataloader:
                yield od      # 使用 yield


def get_OD_v():
    try:
        od = get_OD_v.resource.next()
    except AttributeError:
        get_OD_v.resource = ODResource()
        od = get_OD_v.resource.next()
    return {
        'od': od,
        'scaler': get_OD_v.resource.scaler,
        'sensor': 'virtual od, xian'
    }
