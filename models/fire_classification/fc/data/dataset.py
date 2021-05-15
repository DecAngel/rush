import torch
import torch.utils.data
from PIL import Image
import torchvision.transforms as T


def load_annotation_list(filename):
    """create an annotation list from file.
    return a list of [filename: label] pairs

    """
    annotations = []
    with open(filename) as ann:
        for line in ann:
            annotations.append(line.strip())

    return annotations


class DataSet(torch.utils.data.Dataset):
    """creat a dataset from annotation_list.

    Argus:
        annotation_list: a list with each item in the form of “image_path_name:label”
        transform: pre-designed transformation applied on each img
        normalize(bool): batch normalization

    """

    def __init__(self, annotation_list, transform, normalize=False):
        super().__init__()
        self.classes = ('safe', 'fire_detected')
        self.annotations = annotation_list
        self.img_list = []
        self.label_list = []
        self.transform = transform

        for line in annotation_list:
            if line[0] != '#':
                line = line.rstrip().split(':')
                file = line[0]
                img = Image.open(file)

                if self.transform:
                    img = self.transform(img)
                label = torch.tensor(int(line[1]))
                self.img_list.append(img)
                self.label_list.append(label)

        self.length = len(self.label_list)

        if normalize:
            mean, std = self.get_batch_nomalize()
            for img in self.img_list:
                T.Normalize(mean, std)(img)

    def __getitem__(self, index):
        return self.img_list[index], self.label_list[index]

    def __len__(self):
        return self.length

    def get_batch_nomalize(self):
        """:returns mean,std"""
        # pass
        mean = {0: 0, 1: 0, 2: 0}
        std = {0: 0, 1: 0, 2: 0}
        for i in range(3):
            for img in self.img_list:
                mean[i] += img[i].sum()
            mean[i] /= 250*250*self.length
        for i in range(3):
            for img in self.img_list:
                temp = img[i] - mean[i]
                std[i] += pow(temp, 2).sum()
            std[i] /= 250*250*self.length
        return (mean[0], mean[1], mean[2]), (std[0], std[1], std[2])


def log_dateset_info(dataset: DataSet):
    print(f'dataset length: {len(dataset)}')
    print(f'labels: {dataset.classes}')
