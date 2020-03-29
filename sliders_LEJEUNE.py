# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:05:35 2020

@author: sebas
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)
t = np.arange(0.0, 1.0, 0.001)
p0 = np.array([0., 0., 0.])
p1 = np.array([0., -1., 0.])
m = 1.0
k = 0.1
amort = 0.1
deltat = 1.0
time_sim = 50
longueur_0 = np.sqrt(np.dot(p1-p0, p1-p0))
p1 = np.array([0., -1.1, 0.])
v = np.array([0., 0., 0.])
longueur = np.sqrt(np.dot(p1-p0, p1-p0))
deltalong = longueur - longueur_0
ldp = []
at = np.arange(0, time_sim, deltat)
for i in at:
    ldp.append(deltalong)
    longueur = np.sqrt(np.dot(p1-p0, p1-p0))
    deltalong = longueur - longueur_0
    gamma = (-amort*v - k*deltalong * (p1-p0) / longueur)/m
    v = v + gamma * deltat
    p1 = p1 + v * deltat   
l, =plt.plot(at, ldp)
ax.margins(x=0)

axcolor = 'lightgoldenrodyellow'
axraideur = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
axmasse = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
axamort = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axdeltat = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
axtime_sim = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

smasse = Slider(axmasse, 'Masse', 0.1, 7.0, valinit=m)
sraideur = Slider(axraideur, 'Raideur', 0, 1, valinit=k)
samort = Slider(axamort, 'Amort', 0, 1.0, valinit=amort)
sdeltat = Slider(axdeltat, 'Deltat t', 0.1, 5.0, valinit=deltat)
stime_sim = Slider(axtime_sim, 'time_sim', 0.1, 100.0, valinit=time_sim)

def update(val):
    t = np.arange(0, stime_sim.val, sdeltat.val)
    ld = []
    p0 = np.array([0., 0., 0.])
    p1 = np.array([0., -1., 0.])
    longueur_0 = np.sqrt(np.dot(p1-p0, p1-p0))
    p1 = np.array([0., -1.1, 0.])
    v = np.array([0., 0., 0.])
    longueur = np.sqrt(np.dot(p1-p0, p1-p0))
    deltalong = longueur - longueur_0
    for i in t:
        ld.append(deltalong)
        longueur = np.sqrt(np.dot(p1-p0, p1-p0))
        deltalong = longueur - longueur_0
        gamma = (-samort.val*v - sraideur.val*deltalong * (p1-p0) / longueur)/smasse.val
        v = v + gamma * deltat
        p1 = p1 + v * deltat
    print(ld) #print the new data in the terminal 
    l.set_ydata(ld)
    l.set_xdata(t)
    ax.set_xlim(min(t), max(t)) #set the scale of the x axis
    fig.canvas.draw_idle()

smasse.on_changed(update)
sraideur.on_changed(update)
samort.on_changed(update)
sdeltat.on_changed(update)
stime_sim.on_changed(update)

resetax = plt.axes([0.1, 0.9, 0.1, 0.1])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    smasse.reset()
    sraideur.reset()
    samort.reset()
    sdeltat.reset()
    stime_sim.reset()
    
button.on_clicked(reset)

rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)

def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

plt.show()