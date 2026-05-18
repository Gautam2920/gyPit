import network
import socket
import json

SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"

wifi = network.WLAN(network.STA_IF)

wifi.active(True)

wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...")

while not wifi.isconnected():
    pass

print("Connected")

ip = wifi.ifconfig()[0]

print("Pico IP:", ip)

server = socket.socket()

server.bind(("0.0.0.0", 9000))

server.listen(1)

print("Listening on port 9000")

while True:
    client, addr = server.accept()

    print("Connection from", addr)

    data = client.recv(65536)

    files = json.loads(data.decode())

    for filename, content in files.items():
        with open(filename, "w") as f:
            f.write(content)

        print("Saved", filename)

    client.send(b"Deployment successful")

    client.close()