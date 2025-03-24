# in stage 1 of this experiment, mice are trained to lick
# in stage 2 of this experiment, mice are trained to lick when stimulus on paw
# in stage 3 of this experiment, mice are trained to lick associate with one stimulus when only that stimulus is present
# in stage 4 of this experiment, mice are trained to lick associate with one stimulus when the other direction is present


import machine as Pin
import machine as UART
import utime
from json import (load as jsonload, dump as jsondump)
import PySimpleGUI as sg

valve = Pin(0, Pin.OUT)
led = Pin(25, Pin.OUT)
lick = Pin(1, Pin.IN, Pin.PULL_DOWN)
stimulusPinOut = Pin(12, Pin.OUT)
stimulusPinIn = Pin(10, Pin.IN, Pin.PULL_DOWN)
respondWinPin = Pin(2, Pin.OUT)

interrupt_flag = 0
valveOpenDuration = 1
trial_counter = 0
trial_ids = []
trialStartTimestamps = []
stimulusStartTimestamps = []
respondWinTimestamps = []
rewardwinTimestamps = []
lick_times = []
valveTimestamps = []
trialEndTimestamps = []

trial_counter
interrupt_flag

trial_counter += 1

with open('timestamps.json', 'w') as file:
    data_dict = {}

def stage_1():
    with open('stage1_timestamps.json','w') as file:
        data_1 = {}
        trial_ids.append(trial_counter)
        data_1[trial_counter] = {
            'trial start':trialStartTimestamps[-1],
            'lick':lick_times[-1],
            'valve open':valveTimestamps[-1],
            'trial end':trialEndTimestamps[-1]
        }
        trial_ids = trial_counter

        trialStartTimestamps.append(utime.ticks_ms())
        data_1[trial_ids]['trial start'] = trialStartTimestamps[-1]
        utime.sleep(1000)

    if lick.value():
        
    try:
        while True:
            if lick.value():valve.value(1)
            
        try:
    while True:
        if lick.value() and reward_window_open():
            led.toggle()
            openValve(50)  # Open valve for 50 ms (0.05 seconds)
finally:
    valve.value(0) 

def stage_2():

def stage_3():

def stage_4():
    def runTrial_4():

        trial_ids.append(trial_counter)
        data_dict[trial_counter] = {
            'trial start':trialStartTimestamps[-1],
            'stimulus start':stimulusStartTimestamps[-1],
            'respond window open':respondWinTimestamps[-1],
            'reward window open':rewardwinTimestamps[-1],
            'lick':lick_times[-1],
            'valve open':valveTimestamps[-1],
            'trial end':trialEndTimestamps[-1]
        }

        trial_ids = trial_counter

        trialStartTimestamps.append(utime.ticks_ms())
        data_dict[trial_ids]['trial start'] = trialStartTimestamps[-1]
        utime.sleep(1000)
        stimulusPinOut.value(1)
        stimulusStartTimestamps.append(utime.ticks_ms())
        data_dict[trial_ids]['stimulus start'] = stimulusStartTimestamps[-1]
        if stimulusPinOut.value() == 1:
            stimulusPinOut.value(0)

        if stimulusPinIn.value():
            respondWinPin.value(1)
            respondWinTimestamps.append(utime.ticks_ms())
            data_dict[trial_ids]['respond window open'] = respondWinTimestamps[-1]
            utime.sleep(3000)  # reward window opening time
            respondWinPin.value(0)

        def lickCallback(pin):
            interrupt_flag
            lick_times.append(utime.ticks_ms())
            data_dict[trial_ids]['lick'] = lick_times[-1]
            interrupt_flag = 1

        lick.irq(trigger=lick.IRQ_RISING, handler=lickCallback)

        def openValve(duration):
            interrupt_flag
            valve.value(1)
            valveTimestamps.append(utime.ticks_ms())
            data_dict[trial_ids]['valve open'] = valveTimestamps[-1]
            utime.sleep_ms(duration)
            valve.value(0)

            if interrupt_flag == 1 and respondWinPin.value() == 1:
                interrupt_flag = 0
                valveTimestamps.append(utime.ticks_ms())
                data_dict[trial_ids]['valve open'] = valveTimestamps[-1]
                openValve(2000)
            else:
                utime.sleep(5000)

    # Main Trial
    while True:
        for i in range(100):
            runTrial()
            trialEndTimestamps.append(utime.ticks_ms())
            data_dict[trial_ids]['trial end'] = trialEndTimestamps[-1]

            with open('timestamps.json', 'w') as json_file:
                json.dump(data_dict, json_file, indent=4)
                

sg.theme('DarkAmber') 
layout = [  
    [sg.Text('Settings')],
    [sg.Text('Select Stage:')],
    [sg.Radio('Stage 1', 'stage', key='stage_1'), sg.Radio('Stage 2', 'stage', key='stage_2')],
    [sg.Radio('Stage 3', 'stage', key='stage_3'), sg.Radio('Stage 4', 'stage', key='stage_4')],
    [sg.Button('Save'), sg.Button('Exit')] 
]

window = sg.Window('Setting', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Save':
        selected_stage = None
        for stage_key in ['stage_1', 'stage_2', 'stage_3', 'stage_4']:
            if values[stage_key]:
                selected_stage = stage_key
                break

        if selected_stage:
            if selected_stage == 'stage_1':
                stage_1()
            elif selected_stage == 'stage_2':
                stage_2()
            elif selected_stage == 'stage_3':
                stage_3()
            elif selected_stage == 'stage_4':
                stage_4()

window.close()



