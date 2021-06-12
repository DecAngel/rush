from typing import Dict
from functools import reduce


def merge_results_dict(d1: Dict[str, Dict[str, object]], d2: Dict[str, Dict[str, object]]):
    merged_results_dict = dict()
    
    model_name_list = d1.keys() | d2.keys()
    for model_name in model_name_list:
        model_results_dict_list = [d.get(model_name, {}) for d in [d1, d2]]
        combined_model_results_dict = {
            'results': reduce(
                lambda pre, cur: pre+cur.get('results', []),
                model_results_dict_list,
                list() 
            ),
            'displays': [
                None
            ],
            'solves': [
                None
            ]
        }
        merged_results_dict[model_name] = combined_model_results_dict
    
    return merged_results_dict


if __name__ == '__main__':
    from framework.config import results_dict_list

    print(merge_results_dict(results_dict_list[3], results_dict_list[4]))