from cnn import CNN
from img import ImgProcess
from gui import MainWindow

import os
from os.path import exists

if __name__ == "__main__":

    ai = CNN('C:\\Users\\timvd\\Documents\\Programming\\Python\\Tensorflow\\handgestures\\data\\leapGestRecog\\00\\',
             'C:\\Users\\timvd\\Documents\\Programming\\Python\\Tensorflow\\handgestures\\data\\leapGestRecog\\0')
    win = MainWindow()

    img = []
    dir = ""

    ai.create_model("handgestures")

    ###### GUI
    def add_img():
        dir = win.open_img()
        ai.test_batch_img_add(dir)
        win.add_img(dir)

    def test_model():
        res = ai.test_model()

        for i in range(len(res)):
            win.add_img_label(ai.CONST.IMG_CATG_NAME[res[i]], i)

    def add_folder():
        dir = win.open_dir()

        if (exists(dir)):
            for k in os.listdir(dir):
                ai.test_batch_img_add(dir + "/" + k)
                win.add_img(dir + "/" + k)

    win.create_button("Add image to list", 20, 5, add_img)
    win.create_button("Load images from folder", 20, 5, add_folder)
    win.create_button("Test model", 20, 5, test_model)

    ## Start main loop
    win.run()

