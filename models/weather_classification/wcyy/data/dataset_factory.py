from models.weather_classification.wcyy.data.dataset import CustomDataset
import models.weather_classification.config as config


def create_full_dataset(cfg):
    classes = getattr(config, cfg['classes']) if type(
        cfg['classes']) == str else cfg['classes']
    return CustomDataset(cfg['data_dir'], classes=classes)
