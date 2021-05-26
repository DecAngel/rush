from crowd_counting.model import CrowdCounter
import cv2
from PIL import Image, ImageOps

img = Image.open('./test.jpg').convert('RGB')


cc = CrowdCounter()
x,y =cc.one_step(img)
print(x,y)