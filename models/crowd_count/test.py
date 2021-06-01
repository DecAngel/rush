import cv2
from PIL import Image, ImageOps

from models.crowd_count.crowd_counting.model import CrowdCounter


img = Image.open('./test.jpg').convert('RGB')
cc = CrowdCounter()
x, y = cc.one_step(img)
print(x, y)
