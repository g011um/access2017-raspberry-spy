#!/usr/bin/python
# import the necessary packages 
from io import BytesIO
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import imutils
import cv2
import sys

#my_stream = BytesIO()
camera = PiCamera()
rawCapture = PiRGBArray(camera)
camera.start_preview()
sleep(2)
#camera.capture(my_stream, 'jpeg')
camera.capture(rawCapture, format="bgr")
image = rawCapture.array


firstFrame = None

# loop over the rawCaptures of the video
while True:
#    (grabbed, rawCapture) = camera.read()
    text = "Unoccupied"

#    if not grabbed:
#        break

    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BCR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    imageDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(imageDelta, 25, 255, cv2.THRESH_BINARY)[1]


    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image, (x,y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    cv2.putText(image, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(image, datetime.datetime.now(). strftime("%A %d %B %Y %I:%M:%S%p"), (10, image.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Security Feed", image)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", imageDelta)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
