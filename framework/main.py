from framework.request import (
    request_all_data
)
from framework.data_preprocess import (
    filter_data,
    distribute_data
)
from framework.model_deploy import init_all_models
from framework.anomaly_response_strategy import response_anomaly
from framework.config import (
    data_meteinfo_dict,
    model_config_dict
)


def one_step(models_dict):
    data_dict = request_all_data(data_meteinfo_dict)
    data_dict = filter_data(data_dict)
    # print(f'data_dict: {data_dict}')

    distributed_data_dict = distribute_data(data_dict, model_config_dict)
    # print(f'distributed_data_dict: {distributed_data_dict}')
    for model_name, data_list in distributed_data_dict.items():
        pass
        for data_dict in data_list:
            # print(f'data_dict: {data_dict}')
            result = models_dict[model_name].one_step(data_dict)
            print(f'result: {result}')
            display_, solve_ = response_anomaly(result)
            pass
    pass


def main():
    models_dict = init_all_models(model_config_dict)
    pass
    while True:
        pass
        one_step(models_dict)
        input('press key "enter" to continue...')


if __name__ == '__main__':
    main()
