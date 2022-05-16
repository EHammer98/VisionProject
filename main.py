from cnn import CNN
from img import ImgProcess

import os
from PIL import Image # For handling the images
import numpy as np # We'll be storing our data as numpy arrays
from re import L

if __name__ == "__main__":

    ai = CNN('C:\\Users\\timvd\\Documents\\Programming\\Python\\Tensorflow\\handgestures\\data\\leapGestRecog\\00\\',
             'C:\\Users\\timvd\\Documents\\Programming\\Python\\Tensorflow\\handgestures\\data\\leapGestRecog\\0')

    # imp = ImgProcess()
    # imp.image_array(9)

    img = []
    dir = "C:\\Users\\timvd\\Documents\\Programming\\Python\\Tensorflow\\handgestures\\testdata\\test"

    img.append(Image.open(dir + "1.png").convert('L').resize( (320, 120) ))
    img.append(Image.open(dir + "2.png").convert('L').resize( (320, 120) ))

    ai.create_model("handgestures")
    # ai.test_model(imp.img_array)
    ai.test_model(img)