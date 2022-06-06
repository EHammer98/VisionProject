import numpy as np
import imutils
import argparse
import cv2
import glob
import os
from matplotlib import pyplot as plt


def convertImage(imdir): 

    image = cv2.imread(imdir)
    # cv2.imshow("Thumbs-up", image)


    #resize picture 5 for clarity
    width = int(816* 0.5)
    height = int(612 * 0.5)
    dim = (width, height)

        # Make pictutre bigger
    resizedImg = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    #cv2.imshow("Thumbs-up", resizedImg)

    # Rgb2gray
    img = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY) 
    #cv2.imshow('imga', img)

    kernel = np.ones((5, 5), 'uint8')
    dilate_img = cv2.dilate(img, kernel, iterations=1)

    z = dilate_img - img

    blur = cv2.bilateralFilter(dilate_img,3,10,10)
    #blur = cv2.medianBlur(dilate_img, 5) # Add median filter to image
    #blur = cv2.GaussianBlur(dilate_img, (5,5), 0)


    # binarize
    thresh = cv2.threshold(blur,118,255,cv2.THRESH_BINARY_INV)[1]

    kernel = np.ones((5, 5), 'uint8')
    dilate_img1 = cv2.dilate(thresh, kernel, iterations=5)

    kernel = np.ones((5, 5), 'uint8')
    dilate_img2 = cv2.erode(dilate_img1, kernel, iterations=3)

    l = len(imdir) # Get length of string 
    newPath = imdir[l - 7:].replace('/', '') # Get last 7 char of string and remove '/'
    cv2.imwrite(("testdata\\bw" + newPath), dilate_img2) # Write out new image



    #Closing all windows after key press
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

