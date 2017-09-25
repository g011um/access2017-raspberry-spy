#
# Monitor activity using the PIR sensor.
# When movement is seen, start the full screen camera preview for 10 seconds
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
from time import sleep

# PIR sensor is attached to pin #4 on the GPIO
pir = MotionSensor(24)

# Camera does not use the GPIO; it has it's own dedicated interface
camera = PiCamera()

# Loop forever!
while True:
    if pir.motion_detected:
        camera.start_preview()
        sleep(10)
        camera.stop_preview()

    # Don't need to constantly poll the PIR sensor
    sleep(0.025)
