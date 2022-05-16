import os
from PIL import Image # For handling the images
import numpy as np # We'll be storing our data as numpy arrays
from re import L
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # Plotting
from datetime import datetime
import random

class ImgProcess:
    def __init__(self) -> None:
        self.img_array = []


    def image_array(self, img_count):

        random.seed(datetime.now().timestamp())
        self.img_array.clear()

        for i in range(img_count):
            dir = "C:/Users/timvd/Documents/Programming/Python/Tensorflow/handgestures/data/leapGestRecog/"
            subdir = random.randint(0, len(os.listdir(dir)) - 1)
            dir += "0" + str(subdir) + "/"

            batchdir = os.listdir(dir)[ random.randint(0, len(os.listdir(dir)) - 1) ]
            dir += batchdir + "/"

            filedir = os.listdir(dir)[ random.randint(0, len(os.listdir(dir)) - 1) ]
            dir += filedir

            self.img_array.append(Image.open(dir).convert('L').resize( (320, 120) ))


        # for k in os.listdir(dir):
        #     if (count >= datacount):
        #         break

        #     img = Image.open(dir + k).convert('L')
        #     img = img.resize( (320, 120) )

        #     self.img_array.append(np.array(img))
        #     count += 1

        # self.img_array = np.array(self.img_array, dtype = 'float32')
        # self.img_array = self.img_array.reshape((count, 120, 320, 1))


    def show_image(self, index):
        plt.imshow(self.img_array[index])
        plt.show()