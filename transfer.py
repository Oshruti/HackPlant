import serial

# Configure the serial connection
port = "COM4" 
baudrate = 115200
serial_connection = serial.Serial(port, baudrate, timeout =1)

# Open a file on your computer to write the received data
destination_file = open("sensor_data.csv", "wb")

# Read and write data until the transfer is complete
while True:
    data = serial_connection.read(128)
    if data == b"EOF":
        break
    print(data)
    destination_file.flush()
    destination_file.write(data)

# Close the files and serial connection
destination_file.close()
serial_connection.close()