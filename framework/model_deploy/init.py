from typing import Dict


from typing import Dict


def init_all_models(model_config: Dict[str, object]) -> Dict[str, object]:
    model_dict = dict()
    for name, cfg in model_config.items():
        model_dict[name] = cfg['model']()
    
    return model_dict
