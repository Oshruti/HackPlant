
# AHT10 Temp,RH sensor on Pi Pico / micropython
#import servo
import machine
import uos
import time
from machine import Pin, I2C, Pin, PWM

#----------------------------
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-servo-motor-micropython/

class Servo:
    __servo_pwm_freq = 50
    __min_u16_duty = 1802
    __max_u16_duty = 7864
    min_angle = 0
    max_angle = 270
    current_angle = 0.001


    def __init__(self, pin):
        self.__initialise(pin)


    def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u16_duty = min_u16_duty
        self.__max_u16_duty = max_u16_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    def move(self, angle):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self.__angle_to_u16_duty(angle)
        self.__motor.duty_u16(duty_u16)
    
    def stop(self):
        self.__motor.deinit()
    
    def get_current_angle(self):
        return self.current_angle

    def __angle_to_u16_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty


    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)

#----------------------------
import ahtx0
uart = machine.UART(0, baudrate=115200)
uart.init(115200, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))
uos.dupterm(uart)
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400_000)
sensor = ahtx0.AHT10(i2c)
servo1 = Servo(pin=0)

#csv_filename = "sensor_data.csv"
# file_path = "sensor_data.csv"

# Initialize the CSV file with a header (run this once)
# with open(csv_filename, "w") as file:
#    file.write("Timestamp,Temperature (C),Humidity (%)\n")

servo1.move(200)
while True:
    print("%0.2f, %0.2f" %
          (sensor.temperature,
          sensor.relative_humidity))
    time.sleep(1)
    if (sensor.relative_humidity < 70):
        servo1.move(0)
    else:
        servo1.move(200)
        
uart.write(b"EOF")
source_file.close()


        

