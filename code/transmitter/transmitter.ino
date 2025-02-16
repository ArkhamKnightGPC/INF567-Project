#include <WiFi.h>
#include <PubSubClient.h>

// wifi
const char *ssid = "ZeroYear";
const char *password = "olar1234";

// we'll use the public emqx broker for this demo
const char *mqtt_broker = "broker.emqx.io";
const char *topic = "emqx/INF567";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

#define MAX_MESSAGE_LEN 50  // Maximum message length
char msgBuffer[MAX_MESSAGE_LEN];

#define LED_PIN 15  // LED connected to A4 (pin 15)
const int bitDuration = 2000;  // Bit duration

void setup() {
  Serial.begin(115200);

  // First, we connect to WiFi
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  // Second, we connect to MQTT broker, set callback function
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
      String client_id = "esp32-client-";
      client_id += String(WiFi.macAddress());
      Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
      if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
          Serial.println("Public EMQX MQTT broker connected");
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
      }
  }

  // Finally subscribe to topic where we will receive stimulus
  client.subscribe(topic);
  // and setup analog pin we will use to modulate the LED
  pinMode(LED_PIN, OUTPUT);

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// Function to send a Manchester-encoded bit
void sendManchesterBit(int bit) {
  Serial.print(bit);
  if (bit == 0) {
    analogWrite(LED_PIN, 255);  // HIGH
    delay(bitDuration / 2);
    analogWrite(LED_PIN, 0);    // LOW
    delay(bitDuration / 2);
  } else {
    analogWrite(LED_PIN, 0);    // LOW
    delay(bitDuration / 2);
    analogWrite(LED_PIN, 255);  // HIGH
    delay(bitDuration / 2);
  }
}

// Function to send a character in Manchester encoding
void sendManchesterChar(char c) {
  for (int i = 7; i >= 0; i--) {  // Send 8-bit binary (MSB first)
    int bit = (c >> i) & 1;
    sendManchesterBit(bit);
  }
}

// Function to send a string in Manchester encoding
void sendManchesterString(const char* text) {
  while(*text) {
    Serial.print(*text);
    sendManchesterChar(*text++);
  }
}

void callback(char *topic, byte *payload, unsigned int length) {
  snprintf(msgBuffer, sizeof(msgBuffer), "%s#", (char*)payload); // we use # to indicate end of transmission
  Serial.print(msgBuffer); //to debug
  sendManchesterString(msgBuffer);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
