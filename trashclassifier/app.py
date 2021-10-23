import os
import openai
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder="static", static_url_path="/static", template_folder="templates")
prediction = ""


@app.route('/send', methods=['POST'])
def my_form_post():
    global prediction
    input = request.values.get('input')
    prediction = predict(input)
    return prediction

@app.route('/')
def index():
    return render_template('index.html')


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
