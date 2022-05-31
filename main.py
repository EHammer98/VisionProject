from os.path import exists
import os
import sys
sys.path.insert(1, "\\")
from cnn import CNN
from img import ImgProcess
import tkinter as tk
import os
from tkinter import *
from tkinter import ttk 
from idlelib.tooltip import Hovertip
from tkinter import filedialog
from PIL import Image # For handling the images
from constants import GUI_CONSTANTS

import math

from matplotlib import image


if __name__ == "__main__":

    ai = CNN('C:\\Users\\timvd\\Documents\\Programming\\Python\\Tensorflow\\handgestures\\data\\leapGestRecog\\00\\',
             'C:\\Users\\timvd\\Documents\\Programming\\Python\\Tensorflow\\handgestures\\data\\leapGestRecog\\0')

    img = []
    dir = ""

    ai.create_model("handgestures")



state = 0

class MainWindow:
    def __init__(self) -> None:

  


        self.CONST = GUI_CONSTANTS()

        self.win = tk.Tk() # Creating the main window and storing the window object in 'win'



        #self.win.geometry( str(self.CONST.WIN_WIDTH) + "x" + str(self.CONST.WIN_HEIGHT) ) # Setting the size of the window
        self.win.resizable(False, False) # Disable window resizing
        self.win.title("Hand Gesture Detector") # Program titel
        directory = os.getcwd() # Get local directory
        self.win.iconphoto(False, tk.PhotoImage(file= (directory + '\\icon.png'))) # Get logo for program
        self.txtlabels = []
        self.imglabels = []
        self.imgfiles = []

        frame0 = LabelFrame(self.win, text="Images")
        
        # Displaying the frame1 in row 0 and column 0
        frame0.grid(row=1, column=0)
        def resetFrame0():
            global state
            global img
            for widgets in frame0.winfo_children():
                widgets.destroy()      
                state = 0    
                self.txtlabels = []
                self.imglabels = []
                self.imgfiles = []
                img = []
                ai.test_batch = []

        def add_img():
            global state
            if state == 2:
                resetFrame0()  
            else:            
                state = 1                          
                dir = filedialog.askopenfilename(initialdir = "./",
                                                title = "Select a file",
                                                filetypes = (("PNG images", "*.png*"),
                                                            ("All files", "*.*"))) 
                ai.test_batch_img_add(dir)
                #self.win.add_img_win(dir)
                self.imgfiles.append(tk.PhotoImage(file = dir).subsample(3, 3))
                self.imglabels.append( tk.Label(frame0, image = self.imgfiles[len(self.imgfiles) - 1]) )

                index = len(self.imglabels) - 1

                row = self.CONST.IMG_ROW + math.floor( (len(self.imgfiles) - 1) / self.CONST.IMG_PER_ROW ) * 2
                column = (len(self.imgfiles) - 1) % self.CONST.IMG_PER_ROW

                self.imglabels[index].grid(row = row, column = column, 
                                        padx = self.CONST.STD_PADX, pady = self.CONST.STD_PADY)


        def test_model():
            global state
            if state == 1:

                res = ai.test_model()

                for i in range(len(res)):
                    #self.win.add_img_label(ai.CONST.IMG_CATG_NAME[res[i]], i)
                    self.txtlabels.append( tk.Label(frame0, text = ai.CONST.IMG_CATG_NAME[res[i]], font=("Bahnschrift", 14), borderwidth=2, relief="ridge") )

                    row = self.CONST.IMGLABEL_ROW + math.floor( (len(self.txtlabels) - 1) / self.CONST.IMG_PER_ROW ) * 2
                    column = (len(self.txtlabels) - 1) % self.CONST.IMG_PER_ROW        
                    self.txtlabels[i].grid(row = row, column = column,
                                                padx = self.CONST.STD_PADX, pady = self.CONST.STD_PADY)
                state = 2
            elif state == 2:
                resetFrame0()
                    

        def add_folder():
            global state
            if state == 2:
                resetFrame0()
            else:            
                state = 1   


                dir = filedialog.askdirectory(initialdir = "./", title = "Select a folder")
                if (exists(dir)):
                    for k in os.listdir(dir):
                        ai.test_batch_img_add(dir + "/" + k)
                        #self.win.add_img(dir + "/" + k) 
                        self.imgfiles.append(tk.PhotoImage(file = (dir + "/" + k)).subsample(3, 3))
                        self.imglabels.append( tk.Label(frame0, image = self.imgfiles[len(self.imgfiles) - 1]) )

                        index = len(self.imglabels) - 1

                        row = self.CONST.IMG_ROW + math.floor( (len(self.imgfiles) - 1) / self.CONST.IMG_PER_ROW ) * 2
                        column = (len(self.imgfiles) - 1) % self.CONST.IMG_PER_ROW

                        self.imglabels[index].grid(row = row, column = column, 
                                                padx = self.CONST.STD_PADX, pady = self.CONST.STD_PADY)        

                                                        

        directory = os.getcwd() #to get the current working directory
        self.img0 = tk.PhotoImage(file=(directory + "\\addImage.png")) 
        self.img1 = tk.PhotoImage(file=(directory + "\\addImageFolder.png")) 
        self.img2 = tk.PhotoImage(file=(directory + "\\testImage.png")) 
        self.img3 = tk.PhotoImage(file=(directory + "\\reset.png")) 
       
        
        # Constructing the first frame, frame1
        frame1 = LabelFrame(self.win, text="Menu")
        
        # Displaying the frame1 in row 0 and column 0
        frame1.grid(row=0, column=0, sticky=NW)
        
        # Constructing the button b1 in frame1
        b0 = Button(frame1, command = add_img, width = 50, height=50, image=self.img0, padx=5, pady=5,borderwidth=4, relief="groove")
        myTip = Hovertip(b0,"Add just a single image from your system") # Generate tooltip on hover for each button
        
        # Displaying the button b1
        b0.grid(row=0, column=0, sticky=NE, padx=5, pady=5)
        # Constructing the button b1 in frame1
        b1 = Button(frame1, command = add_folder, width = 50, height=50, image=self.img1, padx=5, pady=5,borderwidth=4, relief="groove")
        myTip = Hovertip(b1,"Select folder with images from your system") # Generate tooltip on hover for each button
        
        # Displaying the button b1
        b1.grid(row=0, column=1, sticky=NE, padx=5, pady=5)
        # Constructing the button b1 in frame1
        b2 = Button(frame1, command = test_model, width = 50, height=50, image=self.img2, padx=5, pady=5,borderwidth=4, relief="groove")
        myTip = Hovertip(b2,"Perform testing and show results") # Generate tooltip on hover for each button
        
        # Displaying the button b1
        b2.grid(row=0, column=2, sticky=NE, padx=5, pady=5)


        b3 = Button(frame1, command = resetFrame0, width = 50, height=50, image=self.img3, padx=5, pady=5,borderwidth=4, relief="groove")
        myTip = Hovertip(b3,"Reset") # Generate tooltip on hover for each button
        
        # Displaying the button b1
        b3.grid(row=0, column=3, sticky=NE, padx=5, pady=5)

    def run(self) -> None:
        self.win.mainloop()
                                      





app = MainWindow()
app.run()                                      

