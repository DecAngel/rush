import numpy as np
import cv2


def np_load_frame(filename, resized_size=None):
    """
    Load image path and convert it to numpy.ndarray. Notes that the color channels are BGR and the color space
    is normalized from [0, 255] to [-1, 1].

    :param filename: the full path of image
    :param resized_size: resized width & height
    :return: numpy.ndarray
    """
    image = cv2.imread(filename)
    if resized_size is not None:
        image = cv2.resize(image, resized_size)
    image = image.astype(dtype=np.float32)
    return image
