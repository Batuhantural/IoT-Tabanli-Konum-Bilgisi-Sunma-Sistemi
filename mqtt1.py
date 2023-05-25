import serial
import webbrowser
import sys
from time import sleep
from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 8883
topic = "deneme"
client_id = 'deneme12'
username = 'batuhan'
password = '12345678'

def GPS_Info(NMEA_buff):
    nmea_time = NMEA_buff[0]                    # extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                # extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               # extract longitude from GPGGA string

    print("NMEA Time:", nmea_time)
    print("NMEA Latitude:", nmea_latitude)
    print("NMEA Longitude:", nmea_longitude)

    lat = float(nmea_latitude)
    longi = float(nmea_longitude)
    lat_in_degrees = convert_to_degrees(lat)
    long_in_degrees = convert_to_degrees(longi)
    
    payload = "Latitude: {}, Longitude: {}".format(lat_in_degrees, long_in_degrees)
    publish_message(payload)
    
    return lat_in_degrees, long_in_degrees

    map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees
    print("Konumu Google Haritalar üzerinde görmek için aşağıdaki bağlantıyı kullanabilirsiniz:")
    print(map_link)

def publish_message(payload):
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker, port)

    client.publish(topic, payload)

    client.disconnect()

    # Olacak.txt dosyasına ekle
    with open("olacak.txt", "w+") as f:
        f.write(payload + "\n")

def convert_to_degrees(raw_value):
    decimal_value = raw_value / 100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
    position = degrees + mm_mmmm
    position = "%.4f" % (position)
    return position

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code:", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, lat_in_degrees, long_in_degrees):
    msg = "Latitude: {}, Longitude: {}".format(lat_in_degrees, long_in_degrees)
    result = client.publish(topic, msg)
    status = result[0]
    print(f"Published message: {msg}")
   
def run():
    ser = serial.Serial("/dev/ttyAMA0", 9600)
    client = connect_mqtt()
    client.loop_start()
    while True:
        received_data = str(ser.readline())
        GPGGA_data_available = received_data.find("$GPGGA,")
        if GPGGA_data_available > 0:
            GPGGA_buffer = received_data.split("$GPGGA,", 1)[1]
            NMEA_buff = GPGGA_buffer.split(',')
            if len(NMEA_buff) >= 4:
                lat_in_degrees, long_in_degrees = GPS_Info(NMEA_buff)
                publish(client, lat_in_degrees, long_in_degrees)
                print("Latitude:", lat_in_degrees)
                print("Longitude:", long_in_degrees)
                print("------------------------------------------------------------")
        else:
            sleep(0.2)

run()

