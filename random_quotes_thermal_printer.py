#Code in development. Absolutely do not fork.

#Original sources for project and code:
#Make a Raspberry Pi fortune teller that prints your future on Howchoo - https://howchoo.com/g/zdg2zgm1yjn/make-a-raspberry-pi-fortune-teller
#Sending Things to a Printer in Python - https://smallbusiness.chron.com/sending-things-printer-python-58655.html

#TO DO
#Proof of concept had problems printing graphics and unicode characters.
#Testing using the os.system printing functions first. THEN:
#Testing using code at https://github.com/adafruit/Python-Thermal-Printer and methodology at https://learn.adafruit.com/pi-thermal-printer/pi-setup-part-3 needed.

import random #Importing random module for randomness and stuff
import serial #Importing serial module for communcation
import adafruit_thermal_printer #Importing adafruit thermal printer library
import RPi.GPIO as GPIO #Importing Raspberry Pi GPIO module
import time #Importing time module
#import os #Importing the os module to be able to access command line/OS functions

#We create a list of quotes to be chosen from.
quotes = [
    "Quote 1 --Quotesperson",
    "Quote 2 --Quotesperson",
    "Quote 3 --Quotesperson",
]


GPIO.setmode(GPIO.BOARD) #We activate the pins with the physical GPIO numbering scheme
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #We tell the Pi to look out for a connection between 3.3V and GPIO 18 pin. We can change pins if we wanna.
GPIO.setwarnings(False) #YOLO, disabling warnings from GPIOs.

def button(): #Defining the button method
    while True: # Run the button method forever
        if GPIO.input(18) == GPIO.HIGH: #If the button connected to pins is pressed...
            time.sleep(1) #Put the pins to sleep for a beat - our guess: so we don't get multiple presses
            getfortune() #Trigger the getfortune() method

def getfortune():
    #Initiates necessary printer functions
    uart = serial.Serial("/dev/USB0", baudrate=9600, timeout=3000) #Modified the parameters for Adafruit's USB thermal printer - usually /dev/usb0
    ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
    printer = ThermalPrinter(uart, auto_warm_up=False) #Defining comm protocol, deactivating auto warmup
    printer.warm_up() #Warming up the printer

    #Edit the text below to adjust the receipt design
    printer.feed(2) #Blank line
    printer.underline = adafruit_thermal_printer.UNDERLINE_THIN #Add a thin underline
    printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER #Center the text
    printer.print(' *.. Quote 2 Go ..* ') #We got a title!
    printer.feed(2) #Blank line
    printer.underline = None #Removes underline
    printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT #Left alight text
    printer.print(random.choice(fortunes)) #Second line of text will be a random fortune
    printer.feed(2) #Blank line
    printer.feed(2) #Blank line  
    #os.system("lpr -P zj-58 file_name.txt") #Testing printing out a picture through the OS command line via Python. Thank you os module!
    print("Button was pushed!") #Tell the world that the button has been pushed!

button() #We call the button method to check the button state
GPIO.cleanup() #We clean up the state of GPIOs
