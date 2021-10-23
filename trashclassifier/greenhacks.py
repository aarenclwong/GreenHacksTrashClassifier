# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 12:34:59 2021

@author: rjasp
"""

import numpy as np
import matplotlib.pyplot as plt

import keras.applications.xception as xception

import tensorflow.keras as keras
import tensorflow as tf


from keras.models import load_model
from keras.preprocessing import image


loaded_model = load_model('greenhacks.h5')


categories = {0: 'battery', 1: 'food/biological', 2: 'brown-glass', 3: 'cardboard', 4: 'clothes', 5: 'green-glass', 6: 'metal', 7: 'paper', 8: 'plastic', 9: 'shoes', 10: 'trash', 11: 'white-glass'}
categories2 = {0: 'Recycle at facility or incinerate ', 1:'Compostable', 2: 'Recyclable in most areas', 3: "Recyclable", 4: "Recyclable, with most common fabrics compostable", 5: "Recyclable in most areas", 6: "Recyclable", 7: "Recyclable", 8: "Recyclable", 9: "Recyclable if material is simple, if unsure, incinerate", 10:"Incinerate", 11:"Recyclable in most areas"}

IMG_SIZE = 320 # All images will be resized to 160x160
image_path="pizza.jpg"

def predict_image(image_path):
    img = image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
    plt.imshow(img)
    img = np.expand_dims(img, axis=0)
    result=loaded_model.predict(img)
    return np.argmax(result, axis =1)

print(f"Oscar sees: {categories[predict_image(image_path)[0]]}, it is {categories2[predict_image(image_path)[0]]}")






