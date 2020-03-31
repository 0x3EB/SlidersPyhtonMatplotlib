# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:05:35 2020

@author: sebastien lejeune A3 alternance
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

axcolor = 'lightgoldenrodyellow' #color of the slider

fig, ax = plt.subplots()
plt.grid(True) #add a grid in the graph
#set label of X and Y
plt.ylabel('Delta length')
plt.title('Spring Mass')


def creatingData(m = 1.0, k = 0.1, amort = 0.1, deltat = 1.0, time_sim = 50):
    '''

    Parameters
    ----------
    m : float, optional
        The mass of the free end. The default is 1.0.
    k : float, optional
        The stiffness of the spring. The default is 0.1.
    amort : float, optional
        Spring damping. The default is 0.1.
    deltat : float, optional
        Step of integration. The default is 1.0.
    time_sim : int, optional
        Simulation time. The default is 50.

    Returns
    -------
    dataX : 1D Array with ints
        Array with data for the X axis.
    dataY : 1D Array with floats
        Array with data for the Y axis.

    '''
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
    '''
    Function that permit to setup all the sliders for the graph

    Returns
    -------
    smasse :
        slider for the mass.
    sraideur :
        slider for the Stiffness.
    samort :
        slider for the Amortization.
    sdeltat :
        slider for the Step of integration.
    stime_sim :
        slider for the Simulation time.

    '''
    #setting the position and color of the sliders 
    sliderMassAxis = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
    sliderStiffnessAxis = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
    sliderAmortAxis = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    sliderDeltatAxis = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
    sliderTimeSimAxis = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
    
    #creating all the sliders with their position, title, min, max and default value 
    massSlider = Slider(sliderMassAxis, 'Mass', 0.1, 7.0, valinit=1)
    stiffnessSlider = Slider(sliderStiffnessAxis, 'Stiffness', 0, 0.5, valinit=0.1)
    amortSlider = Slider(sliderAmortAxis, 'Amortization', 0, 0.5, valinit=0.1)
    deltatSlider = Slider(sliderDeltatAxis, 'Step of integration', 0.1, 5.0, valinit=1)
    simTimeSlider = Slider(sliderTimeSimAxis, 'Simulation time', 0.1, 200.0, valinit=50)
    
    return massSlider,stiffnessSlider,amortSlider,deltatSlider,simTimeSlider

dataX,dataY  = creatingData()
l, =plt.plot(dataX,dataY)

massSlider,stiffnessSlider,amortSlider,deltatSlider,simTimeSlider = SliderSettings()

def update(val):
    '''
    update(val) is a function that will update in live the graph with the value of the sliders

    Parameters
    ----------
    val :
        The value of the slider.

    Returns
    -------
    None.

    '''
    dataX,dataY = creatingData(massSlider.val,stiffnessSlider.val,amortSlider.val,deltatSlider.val,simTimeSlider.val)# retrieve new data with updated values
    print(dataY) #print the new data in the terminal 
    l.set_ydata(dataY) # change the Y data of the graph
    l.set_xdata(dataX) # change the X data of the graph
    ax.set_ylim(min(dataY), max(dataY)) #set the scale of the y axis
    ax.set_xlim(min(dataX), max(dataX)) #set the scale of the x axis
    fig.canvas.draw_idle()

def reset(event):
    '''
    Reset(event) permit the user to reset with default values of the slider
    
    Parameters
    ----------
    event :
        the slider event

    Returns
    -------
    None.

    '''
    massSlider.reset() # reset the slider of the mass
    stiffnessSlider.reset() # reset the slider of the stiffness
    amortSlider.reset() # reset the slider of the amortization
    deltatSlider.reset() # reset the slider of the step of integration
    simTimeSlider.reset() # reset the slider of the time of the simulation 


resetax = plt.axes([0.0, 0.7, 0.1, 0.1]) #setting the position of the reset button 
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
rax = plt.axes([0.0, 0.5, 0.10, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
invisibleBtn = plt.axes([0.0, 0.0, 0.0, 0.0], facecolor=axcolor)
invisibleBtn.set_visible(False)

def colorfunc(label):
    '''
    colorFunc(label) that allows changing the color of the something

    Parameters
    ----------
    label :
        Event when you click on a different label.

    Returns
    -------
    None.

    '''
    l.set_color(label) #set the color
    fig.canvas.draw_idle() #update the graph

def drawPlot():
    ''' 
    Draw the graph with all the settings (sliders, buttons, radio buttons, label, title)
    
    Returns
    -------
    None.

    '''
    plt.subplots_adjust(left=0.25, bottom=0.35)
    dataX, dataY = creatingData()
    
    l, =plt.plot(dataX, dataY)
    ax.margins(x=0)
    
    #Updating the graph by moving any sliders
    massSlider.on_changed(update) 
    stiffnessSlider.on_changed(update)
    amortSlider.on_changed(update)
    deltatSlider.on_changed(update)
    simTimeSlider.on_changed(update)
    
    #Reset the data of the sliders
    button.on_clicked(reset)
    radio.on_clicked(colorfunc)
    
    #display the graph
    plt.show()

if __name__ == '__main__':
    drawPlot()