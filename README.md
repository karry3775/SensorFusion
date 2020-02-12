# SensorFusion

## Cloning the package
- create an empty workspace in a local directory
```
$ mkdir -p ~/sensor_fusion_ws/src 
$ cd sensor_fusion_ws
$ catkin_make
$ cd src
$ git clone https://github.com/karry3775/SensorFusion.git
```

## Using the package
- Connect your phone and computer to the same network (Hotspot can be used)
- Enter ip address : 5000 to the URL field in PhonePi app
- run the following commands
```
$ roscore
$ rosrun SensorFusion sensor_streamer.py
```
- if the above command gives error then move to the location of this file
```
$ roscd SensorFusion/src/
$ chmod +x sensor_streamer.py
```
- The above line will make this file executable
- Activate the sensor readings you want on the PhonePi App
- Current implementation only supports Accelerometer, Gyroscope, Magnetometer and Orientation data
- You will see data printed on the terminal from which the following command was run
```
$ rosrun SensorFusion sensor_streamer.py
```
- Open another terminal and type
```
rostopic echo \<topic_name>
```
- This will stream data for the specific topic you want

## Topics
- Gyro_topic
- Accel_topic
- Magneto_topic
- Orientation_topic