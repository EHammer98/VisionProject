from os.path import exists
import os
import sys
sys.path.insert(1, "\\")
from cnn import CNN
from img import ImgProcess
from gui import MainWindow
67


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

    #to get the current working directory
    directory = os.getcwd()
    win.create_button("Add image to list", 50, 50, add_img, (directory + "\\addImage.png"), "Add just a single image from your system")
    win.create_button("Load images from folder", 50, 50, add_folder, (directory + "\\addImageFolder.png"), "Select folder with images from your system")
    win.create_button("Test model", 50, 50, test_model, (directory + "\\testImage.png"), "Perform testing and show results")

    ## Start main loop
    win.run()

