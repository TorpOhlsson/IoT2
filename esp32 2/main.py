import network
import espnow
from machine import UART
from time import sleep
port = 2
speed = 9600
uart = UART(port, speed, tx=16, rx=17, bits=8, parity=None, stop=1) # UART objekt



# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point


mac = sta.config('mac')
print("MAC Address:", mac)  # Show MAC for peering


e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv()
    if host == b'\xe4e\xb8\xa3\x84\xe8':
        if msg:
            uart.write(msg + "\n")
            print(msg + "-" + host)