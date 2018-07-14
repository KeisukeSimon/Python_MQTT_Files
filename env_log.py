import paho.mqtt.client as mqtt
import sqlite3
import sys
import time

#variables para mqtt
hostname = "192.168.1.5"
port = 1883
keepalive = 0
qos = 0
retain = "False"
mqttc = mqtt.Client()

#Metodo de mensaje de suscripcion
def on_subscribe(client, userdata, mid, granted_qos):
	print('subscribed with Qos: {}'.format(granted_qos[0]))
#Metodo avisar en terminar al recibir cualquier mensaje
def on_message(client, userdata, msg):
	payload_string = msg.payload.decode('utf-8')
	print('Topic: {}. Payload: {}'.format(msg.topic,payload_string))

#Metodo al recibir mensaje de tema especifico
def on_message_temperature(client, userdata, msg):
	print(msg.topic + ' ' + str(msg.payload))
	conn=sqlite3.connect('/var/www/mqtt_app/mqtt_app.db')
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))""", ('1', float(msg.payload)))
	conn.commit()
	conn.close()


def on_message_humidity(client, userdata, msg):
	conn=sqlite3.connect('/var/www/mqtt_app/mqtt_app.db')
	curs=conn.cursor()
	curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))""", ('1',float(msg.payload)))
	conn.commit()
	conn.close()

#Agregar tema de suscripcion
mqttc.message_callback_add('temperature',on_message_temperature)
mqttc.message_callback_add('humidity',on_message_humidity)

#Mensaje al conectarse
def on_connect(self, client, userdata, rc):
	print('Connect result: {}'.format(mqtt.connack_string(rc)))
	print("Subscribing to: " + str('temperature' + "..."))
	self.subscribe('temperature',0)
	time.sleep(0.5)
	print("Subscribing to: " + str('humidity' + "..."))
	self.subscribe('humidity',0)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

#Conectarse al broker
mqttc.connect(hostname,port,keepalive)
#Iniciar loop para escuchar todos los mensajes de temas suscritos
mqttc.loop_forever()
