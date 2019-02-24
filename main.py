import os
import io
from flask import Flask, render_template, request
from google.cloud import vision
from google.cloud.vision import types
from nutritionix import Nutritionix

# Import wikipedia library for getting the description
import wikipedia

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("app_body.html")

@app.route("/upload", methods=['POST'])
def upload():
    client = vision.ImageAnnotatorClient()
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    if request.files['file']:
        file = request.files['file']
        destination = "/".join([target, "temp.jpg"])
        file.save(destination)

    file_name = "/".join([target, "temp.jpg"])

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description + " " + str(label.score))

    # Let the user choose what label best fits
    chosenLabel = input("Which label do you choose? ")
    for label in labels:
        if label.description == chosenLabel:
            # Scrape description from Wikipedia


            # Scrape nutrition data
            nix = Nutritionix(app_id="149637d3", api_key="db3b7737e2bb69592a78ddea290e1704")
            apple = nix.search(chosenLabel)
            results = apple.json()
            resultsItem = nix.item(id=results['hits'][0]['fields']['item_id']).json()
            return "Description: " + wikipedia.summary(chosenLabel, sentences=3) + "<br/>" + \
                                        "Calories: " + str(resultsItem['nf_calories']) + "kcal" + "<br/>" + \
                            "Serving Weight: " + str(resultsItem['nf_serving_weight_grams']) + "g"
    #return render_template("app_body.html")

if __name__ == "__main__":
    app.run(port=8080, debug=True)
