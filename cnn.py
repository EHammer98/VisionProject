from re import L
import numpy as np # We'll be storing our data as numpy arrays
import os # For handling directories
from PIL import Image # For handling the images
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # Plotting
from random import randint

import keras
from keras.utils.np_utils import to_categorical
from keras import layers
from keras import models
from sklearn.model_selection import train_test_split

class CNN:
    def __init__(self, check_dir, data_dir):
        self.check_dir = check_dir
        self.data_dir = data_dir
        self.img_data = []
        self.img_catg = []
        self.test_img_data = []
        self.test_img_catg = []
        self.model = ""

        self.IMG_CATG_NAME = ["Thumbs-up", "Thumbs-down", "High five", "-", "-", "-", "-", "-", "-", "-"]

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
                        img = img.resize((320, 120)) # Resize images
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

        self.img_data = self.img_data.reshape((datacount, 120, 320, 1))
        self.img_data /= 255

        # Split dataset into training set and test set
        x_train,x_further,y_train,y_further = train_test_split(self.img_data,self.img_catg,test_size = 0.2)
        x_validate,self.test_img_data,y_validate,self.test_img_catg = train_test_split(x_further,y_further,test_size = 0.5)

        # Add layers to CNN for image analysation
        self.model = models.Sequential()
        self.model.add(layers.Conv2D(32, (5, 5), strides=(2, 2), activation='relu', input_shape=(120, 320,1))) 
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu')) 
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(128, activation='relu'))
        self.model.add(layers.Dense(10, activation='softmax'))

        # Train and compile CNN model (might take a while to complete)
        self.model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
        self.model.fit(x_train, y_train, epochs=1, batch_size=64, verbose=1, validation_data=(x_validate, y_validate))

        # Evaluate model accuracy
        [loss, acc] = self.model.evaluate(self.test_img_data,self.test_img_catg,verbose=1)
        print("Accuracy:" + str(acc))

        # Save model for future use
        self.model.save(name + ".h5", include_optimizer=True)

    # def test_model(self, batch_size):
    #     test_batch = []
    #     test_result = []

    #     # Add layer so the model outputs its predictions
    #     probability_model = keras.Sequential([self.model, 
    #                                          keras.layers.Softmax()])

    #     for i in range (0, batch_size):
    #         test_batch.append(self.test_img_data[i])
    #         test_batch[i] = (np.expand_dims(test_batch[i],0))

    #         test_result.append(probability_model.predict(test_batch[i]))

    #         print(np.argmax(test_result[i]))

    #         plt.subplot(3, 3, i + 1)
    #         plt.imshow(self.test_img_data[i])
    #         plt.title(self.test_img_catg[i])

    #     plt.show()

    def test_model(self, test_batch = []):
        test_batch_pred = []
        test_result = []

        # Add layer so the model outputs its predictions
        probability_model = keras.Sequential([self.model, 
                                             keras.layers.Softmax()])                                  

        for i in range( len(test_batch) ):

            test_batch_pred.append(np.expand_dims(test_batch[i],0))
            test_result.append(probability_model.predict( test_batch_pred[i]))  

            # print(np.argmax(test_result[i]))

            plt.subplot(3, 3, i + 1)
            plt.imshow(test_batch[i])
            plt.title( self.IMG_CATG_NAME[ np.argmax(test_result[i]) ] )

        plt.show()

    def load_model(self, name):
        self.model = keras.models.load_model(name + ".h5")
        self.model.compile(optimizer='rmsprop',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])