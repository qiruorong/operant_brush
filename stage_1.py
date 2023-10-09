# in stage 1 of this experiment, mice are trained to lick


import machine as Pin
import machine as UART
import utime
import json
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
