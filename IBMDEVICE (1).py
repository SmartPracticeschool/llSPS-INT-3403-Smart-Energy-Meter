import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "p4ogaa"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='switchon':
            print("switch is on")
        elif i=='switchoff':
            print("switch is off")    
            
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        volt =random.randint(10, 40)
        #print(volt)
        cur =random.randint(30, 80)
        #Send Current & Voltage to IBM Watson
        data = { 'Current': cur, 'Voltage': volt }
        #print (data)
        def myOnPublishCallback():
            print ("Published Current = %s C" % cur, "Voltage = %s %%" % volt, "to IBM Watson")

        success = deviceCli.publishEvent("smart energy meter", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
