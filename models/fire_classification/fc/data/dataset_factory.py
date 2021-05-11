from models.fire_classification.fc.data.dataset import load_annotation_list, DataSet
import config


def create_dataset(cfg, train=True):
    annotations = load_annotation_list(cfg[f'{"train" if train else "valid"}_ann_file_path'])
    transform = getattr(config, cfg[f'{"train" if train else "valid"}_transform'])
    return DataSet(annotations, transform, normalize=True)
