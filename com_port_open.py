import serial
ser = serial.Serial(input('Please enter the com port as "COMXX": '),
                    baudrate=input('Please enter the baudrate: '), timeout=1)
while True:
    while (ser.inWaiting() == 0):  # Wait here until there is data
        pass
    arduinoData = ser.readline().decode('ascii')  # creating serial object
    print(ser)
    # data = (arduinoData.strip())
    # print(data)
    # temp=data
    # count=0
    # while temp != 0:
    #     temp=temp/10
    #     count = count + 1

    # if count != 4:
    #     ser.write(b'data not received properly')
