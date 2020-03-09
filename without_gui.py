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
class loop2:
    i=-1

global i

# bars =[0]*8
# bars=[]

style.use('classic')
fig = plt.figure()
ax = p3.Axes3D(fig)

def getValues(ser):
    print('sending g')
    ser.write(b'g')
    for k in range(8):
        for j in range(8):
            # print("j=",j)
            # while (ser.inWaiting() == 0):  # Wait here until there is data
            #     # print('.', end="")
            #     pass
            # print(ser.readline().decode('ascii'))
            arduinoData=ser.readline().decode('ascii')
            # print(arduinoData)
            data=int(arduinoData.strip())
            print(data)       
            yield k,(j,data)

def rep(num,bars):
    if not q.empty():
        data = q.get()
        # print(data)
        # print (bars)
        # print (num)
        (k, (j, data)) = data
    else:

        return bars
    # for c,ypos,i in zip(['c', 'y','r','b'], np.arange(8),np.arange(8)):
    # for ypos,i in zip(np.arange(8),np.arange(8)):
    # 
    #
    # global i
    # i=-1
    # if k ==0:
    #     loop2.i=loop2.i+1
        # i=i+1
    xpos = [k]
        
    ypos = [j]
    print("xpos ypos= ",k,j)
    zpos = [0]
    dx = [0.5]
    dy = [0.5]
    dz = data
    bars[k]=ax.bar3d(xpos, ypos, zpos, dx, dy, dz)
    # bars.append(ax.bar3d(xpos, ypos, zpos, dx, dy, dz))
    # stop=(time.time())-time_start
    # print("time taken= ",stop)
    return bars

def loopGetValue():
    global q
    print('threading')
    with serial.Serial('COM25', baudrate = 9600, timeout = 1) as ser:
        while True:
            print("Loop disp")
            # for k in range(8):
            for eachVal in getValues(ser):
                # print("i=",i)
                q.put(tuple((eachVal)))

print(' start ')
# time_start=(time.time())
bars = []
for ypos in np.arange(8):
    xpos = np.arange(8)
    zpos=np.zeros(8)  #ypos  = [np.arange(8)]*8
    dx = [0.5]*8
    dy = [0.5]*8
    # dz = 0
    bars.append(ax.bar3d(xpos, ypos, zpos, dx, dy,0))

# start=time.time()
threading.Thread(target=loopGetValue).start()
# t.start()
# end=time.time()
# print(f"{end-start}")
ani=animation.FuncAnimation(fig,rep,fargs=[bars],interval=10, blit = False)    
plt.show()