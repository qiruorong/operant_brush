import serial

arduino_port = 'COM11'

ser = serial.Serial(arduino_port, 9600)

with open('data.txt', 'w') as file:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            print(line)
            file.write(line + '\n')

ser.close()

