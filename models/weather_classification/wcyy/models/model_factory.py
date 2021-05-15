from models.weather_classification.wcyy.utils.device import to_device
from models.weather_classification.wcyy.models.resnet_clf import *
from models.weather_classification.wcyy.models.timm_clf import *


def create_model(cfg, num_classes):
    model = globals()[cfg['model']]
    model = model(num_classes, cfg['pretrained_model'], cfg['pretrained'], cfg)
    model = to_device(model, cfg['device'])
    return model
