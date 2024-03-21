import paho.mqtt.client as mqtt
import sqlite3

broker = "172.190.139.34"
port = 1883
topic = "test"
client_id = f'python-mqtt123_asd'
username = 'admin'
password = 'Admin1234567'

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("test/#")


def on_message(client, userdata, msg):
	data = str(msg.payload.decode("utf-8"))
	d = data.split("|")
	print(data)	
	try:
		sqliteConnection = sqlite3.connect('database/ppm_database.db')
		cursor = sqliteConnection.cursor()
		cursor.execute('INSERT INTO sensor ("measurement_1","measurement_2","measurement_3","latitude","longtitude","error","battery","datetime","Title") VALUES(?,?,?,?,?,?,?,?,?)',(float(d[0]),float(d[1]),float(d[2]),float(d[3]),float(d[4]),str(d[5]),int(d[6]),str(d[7]),str(d[8]) ))
		sqliteConnection.commit()
		sqliteConnection.close()
	except sqlite3.Error as er:
        	print('SQLite error: %s' % (' '.join(er.args)))
        	print("Exception class is: ", er.__class__)
        	print('SQLite traceback: ')


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(username, password)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(broker, 1883, 60)

mqttc.loop_forever()
