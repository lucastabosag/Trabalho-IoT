import time
import psutil
import paho.mqtt.client as mqtt

# conectar ao broker
client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

while True:
    temp = psutil.sensors_temperatures()

    # pega qualquer sensor disponível
    cpu_temp = None
    for sensor in temp.values():
        for entry in sensor:
            cpu_temp = entry.current
            break
        if cpu_temp:
            break

    if cpu_temp:
        print("Enviando:", cpu_temp, "°C")
        client.publish("iot/maquina/temperatura", str(cpu_temp))

    time.sleep(2)
