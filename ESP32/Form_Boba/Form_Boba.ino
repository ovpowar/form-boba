#include <ESP_FlexyStepper.h>
#include <CommandParser.h>

typedef CommandParser<> MyCommandParser;

MyCommandParser parser;

// create the stepper motor object
ESP_FlexyStepper shotdispense1;
ESP_FlexyStepper shotdispense2;
ESP_FlexyStepper shotdispense3;
ESP_FlexyStepper shotdispense4;
ESP_FlexyStepper rawbobadispense;
ESP_FlexyStepper bobaflipper;

const int SD1_STEP = 22;
const int SD2_STEP = 19;
const int SD3_STEP = 18;
const int SD4_STEP = 5;
const int RBD_STEP = 4;
const int BF_STEP = 2;

const int SD1_DIR = 23;
const int SD2_DIR = 23;
const int SD3_DIR = 23;
const int SD4_DIR = 23;
const int RBD_DIR = 23;
const int BF_DIR = 23;

#define COOKER_PIN 35
#define LATCH_PIN 2
#define STEPS_PER_REVOLUTION 200;

void setup() 
{
  pinMode(2, OUTPUT);
  pinMode(COOKER_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  Serial.begin(115200);
  Serial.println("HELLO BOBA LOVER");
  // connect and configure the stepper motor to its IO pins
  shotdispense1.connectToPins(SD1_STEP, SD1_DIR);
  shotdispense2.connectToPins(SD2_STEP, SD2_DIR);
  shotdispense3.connectToPins(SD3_STEP, SD3_DIR);
  shotdispense4.connectToPins(SD4_STEP, SD4_DIR);
  rawbobadispense.connectToPins(RBD_STEP, RBD_DIR);
  bobaflipper.connectToPins(BF_STEP, BF_DIR);
  
  shotdispense1.startAsService();
  shotdispense2.startAsService();
  shotdispense3.startAsService();
  shotdispense4.startAsService();
  rawbobadispense.startAsService();
  bobaflipper.startAsService();

  shotdispense1.setSpeedInStepsPerSecond(100);
  shotdispense2.setSpeedInStepsPerSecond(100);
  shotdispense3.setSpeedInStepsPerSecond(100);
  shotdispense4.setSpeedInStepsPerSecond(100);
  rawbobadispense.setSpeedInStepsPerSecond(10);
  bobaflipper.setSpeedInStepsPerSecond(10);
  shotdispense1.setAccelerationInStepsPerSecondPerSecond(100);
  shotdispense2.setAccelerationInStepsPerSecondPerSecond(100);
  shotdispense3.setAccelerationInStepsPerSecondPerSecond(100);
  shotdispense4.setAccelerationInStepsPerSecondPerSecond(100);



  parser.registerCommand("B0", "sd", &stepper_move);
  parser.registerCommand("B1", "sd", &latch);
  parser.registerCommand("B91", "sd", &stepper_speed);
  parser.registerCommand("B92", "sd", &stepper_acceleration);
  parser.registerCommand("?","", &cmd_status);
}

void cmd_status(MyCommandParser::Argument *args, char *response){
  Serial.println("HELLO");
  strlcpy(response, "success", MyCommandParser::MAX_RESPONSE_SIZE);
}
void latch(MyCommandParser::Argument *args, char *response){
  if (args[0].asInt64 == 76){ // ASCII Value for L is 76
    digitalWrite(LATCH_PIN, args[1].asDouble);
  }
  else if (args[1].asInt64 == 77){ // ASCII Value for L is 78
    digitalWrite(COOKER_PIN, args[1].asDouble);
  }
}
void stepper_speed(MyCommandParser::Argument *args, char *response) {
  if (args[0].asInt64 == 88){ // ASCII Value for X is 88
    int move_speed = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense1.setSpeedInStepsPerSecond(move_speed);
  }
  else if (args[0].asInt64 == 89){ // ASCII Value for Y is 89
    int move_speed = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense2.setSpeedInStepsPerSecond(move_speed);
  }
  else if (args[0].asInt64 == 90){ // ASCII Value for Z is 90
    int move_speed = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense3.setSpeedInStepsPerSecond(move_speed);
  }
  else if (args[0].asInt64 == 65){ // ASCII Value for A is 65
    int move_speed = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense4.setSpeedInStepsPerSecond(move_speed);
  }
  else if (args[0].asInt64 == 66){ // ASCII Value for B is 66
    int move_speed = args[1].asDouble*STEPS_PER_REVOLUTION
    rawbobadispense.setSpeedInStepsPerSecond(move_speed);
  }
  else if (args[0].asInt64 == 67){ // ASCII Value for C is 67
    int move_speed = args[1].asDouble*STEPS_PER_REVOLUTION
    bobaflipper.setSpeedInStepsPerSecond(move_speed);
  }

}

void stepper_acceleration(MyCommandParser::Argument *args, char *response) {
  if (args[0].asInt64 == 88){ // ASCII Value for X is 88
    int move_acceleration = args[1].asDouble*STEPS_PER_REVOLUTION
    
    shotdispense1.setAccelerationInStepsPerSecondPerSecond(move_acceleration);
  }
  else if (args[0].asInt64 == 89){ // ASCII Value for Y is 89
    int move_acceleration = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense2.setAccelerationInStepsPerSecondPerSecond(move_acceleration);
  }
  else if (args[0].asInt64 == 90){ // ASCII Value for Z is 90
    int move_acceleration = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense3.setAccelerationInStepsPerSecondPerSecond(move_acceleration);
  }
  else if (args[0].asInt64 == 65){ // ASCII Value for A is 65
    int move_acceleration = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense4.setAccelerationInStepsPerSecondPerSecond(move_acceleration);
  }
  else if (args[0].asInt64 == 66){ // ASCII Value for B is 66
    int move_acceleration = args[1].asDouble*STEPS_PER_REVOLUTION
    rawbobadispense.setAccelerationInStepsPerSecondPerSecond(move_acceleration);
  }
  else if (args[0].asInt64 == 67){ // ASCII Value for C is 67
    int move_acceleration = args[1].asDouble*STEPS_PER_REVOLUTION
    bobaflipper.setAccelerationInStepsPerSecondPerSecond(move_acceleration);
  }

}

void stepper_move(MyCommandParser::Argument *args, char *response) {
  // Pick the stepper
  if (args[0].asInt64 == 88){ // ASCII Value for X is 88
    int steps_to_move = args[1].asDouble*STEPS_PER_REVOLUTION
    Serial.println(steps_to_move);
    shotdispense1.moveRelativeInSteps(steps_to_move);
    Serial.println("ok");
  }
  else if (args[0].asInt64 == 89){ // ASCII Value for Y is 89
    int steps_to_move = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense2.moveRelativeInSteps(steps_to_move);
    Serial.println("ok");
  }
  else if (args[0].asInt64 == 90){ // ASCII Value for Z is 90
    int steps_to_move = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense3.moveRelativeInSteps(steps_to_move);
    Serial.println("ok");
  }
  else if (args[0].asInt64 == 65){ // ASCII Value for A is 65
    int steps_to_move = args[1].asDouble*STEPS_PER_REVOLUTION
    shotdispense4.moveRelativeInSteps(steps_to_move);
    Serial.println("ok");
  }
  else if (args[0].asInt64 == 66){ // ASCII Value for B is 66
    int steps_to_move = args[1].asDouble*STEPS_PER_REVOLUTION
    rawbobadispense.moveRelativeInSteps(steps_to_move);
    digitalWrite(2, 1);
    Serial.println("ok");
  }
  else if (args[0].asInt64 == 67){ // ASCII Value for C is 67
    int steps_to_move = args[1].asDouble*STEPS_PER_REVOLUTION
    bobaflipper.moveRelativeInSteps(steps_to_move);
    Serial.println("ok");
  }
  else{
    Serial.println(args[0].asString);
    Serial.println("FAILED");
  }

}

void loop() {
  if(Serial.available()) {
    char line[128];
    char response[MyCommandParser::MAX_RESPONSE_SIZE];
    size_t lineLength = Serial.readBytesUntil('\r\n', line, 127);
    line[lineLength] = '\0';
    
    Serial.println(line);
    parser.processCommand(line, response);
    Serial.println(response);
  }


}
