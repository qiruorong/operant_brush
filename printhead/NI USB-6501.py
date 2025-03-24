#!/usr/bin/env python
import time
import numpy as np
import nidaqmx

# Define the pin mappings
pin_mappings = ['port0/line0', 'port0/line1', 'port0/line2', 'port0/line3',
                'port0/line4', 'port0/line5', 'port0/line6', 'port0/line7',
                'port1/line0', 'port1/line1', 'port1/line2', 'port1/line3',
                'port1/line4', 'port1/line5', 'port1/line6', 'port1/line7',
                'port2/line0', 'port2/line1', 'port2/line2', 'port2/line3',
                'port2/line4', 'port2/line5', 'port2/line6', 'port2/line7']

for i, pip in enumerate(pin_mappings):
    pin_mappings[i] = 'Dev1' + pin

# Define parameters
tone_duration = 0.5  # seconds
Fs = 2000

# Initialize the NI USB-6501 device
with nidaqmx.Task() as task:
    for pin in pin_mappings:
        task.do_channels.add_do_chan(pin)
    
    # parameters
    stimulus = 'printHead'
    interSweepInterval = 3  # in s
    interSweep_samples = interSweepInterval * Fs
    num_sweeps = 2

    num_sweeps = 10
    speed = 0.1 # in mm/s
    print(f'speed {speed} mm/s')
    time_stim = 4/speed 
    time_isi = 3 # in s
    time_isi_samples = int(time_isi * Fs)
    overlap = 6 # # of pins to have activated at once
    pinOrder = [1, 13, 2, 14, 3, 15, 4, 16, 5, 17, 6, 18, 7, 19, 8, 20, 9, 21, 10, 22, 11, 23, 12, 24]
    time_pin = (overlap * time_stim) / (24 + overlap - 1)
    time_pin_samples = int(np.floor(time_pin * Fs))
    stim = np.zeros((24, int(time_stim*Fs)),dtype = bool)
    for i in range(24): # for each pin
        if i == 0:
            indentStart = 0
        else:
            indentStart = int(np.floor((i-1)/(24+overlap-1) * time_stim * Fs))
        indentEnd = indentStart + time_pin_samples
        if indentEnd > time_stim * Fs:
            indentEnd = int(np.floor(time_stim * Fs - 1))
        stim[pinOrder[i]-1, indentStart:indentEnd] = 1

    stim_isi = np.zeros((24, time_isi_samples),dtype = bool)
    half_stim_isi = np.zeros((24, int(time_isi_samples/2)),dtype = bool)
    revStim = np.flip(stim)
    fullStim = np.tile(np.concatenate((half_stim_isi, stim, stim_isi, revStim, half_stim_isi),axis = 1), (1, num_sweeps))
    fullTrigger = np.zeros((len(fullStim), 1))
    fullTrigger[1:-1] = 1

    digital_signal = fullStim
    for i in fullStim.shape[1]:
        task.write(np.ascontiguousarray(fullStim[:,i]), auto_start=True)
        time.sleep(1/Fs)
