from typing import Dict, Callable


def init_all_models(model_config: Dict[str, Dict[str, Callable]]) -> Dict[str, object]:
    model_dict = dict()
    for name, cfg in model_config.items():
        model_dict[name] = cfg['model']()
    return model_dict
