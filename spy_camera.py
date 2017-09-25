#
# Monitor activity using the PIR sensor.
# When movement is detected, capture a still image from the camera
#
# Note:
#  - The PIR sensor seems a little flaky.  It appears to pick up sporatic movement
#    even when there is none.  This can cause the timeout threshold to be not met,
#    or cause a pre-mature in-office event to be triggered
#  - Research and testing seem to point to WiFi interference as the culprit.  Turning off the
#    WiFi adapter on the Pi, or using longer cables and/or sheilding seems to help.
#
from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep,strftime,localtime

# PIR sensor is attached to pin #4 on the GPIO
pir = MotionSensor(24)

# Camera does not use the GPIO; it has it's own dedicated interface
camera = PiCamera()

# Resolution can be adjusted
camera.resolution = (1024, 768)

# Camera effects are possible too!
#camera.image_effect = 'sketch'

# Loop forever!
while True:
    if pir.motion_detected:
        filename = strftime("Pictures/%Y-%m-%d-%H%M%S.jpg", localtime())
        print("Capturing photo " + filename)
        camera.start_preview()
        camera.annotate_text = 'Intruder alert!'
        sleep(2)
        camera.capture(filename)
        camera.stop_preview()

    # Let's not go crazy and take too many pictures!
    sleep(3)
