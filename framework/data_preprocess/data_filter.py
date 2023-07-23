from typing import Dict, Any


def filter_data(data_dict: Dict[str, Any]):
    for name in data_dict.keys():
        data_dict[name]['anomaly'] = True
    return data_dict
