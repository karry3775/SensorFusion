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
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler

from tf import TransformBroadcaster
from rospy import Time

"""
GLobal data that can be shared between socket communication and ros publishers
"""
gyro_data = []
accel_data = []
magneto_data = []
orient_data = []
geoloc_data = []
# lets create our publishers
rospy.init_node("sensor_streamer_node",disable_signals=True)

gyro_pub = rospy.Publisher("/Gyro_topic", SensorMsg, queue_size = 10)
accel_pub = rospy.Publisher("/Accel_topic", SensorMsg, queue_size = 10)
magneto_pub = rospy.Publisher("/Magneto_topic", SensorMsg, queue_size = 10)
orient_pub = rospy.Publisher("/Orientation_topic", SensorMsg, queue_size = 10)
geoloc_pub = rospy.Publisher("/Geolocation_topic", SensorMsg, queue_size = 10)
pose_pub = rospy.Publisher("/Pose_topic", Pose, queue_size = 10)
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
	global orient_data, orient_pub, pose_pub

	b = TransformBroadcaster()

	f=open("orientation.txt","a")
	while True:
		message = ws.receive()
		orient_data = message.split(',')
		orient_data = [float(data) for data in orient_data]
		orient_pub.publish(orient_data)
		### Publish to Pose topic for visualization ###
		q = quaternion_from_euler(orient_data[0], orient_data[1], orient_data[2])
		pose_msg = Pose()
		pose_msg.orientation.x = q[0]
		pose_msg.orientation.y = q[1]
		pose_msg.orientation.z = q[2]
		pose_msg.orientation.w = q[3]
		pose_pub.publish(pose_msg)

		b.sendTransform((1,1,1), (q[0],q[1],q[2],q[3]), Time.now(), 'child_link', 'base_link')
		### END HERE ###
		print("[INFO:] Orientation{}".format(orient_data))
        ws.send(message)
        print>>f,message

	f.close()

@sockets.route('/geolocation')
def echo_socket(ws):
	global geoloc_data, geoloc_pub
	f=open("geolocation.txt","a")
	while True:
		message = ws.receive()
		geoloc_data = message.split(',')
		geoloc_data = [float(data) for data in geoloc_data]
		geoloc_pub.publish(geoloc_data)
		print("[INFO:] Geolocation{}".format(geoloc_data))
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
