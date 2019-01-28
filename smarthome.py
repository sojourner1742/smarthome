#---------------Library Setup----------------#
import pubnub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
 
from gpiozero import Button, LED
from time import sleep
 
#--------------------------------------------#
 
 
 
 
#----------------PubNub Setup----------------#
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "YOUR SUBSCRIBE KEY"
pnconfig.publish_key = "YOUR PUBLISH KEY"
pnconfig.ssl = False
pubnub = PubNub(pnconfig)
#--------------------------------------------#

#------------Sensor Declarations-------------#
#lamp is connected to GPIO21 as an LED
lamp = LED(21)
 
#door sensor is connected to GPIO20 as a Button
door_sensor = Button(20)
 
#light sensor is connected to GPIO19 as a Button
light = Button(19)
#--------------------------------------------#
#door counter
doorCount = 0
class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult <link to the PNCONFIGURATION heartbeart config>
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type
 
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def message(self, pubnub, message):
#message handler for Lamp commands
        #Turn the lamp on if client receives the message “ON”
        if message.message == 'ON':
        lamp.on()
              #let your subscriber client know that the lamp has been turned off
        pubnub.publish().channel('ch1').message("lamp has been turned on").async(publish_callback)
        sleep(3)
        #Turn the lamp on if client receives the message “OFF”
        elif message.message == 'OFF':
        lamp.off()
              #let your subscriber client know that the lamp has been turned off
        pubnub.publish().channel('ch1').message("lamp has been turned off").async(publish_callback)
 
 
 
 
pubnub.add_listener(MySubscribeCallback())
#make sure to subscribe to the channel of your choice. In this case, we #chose to create a channel called “ch1” to publish to
pubnub.subscribe().channels('ch1').execute()

while True:

#polling loop to check if the door sensor is on
while door_sensor.is_held:
      #increment the door counter to count how many times the door has been opened
  doorCount = doorCount + 1
  door = "door has been opened: " + str(doorCount) + "times"
  pubnub.publish().channel('ch1').message(door).async(publish_callback)
 
 
door = "door is closed"
pubnub.publish().channel('ch1').message(door).async(publish_callback)
 
#polling loop to check if the lights are on
while light.is_held:
  pubnub.publish().channel('ch2').message("lights are on").async(publish_callback)
 
pubnub.publish().channel('ch2').message("lights are off").async(publish_callback)
 
sleep(3)
