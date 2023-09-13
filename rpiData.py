import utime
from machine import Pin
import json

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

with open('timestamps.json', 'w') as file:
    data_dict = {}

    def runTrial():
        trial_counter
        interrupt_flag

        trial_counter += 1

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
