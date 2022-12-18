#-------------------------------------#
#       对单张图片进行预测
#-------------------------------------#

from yolo import YOLO
from PIL import Image
from matplotlib import pyplot as plt
yolo = YOLO()

img = "3.jpg"
try:
    image = Image.open(img)
except:
    print('Open Error! Try again!')
else:
    r_image = yolo.detect_image(image)
    # r_image.show()
    plt.imshow(r_image)
    r_image.save("33.jpg")
    plt.show()
