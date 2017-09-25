#
# Monitor activity using the PIR sensor.
# If no movement is seen for the specified period, update Slask with an out-of-office message.
# When movement is seen again, update Slack with an in-office message.
#
# Note:
#  - The PIR sensor seems a little flaky.  It appears to pick up sporatic movement
#    even when there is none.  This can cause the timeout threshold to be not met,
#    or cause a pre-mature in-office event to be triggered
#  - Research and testing seem to point to WiFi interference as the culprit.  Turning off the
#    WiFi adapter on the Pi, or using longer cables and/or sheilding seems to help.
#
from gpiozero import MotionSensor
from time import *

# SlackClient is an external library that may need to be installed via pip
from slackclient import SlackClient


# Function to update a persons Slack status with the given text and emoji
def setSlackStatus(status_test, status_emoji):
    # IMPORTANT: It's a super bad idea to put a Slack tokens here
    # They should come from some secure external source and not be inside the code
    # The token used here is a legacy test token generated here: https://api.slack.com/custom-integrations/legacy-tokens
    slack_api_token = 'xxxx-12345-12345-12345-1234567890'
    user_token = slack_api_token

    sc = SlackClient(slack_api_token)
    ret = sc.api_call(
        'users.profile.set',
        token=user_token,
        profile="{'status_text': '" + status_test + "', 'status_emoji': '" + status_emoji + "'}"
    )


# Actions to perform when transitioning to an Out Of Office state
def outOfOffice():
    print(strftime("%a, %d %b %Y %H:%M:%S", localtime()) + ": You are now Out-Of-Office")
    setSlackStatus('Out of the office', ':x:')


# Actions to perform when transitioning to an In Office stat
def inOffice():
    print(strftime("%a, %d %b %Y %H:%M:%S", localtime()) + ": You are now In-Office. Welcome back!")
    setSlackStatus('Back in the office', ':white_check_mark:')


# The PIR sensor is attached to pin 4 on the GPIO
pir = MotionSensor(4)

# This is the inactivity threshold (in seconds) after which the status is updated
threshold = 180

# A flag indicting the current state
active = True

# The time of the last activity sensed by the PIR
lastActivity = time()

print(strftime("%a, %d %b %Y %H:%M:%S", localtime()) + ": Activity monitor started")

# Loop forever!
while True:
    if pir.motion_detected:
        # Motion detected; update the last active time
        lastActivity = time()
        if not active:
            # If the current state is "Not Active", wake up!
            active = True
            inOffice()
    else:
        # No motion detected
        # Don't do anything unless the current state is Active, AND
        # the amount of inactivity has passed the defined threshold
        if active and ((time() - lastActivity) > threshold):
            # Passed the inactivity threshold; go to sleep
            active = False
            outOfOffice()
            
    # Don't need to constantly poll the PIR sensor
    sleep(0.025)

