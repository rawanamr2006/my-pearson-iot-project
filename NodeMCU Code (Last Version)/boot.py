import network
import socket
import os
import time
import json


# def connect_to_wifi():
#     try:
#         with open("config.json", "r") as f:
#             config = json.load(f)
#             ssid = config['ssid']
#             password = config["password"]
#     except Exception as e:
#         print("Error loading Wi-Fi credentials:", e)
#         return False
# 
#     # Connect as a station
#     sta = network.WLAN(network.STA_IF)
#     sta.active(True)
#     sta.connect(ssid, password)
# 
#     print(f"Connecting to Wi-Fi SSID: {ssid}...")
#     for _ in range(10):  # Try for 10 seconds
#         if sta.isconnected():
#             print(f"Connected! IP: {sta.ifconfig()[0]}")
#             return True
#         time.sleep(1)
# 
#     print("Failed to connect to Wi-Fi.")
#     return False
# 
# connect_to_wifi()


def start_config_portal():
    # Create an Access Point
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='Config-IoT-System', password='i0t_1s_FuN!')
    print("Access Point active. Connect to 'Config-IoT-System' at 192.168.4.1 (password: i0t_1s_FuN!)")

    # Start a web server
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print(f"Listening for configuration on {addr}")

    while True:
        cl, addr = s.accept()
        print(f"Connection from {addr}")

        # Read the request
        request = b""
        while True:
            part = cl.recv(1024)
            if not part:  # No more data
                break
            request += part

            if b"\r\n\r\n" in request:  # End of headers
                break

        request_str = request.decode('utf-8')
        print(f"Request received: {request_str}")

        # Handle POST request
        if "POST" in request_str:
            try:
                headers, body = request_str.split("\r\n\r\n", 1)

                # Parse Content-Length
                content_length = None
                for line in headers.split("\r\n"):
                    if line.startswith("Content-Length:"):
                        content_length = int(line.split(":")[1].strip())
                        break

                # Read remaining body if necessary
                while content_length and len(body) < content_length:
                    body += cl.recv(1024).decode('utf-8', errors='ignore')

                print(f"Complete body received: {body}")

                # Parse POST data
                params = parse_post_data(body) #{k: v for k, v in (x.split('=') for x in body.split('&'))}
#                 params['email'] = '@'.join(params['email'].split("%40"))  # Decode email
#                 params['ssid'] = " ".join(params['ssid'].split("+"))
                print(f"Parsed parameters: {params}")

                # Save configuration
                if "ssid" in params and "password" in params and "email" in params:
                    save_config(params)
                    response = """
HTTP/1.1 200 OK

<html>
    <body>
        <h1>Configuration Saved!</h1>
        <p>Device will restart...</p>
    </body>
</html>
"""
                    cl.send(response.encode('utf-8'))
                    time.sleep(5)
                    cl.close()
                    # Disable access point
                    ap = network.WLAN(network.AP_IF)
                    ap.active(False)
                    restart_device()
                else:
                    raise ValueError("Missing required parameters.")
            except Exception as e:
                print(f"Error processing POST request: {e}")
                response = """
HTTP/1.1 400 Bad Request

<html>
    <body>
        <h1>Error Processing Request</h1>
        <p>Invalid data submitted. Please try again.</p>
    </body>
</html>
"""
                cl.send(response.encode('utf-8'))
                cl.close()
        else:
            # Serve configuration portal form
            response = serve_config_form()
            cl.send(response.encode('utf-8'))
            cl.close()

def serve_config_form():
    return """
HTTP/1.1 200 OK

<html>
    <head>
        <title>Configuration Portal</title>
    </head>
    <body>
        <h1>Configuration Portal - Rawan Amr ;) </h1>
        <form method="POST" action="/">
            <label for="ssid">Wi-Fi SSID:</label>
            <input type="text" name="ssid" required>
            <label for="password">Wi-Fi Password:</label>
            <input type="password" name="password">
            <label for="email">Recipient Email:</label>
            <input type="email" name="email" required>
            <button type="submit">Save</button>
        </form>
    </body>
</html>
"""

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)
    print("Configuration saved.")

def restart_device():
    import machine
    machine.reset()

def connect_to_wifi():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            ssid = config['ssid']
            password = config['password']
    except Exception as e:
        print(f"Error loading Wi-Fi credentials: {e}")
        return False

    # Connect as a station
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)

    print(f"Connecting to Wi-Fi SSID: {ssid}...")
    for _ in range(10):  # Try for 10 seconds
        if sta.isconnected():
            print(f"Connected! IP: {sta.ifconfig()[0]}")
                # Disable access point
            ap = network.WLAN(network.AP_IF)
            ap.active(False)
            return True

        time.sleep(1)

    print("Failed to connect to Wi-Fi.")
    return False

def parse_post_data(data):
    """Parse and decode URL-encoded POST data."""
    params = {}
    pairs = data.split("&")
    
    for pair in pairs:
        key, value = pair.split("=")
        # Decode percent-encoded values
        params[key] = percent_decode(value)

    return params


def percent_decode(value):
    """Decode percent-encoded string."""
    from ubinascii import unhexlify  # MicroPython's equivalent to `binascii.unhexlify`
    decoded = ""
    i = 0
    while i < len(value):
        if value[i] == '%':
            # Decode percent-encoded characters
            hex_value = value[i+1:i+3]
            decoded += chr(int(hex_value, 16))
            i += 3
        elif value[i] == '+':
            # Replace '+' with space
            decoded += ' '
            i += 1
        else:
            decoded += value[i]
            i += 1
    return decoded


def start():
    connected = connect_to_wifi()

    if not connected:
        print("Wi-Fi not connected. Starting configuration portal.")
        start_config_portal()
    else:
        print("Connected to Wi-Fi. Access Point disabled.")

# Main entry point
start()

