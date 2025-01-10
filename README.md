
![Capture3](https://github.com/user-attachments/assets/030f977b-37d4-4033-9435-96efa15aa4c3)


How To Test
1)	Connect Battery terminals to the breadboard as in design (circuit design)
2)	Connect to the Config-IoT-System Wi-Fi network (using phone or PC), credentials above (SSID:"Config-IoT-System", password:"i0t_1s_FuN!")
3)	Go to your browser and type http://192.168.4.1 
4)	Fill in the Configuration Form (use the SSID you want node to connect to, password and your email to receive notifications) and click “save”
5)	Device will restart and retry connecting 
6)	If led on NodeMCU lights up this means it’s connected and started detection
7)	If not connected (led did not light), try restarting the device or go through configuration again


How It Works

![Flowchart](https://github.com/user-attachments/assets/c3a76ccc-593f-4268-b75c-370ec99a97ea)

Some Notes
 Device may need to be manually reset after saving configuration
 If connected to Wi-Fi but no internet connection, only the buzzer will start but no email
notification or dashboard update can be done. But connection to Wi-Fi Network (any
WLAN) is mandatory to start detection.
 Make sure to consider placing the sensor away from any sources of interference or heat
sources as this will cause false positives
 When testing, kindly make sure that the battery is not faulty or drained.
