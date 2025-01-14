from models.fire_classification.fc.models.resnet_clf import *
from models.fire_classification.fc.models.timm_clf import *


def create_model(cfg, num_classes):
    model = globals()[cfg['model']]
    model = model(num_classes, cfg['pretrained_model'], cfg['pretrained'])
    return model
