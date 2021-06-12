from typing import Dict
import glob

import pandas as pd

from urls import gas_dir, mode


class GasResource:
    def __init__(self) -> None:
        self.data_dir = gas_dir

        self.gas_file_path_list = glob.glob(f'{gas_dir}/*.csv')
        # valid_dl = DeviceDataLoader(
        #     DataLoader(valid_ds, 1, num_workers=2, pin_memory=True),
        #     cfg['device'])
        # self.imgs = glob.glob(os.path.join(fire_image_dir, '*.jpg'))
        # self.imgs.sort()
        self.cur_idx = 0
        # self.length = len(self.imgs)
        self.length = len(self.gas_file_path_list)

    def next(self):
        # img_path = self.imgs[self.cur_idx]
        # img = Image.open(img_path)
        gas_file_path = self.gas_file_path_list[self.cur_idx]
        gas_pd = pd.read_csv(gas_file_path, skipinitialspace=True)

        self.cur_idx = (self.cur_idx + 1) % self.length

        return gas_pd

if mode == 'run':
    gas_resource = GasResource()

# PM1,PM10,PM2_5,CH4,H2S,CO,flamGas
def get_gas() -> Dict[str, object]:
    gas_pd = gas_resource.next()
    return {
        'PM1': gas_pd['PM1'],
        'PM10': gas_pd['PM10'],
        'PM2_5': gas_pd['PM2_5'],
        'CH4': gas_pd['CH4'],
        'H2S': gas_pd['H2S'],
        'CO': gas_pd['CO'],
        'flamGas': gas_pd['flamGas'],
        'sensors': [
            'PM',
            'CH4',
            'H2S',
            'CO',
            'flamGas'
        ]
    }