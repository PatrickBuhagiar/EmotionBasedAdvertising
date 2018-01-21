from __future__ import print_function

import time
import cv2
# Import library to display results
import matplotlib.pyplot as plt
import numpy as np
import score_age

from PIL import Image
import cognitive_api
import score_emotion
import score_gender
import psutil
import requests
from io import BytesIO
from io import StringIO
import urllib

# Camera 0 is the integrated web cam on my netbook
camera_port = 0

# Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30

# Variables
_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses,emotion,hair'
_key = 'c82e927ab44c4a31904d75d2d81e2681'  # Here you have to paste your primary key
_maxNumRetries = 10

# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)


# Captures a single image from the camera and returns it in PIL format
def take_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im


def get_image():
    for i in range(ramp_frames):
        temp = take_image()
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = take_image()
    file = "current_image.png"
    cv2.imwrite(file, camera_capture)
    with open(file, 'rb') as f:
        data = f.read()
    return data

def makePostRequest(score):
    _url = 'http://localhost:8080/adverts/choose'
    response = requests.request('post', _url, json=score)
    return response

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

json = None
params = None

while True:

    data = get_image()

    result = cognitive_api.processRequest(json, data, headers, params)

    if result is not None and result != []:

        # Find dominant emotion
        scoreEmotion = score_emotion.calculate(result)
        print(scoreEmotion, " (dominant emotion)")

        # Find dominant gender
        scoreGender = score_gender.calculate(result)
        print(scoreGender, "(most gender)")

        # Find dominant age
        scoreAge = score_age.calculate(result)
        print(scoreAge, "(most age)")

        score = {"emotion":scoreEmotion.upper(), "gender":scoreGender.upper(), "ageGroup":"ALL"}
        print(str(score))
        advert = makePostRequest(score).json()
        print(str(advert))

        # Load the original image from disk
        data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
        img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

        cognitive_api.renderResultOnImage(result, img)

        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()

        #advert = Image.open('Adverts/3.jpg')
        #img.show()


        URL = advert["imgURL"]

        with urllib.request.urlopen(URL) as url:
            with open('temp.jpg', 'wb') as f:
                f.write(url.read())

        advertImage = Image.open('temp.jpg')

        #urllib.urlopen(url).read()
        #print(advert["imgURL"])
        #cv2.imshow('advert', advert)
        advertImage.show()

        # A nice feature of the imwrite method is that it will automatically choose the
        # correct format based on the file extension you provide. Convenient!
        #ig, ax = plt.subplots(figsize=(15, 20))
        #ax.imshow(img)
        #cv2.imshow('image', img)

        time.sleep(3)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # You'll want to release the camera, otherwise you won't be able to create a new
        # capture object until your script exits
del (camera)
for proc in psutil.process_iter():
    if proc.name() == "display":
        proc.kill()
