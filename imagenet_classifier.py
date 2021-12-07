import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PIL import ImageFile, Image
from numpy import expand_dims
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as image_preprocessing
from tensorflow.keras.applications.resnet50 import ResNet50
import requests
from io import BytesIO
import sys

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Load ResNet50 model with imagenet weights
model = ResNet50(weights='imagenet')

def get_prediction(url, model):

    # Request image
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, stream=True, headers=headers)
    
    image = Image.open(BytesIO(response.content))

    # Convert to RGB space and transfrom to (224, 224, 3) shape (resnet shape)
    image = image.convert('RGB')
    image = image.resize((224, 224), Image.NEAREST)
    
    # Image to numpy array
    image = image_preprocessing.img_to_array(image)

    # Expand dimension (resnet expects (batch_size, 224, 224, 3) shape)
    image = expand_dims(image, axis=0)

    # Use the preprocessing pipeline resnet
    image = preprocess_input(image, mode='caffe')

    # Predict
    preds = model.predict(image)
    
    return preds

def classify_image(url):
    # Call the predict pipeline
    preds = get_prediction(url, model)

    # Decode the output (matrix of probabilities) to string (highest prob)
    prediction = decode_predictions(preds, top=1)
    result = str(prediction[0][0][1])

    # Make the string more appealing
    result = " ".join([x.capitalize() for x in result.split('_')])
    return result