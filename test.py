import io
import os
import requests
from bs4 import BeautifulSoup

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Import wikipedia library for getting the description
import wikipedia
import json

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
		URL = "https://www.walmart.ca/search/banana/N-117"
		page = requests.get(URL,headers={"User-Agent":"Defined"})
		json = page.json()

		soup = BeautifulSoup(page.content, "html.parser")
		price = json
		#price = soup.find(class_="price-current width-adjusted").get_text()
		print(price)