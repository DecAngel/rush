from typing import Dict, List


def request_all_data(data_meteinfo_dict: Dict[str, object]) -> Dict[str, object]:
    data_dict = dict()
    for name, cfg in data_meteinfo_dict.items():
        data_dict[name] = cfg['method'](**cfg['args'])

    return data_dict
