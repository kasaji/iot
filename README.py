"""
My First Internet of Things

Temperature/Humidity Light monitor using Raspberry Pi, DHT11, and photosensor 
Data is displayed at thingspeak.com
2015/06/15
SolderingSunday.com

Based on project by Mahesh Venkitachalam at electronut.in

"""
# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2
import requests



DEBUG = 1
#Common pin of LDR and Capacitor
RCpin = 24
#Temperature Pin
DHTpin = 2 

#Setup our API and delay

#get your WRITE API KEY from thingspeak
myAPI = "YOUR_API_KEY"

#how many seconds between posting data
myDelay = 2

GPIO.setmode(GPIO.BCM)

#Put RC Pin as input 
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
    
    #Convert from Celius to Farenheit
    TWF = 9/5*TW+32
   
    # return dict
    print ('1: ' + str(RHW) + '2: '+ str(TW) +'3: '+ str(TWF))
    return (str(RHW), str(TW),str(TWF))

def RCtime(RCpin):
    LT = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    sleep(int(0.1))

    GPIO.setup(RCpin, GPIO.IN)
    
    if (GPIO.input(RCpin) == True):
        LT += 1
    print(str(LT))
    return (str(LT))

    
# main() function
def main():
    
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    
    while True:
        try:
            RHW, TW, TWF = getSensorData()
            LT = RCtime(RCpin)
            
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s&field3=%s" % (TW, TWF, RHW)+
                                "&field4=%s" % (LT))
            
            #print f.read()
            print f
            print TW + " " + TWF+ " " + RHW + " " + LT
            f.close()
            if (TW > 25) :
                r = requests.post(url = "https://maker.ifttt.com/trigger/high_temp/with/key/cf8MIaFApx7BMy45EzU12Sovp0MqLERe-KSjWgyAjrG", data = None)

            sleep(int(myDelay))
        except:
            print 'exiting.'
            break

# call main

if __name__ == '__main__':
    main()


