from __future__ import print_function

import cv2
# Import library to display results
import matplotlib.pyplot as plt
import numpy as np
import score_age

import cognitive_api
import score_emotion
import score_gender

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
def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im


# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in range(ramp_frames):
    temp = get_image()
print("Taking image...")
# Take the actual image we want to keep
camera_capture = get_image()
file = "current_image.png"

# analyze image
cv2.imwrite(file, camera_capture)
with open(file, 'rb') as f:
    data = f.read()

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

json = None
params = None

result = cognitive_api.processRequest(json, data, headers, params)

# Find dominant emotion
scoreEmotion = score_emotion.calculate(result)
print(scoreEmotion, " (dominant emotion)")

# Find dominant gender
scoreGender = score_gender.calculate(result)
print(scoreGender, "(most gender)")

# Find dominant age
scoreAender = score_age.calculate(result)
print(scoreAender, "(most age)")

if result is not None:
    # Load the original image from disk
    data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
    img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

    cognitive_api.renderResultOnImage(result, img)

    advert = cv2.imread('Adverts/' + '3' + '.jpg',0)
    cv2.imshow('advert', advert)

    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    ig, ax = plt.subplots(figsize=(15, 20))
    ax.imshow(img)
    cv2.imshow('image', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    del (camera)
