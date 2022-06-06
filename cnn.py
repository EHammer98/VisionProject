from re import L
import numpy as np # We'll be storing our data as numpy arrays
import os # For handling directories
from os.path import exists
from PIL import Image # For handling the images
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # Plotting
from random import randint

import keras
from keras.utils.np_utils import to_categorical
from keras import layers
from keras import models
from sklearn.model_selection import train_test_split

from constants import CNN_CONSTANTS

class CNN:
    def __init__(self, check_dir, data_dir):
        self.CONST = CNN_CONSTANTS()

        self.model = ""
        self.check_dir = check_dir
        self.data_dir = data_dir

        # Used to train the model
        self.img_data = []
        self.img_catg = []
        self.test_img_data = []
        self.test_img_catg = []

        # Used to test the model
        self.test_batch = []


    def create_model(self, name):
        if (os.path.exists(name + ".h5") == True):
            self.load_model(name)
            return

        # Ensure program doesn't read from hidden folders
        lookup = dict()
        reverselookup = dict()
        count = 0
        for j in os.listdir(self.check_dir):
            if not j.startswith('.'): 
                lookup[j] = count
                reverselookup[count] = j
                count = count + 1
        lookup

        datacount = 0
        for i in range(0, 10): # Loop over the ten top-level folders
            for j in os.listdir(self.data_dir + str(i) + '/'):
                if not j.startswith('.'): # Avoid hidden folders
                    count = 0
                    for k in os.listdir(self.data_dir + 
                                        str(i) + '/' + j + '/'):
                                        # Loop over the images
                        img = Image.open(self.data_dir + 
                                         str(i) + '/' + j + '/' + k).convert('L')
                                        # Read in and convert to greyscale
                        img = img.resize( self.CONST.IMG_TARGET_SIZE) # Resize images
                        arr = np.array(img) # Add to NumPy array
                        self.img_data.append(arr) 
                        count = count + 1
                    y_values = np.full((count, 1), lookup[j]) 
                    self.img_catg.append(y_values)
                    datacount = datacount + count
        self.img_data = np.array(self.img_data, dtype = 'float32')
        self.img_catg = np.array(self.img_catg)
        self.img_catg = self.img_catg.reshape(datacount, 1) # Reshape to be the correct size

        self.img_catg = to_categorical(self.img_catg)

        self.img_data = self.img_data.reshape((datacount, self.CONST.IMG_TARGET_SIZE[1], self.CONST.IMG_TARGET_SIZE[0], 1))
        self.img_data /= 255

        # Split dataset into training set and test set
        x_train,x_further,y_train,y_further = train_test_split(self.img_data,self.img_catg,test_size = 0.2)
        x_validate,self.test_img_data,y_validate,self.test_img_catg = train_test_split(x_further,y_further,test_size = 0.5)

# Add layers to CNN for image analysation
        self.model = models.Sequential()
        self.model.add(layers.Conv2D(32, (5, 5), strides=(2, 2), activation='relu', input_shape=(self.CONST.IMG_TARGET_SIZE[1], self.CONST.IMG_TARGET_SIZE[0], 1))) 
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu')) 
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu')) 
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(256, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(180, activation='relu'))
        self.model.add(layers.Dropout(0.10))
        self.model.add(layers.Dense(10, activation='softmax'))

        # Train and compile CNN model (might take a while to complete)
        self.model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
        self.model.fit(x_train, y_train, epochs=2, batch_size=64, verbose=1, validation_data=(x_validate, y_validate))

        # Evaluate model accuracy
        [loss, acc] = self.model.evaluate(self.test_img_data,self.test_img_catg,verbose=1)
        print("Accuracy:" + str(acc))

        # Save model for future use
        self.model.save(name + ".h5", include_optimizer=True)

    def test_batch_img_add(self, imgdir):
        if (exists(imgdir)):
            self.test_batch.append( Image.open(imgdir).convert('L').resize(self.CONST.IMG_TARGET_SIZE) )
        else: 
            print("File does not exist")

    def test_model(self) -> list:
        test_batch_pred = []
        test_result = []
        res = []

        # Add layer so the model outputs its predictions
        probability_model = keras.Sequential([self.model, 
                                             keras.layers.Softmax()])                                  

        for i in range( len(self.test_batch) ):

            test_batch_pred.append(np.expand_dims(self.test_batch[i],0))
            test_result.append(probability_model.predict( test_batch_pred[i]))
            index = np.argmax(test_result[i])

            if ( test_result[i][0][index] >= self.CONST.UNCERTAINTY_THRESHOLD): 
                res.append( np.argmax(test_result[i]) )
            else:
                res.append( len(self.CONST.IMG_CATG_NAME) - 1 )

        return res

    def load_model(self, name):
        self.model = keras.models.load_model(name + ".h5")
        self.model.compile(optimizer='rmsprop',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])