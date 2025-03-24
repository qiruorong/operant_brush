import utime
import json
from machine import Pin

solenoid = Pin(0, Pin.OUT, Pin.PULL_DOWN)
led = Pin(25, Pin.OUT)
lick = Pin(1, Pin.IN, Pin.PULL_DOWN)
timestamps = []
count = 0
file_path = "C:/Users/rqi9/Desktop/stage1.json"

try:
    with open(file_path, "r") as file:
        data = json.load(file)
except OSError:
    # The file doesn't exist, create an empty list
    data = []

# Open the valve initially
solenoid.value(1)
utime.sleep(0.1)
solenoid.value(0)

try:
    while True:
        if lick.value(): 
            current_time = utime.time() 
            formatted_time = utime.localtime(current_time)
            formatted_timestamp = "{}/{}/{} {}:{}:{}".format(
                formatted_time[2], formatted_time[1], formatted_time[0],
                formatted_time[3], formatted_time[4], formatted_time[5]
            )
            count += 1

            data_entry = {
                "lickCounter": count,
                "lickTimestamps": formatted_timestamp,
            }
            data.append(data_entry)

            with open(file_path, 'w') as file:
                json.dump(data, file)

            print("lick counter:", count)

            # when lick
            led.value(1)
            solenoid.value(1)
            utime.sleep(0.1)
            led.value(0)
            solenoid.value(0)
            utime.sleep(2)

except KeyboardInterrupt:
    pass

