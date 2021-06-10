from typing import Dict, List
from functools import reduce


def distribute_data(data_dict: Dict[str, object], model_config_dict: Dict[str, object]) -> Dict[str, object]:
    distributed_data = dict()
    pass
    for model_name, model_cfg in model_config_dict.items():
        distributed_data[model_name] = list()
        for data_name_list in model_cfg['data_lists']:
            if _has_anomaly(data_dict, data_name_list):
                tmp_dict = dict()
                for data_name in data_name_list:
                    for key, value in data_dict[data_name].items():
                        tmp_dict[key] = value
                if tmp_dict.get('sensor', None) is not None:
                    tmp_dict.pop('sensor')
                tmp_dict.pop('anomaly')
                # tmp_dict['sensors'] = [data_dict[data_name]['sensor']
                #                        for data_name in data_name_list]
                tmp_dict['sensors'] = list()
                for data_name in data_name_list:
                    if data_dict[data_name].get('sensor', None) is not None:
                        tmp_dict['sensors'].append(data_dict[data_name]['sensor'])
                    if data_dict[data_name].get('sensors', None) is not None:
                        tmp_dict['sensors'].extend(data_dict[data_name]['sensors'])
                distributed_data[model_name].append(
                    tmp_dict)
    pass

    return distributed_data


def _has_anomaly(data_dict: Dict[str, object], data_name_list: List[str]) -> bool:
    def helper(pre, cur):
        return pre or data_dict[cur]['anomaly']
    return reduce(helper, data_name_list, False)
