class GUI_CONSTANTS:
    def __init__(self):
        self.WIN_WIDTH = 1024
        self.WIN_HEIGHT = 600

        self.BTN_ROW = 0

        self.IMG_ROW = 1
        self.IMG_PER_ROW = 6

        self.IMGLABEL_ROW = 2
        self.IMGLABEL_WIDTH = 10
        self.IMGLABEL_HEIGHT = 10

        self.STD_PADX = 5
        self.STD_PADY = 5

class CNN_CONSTANTS:
    def __init__(self):
        self.IMG_TARGET_SIZE = [320, 120]
        self.IMG_CATG_NAME = ["Thumbsup", "Finger gun", "Peace", "Thumbsdown", "Left", "Right", "Up", "Down", "Fist", "High five", "Uncertain"]
        self.UNCERTAINTY_THRESHOLD = 0.2