from mpl_toolkits.mplot3d import Axes3D  # import mathplot tookkits
import matplotlib.pyplot as plt  # import pyplot
import matplotlib.animation as animation  # import animation
import mpl_toolkits.mplot3d.axes3d as p3  # import 3d axes
from matplotlib import style  # import graph styles
import numpy as np  # import numpy
import serial  # import serial
import time  # import time
import multiprocessing  # import thread
import queue  # import queue
import matplotlib.cm as cm
import sys
import glob
import serial
import xlwt
from xlwt import Workbook

# queue.Queue()   # creating queue
q = multiprocessing.Queue()
i = -1


list1 = []

wb = Workbook()
sh1 = wb.add_sheet('Sheet 1', cell_overwrite_ok=True)

global st, st1, st2

# st = xlwt.easyxf('pattern: pattern solid;')
# st1 = xlwt.easyxf('pattern: pattern solid;')
# st2 = xlwt.easyxf('pattern: pattern solid;')

# st.pattern.pattern_fore_colour = 10
# st1.pattern.pattern_fore_colour = 13
# st2.pattern.pattern_fore_colour = 11

style = xlwt.easyxf('font: bold 1, color red;')
style1 = xlwt.easyxf('font: bold 1, color yellow;')
style2 = xlwt.easyxf('font: bold 1, color green;')


class xyz:
    r1 = -1
    c1 = -1


bars = [None]*64

# style.use('classic')  # graph style
fig = plt.figure()  # creating plot name as fig
ax = p3.Axes3D(fig)


def serial_ports():
    print("inisde com===============")

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def getValues(ser):  # create a function to get data from bluetooth

    print('sending y')
    time.sleep(1)
    ser.write(b'y')
    # print("j=",j)
    for j in range(64):
        while (ser.inWaiting() == 0):  # Wait here until there is data
            pass
        arduinoData = ser.readline().decode('ascii')  # creating serial object
        # print(arduinoData)
        data = arduinoData.strip()
        length = len(data)
        # print(length, data)
        if(length == 4):
            # print(j%8, int(data))
            yield j % 8, int(data)
        else:
            print("error ")
            j -= 1
            ser.write(b'g')


def rep(num, bars):  # create a function to update the bars
    global q, i
    # plt.cla()

    if q.empty():
        return bars

    while not q.empty():

        data = q.get()

        (k, (j, data)) = data

        xpos = [k//8 % 8]
        # print("xpos,k,j ", xpos, k, j)

        ypos = [j]
        xyz.r1 += 1
        # r2 = xyz.r1//8 % 8

        if(j == 0):
            xyz.c1 += 1

        # def forstyle(x):
        #     if((x > 0) and (x < 400)):
        #         return xlwt.easyxf('font:,color green')
        #     elif ((x >= 400) and (x < 800)):
        #         return xlwt.easyxf('font:,color yellow')
        #     else:
        #         return xlwt.easyxf('font:,color red')

        # print("m2,j,r1,xyz.c1", r2, j, xyz.r1, xyz.c1)
        # sh1.write(xyz.c1, j, data, forstyle(data))
        wb.save('xlwt_ex.xls')

        zpos = [0]
        dx = [0.5]
        dy = [0.5]

        # if (data < 150):
        #     data = 0
        # else:
        #     data = data-150

        dz = data
        print(data)

        def rgba(data):
            if ((data >= 0) and (data < 400)):
                sh1.write(xyz.c1, j, data, style)
                return 'r'
            elif ((data >= 400) and (data < 800)):
                sh1.write(xyz.c1, j, data, style)
                return 'y'
            else:
                sh1.write(xyz.c1, j, data, style2)
                return 'g'

        # plt.cla()
        if bars[k % 64]:
            bars[k % 64].remove()
        bars[k % 64] = ax.bar3d(xpos, ypos, zpos, dx,
                                dy, dz, color=rgba(dz))

        # return bars


def loopGetValue(q, com):  # create function to turn on serial port and excepting data
    print('threading')
    with serial.Serial('COM'+str(com), baudrate=9600, timeout=1) as ser:
        # with seri as ser:
        while True:
            for k, eachVal in enumerate(getValues(ser)):
                # print("i=",i)
                # print("Loop")
                q.put(tuple((k, eachVal)))
                # print(k, eachVal)


if __name__ == '__main__':
    # print(' The Available COM ports are as below please select the one required ')
    # print(serial_ports())
    # seri=serial.Serial(input('Please enter the com port as "COMXX": '), baudrate = input('Please enter the baudrate: '), timeout = 1)
    com = input('Please enter the com port as "XX": ')
    # com = 11

    for ypos in np.arange(8):
        xpos = np.arange(8)
        zpos = np.zeros(8)  # ypos  = [np.arange(8)]*8
        dx = [0.5]*8
        dy = [0.5]*8
        # dz = 0
        ax.bar3d(xpos, ypos, zpos, dx, dy, 0)  # initializng the plot positions
    # crete a thread to get value
    p1 = multiprocessing.Process(target=loopGetValue, args=(q, com))
    p1.start()
    time.sleep(0.5)  # animation function to plot data
    ani = animation.FuncAnimation(
        fig, rep, fargs=[bars], interval=5)
    plt.show()  # plot
    # input('press y to exit')
