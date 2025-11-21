import time
import paho.mqtt.client as mqtt
import wmi

# Conecta à API de sensores do OpenHardwareMonitor
w = wmi.WMI(namespace="root\OpenHardwareMonitor")

def ler_temperatura_cpu():
    sensores = w.Sensor()
    for s in sensores:
        if s.SensorType == 'Temperature' and "CPU" in s.Name:
            return s.Value
    return None


# Conexão MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

while True:
    temp = ler_temperatura_cpu()

    if temp is not None:
        print(f"Temperatura REAL da CPU: {temp} °C")
        client.publish("iot/maquina/temperatura", str(temp))
    else:
        print("Nenhum sensor encontrado! Abra o OpenHardwareMonitor!")

    time.sleep(2)
