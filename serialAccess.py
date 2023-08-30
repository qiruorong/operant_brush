import serial

arduino_port = 'COM11'
ser = serial.Serial(arduino_port, 9600)
file_path = "C:/Users/rqi9/Desktop/trial_ids(m).txt"

with open(file_path, "a") as file:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            data = line.split(",") 

            if len(data) == 2:  
                randomNum = data[0]
                stimTimestamp = data[1]
            print(randomNum)
            print(stimTimestamp)
            
            # Write them as separate lines in the file
            file.write("Random Number: " + randomNum + '\n')
            file.write("Stimulus Timestamp: " + stimTimestamp + '\n')
            file.flush() 

ser.close()


