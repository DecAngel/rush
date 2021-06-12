from models.PVCGN.lib import utils
from models.PVCGN.ggnn_train import read_cfg_file
from urls import PV_cfg_path, mode


class ODResource:
    def __init__(self) -> None:
        self.cfg = read_cfg_file(PV_cfg_path)['data']

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


if mode == 'run':
    OD_Resource = ODResource()


def get_OD_v():
    od = OD_Resource.next()
    return {
        'od': od,
        'scaler': OD_Resource.scaler,
        'sensor': 'virtual od, xian'
    }