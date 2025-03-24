import serial
import json

arduino_port = 'COM11'
ser = serial.Serial(arduino_port, 9600)
file_path = "C:/Users/rqi9/Desktop/data.json"

try:
    with open(file_path, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = []

trail_id = len(data) + 1

try:
    while True:
        if ser.in_waiting > 0:
            randomNum = int(ser.readline().decode().strip())
            stimTimestamp = int(ser.readline().decode().strip())
            
            data_entry = {
                "trial_id": trail_id,
                "stimulus_timestamps": stimTimestamp,
                "stimulus_direction": randomNum
            }
            data.append(data_entry)
            
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                
            print("Trial ID:", trail_id)
            print("Stimulus Timestamps:", stimTimestamp)
            print("Stimulus Direction:", randomNum)
            
            trail_id += 1
            
except KeyboardInterrupt:
    pass
finally:
    ser.close()

