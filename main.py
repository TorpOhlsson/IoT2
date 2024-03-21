from machine import Pin, ADC, UART, Timer, SoftI2C, deepsleep
from time import sleep_ms, sleep
from gps_GPGGA_GPZDA import GPS_GPGGA_GPZDA
from stepmotor import Step_motor
from mpu6050 import MPU6050
import network
import espnow
import time
import esp32

class Board():
    error = "none"
    latitude = ""
    longitude = ""
    battery = 0
    daytime ="329319391"
    
red_led = Pin(15, Pin.OUT)
red_led.off()

battery_pin = ADC(Pin(33))
battery_pin.atten(ADC.ATTN_11DB)
battery_pin.width(ADC.WIDTH_12BIT)
battery_total = 0

step_motor = Step_motor()



max_batt = 2325
min_batt = 2010
battery_total = 0
for i in range(128):
    battery_total = battery_total + battery_pin.read()
battery_total = battery_total >> 7 

measurement_batt = battery_total - min_batt
prc = (max_batt - min_batt) / 100
actual_battery = measurement_batt / prc
if actual_battery < 0:
    actual_battery = 0
elif actual_battery > 100:
    actual_battery = 100
Board.battery = round(actual_battery)

sta = network.WLAN(network.STA_IF)    # Enable station mode for ESP
sta.active(True)
sta.disconnect()        # Disconnect from last connected WiFi SSID

wake1 = Pin(2, mode=Pin.IN, pull=Pin.PULL_UP)
esp32.wake_on_ext0(pin = wake1, level = esp32.WAKEUP_ALL_LOW)

gpsModule = UART(2, baudrate=9600)
GPGGA = GPS_GPGGA_GPZDA(gpsModule)

i2c = SoftI2C(scl=Pin(23), sda=Pin(22),freq=100000)
gyroskop = MPU6050(i2c)
gyroskopliste=[]

while len(gyroskopliste) < 3:    
    try:
        gyroskopliste.append(gyroskop.get_values()["acceleration y"])
    except:
        pass


if sum(gyroskopliste) >=-36000:
    Board.error="Gyro Fejl"


# timer_2 = Timer(2)
# timer_2.init(period=2000, mode=Timer.PERIODIC, callback=gyroskop_tjekker)


sensor = ADC(Pin(32))
sensor.atten(ADC.ATTN_11DB)
sensor_data = [0, 0, 0]

current_list = []
def gps_timer(t):
    try:
        if GPGGA.receive_nmea_data()!="":
            Board.latitude = GPGGA.get_latitude()
            Board.longitude = GPGGA.get_longitude()
            daytime = "1243132"
            daytime = str(GPGGA.get_utc_day()) + "/"
            daytime = daytime + str(GPGGA.get_utc_month()) + "/"
            daytime = daytime + str(GPGGA.get_utc_year()) + " "
            daytime = daytime + str(GPGGA.get_utc_hours()) + ":"
            daytime = daytime + str(GPGGA.get_utc_minutes())
            if len(daytime) > 0:
                Board.daytime = daytime
    except:
        Board.error = "GPS failure"
        
timer_1 = Timer(1)
timer_1.init(period=2000, mode=Timer.PERIODIC, callback=gps_timer)

if Board.error == "none":
    # Startposition
    print("starting up...")
    sleep_ms(2000)  # Vent i 2 sekunder

    print("Moving to depth 1..")

    step_motor.move_stepper(1000, "forward")
    sensor_data[0] = (sensor.read()/2)
    sleep_ms(5000)  # Vent i 5 sekunder

    #print("Moving to depth 2..")
    step_motor.move_stepper(1700, "forward")
    sensor_data[1] = (sensor.read()/2)
    sleep_ms(5000)  # Vent i 5 sekunder

    #print("Moving to depth 3...")
    step_motor.move_stepper(2000, "forward")
    sensor_data[2] = (sensor.read()/2)
    sleep_ms(5000)  # Vent i 5 sekunder

    #print("Moving back to start position...")
    step_motor.move_stepper(4700, "backward")
else:
    print("sprunget motor over, men jeg venter sku lige på gps'en")
    sleep(10) #vent 120 sekunder så gps kan få signal?
timer_1.deinit()
# timer_2.deinit()


esp_now_data = (str(sensor_data[0]) + "|" +
                str(sensor_data[1]) + "|" +
                str(sensor_data[2]) + "|" +
                str(Board.latitude) + "|" +
                str(Board.longitude) + "|" +
                str(Board.error) + "|" +
                str(Board.battery) + "|" +
                str(Board.daytime) + "|" +
                "1" 
                )

try:
    sta.active(True)
    e = espnow.ESPNow()     # Enable ESP-NOW
    e.active(True)
    peer1 = b'\xb0\xa72\xdebP'   # MAC address of peer1's wifi interface
    e.add_peer(peer1)     
    e.send(peer1, esp_now_data , True)
    print(esp_now_data)
    e.active(False)
    sta.disconnect()
    
except:
    Board.error = "ESPnow failure"
    print("ESPnow failure")

print(Board.battery)

if Board.battery > 20:                 
    print("end program. go to sleep")
    sleep_ms(3000)
    deepsleep(40000)
else:
    while True:
        if Board.error == "none":
            red_led.on()
        else:
            red_led.on()
            sleep_ms(2000)
            red_led.off()
            sleep_ms(2000)