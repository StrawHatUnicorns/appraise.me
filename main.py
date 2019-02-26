import os
import io
from flask import Flask, render_template, request
from google.cloud import vision
from google.cloud.vision import types
from nutritionix import Nutritionix

# Import wikipedia library for getting the description
import wikipedia

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\danie\hackvalley\appraise-me-7c169997506a.json"

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("app_body.html")

@app.route("/upload", methods=['POST'])
def upload():
    client = vision.ImageAnnotatorClient()

    if request.files['file']:
        file = request.files['file']
    # Loads the image into memory
        content = file.read()
        image = types.Image(content=content)
        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        return render_template('app_select.html', labels = labels)


@app.route("/result", methods=['Get','POST'])
def result():
        print(request.form['out'])
        chosenLabel= request.form['out']
        nix = Nutritionix(app_id="b3151f58", api_key="f9c4b99b77d236006962c81e4ddbffee")
        apple = nix.search(chosenLabel)
        results = apple.json()
        resultsItem = nix.item(id=results['hits'][0]['fields']['item_id']).json()
        return render_template('description.html', sum = wikipedia.summary(chosenLabel, sentences=3), calories = str(resultsItem['nf_calories']), serving =str(resultsItem['nf_serving_weight_grams']))


if __name__ == "__main__":
    app.run(port=8080, debug=True)
