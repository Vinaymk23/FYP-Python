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

import xlwt
from xlwt import Workbook

import tkinter as tk
from tkinter import ttk


LARGE_FONT= ("Verdana", 12)
wb= Workbook()
sh1=wb.add_sheet('Sheet 1')
global currow
currow = 0
pause=0
fig = plt.figure()
ax = p3.Axes3D(fig)
count=0
sum=[[1,2,1,1,1,2,1,1],[1,1,2,8,10,9,1,2],[1,1,12,1,2,1,12,1],[2,1,13,1,2,1,14,1],[1,15,2,1,1,2,16,1],[1,16,1,1,1,2,18,1],[1,17,2,1,1,2,17,1],[17,2,2,1,1,1,16,2]]
#list1=list(np.zeros((8,8),dtype=int))

ser = serial.Serial('COM26', baudrate = 9600, timeout = 1)
time.sleep(3)
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

#def writexl():
#    global currow
#    for i in range(0,8):
#        for j in range(0,8):
#            sh1.write(currow + i,j,list1[i][j],forstyle(list1[i][j]))
#    currow=currow + 9
#    wb.save("occlusion_values.xls")        


"""def getValues():
    
    ser.write(b'g')
    list1=[]
    for j in range(0,8):
                                arduinoData=ser.readline().decode('ascii')
                                #print(type(arduinoData))
                                data=list(map(int,arduinoData.split()))
                                #print(data)       
                                list1.append(data)
    #print(list1)

    
    return list1"""
def getValues():
    
        
    global currow
    global count
    global list1
    if (count==63):
        count=0
        #writexl()
        currow=currow+9
        time.sleep(5)
    if (count==0):
        list1=list(np.zeros((8,8),dtype=int))
    
    ser.write(b'g')
    arduinoData=ser.readline().decode('ascii')
    #print(arduinoData)
    list1[int(count/8)][count%8]=int(arduinoData)
    sh1.write(currow+int(count/8),count%8,int(arduinoData),forstyle(int(arduinoData)))
    wb.save('occlusion_values.xls')
    count=count+1
    
    #if (len(data)==8):
    #    list1.append(data)
    #    data=[]
    #return list1
    print(list1)
    
"""def rep(i):
    if (pause==0):
        plt.cla()
        list1=getValues()
        for y,k in zip([0,10,20,30,40,50,60,70],[0,1,2,3,4,5,6,7]):
            xs = np.arange(8)
            zs=list(map(forcutoff,list1[k]))
            s=[0.5]*8
            zref=[0]*8
            ax.bar3d(xs,y,zref,s,s,zs, color=list(map(forcolour,zs)))"""
def rep(i):
    
    plt.cla()
    getValues()
    for y,k in zip([0,10,20,30,40,50,60,70],[0,1,2,3,4,5,6,7]):
        xs = np.arange(8)
        zs=list(map(forcutoff,list1[k]))
        s=[0.5]*8
        zref=[0]*8
        ax.bar3d(xs,y,zref,s,s,zs, color=list(map(forcolour,zs)))
        
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

        
        
       
app = SeaofBTCapp()

ani=animation.FuncAnimation(fig,rep,interval=500)   
app.mainloop()