import os, sys
import openai
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
import cv2
import string
import datetime, time
import numpy as np
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt

import keras.applications.xception as xception

import tensorflow.keras as keras
import tensorflow as tf


from keras.models import load_model
from keras.preprocessing import image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder="static", static_url_path="/static", template_folder="templates")
prediction = ""
camera = cv2.VideoCapture(0)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camerapage():
    return render_template('camera.html')

@app.route('/send', methods=['POST'])
def my_form_post():
    global prediction
    input = request.values.get('input')
    prediction = predict(input)
    return prediction

global capture, switch, frame, img_pred
capture=0
switch=1


@app.route('/camera/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            success, frame = camera.read()
            if(success):
                p = os.path.sep.join(['static', "shot.jpg"])
                cv2.imwrite(p, frame)
                return render_template('camera.html', img_pred=predict_image("static/shot.jpg"))
        elif request.form.get('stop') == 'Stop/Start':
            if (switch == 1):
                switch = 0
                camera.release()
                cv2.destroyAllWindows()

            else:
                camera = cv2.VideoCapture(0)
                switch = 1


    elif request.method == 'GET':
        return render_template('camera.html')
    return render_template('camera.html')

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass
@app.route('/camera/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():  # generate frame by frame from camera
    global capture, rec_frame, img_pred
    while True:
        success, frame = camera.read()
        if success:
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


def predict(message):
    if message is None:
        return ""
    else:
        prompt = f"The following is a list of trash items classified into Compost, Recycle, or Incinerate\n\nPlastic Bag: Incinerate\nPaper: Recycle\nCardboard: Recycle\nNapkin: Compost\nFruit: Compost\nClothing: Incinerate\nFlower: Compost\nChip Bag: Incinerate\nMetal Can: Recycle\nStyrofoam: Incinerate\nRubber: Incinerate\nEggs: Compost\nCoffee Grinds: Compost\nGlass: Recycle\nMeat: Incinerate\nVegetable: Compost\nNewspaper: Recycle\nPlastic: Incinerate\nMagazine: Recycle\nCandy Wrapper: Incinerate\nAluminum Foil: Recycle\nTea Bag: Compost\npizza: Compost\n{message}:",
        response = openai.Completion.create(
            model="davinci",
            prompt=prompt,
            temperature=.2,
            max_tokens=3,
            top_p=.2,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )

        prediction = response.choices[0].text.strip()
        return prediction
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
    maxval= np.argmax(result, axis =1)[0]
    return(f"Oscar sees: {categories[maxval]}, it is {categories2[maxval].lower()}")


if __name__ == '__main__':
    app.run()
