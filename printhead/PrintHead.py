#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import midaqmx

def acquireIntanPrinthead(protocol):

# Init DAQ
    Fs = 20000
    #s = daqSetup(Fs, 'printHead')

    # parameters
    stimulus = 'printHead'
    interSweepInterval = 3  # in s
    interSweep_samples = interSweepInterval * Fs
    num_sweeps = 2

    if protocol == 'test':
        sweepDuration = 4.5  # in s
        sweepDurationinSamples = int(Fs * sweepDuration)
        time_pin = 0.25  # in s
        indentDur_samples = int(time_pin * Fs) 
        squareWaveT = np.arange(0, sweepDuration, 1/Fs)

        numPositions = 24
        indentFrequency = sweepDuration/numPositions
        dutyCycle = time_pin/(sweepDuration/numPositions)*100
        squareWaveY = np.zeros((numPositions, sweepDurationinSamples))  

        for i in range(numPositions):
            print(i)
            if i == 0:
                indentStart = 0
            else:
                indentStart = int((i-1) * (sweepDuration/numPositions) * Fs)
                

            indentEnd = indentStart + indentDur_samples
            if indentEnd > sweepDurationinSamples:
                indentEnd = sweepDurationinSamples - 1
            print(indentStart, indentEnd)
            squareWaveY[i, int(indentStart):int(indentEnd)] = 1

        squareWaveY = np.transpose(squareWaveY)

        trigger = np.zeros((sweepDurationinSamples, 1))
        trigger[1::2] = 1
        fullTrigger = np.tile(np.concatenate((trigger, np.zeros((interSweep_samples, 1)))), (num_sweeps, 1))
        fullStim = np.tile(np.concatenate((squareWaveY, np.zeros((interSweep_samples, numPositions)))), (num_sweeps, 1))
        plt.plot(fullStim)
        
    elif protocol == 'directional':
        num_sweeps = 10
        speed = 16 # in mm/s
        print(f'speed {speed} mm/s')
        time_stim = 4/speed 
        time_isi = 3 # in s
        time_isi_samples = int(time_isi * Fs)
        overlap = 6 # # of pins to have activated at once
        pinOrder = [1, 13, 2, 14, 3, 15, 4, 16, 5, 17, 6, 18, 7, 19, 8, 20, 9, 21, 10, 22, 11, 23, 12, 24]
        time_pin = (overlap * time_stim) / (24 + overlap - 1)
        time_pin_samples = int(np.floor(time_pin * Fs))
        stim = np.zeros((int(time_stim*Fs), 24))
        for i in range(24): # for each pin
            if i == 0:
                indentStart = 0
            else:
                indentStart = int(np.floor((i-1)/(24+overlap-1) * time_stim * Fs))
            indentEnd = indentStart + time_pin_samples
            if indentEnd > time_stim * Fs:
                indentEnd = int(np.floor(time_stim * Fs - 1))
            stim[indentStart:indentEnd, pinOrder[i]-1] = 1

        stim_isi = np.zeros((time_isi_samples, 24))
        half_stim_isi = np.zeros((int(time_isi_samples/2), 24))
        revStim = np.flip(stim)
        fullStim = np.tile(np.concatenate((half_stim_isi, stim, stim_isi, revStim, half_stim_isi)), (num_sweeps, 1))
        fullTrigger = np.zeros((len(fullStim), 1))
        fullTrigger[1:-1] = 1

        s1 = {'speed': speed,
                'num_sweeps': num_sweeps,
              'time_isi': time_isi,
              'overlap': overlap}
