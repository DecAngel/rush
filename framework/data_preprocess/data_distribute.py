from typing import Dict, List, Any
from functools import reduce
from collections import defaultdict


def distribute_data(data_dict: Dict[str, Any], model_config_dict: Dict[str, Any]) -> Dict[str, Any]:
    distributed_data = defaultdict(list)
    for model_name, model_cfg in model_config_dict.items():
        for data_name_list in model_cfg['data_lists']:
            if _has_anomaly(data_dict, data_name_list):
                tmp_dict = {'sensors': []}
                for data_name in data_name_list:
                    for k, v in data_dict[data_name].items():
                        if k == 'anomaly':
                            continue
                        elif k == 'sensor':
                            tmp_dict['sensors'].append(v)
                        elif k == 'sensors':
                            tmp_dict['sensors'].extend(v)
                        else:
                            tmp_dict[k] = v
                distributed_data[model_name].append(tmp_dict)

    return distributed_data


def _has_anomaly(data_dict: Dict[str, Any], data_name_list: List[str]) -> bool:
    def helper(pre, cur):
        return pre or data_dict[cur]['anomaly']
    return reduce(helper, data_name_list, False)
