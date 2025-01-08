# My Project For Pearson Accredition "U18 IoT", Network & Cybersecurity Specialization
# Rawan Amr Abdelsattar @ WE Zayed ATS

#importing libraries to be used

from machine import Pin
import time 
import json
import urequests
import network
import usocket

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
recipient_email = config['email']
print(recipient_email)

sta_if = network.WLAN(network.WLAN.IF_STA)

# Declaring and assigning pins

PIR = Pin(5, Pin.IN)
buzzer = Pin(4, Pin.OUT)
led = Pin(2, Pin.OUT)

last_trigger_time = 0  # To store the last trigger time
last_email_sent_time = 0
pause_time = 5  # Pause time to ignore rapid successive triggers

# logs to the flask api I hosted on PythonAnywhere.com    
def log_to_api():
    
    url = "http://rawanamr.pythonanywhere.com/log" # My Flask API URL (github link provided)
    
    data = {"event":"motion_detected","message": "Motion Deteced! Sending an Email ...","email": recipient_email} # Request Body
    headers = {'Content-Type': 'application/json'} # Request Headers
    
    # Trying to send POST request to the Flask API I hosted on PythonAnywhere.com (+ Handling Errors)
    try:
        response = urequests.post(url, data=json.dumps(data), headers=headers) 
        print("Dashboard updated, API Response: "+ response.text) # Sending POST Request to API
        
    except:
        print("Failed to update dashboard,\nTry to access the API through the URL and check internet connection\n")
    
    
def alert(pin):
    global last_trigger_time
    current_time = time.time()
    time_passed = current_time - last_trigger_time
    
    # checking time passed since last trigger, to avoid rapid notification
    if time_passed > pause_time:
        print("Motion Detected,  seconds passed since last trigger: ", time_passed)
        print("Sending Email and updating Dashboard logs...\n")
        
        # playing buzzer for alert (to detect and deter)
        buzzer.value(1)
        time.sleep(1)
        buzzer.value(0)
        
        #sending email and log 
        log_to_api() # Note: needs internet connection to connect to my Flask API  (github link provided)
        
        last_trigger_time  = current_time # update last trigger time  


PIR.irq(trigger=Pin.IRQ_RISING, handler=alert) # attaching interrupter to PIR, to handle motion detection


# Main loop
while True:
    print(PIR.value()) # printing PIR output values (for debugging purposes)
    
    time.sleep(1) # to prevent rapid notifications and logs



  
  
