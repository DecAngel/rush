from typing import Dict, List

from framework.config import results_dict_list


class ResultResource:
    def __init__(
            self,
            _results_dict_list: List[Dict[str, object]] = results_dict_list
    ) -> None:
        self.results_dict_list = _results_dict_list

        self.length = len(self.results_dict_list)
        self.cur_idx = 0

    def next(self):
        results_dict = self.results_dict_list[self.cur_idx]
        self.cur_idx = (self.cur_idx + 1) % self.length

        return results_dict


def get_all_results() -> Dict[str, object]:
    try:
        return get_all_results.resource.next()
    except AttributeError:
        get_all_results.resource = ResultResource()
        return get_all_results.resource.next()
