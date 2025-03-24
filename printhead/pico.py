#!/usr/bin/env python
import numpy as np
from machine import Pin
import utime

## GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Define the pin mappings
pinDict = {}
pins = [4,5,6,7,9,10,11,12,13,14,15,16,17,19,20,21,22,24,25,26,27,29,31,32,34]
for pin in pins:
    pinDict[pin] = Pin(pin,Pin.OUT)
rewardPin = Pin(1, Pin.OUT)
trialPin = Pin(0,Pin.OUT)

    # Define parameters
    tone_duration = 0.5  # seconds
    Fs = 200

    speed = 0.1 # in mm/s
    time_stim = 1/speed 
    overlap = 3 # # of pins to have activated at once
    pinOrder = [1, 13, 2, 14, 3, 15, 4, 16, 5, 17, 6, 18, 7, 19, 8, 20, 9, 21, 10, 22, 11, 23, 12, 24]
    time_pin = (overlap * time_stim) / (24 + overlap - 1)
    time_pin_samples = int(np.floor(time_pin * Fs))
    numSamples = int(time_stim*Fs)
    stim = np.zeros(24, numSamples)
    
    
    for i in range(24): # for each pin
        if i == 0:
            indentStart = 0
        else:
            indentStart = int(np.floor((i-1)/(24+overlap-1) * time_stim * Fs))
        indentEnd = indentStart + time_pin_samples
        if indentEnd > time_stim * Fs:
            indentEnd = int(np.floor(time_stim * Fs - 1))
        stim[pinOrder[i]-1, indentStart:indentEnd] = 1

    
    # fullStim = np.tile(np.concatenate(stim,axis = 1), (1, num_sweeps))
    # fullTrigger = np.zeros((len(fullStim), 1))
    # fullTrigger[1:-1] = 1

    for sample in range(numSamples):
        #stim[:,sample]
        for i, pin in enumerate(pins):
            pinDict[pin].value(stim[i,sample])
        utime.sleep(1/Fs)
    
    digital_signal = stim
    task.write(digital_signal, auto_start=True)
    
