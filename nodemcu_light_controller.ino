#include <ESP8266WiFi.h>

#define CEILING_LIGHT D1
#define DESK_LAMP D2
#define BEDSIDE_LIGHT D3
#define AMBIENT_LIGHT D4

bool ceilingState = false;
bool deskState = false;
bool bedsideState = false;
bool ambientState = false;

void setup() {
    Serial.begin(9600);
    pinMode(CEILING_LIGHT, OUTPUT);
    pinMode(DESK_LAMP, OUTPUT);
    pinMode(BEDSIDE_LIGHT, OUTPUT);
    pinMode(AMBIENT_LIGHT, OUTPUT);

    digitalWrite(CEILING_LIGHT, LOW);
    digitalWrite(DESK_LAMP, LOW);
    digitalWrite(BEDSIDE_LIGHT, LOW);
    digitalWrite(AMBIENT_LIGHT, LOW);

    Serial.println("NodeMCU Ready for Light Control");
}

void loop() {
    if (Serial.available()) {
        char command = Serial.read();

        switch (command) {
            case '1':
                ceilingState = !ceilingState;
                digitalWrite(CEILING_LIGHT, ceilingState ? HIGH : LOW);
                Serial.println(ceilingState ? "Light 1: ON" : "Light 1: OFF");
                break;
            case '2':
                deskState = !deskState;
                digitalWrite(DESK_LAMP, deskState ? HIGH : LOW);
                Serial.println(deskState ? "Light 2: ON" : "Light 2: OFF");
                break;
            case '3':
                bedsideState = !bedsideState;
                digitalWrite(BEDSIDE_LIGHT, bedsideState ? HIGH : LOW);
                Serial.println(bedsideState ? "Light 3: ON" : "Light 3: OFF");
                break;
            case '4':
                ambientState = !ambientState;
                digitalWrite(AMBIENT_LIGHT, ambientState ? HIGH : LOW);
                Serial.println(ambientState ? "Light 4: ON" : "Light 4: OFF");
                break;
            case '5':
                // Toggle all lights
                bool newState = !(ceilingState && deskState && bedsideState && ambientState);
                ceilingState = deskState = bedsideState = ambientState = newState;

                digitalWrite(CEILING_LIGHT, ceilingState ? HIGH : LOW);
                digitalWrite(DESK_LAMP, deskState ? HIGH : LOW);
                digitalWrite(BEDSIDE_LIGHT, bedsideState ? HIGH : LOW);
                
                digitalWrite(AMBIENT_LIGHT, ambientState ? HIGH : LOW);

                Serial.println(newState ? "All Lights: ON" : "All Lights: OFF");
                break;
        }
    }
}
