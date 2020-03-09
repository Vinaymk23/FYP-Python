import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
#import NavigationToolbar2QT
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
import serial
import time
from matplotlib.figure import Figure
import threading

import xlwt
from xlwt import Workbook

import tkinter as tk
from tkinter import ttk
import queue 

q = queue.Queue()   # creating queue                      
class loop2:
    i=-1    #creating static variable i

bars =[]

LARGE_FONT= ("Verdana", 12)
wb= Workbook()
sh1=wb.add_sheet('Sheet 1')
# global currow
# currow = 0
pause=0
fig = plt.figure()
ax = p3.Axes3D(fig)
count=0
# sum=[[1,2,1,1,1,2,1,1],[1,1,2,8,10,9,1,2],[1,1,12,1,2,1,12,1],[2,1,13,1,2,1,14,1],[1,15,2,1,1,2,16,1],[1,16,1,1,1,2,18,1],[1,17,2,1,1,2,17,1],[17,2,2,1,1,1,16,2]]
#list1=list(np.zeros((8,8),dtype=int))

def forstyle(x):
    if((x>0) and (x<400)):
        return xlwt.easyxf('font:,color green')
    elif ((x>=400) and (x<800)):
        return xlwt.easyxf('font:,color yellow')
    else:
        return xlwt.easyxf('font:,color red')

def forcolour(x):
    if ((x>0) and (x<400)):
        return 'g'
    elif ((x>=400) and (x<800)):
        return 'y'
    else:
        return 'r'

def forcutoff(x):
    if (x<100):
        return 0
    else:
        return (x-100)

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)     
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

   
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
       
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="Dental Occlusion Scan", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button3 = ttk.Button(self, text="View Graph",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Dental Occlusion", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

            

def getValues(ser):     #create a function to get data from bluetooth
    # ser.write(b'g')
    for j in range(0,8):
        print('sending g')
        ser.write(b'g')
        print("j=",j)
        while (ser.inWaiting() == 0):  # Wait here until there is data
            # print('.', end="")
            pass
        arduinoData=ser.readline().decode('ascii')      #creating serial object 
        # print(arduinoData)
        data=int(arduinoData.strip())
        

        print(data)       
        yield j,data

def rep(num,bars):          #create a function to update the bars
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

    global i
    i=-1
    if k ==0:
        loop2.i=loop2.i+1
        # i=i+1
    xpos = [loop2.i%8]
        
    ypos = [j]
    print("xpos ypos= ",loop2.i,j)
    zpos = [0]
    dx = [0.5]
    dy = [0.5]
    dz = data
    # data = list(map(forcutoff,data))
    # data=list(map(int,data))
    bars.append( ax.bar3d(xpos, ypos, zpos, dx, dy, dz))    #update bars data each time with new data
    return bars

def loopGetValue():         #create function to turn on serial port and excepting data
    global q
    print('threading')
    with serial.Serial('COM26', baudrate = 9600, timeout = 1) as ser:
        while True:
            for k,eachVal in enumerate(getValues(ser)):
                # print("i=",i)
                q.put(tuple((k, eachVal)))
app = SeaofBTCapp()
print(' start ')
for ypos in np.arange(8):
    xpos = np.arange(8)
    zpos=np.zeros(8)  #ypos  = [np.arange(8)]*8
    dx = [0.5]*8
    dy = [0.5]*8
    dz = 0
    bars.append(ax.bar3d(xpos, ypos, zpos, dx, dy,dz) )        #initializng the plot positions
threading.Thread(target=loopGetValue).start()        #crete a thread to get value
# app = SeaofBTCapp()
ani=animation.FuncAnimation(fig,rep,fargs=[bars],interval=50, blit = False)   #animation function to plot data        
app.mainloop()