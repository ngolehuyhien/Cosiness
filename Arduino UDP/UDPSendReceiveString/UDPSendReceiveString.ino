#include <Ethernet.h>
#include <EthernetUdp.h>

#include <math.h>
 
const int B = 4275;               // B value of the thermistor
const float R0 = 100000.0;        // R0 = 100k
const int pinTempSensor = A0;     // Grove - Temperature Sensor connect to A0
const int pinSound = A3;            // Grove - sound Sensor connect to A3
const int pinLight = A1;            // Grove - light Sensor connect to A1

// Enter a MAC address and IP address for your controller below.
byte mac[] = {
  0x90, 0xA2, 0xDA, 0x10, 0xC0, 0x67
};

IPAddress ip(192, 168, 0, 3); // The IP address will be dependent on your local network:

unsigned int localPort = 7777;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  // buffer to hold incoming packet,
char ReplyBuffer[] = "acknowledged";        // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

String answer;

void setup() {
  
  Ethernet.begin(mac, ip); // start the Ethernet

  Serial.begin(9600); // Open serial communications and wait for port to open:
  
  Udp.begin(localPort); // start UDP
}

void loop() {
  
  int packetSize = Udp.parsePacket(); // if there's data available, read a packet
  
  if (packetSize) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remote = Udp.remoteIP();
    for (int i=0; i < 4; i++) {
      Serial.print(remote[i], DEC);
      if (i < 3) {
        Serial.print(".");
      }
    }
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    Serial.println("Contents:");
    Serial.println(packetBuffer);

    // temperature
    if (strcmp(packetBuffer,"tempe")==0){
      
      int a = analogRead(pinTempSensor);
 
      float R = 1023.0/a-1.0;
      R = R0*R;
   
      float temperature = 1.0/(log(R/R0)/B+1/298.15)-273.15; // convert to temperature via datasheet

      answer = temperature;
   
      Serial.print("temperature = ");
      Serial.println(answer);
    }
    else if (strcmp(packetBuffer,"light")==0){
      
      int light = analogRead(pinLight);

      float lux = exp(light/80);
      answer = lux;
     
      Serial.print("light = ");
      Serial.println(answer);
    }
    else if (strcmp(packetBuffer,"sound")==0){
      //long  sum = 0;
      
      //for(int i=0; i<32; i++)
      //{
          //sum += analogRead(pinSound);
      //}
      //sum >>= 5;
      

      float adcSound = analogRead(pinSound);

      float db =  20.0*log10(adcSound);

      //long dbSound = (sum+83.2073)/11.003;  // convert adc value to db
      
      answer = db;

      Serial.print("sound = ");
      Serial.println(answer);
    }
    else{
      answer = "";
    }

    char Reply[answer.length()+1];
    strcpy(Reply, answer.c_str());
    
    // send a reply to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Serial.print("I am sending");
    Serial.println(Reply);
    Udp.write(Reply);
    Udp.endPacket();
  }
  delay(1000);
}
