from typing import Dict, Any
import glob

import pandas as pd

from settings import gas_dir


class GasResourceD:
    def __init__(self) -> None:
        self.data_dir = gas_dir
        self.gas_file_path_list = glob.glob(f'{gas_dir}/*.csv')
        self.cur_idx = 0
        self.length = len(self.gas_file_path_list)

    def next(self) -> pd.DataFrame:
        gas_file_path = self.gas_file_path_list[self.cur_idx]
        gas_pd = pd.read_csv(gas_file_path, skipinitialspace=True)
        self.cur_idx = (self.cur_idx + 1) % self.length
        return gas_pd


# PM1,PM10,PM2_5,CH4,H2S,CO,flamGas
def get_gas() -> Dict[str, Any]:
    try:
        gas_pd = get_gas.resource.next()
    except AttributeError:
        get_gas.resource = GasResourceD()
        gas_pd = get_gas.resource.next()
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
