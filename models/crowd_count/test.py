from PIL import Image

from models.crowd_count.framework import CrowdCounter


img = Image.open('./test.jpg').convert('RGB')
cc = CrowdCounter()
x, y = cc.one_step(img)
print(x, y)
