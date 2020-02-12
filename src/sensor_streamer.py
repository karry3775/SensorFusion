#!/usr/bin/env python

"""
This code takes Android data using PhonePi App and streams it to accel_topic, magneto_topic, gyro_topic
"""
import rospy
import sys
from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from sensor_fusion_pkg.msg import SensorMsg

"""
GLobal data that can be shared between socket communication and ros publishers
"""
gyro_data = []
accel_data = []
magneto_data = []
orient_data = []

# lets create our publishers
rospy.init_node("sensor_streamer_node",disable_signals=True)

gyro_pub = rospy.Publisher("/Gyro_topic", SensorMsg, queue_size = 10)
accel_pub = rospy.Publisher("/Accel_topic", SensorMsg, queue_size = 10)
magneto_pub = rospy.Publisher("/Magneto_topic", SensorMsg, queue_size = 10)
orient_pub = rospy.Publisher("/Orientation_topic", SensorMsg, queue_size = 10)

"""
Code snippet from PhonePi.py
"""
app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/accelerometer')
def echo_socket(ws):
	global accel_data, accel_pub
	f=open("accelerometer.txt","a")
	while True:
		message = ws.receive()
		accel_data = message.split(',')
		accel_data = [float(data) for data in accel_data]
		accel_pub.publish(accel_data)
		print("[INFO:] Accelerometer{}".format(accel_data))
        ws.send(message)
        print>>f,message

	f.close()


@sockets.route('/gyroscope')
def echo_socket(ws):
	global gyro_data, gyro_pub
	f=open("gyroscope.txt","a")
	while True:
		message = ws.receive()
		gyro_data = message.split(',')
		gyro_data = [float(data) for data in gyro_data]
		gyro_pub.publish(gyro_data)
		print("[INFO:] Gyroscope{}".format(gyro_data))
        ws.send(message)
        print>>f,message

	f.close()

@sockets.route('/magnetometer')
def echo_socket(ws):
	global magneto_data, magneto_pub
	f=open("magnetometer.txt","a")
	while True:
		message = ws.receive()
		magneto_data = message.split(',')
		magneto_data = [float(data) for data in magneto_data]
		magneto_pub.publish(magneto_data)
		print("[INFO:] Magnetometer{}".format(magneto_data))
        ws.send(message)
        print>>f,message

	f.close()

@sockets.route('/orientation')
def echo_socket(ws):
	global orient_data, orient_pub
	f=open("orientation.txt","a")
	while True:
		message = ws.receive()
		orient_data = message.split(',')
		orient_data = [float(data) for data in orient_data]
		orient_pub.publish(orient_data)
		print("[INFO:] Orientation{}".format(orient_data))
        ws.send(message)
        print>>f,message

	f.close()

@app.route('/')
def hello():
	return 'Hello World!'

if __name__ == "__main__":
	try:
		server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
		server.serve_forever()
	except rospy.ROSInterruptException:
		server.close()
