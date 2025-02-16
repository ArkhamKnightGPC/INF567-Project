import random
import threading
import warnings
from paho.mqtt import client as mqtt_client

class MqttManager:
    """Class to handle the MQTT connection."""

    def __init__(self, broker: str, port: int, pub_topic: str):
        self.broker = broker
        self.port = port
        self.pub_topic = pub_topic
        self.client_id = f'pub-{random.randint(0, 1000)}'
        self.client: mqtt_client.Client = self.connect_mqtt()

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code {rc}")

        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, msg: str):
        result = self.client.publish(self.pub_topic, msg)
        status = result[0]
        if status == 0:
            print(f"Sent '{msg}' to topic '{self.pub_topic}'")
        else:
            print(f"Failed to send message  '{msg}' to topic {self.pub_topic}")

    def run(self):
        mqtt_thread = threading.Thread(target=self.run, daemon=True)
        mqtt_thread.start()

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    LOCK = threading.Lock()

    mqtt_manager = MqttManager('broker.emqx.io', 1883, "emqx/INF567")
    mqtt_manager.run()

    with LOCK:
        print("MQTT Manager started")
        print("Press Enter to exit\n")

    user_input = input("Send a message to the LED driver:")
    mqtt_manager.publish(user_input)
    
