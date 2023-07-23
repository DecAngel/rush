from typing import Dict, Any


def request_all_data(data_metainfo_dict: Dict[str, Any]) -> Dict[str, Any]:
    data_dict = dict()
    for name, cfg in data_metainfo_dict.items():
        data_dict[name] = cfg['method'](**cfg['args'])

    return data_dict
