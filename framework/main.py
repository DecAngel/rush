from framework.request import (
    request_all_data
)
from framework.data_preprocess import (
    distribute_data
)
from framework.model_deploy import init_all_models
from framework.anomaly_response_strategy import response_anomaly
from framework.config import (
    data_meteinfo_dict,
    model_config
)


def one_step(models_dict):
    data_dict = request_all_data(data_meteinfo_dict)
    distributed_data_dict = distribute_data(data_dict)
    for model_name, data in distributed_data_dict.items():
        pass
        result = models_dict[model_name].one_step(data)
        display_, solve_ = response_anomaly(result)
        pass
    pass


def main():
    models_dict = init_all_models(model_config)
    pass
    while True:
        pass
        one_step(models_dict)


if __name__ == '__main__':
    main()
