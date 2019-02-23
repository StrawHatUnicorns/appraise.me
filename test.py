import io
import os
import requests

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Import wikipedia library for getting the description
import wikipedia

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'C:\\Users\\KArin\\Desktop\\HTV\\red_apple.jpg')

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
		print ("\nDescription: ")
		print (wikipedia.summary(chosenLabel, sentences=3))

		# Scrape price from Walmart
		