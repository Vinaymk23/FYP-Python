from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import style
import numpy as np
import serial
import time
import threading
import queue
import time

q = queue.Queue()

bars = []

style.use('classic')
fig = plt.figure()
ax = p3.Axes3D(fig)


def getValues(ser):
    # ser.write(b'g')
    for j in range(0, 8):
        print('sending g')
        ser.write(b'g')
        while (ser.inWaiting() == 0):  # Wait here until there is data
            # print('.', end="")
            pass
        arduinoData = ser.readline().decode('ascii')
        # print(arduinoData)
        data = int(arduinoData.strip())
        # print(data)
        yield j, data


def rep(num, bars):
    if not q.empty():
        data = q.get()
        print(data)
        i, (j, data) = data
    else:
        return bars
    # for c,ypos,i in zip(['c', 'y','r','b'], np.arange(8),np.arange(8)):
    # for ypos,i in zip(np.arange(8),np.arange(8)):
    xpos = [i]
    ypos = [j]
    zpos = [0]
    dx = [0.5]
    dy = [0.5]
    dz = [data]
    bars[i] = ax.bar3d(xpos, ypos, zpos, dx, dy, dz)
    return bars


def loopGetValue():
    global q
    print('threading')
    with serial.Serial('COM10', baudrate=9600, timeout=1) as ser:
        while True:
            for i, eachVal in enumerate(getValues(ser)):
                q.put(tuple((i, eachVal)))


print(' start ')
xpos = np.arange(8)
zpos = np.zeros(8)
ypos = [np.arange(8)]*8
dx = [0.5]*8
dy = [0.5]*8
bars = [ax.bar3d(xpos, y, zpos, dx, dy, 0) for y in ypos]
threading.Thread(target=loopGetValue).start()
ani = animation.FuncAnimation(fig, rep, fargs=[bars], interval=500, blit=False)
plt.show()
