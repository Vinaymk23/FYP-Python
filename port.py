import serial
import time as t
i = 0
x = 64
while True:
    with serial.Serial('COM4', baudrate=9600, timeout=1) as ser:
        while True:
            # print('loop=', i)
            print("sending y")
            ser.write(b'y')
            t.sleep(0.5)
            ser.write(b'y')
            # ser.write(b'g')
            for item in range(64):
                item += 1
                while (ser.inWaiting() == 0):  # Wait here until there is data
                    # print(".")
                    # ser.write(b'y')
                    pass
                # print(ser.readline().decode('ascii'))
                arduinoData = ser.readline().decode('ascii').strip('\n')
                # print(f"arduinodata = {arduinoData} length = {len(arduinoData)}")
                data = arduinoData.strip('\n')
                # print("arduinodata=", data)
                # print(type(arduinoData))
                # data = int(arduinoData)
                length = len(data)
                # print("length---", length)
                if(length == 4):
                    print(int(data))
                else:
                    item -= 1
                    ser.write(b'g')
                    print("sending g")

print("done")
