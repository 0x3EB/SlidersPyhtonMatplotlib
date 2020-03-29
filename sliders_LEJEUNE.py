# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:05:35 2020

@author: sebastien lejeune A3 alternance
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

axcolor = 'lightgoldenrodyellow' #color of the slider
#set label of X and Y
fig, ax = plt.subplots()
plt.grid(True)
plt.ylabel('Delta length')
plt.title('Spring Mass')


def creatingData(m = 1.0, k = 0.1, amort = 0.1, deltat = 1.0, time_sim = 50):
    p0 = np.array([0., 0., 0.])
    p1 = np.array([0., -1., 0.])
    length_init = np.sqrt(np.dot(p1-p0, p1-p0))
    p1 = np.array([0., -1.1, 0.])
    v = np.array([0., 0., 0.])
    length_updated = np.sqrt(np.dot(p1-p0, p1-p0))
    deltalen = length_updated - length_init
    dataY = []
    dataX = np.arange(0, time_sim, deltat)
    for i in dataX:
       dataY.append(deltalen)
       length_updated = np.sqrt(np.dot(p1-p0, p1-p0))
       deltalen = length_updated - length_init
       gamma = (-amort*v - k*deltalen * (p1-p0) / length_updated)/m
       v = v + gamma * deltat #updat
       p1 = p1 + v * deltat   
    return dataX, dataY

def SliderSettings():
    #setting the position and color of the sliders 
    axraideur = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
    axmasse = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
    axamort = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    axdeltat = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
    axtime_sim = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
    
    #creating all the sliders with their position, title, min, max and default value 
    smasse = Slider(axmasse, 'Mass', 0.1, 7.0, valinit=1)
    sraideur = Slider(axraideur, 'Stiffness', 0, 0.5, valinit=0.1)
    samort = Slider(axamort, 'Amortization', 0, 0.5, valinit=0.1)
    sdeltat = Slider(axdeltat, 'Step of integration', 0.1, 5.0, valinit=1)
    stime_sim = Slider(axtime_sim, 'Simulation time', 0.1, 200.0, valinit=50)
    
    return smasse,sraideur,samort,sdeltat,stime_sim

dataX,dataY  = creatingData()
l, =plt.plot(dataX,dataY)

smasse,sraideur,samort,sdeltat,stime_sim = SliderSettings()

def update(val):
    '''
    update(val) is a function that will update in live the graph with the value of the sliders
    
    params:
        val: is the value of the slider 
    '''
    dataX,dataY = creatingData(smasse.val,sraideur.val,samort.val,sdeltat.val,stime_sim.val)# retrieve new data with updated values
    print(dataY) #print the new data in the terminal 
    l.set_ydata(dataY) # change the Y data of the graph
    l.set_xdata(dataX) # change the X data of the graph
    ax.set_ylim(min(dataY), max(dataY)) #set the scale of the y axis
    ax.set_xlim(min(dataX), max(dataX)) #set the scale of the x axis
    fig.canvas.draw_idle()

def reset(event):
    '''
    Reset(event) permit the user to reset with default values of the slider
    
    params:
        event : the slider in question
    '''
    smasse.reset() # reset the slider of the mass
    sraideur.reset() # reset the slider of the stiffness
    samort.reset() # reset the slider of the amortization
    sdeltat.reset() # reset the slider of the step of integration
    stime_sim.reset() # reset the slider of the time of the simulation 

def buttonSettings():
    resetax = plt.axes([0.1, 0.9, 0.1, 0.1]) #setting the position of the reset button 
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    return button

resetax = plt.axes([0.0, 0.7, 0.1, 0.1]) #setting the position of the reset button 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
rax = plt.axes([0.0, 0.5, 0.10, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
invisibleBtn = plt.axes([0.0, 0.0, 0.0, 0.0], facecolor=axcolor)
invisibleBtn.set_visible(False)

def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()

def drawPlot():

    
    
    plt.subplots_adjust(left=0.25, bottom=0.35)
    dataX, dataY = creatingData()
    
      
    
    l, =plt.plot(dataX, dataY)
    ax.margins(x=0)
    
    #Updating the graph by moving any sliders
    smasse.on_changed(update) 
    sraideur.on_changed(update)
    samort.on_changed(update)
    sdeltat.on_changed(update)
    stime_sim.on_changed(update)
    
    #Reset the data of the sliders
    button.on_clicked(reset)
    radio.on_clicked(colorfunc)
    
   
    
    #display the graph
    plt.show()


if __name__ == '__main__':
    drawPlot()