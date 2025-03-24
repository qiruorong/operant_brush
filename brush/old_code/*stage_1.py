from machine import Pin
import utime
import json

valve = Pin(0, Pin.OUT)
led = Pin(25, Pin.OUT)
lick = Pin(1, Pin.IN, Pin.PULL_DOWN)

trial_counter = 0
trial_ids = []
trialStartTimestamps = []
lick_times = []
valveTimestamps = []
trialEndTimestamps = []

def save_data_to_json():
    data = {
        "trial_ids": trial_ids,
        "trialStartTimestamps": trialStartTimestamps,
        "lick_times": lick_times,
        "valveTimestamps": valveTimestamps,
        "trialEndTimestamps": trialEndTimestamps,
    }

    with open("stage1_data.json", "w") as json_file:
        json.dump(data, json_file)


while True:
    trial_counter += 1
    trial_ids.append(trial_counter)

    trialStartTimestamps.append(utime.ticks_ms())
    utime.sleep(1)  

    valve.value(1)
    valveTimestamps.append(utime.ticks_ms())
    utime.sleep(0.05)
    valve.value(0)

    while True:
        for i in range(30):
            if lick.value():
                lick_times.append(utime.ticks_ms())
                break
            trialEndTimestamps.append(utime.ticks_ms())
            save_data_to_json()

