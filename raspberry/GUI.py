# in stage 1 of this experiment, water despence followed by lick
# in stage 2 of this experiment, lick followed by water despence
# in stage 3 of this experiment, stimulus followed by water despence
# in stage 4 of this experiment, stimulus followed by lick


import machine as Pin
import machine as UART
import utime
import json
import PySimpleGUI as sg
import string
import random


valve = Pin(0, Pin.OUT)
led = Pin(25, Pin.OUT)
lick = Pin(1, Pin.IN, Pin.PULL_DOWN)
stimulusPinOut = Pin(12, Pin.OUT)
stimulusPinIn = Pin(10, Pin.IN, Pin.PULL_DOWN)
respondWinPin = Pin(2, Pin.OUT)

interrupt_flag = 0
valveOpenDuration = 1
trial_counter = 0
string.ascii_letters = 's,t'
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


def stage_1():
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

    valve.value(1)
    valveTimestamps.append(utime.ticks_ms())
    data_1[trial_ids]['valve open'] = valveTimestamps[-1]
    utime.sleep(0.05)
    valve.value(0)

    while True:
        for i in range(100):
            stage_1()
            if lick.value():
                lick_times.append(utime.ticks_ms())
                data_1[trial_ids]['lick'] = lick_times[-1]
                break
            trialEndTimestamps.append(utime.ticks_ms())
            data_1[trial_ids]['trial end'] = trialEndTimestamps[-1]

            with open('stage1_timestamps.json', 'w') as json_file:
                json.dump(data_1, json_file, indent=4)


def stage_2():
    data_2 = {}
    trial_ids.append(trial_counter)
    data_2[trial_counter] = {
        'trial start':trialStartTimestamps[-1],
        'lick':lick_times[-1],
        'valve open':valveTimestamps[-1],
        'trial end':trialEndTimestamps[-1]
    }
    trial_ids = trial_counter

    trialStartTimestamps.append(utime.ticks_ms())
    data_2[trial_ids]['trial start'] = trialStartTimestamps[-1]
    utime.sleep(1000)

    if lick.value():
        lick_times.append(utime.ticks_ms())
        data_2[trial_ids]['lick'] = lick_times[-1]
        valve.value(1)
        valveTimestamps.append(utime.ticks_ms())
        data_2[trial_ids]['valve open'] = valveTimestamps[-1]
        utime.sleep(0.05)
        valve.value(0)

    while True:
        for i in range(100):
            stage_2()
            trialEndTimestamps.append(utime.ticks_ms())
            data_2[trial_ids]['trial end'] = trialEndTimestamps[-1]

            with open('stage2_timestamps.json', 'w') as json_file:
                json.dump(data_2, json_file, indent=4)


def stage_3():
    data_3 = {}
    trial_ids.append(trial_counter)
    data_3[trial_counter] = {
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
    data_3[trial_ids]['trial start'] = trialStartTimestamps[-1]
    utime.sleep(1000)

    UART.write('t')
    stimulusStartTimestamps.append(utime.ticks_ms())
    data_3[trial_ids]['stimulus start'] = stimulusStartTimestamps[-1]
    valve.value(1)
    utime.sleep(0.05)
    valve.value(0)

    while True:
        for i in range(100):
            stage_3()
            if lick.value():
                lick_times.append(utime.ticks_ms())
                data_3[trial_ids]['lick'] = lick_times[-1]
                break
            trialEndTimestamps.append(utime.ticks_ms())
            data_3[trial_ids]['trial end'] = trialEndTimestamps[-1]

            with open('stage3_timestamps.json', 'w') as json_file:
                json.dump(data_3, json_file, indent=4)


def stage_4():
    data_dict ={}
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
    randomLetter = random.choice(string.ascii_letters)
    UART.write(randomLetter)
    stimulusStartTimestamps.append(utime.ticks_ms())
    data_dict[trial_ids]['stimulus start'] = stimulusStartTimestamps[-1]
    if UART.write() == 't':
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
            stage_4()
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
            # elif selected_stage == 'stage_3':
                # stage_3()
            elif selected_stage == 'stage_4':
                stage_4()

window.close()




