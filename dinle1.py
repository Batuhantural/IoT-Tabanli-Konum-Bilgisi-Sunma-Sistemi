import paho.mqtt.client as mqtt
import webbrowser
import sys

gelen_bilgi = []
latitute_str = []
longitute_str = []
latitute = 0.0
longitute = 0.0
map_link = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("deneme", 1)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    global gelen_bilgi
    gelen_bilgi = str(msg.payload.decode("utf-8"))
    print(gelen_bilgi)
    global latitute_str, longitute_str, latitute, longitute, map_link
    latitute_str = gelen_bilgi[12:19]
    longitute_str = gelen_bilgi[23:30]
    print(latitute_str)
    print(longitute_str)
    gec = [latitute_str, longitute_str]
    print(gec)

    with open("olacak.txt", "a") as f:
        f.write(latitute_str)
        f.write(",")
        f.write(longitute_str)
        f.write("\n")
    
    latitute = float(latitute_str)
    longitute = float(longitute_str)
    
 # Dosyanın içeriğini yeniden oku
    with open(file_path, "r") as f:
        veriler = f.read()

    print(veriler)

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 8883, 60)
    client.loop_forever()

except KeyboardInterrupt:
 pass

import os

# Mevcut çalışma dizinini al
current_dir = os.path.dirname(os.path.abspath(__file__))

# Dosya yolunu oluştur
file_path = os.path.join(current_dir, "olacak.txt")


       
with open(file_path,"r") as f:
             veriler = f.read()

print(veriler)
