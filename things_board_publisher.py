import paho.mqtt.client as mqtt
import time
import ADC0832
import math
import RPi.GPIO as GPIO
import json
ACCESS_TOKEN = "sYlvPrNVobW2p2EpJObK"
THINGSBOARD_HOST = "4.206.153.143"

def on_connect(client, userdata, flags, rc):
	print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
collected_data = {
    "temperature" : "INIT",
    }
def send(data):
    client.publish('v1/devices/me/telemetry', json.dumps(collected_data), 1)
    print(f"send {data} to v1/devices/me/telemetry")

def init():
    ADC0832.setup()



def loop():
    while True:
        res = ADC0832.getADC(0)
        if res == 0:
            collected_data["temperature"] = "N.A"
            continue
        Vr = 3.3 * float(res) / 255
        if Vr == 3.3:
            collected_data["temperature"] = "N.A"
            continue

       
        celciusTemp = float
        kelvenTemp = float

        kelvenTemp = 1/298.15 + 1/3455 * math.log((255 / res) - 1)

        kelvenTemp = 1/kelvenTemp
        celciusTemp = kelvenTemp - 273.15

        #Discard Garbage Values
        if celciusTemp >= 50 or celciusTemp<= -50:
            collected_data["temperature"] = "Discarded Value"
            print("Outlier, Descarded value")
        else:
            celciusTemp = round(celciusTemp,2)
            celciusTemp = str(celciusTemp)
            celciusTemp = celciusTemp
            collected_data["temperature"] = celciusTemp
        
        json_data = json.dumps(collected_data)
        send(json_data)
        time.sleep(5)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print('The end!')