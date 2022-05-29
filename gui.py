
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

txt = []
tip = []
img = []

class MainWindow:
    def __init__(self) -> None:
        self.CONST = GUI_CONSTANTS()

        self.win = tk.Tk() # Creating the main window and storing the window object in 'win'
        self.win.geometry( str(self.CONST.WIN_WIDTH) + "x" + str(self.CONST.WIN_HEIGHT) ) # Setting the size of the window
        self.win.resizable(False, False) # Disable window resizing
        self.win.title("Hand Gesture Detector") # Program titel
        self.style = ttk.Style(self.win) # Set style
        self.style.theme_use('classic') # Set theme for program   
        directory = os.getcwd() # Get local directory
        self.win.iconphoto(False, tk.PhotoImage(file= (directory + '\\icon.png'))) # Get logo for program
        self.buttons = []
        self.entryboxes = []
        self.entryboxes_strvar = []
        self.txtlabels = []
        self.imglabels = []
        self.imgfiles = []


    def run(self) -> None:
        self.win.mainloop()
        

    def create_button(self, text, w, h, command, im, tooltip) -> None:
        #self.img = tk.PhotoImage(file=im) 
        global txt 
        global tip 
        global img 

        txt.append(command)  
        tip.append(tooltip)
        img.append(tk.PhotoImage(file=im) )
        self.buttons.append(tk.Button(self.win, text = text, width = w, height = h, command = command))
        # self.buttons[len(self.buttons) - 1].place(x = x, y = y)
        col = len(self.buttons) - 1
        self.buttons[len(self.buttons) - 1].grid(row = self.CONST.BTN_ROW, column = col,
                                                padx = self.CONST.STD_PADX, pady = self.CONST.STD_PADY)
       #Perform some action for every button created
        for i in self.buttons:   
            i.configure(image = img[self.buttons.index(i)])        
            myTip = Hovertip(i,str(tip[self.buttons.index(i)])) # Generate tooltip on hover for each button
                                      


    def create_entrybox(self, text, x, y, w, ) -> None:
        self.entryboxes_strvar.append(tk.StringVar())

        index = len(self.entryboxes_strvar) - 1
        self.entryboxes.append(tk.Entry(self.win, text = text, width = w, textvariable = self.entryboxes_strvar[index]))
        self.entryboxes[index].grid(row = 1, column = 0, padx = 5, pady = 5)


    def get_entrybox_value(self, index) -> str:
        return self.entryboxes_strvar[index].get()


    def open_img(self) -> str:
        return filedialog.askopenfilename(initialdir = "./",
                                              title = "Select a file",
                                              filetypes = (("PNG images", "*.png*"),
                                                           ("All files", "*.*")))  

    def open_dir(self) -> list:
        return filedialog.askdirectory(initialdir = "./", title = "Select a folder")

    def add_img(self, imgdir) -> None:
        self.imgfiles.append(tk.PhotoImage(file = imgdir).subsample(3, 3))
        self.imglabels.append( tk.Label(self.win, image = self.imgfiles[len(self.imgfiles) - 1]) )

        index = len(self.imglabels) - 1

        row = self.CONST.IMG_ROW + math.floor( (len(self.imgfiles) - 1) / self.CONST.IMG_PER_ROW ) * 2
        column = (len(self.imgfiles) - 1) % self.CONST.IMG_PER_ROW

        self.imglabels[index].grid(row = row, column = column, 
                                   padx = self.CONST.STD_PADX, pady = self.CONST.STD_PADY)

    def add_img_label(self, text, img_index):
        self.txtlabels.append( tk.Label( self.win, text = text, relief = tk.RAISED) )

        row = self.CONST.IMGLABEL_ROW + math.floor( (len(self.txtlabels) - 1) / self.CONST.IMG_PER_ROW ) * 2
        column = (len(self.txtlabels) - 1) % self.CONST.IMG_PER_ROW        
        self.txtlabels[img_index].grid(row = row, column = column,
                                       padx = self.CONST.STD_PADX, pady = self.CONST.STD_PADY)



        
