import serial
import sqlite3
from time import sleep
from datetime import datetime
import paho.mqtt.client as mqtt
from gpiozero import LED
red = LED(17)
red.on()
ser = serial.Serial(
  port='/dev/ttyS0',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS
)

broker = "172.190.139.34"
port = 1883
topic = "test"
client_id = f'python-mqtt123_asd'
username = 'admin'
password = 'Admin1234567'

while True:
    data = ser.readline().decode("utf-8").strip()

    if len(data) > 6:
        print(data)
        d = data.split('|')
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.username_pw_set(username, password)
        mqttc.connect(broker, port)
        mqttc.publish("test",data)
        print("send mqtt")
        try:
            sqliteConnection = sqlite3.connect('database.db')
            cursor = sqliteConnection.cursor()
            cursor.execute('INSERT INTO records ("messurement1","messurement2","messurement3","lat","lon","error","batt","time") VALUES(?,?,?,?,?,?,?,?)',(float(d[0]), float(d[1]), float(d[2]), float(d[3]),float(d[4]),str(d[5]),int(d[6]),str(d[7]) ))
            sqliteConnection.commit()
            sqliteConnection.close()
        except:
            print("error")



