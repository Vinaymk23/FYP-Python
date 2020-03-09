import os
import serial
import io
import string
import csv

import openpyxl
import numpy
import pandas



# Global Variables
ser = 0
csvfile = 0
listData = []
# Function to Initialize the Serial Port
def init_serial():
    global ser  # Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = 'COM38'  #COMNUM - 1  # COM Port Name Start from 0
    #  ser.port = '/dev/ttyUSB0' #If Using Linux

    #ser.timeout = None # TimeOut in seconds since we need one line at a time.
    ser.timeout = 2 # Set timeout to 2 seconds to implement the break from UART Rx subroutine.
    ser.open()  # Opens SerialPort


    # print port open or closed
    if ser.isOpen():
        print ('Open: ' + ser.port)
        #temp = b'Type what you want to send, hit enter:\r\n'  # This could be replaced with the 'Curpower Command'
        #ser.write(temp)  # Writes to the SerialPort

# Function Ends Here

def ReadSerialPort():
    global csvfile
    global listData
    TimeoutCounter = 0
    print('Starting UART Rx')
    while 1:
        TimeoutCounter = TimeoutCounter + 1
        bytes = ser.readline().decode('ascii')  # Read from Serial Port
        if bytes :
            TimeoutCounter = 0
            splitstring = str.split(str(bytes))
            print (splitstring)  # Print What is Read from Port
            #csvfile.writerow(splitstring)
        # IF Bytes ends here

        else:
            # print(TimeoutCounter)
            if TimeoutCounter > 1:
                # print('UART Rx Ended')
                break



def ReadSerialPortToCSV():
    global csvfile
    global listData
    listIndex = 0
    TimeoutCounter = 0
    print('Starting UART Rx')

    while 1:
        TimeoutCounter = TimeoutCounter + 1
        bytes = ser.readline().decode('ascii')  # Read from Serial Port

        if bytes :
            TimeoutCounter = 0
            splitstring = str.split(str(bytes))
            #listData.append([])
            listData.append(splitstring)
            listIndex = listIndex + 1

            if splitstring == '>':
                break

            else:
                print (splitstring)  # Print What is Read from Port
                #csvfile.writerow(splitstring)
        # This Else code should execute when UART Rx Times out
        else:
            #print(TimeoutCounter)
            if TimeoutCounter > 2:
                #print('UART Rx Ended')
                break

# Read Serial port endd here.

def send_wl_mpc():
    temp = b'wl mpc 0\r\n'  # This could be replaced with the 'Curpower Command'
    ser.write(temp)  # Writes to the SerialPort

def send_wl_up():
    temp = b'wl up\r\n'  # This could be replaced with the 'Curpower Command'
    ser.write(temp)  # Writes to the SerialPort

def send_wl_conList():
    temp = b'wl country list\r\n'  # This could be replaced with the 'Curpower Command'
    ser.write(temp)  # Writes to the SerialPort

def send_wl_curPow():
    temp = b'wl curpower\r\n'  # This could be replaced with the 'Curpower Command'
    ser.write(temp)  # Writes to the SerialPort


# Call the Serial Initilization Function, Main Program Starts from here

#Init CSV File Creation
os.chdir('C:\\Users\\wwfe\\Desktop')
fp = open('sample1.csv', newline='', mode='w')
csvfile = csv.writer(fp,dialect='excel')
# CSV File Creation Init ends here.


init_serial()       # Init COM Port

send_wl_mpc()
ReadSerialPort()    # Read Data from Serial Port
print('MPC Response Complete')
send_wl_up()
ReadSerialPort()    # Read Data from Serial Port
print('wl_up Response Complete')
send_wl_conList()
ReadSerialPort()

send_wl_curPow()
ReadSerialPortToCSV()    # Read Data from Serial Port
print('Country List Response Complete')
print(listData)
for i in range(14,49):
    csvfile.writerow(listData[i])

for i in range(99,148):
    csvfile.writerow(listData[i])

# Ctrl+C to Close Python Window



