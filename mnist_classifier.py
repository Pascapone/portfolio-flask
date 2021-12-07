import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PIL import ImageFile, Image
from numpy import expand_dims
import numpy as np
from tensorflow.keras.preprocessing import image as image_preprocessing
from tensorflow.keras.models import load_model
from itertools import permutations
from scipy.ndimage.measurements import center_of_mass
import sys
import json
import math
import cv2

model = load_model('./ml/models/mnist-model_cnn.h5')

def byte_string_2_image(data):
    data = data.decode('utf8')
    point_dict = json.loads(data) 

    image = np.zeros(shape=(200,200))
    
    # JSON of points and lines to array
    for line in point_dict['lines']:
        for point in line['points']:
            x, y = point.values()
            x = round(x)
            y = round(y)
            image[y,x] = 1  

    return image

def prerocessing_image(image):
    # The mnist dataset was created using 20x20 pixel images, centered in 28x28 pixel images (regarding to its center of mass). 
    # Transform the data to fit the conditions.
    # The canvas of the input images is size 200x200 pixel
    
    # Thickening our 1 pixel lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    image = cv2.dilate(image, kernel, iterations=9)

    # Applying some blur to better fit the mnist dataset
    image = cv2.blur(image,(5,5))

    # Remove empty columns and rows
    while np.sum(image[0]) == 0:
        image = image[1:]

    while np.sum(image[:,0]) == 0:
        image = np.delete(image,0,1)

    while np.sum(image[-1]) == 0:
        image = image[:-1]

    while np.sum(image[:,-1]) == 0:
        image = np.delete(image,-1,1)

    rows,cols = image.shape[0:2]

    # Resize the image so that either width or height is 20
    if rows > cols:
        factor = 20.0/rows
        rows = 20
        cols = int(round(cols*factor))
        pil_image = Image.fromarray(np.uint8(image.squeeze() * 255), 'L')
        pil_image = pil_image.resize((cols,rows), Image.NEAREST)    
        image = image_preprocessing.img_to_array(pil_image)
    else:
        factor = 20.0/cols
        cols = 20
        rows = int(round(rows*factor))
        pil_image = Image.fromarray(np.uint8(image.squeeze() * 255), 'L')
        pil_image = pil_image.resize((cols,rows), Image.NEAREST)    
        image = image_preprocessing.img_to_array(pil_image) 
  
    # Creating the padding for 28x28 pixel image
    colsPadding = (int(math.ceil((28 - cols)/2.0)),int(math.floor((28 - cols)/2.0)))
    rowsPadding = (int(math.ceil((28 - rows)/2.0)),int(math.floor((28 - rows)/2.0)))
    image = np.lib.pad(image.squeeze(),(rowsPadding,colsPadding),'constant')

    # Get the center of mass    
    cy,cx = center_of_mass(image)
    rows,cols = image.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)   
    
    # Shift the image   
    rows,cols = image.shape
    M = np.float32([[1,0,shiftx],[0,1,shifty]])
    image = cv2.warpAffine(image,M,(cols,rows))  
    np.save(r'C:\Users\pasca\Documents\MonkeyMoon\BaseTemplates\portfolio-project\backend\image.npy', image)
    return image


def get_prediction(image, model): 
    # Expand dimension (model expects (batch_size, 28, 28, 1) shape)
    image = expand_dims(image, axis=0)
    image = expand_dims(image, axis=-1)

    # Predict
    preds = model.predict(image)
      
    return str(np.argmax(preds.squeeze()))

def classify_mnist_image(data): 
    image = byte_string_2_image(data)  

    image = prerocessing_image(image)

    pred = get_prediction(image, model)     
    return pred

