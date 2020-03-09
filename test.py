import serial
data=serial.Serial('COM14',115200)
while True:
    test=data.readline().decode('ascii')
    print(test)