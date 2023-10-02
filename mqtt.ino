#include <WiFi.h> 
#include "Adafruit_MQTT.h" 
#include "Adafruit_MQTT_Client.h" 
#include <analogWrite.h>
/************************* WiFi Access Point *********************************/ 
#define WLAN_SSID       "ni milega" 
#define WLAN_PASS       "9336585507" 
#define MQTT_SERVER      "192.168.43.124"  // give static address
#define MQTT_PORT         1883                    
#define MQTT_USERNAME    "" 
#define MQTT_PASSWORD         "" 
#define left1        25
#define left2        13
#define lefts        20
#define right1       15
#define right2       19
#define rights       20
#define led   2

// Create an ESP8266 WiFiClient class to connect to the MQTT server. 
WiFiClient client; 
// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details. 
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD); 
/****************************** Feeds ***************************************/ 
// Setup a feed called 'pi_led' for publishing. 
// Notice MQTT paths for AIO follow the form: <username>/feeds/<feedname> 
Adafruit_MQTT_Publish pi_led = Adafruit_MQTT_Publish(&mqtt, MQTT_USERNAME "/leds/pi"); 
// Setup a feed called 'esp8266_led' for subscribing to changes. 
Adafruit_MQTT_Subscribe esp8266_led = Adafruit_MQTT_Subscribe(&mqtt, MQTT_USERNAME "/leds/esp8266"); 
/*************************** Sketch Code ************************************/ 
void MQTT_connect(); 
int speeds=255;
void setup() { 
 Serial.begin(115200); 
 delay(10); 

 pinMode(left1, OUTPUT);
 pinMode(left2, OUTPUT);
 pinMode(right1, OUTPUT);
 pinMode(right2, OUTPUT);
 pinMode(lefts, OUTPUT);
 pinMode(rights, OUTPUT);
 pinMode(led, OUTPUT);
 Serial.println(F("RPi-ESP-MQTT")); 
 // Connect to WiFi access point. 
 Serial.println(); Serial.println(); 
 Serial.print("Connecting to "); 
 Serial.println(WLAN_SSID); 
 WiFi.begin(WLAN_SSID, WLAN_PASS); 
 while (WiFi.status() != WL_CONNECTED) { 
   delay(500); 
   Serial.print("."); 
 } 
 Serial.println(); 
 Serial.println("WiFi connected"); 
 right();
 delay(300);
  stopp();
  delay(300);
 left();
 delay(300);
 stopp();
 Serial.println("IP address: "); Serial.println(WiFi.localIP()); 
 // Setup MQTT subscription for esp8266_led feed. 
 mqtt.subscribe(&esp8266_led); 
} 
uint32_t x=0; 
void loop() { 
  analogWrite(lefts, speeds);
  analogWrite(rights, speeds);
 // Ensure the connection to the MQTT server is alive (this will make the first 
 // connection and automatically reconnect when disconnected).  See the MQTT_connect 
 MQTT_connect(); 
 // this is our 'wait for incoming subscription packets' busy subloop 
 // try to spend your time here 
 // Here its read the subscription 
 Adafruit_MQTT_Subscribe *subscription; 
 while ((subscription = mqtt.readSubscription())) { 
   if (subscription == &esp8266_led) { 
     Serial.print(F("Got: ")); 
     Serial.println((char *)esp8266_led.lastread); 
     char aa= *esp8266_led.lastread;
     
    if (aa=='F')
{
     forward();
     Serial.println("F");
}
     else if (aa=='S')
     {
     stopp();
     Serial.println("S");
     Serial.println("Delete this line");
     }
     else if (aa=='B')
     {
     backward();
     Serial.println("B");
     }
     else if(aa=='R')
     {
     right();
     Serial.println("R");
     }
     else if(aa=='L')
     {
     left();  
     Serial.println("L"); 
} 
     else if(aa=='2')
     {
      speeds=200;
      Serial.println(speeds);
     }
     else if(aa=='1')
     {
      speeds=150;
      Serial.println(speeds);
     }
     else if(aa=='3')
     {
      speeds=230;
      Serial.println(speeds);
     }
     else if(aa=='4')
     {
      speeds=255;
      Serial.println(speeds);
     }
 }
 } 

}
// Function to connect and reconnect as necessary to the MQTT server. 
void MQTT_connect() { 
 int8_t ret; 
 // Stop if already connected. 
 if (mqtt.connected()) { 
   return; 
 } 
 Serial.print("Connecting to MQTT... "); 
 uint8_t retries = 3; 
 while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected 
      Serial.println(mqtt.connectErrorString(ret)); 
      Serial.println("Retrying MQTT connection in 5 seconds..."); 
      mqtt.disconnect(); 
      delay(5000);  // wait 5 seconds 
      retries--; 
      if (retries == 0) { 
        // basically die and wait for WDT to reset me 
        while (1); 
      } 
 } 
 Serial.println("MQTT Connected!");
 pi_led.publish("ESPconnected");
   digitalWrite(led, HIGH);
   forward();
   delay(300);
   stopp();
   delay(100);
   digitalWrite(led, LOW); 
   backward();
   delay(300);
   stopp();
   delay(100);
   digitalWrite(led, HIGH);
   forward();
   delay(200);
   stopp();
   delay(100);
   digitalWrite(led, LOW); 
   backward();
   delay(200);
   stopp();
   

}  

 void forward()
 {
  digitalWrite(left1, HIGH);
 digitalWrite(left2, LOW);
 digitalWrite(right1, HIGH);
 digitalWrite(right2, LOW);
 analogWrite(lefts, speeds);
  analogWrite(rights, speeds);
 }
 void backward()
 {
  digitalWrite(left1, LOW);
 digitalWrite(left2, HIGH);
 digitalWrite(right1, LOW);
 digitalWrite(right2, HIGH);
 }
 void stopp()
 {
  digitalWrite(left1, LOW);
 digitalWrite(left2, LOW);
 digitalWrite(right1, LOW);
 digitalWrite(right2, LOW);
 }
 void right()
 {
  digitalWrite(left1, HIGH);
 digitalWrite(left2, LOW);
 digitalWrite(right1, LOW);
 digitalWrite(right2, HIGH);
 }
 void left()
 {
  digitalWrite(left1,LOW);
 digitalWrite(left2, HIGH);
 digitalWrite(right1, HIGH);
 digitalWrite(right2, LOW);
 }
