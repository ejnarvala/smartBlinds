# Smart Blinds

This project prototypes an IoT system that can turn open and close a window blind. The setup includes a Raspberry Pi Zero W that uses Python to host the server and interface with the hardware. The backend consists of a Python server implemented using Flask, a micro web framework, and a start up process that instantiates our own custom classes of the hardware peripherals. For the frontend, HTML (Bootstrap) is used to create the GUI and JavaScript is used to send requests to the server endpoints and update the GUI. The GUI has live updates from the Pi such as the light levels in the room and whether the blinds are currently open or closed and also offers manual control of the motor.


### Parts List

These were the main parts that were used in the project:

* Raspberry Pi Zero W 
  * interfaces with hardware and hosts server
* LSM9DS1 Inertial Measurement Unit (IMU)
  * y component of accelerometer used to measure the tilt of the blind  
* Photoresistor
  * detects the light levels of the room
  * [setup circuit](https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading/)  
* DC Motor
  * turns a wheel attachment that is connected to the tilt wand 
* H Bridge 
  * controls the motor and enables both forward and reverse motion to both open and close the blind
  
  
### Wiring 

|IMU|Connection|
|----|----|
|VDD|3.3V|
|GND|GND|
|SDA|2|
|SCL|3|

|H Bridge|Connection|
|----|----|
|VM|Motor power supply +|
|VCC|3.3V|
|GND|GND|
|PWMA|12|
|AIN1|26|
|AIN2|19|
|STBY|13|
|AO1|Motor lead +|
|AO2|Motor lead -|

### Running the Code

Copy the repository into your directory of choice on the Pi and run the following command 
```
sudo python3 smartblinds.py
```

This command will start the program which begins with instantiation of custom motor, IMU, and photoresistor classes. These were created using RPi.GPIO and an I2C IMU library. The IMU is first calibrated by first closing the blind until the IMU stops changing in value (meaning the blind is no longer turning) in order to establish the readings that correspond to the blind being open or closed. The server is then instantiated and the GUI can be accessed using the IP address of the Pi


[gui](/images/gui.png)
GUI screenshot 


### Demo Video

[Demonstration Link](https://youtu.be/hkg0LA-H65w)

