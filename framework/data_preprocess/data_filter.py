from typing import Dict


def filter_data(data_dict: Dict[str, object]):
    pass
    for name in data_dict.keys():
        data_dict[name]['anomaly'] = True
    return data_dict
