from machine import Pin
from time import sleep_ms

class Step_motor:
    def __init__(self, pin1=14, pin2=27, pin3=26, pin4=25):
        self.seq = [[1,0,0,0],
               [0,1,0,0],
               [0,0,1,0],
               [0,0,0,1]]

        self.seq2 = [[0,0,0,1],
               [0,0,1,0],
               [0,1,0,0],
               [1,0,0,0]]

        self.motor_pins = [0,1,2,3]

        self.motor_pins[0] = Pin(pin1, Pin.OUT)
        self.motor_pins[1] = Pin(pin2, Pin.OUT)
        self.motor_pins[2] = Pin(pin3, Pin.OUT)
        self.motor_pins[3] = Pin(pin4, Pin.OUT)


    def move_stepper(self, steps, direction):
        for step in range(steps):
            if direction == "forward":
                for i in range(4):
                    for pin in range(4):
                        self.motor_pins[pin].value(self.seq[i][pin])
                    sleep_ms(5)

            if direction == "backward":
                for i in range(4):            
                    for pin in range(4):
                        self.motor_pins[pin].value(self.seq2[i][pin])
                    sleep_ms(5)
                    