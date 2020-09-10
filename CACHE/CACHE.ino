#define BLYNK_PRINT Serial


#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "g1mDWpqxkI98HMudk9ovUj8YAOrAtXMX"; //false auth-token to prevent any perjury

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "Home";
char pass[] = "Lagan1998";

void setup()
{
  // Debug console
  Serial.begin(9600);

  Blynk.begin(auth, ssid, pass);
}

void loop()
{
  Blynk.run();
}
