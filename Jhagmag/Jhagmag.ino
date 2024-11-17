#include <SoftwareSerial.h>

const int buttonPin = 8, redPin = 9, greenPin = 10, bluePin = 11;
const unsigned long timeout = 200, cycleDelay = 5;
const int fadeStepDelay = 50, fadeAmount = 15;
unsigned long lastReceivedTime = 0, lastCycleTime = 0, lastEffectTime = 0, lastBreathingTime = 0, lastRainbowTime = 0, lastFlashTime = 0, lastDebounceTime = 0, debounceDelay = 50;
int state = 0, buttonState = 0, lastButtonState = HIGH;
bool timeoutEnabled = false;
byte red, green, blue, pattern = 0;

SoftwareSerial bluetoothSerial(4, 5);

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  Serial.begin(38400);
  // Initialize software serial for Bluetooth
  bluetoothSerial.begin(9600);
}

void loop() {
  handleCommand(pattern);

  int reading = digitalRead(buttonPin);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState == LOW) {
        pattern = (pattern % 6) + 1;
        handleCommand(pattern);
      }
    }
  }

  lastButtonState = reading;

  // if (Serial.available() > 0) {
  //   byte incomingByte = Serial.read();
  //   Serial.println(incomingByte);
  if (bluetoothSerial.available() > 0) {
    byte incomingByte = bluetoothSerial.read();
    Serial.println(incomingByte);

    lastReceivedTime = millis();

    switch (state) {
      case 0:
        if (incomingByte == 0x01) {
          state = 1;
        } else if (incomingByte == 0x02) {
          state = 2;
        } else if (incomingByte == 0x03) {
          state = 3;
        } else {
          state = 0;
        }
        break;
      case 1:
        timeoutEnabled = (incomingByte != 0);
        state = 0;
        break;
      case 2:
        if (incomingByte == 0)
          setColor(0, 0, 0);
        handleCommand(incomingByte);
        state = 0;
        break;
      case 3:
        red = incomingByte;
        state = 4;
        break;
      case 4:
        green = incomingByte;
        state = 5;
        break;
      case 5:
        blue = incomingByte;
        setColor(red, green, blue);
        state = 0;
        break;
      default:
        state = 0;
        break;
    }
  }

  if (timeoutEnabled && (millis() - lastReceivedTime > timeout)) {
    if (red > 0) red = max(red - fadeAmount, 0);
    if (green > 0) green = max(green - fadeAmount, 0);
    if (blue > 0) blue = max(blue - fadeAmount, 0);

    setColor(red, green, blue);
    delay(fadeStepDelay);
  }
}

void handleCommand(byte command) {
  switch (command) {
    case 0:
      pattern = 0;
      break;
    case 1:
      fadeEffect();
      pattern = 1;
      break;
    case 2:
      cycleEffect();
      pattern = 2;
      break;
    case 3:
      rainbowCycleEffect();
      pattern = 3;
      break;
    case 4:
      breathingEffect();
      pattern = 4;
      break;
    case 5:
      randomFlashEffect();
      pattern = 5;
      break;
    case 6:
      setColor(0, 0, 0);
      pattern = 0;
    default:
      pattern = 0;
      break;
  }
}

void setColor(int r, int g, int b) {
  analogWrite(redPin, r);
  analogWrite(greenPin, g);
  analogWrite(bluePin, b);
}

void fadeEffect() {
  static int brightness = 0;
  static bool increasing = true;
  static int colorStep = 0;

  if (millis() - lastEffectTime >= fadeStepDelay) {
    if (increasing) {
      brightness += fadeAmount;
      if (brightness >= 255) {
        brightness = 255;
        increasing = false;
      }
    } else {
      brightness -= fadeAmount;
      if (brightness <= 0) {
        brightness = 0;
        increasing = true;
        colorStep = (colorStep + 1) % 3;
      }
    }

    if (colorStep == 0) {
      setColor(brightness, 0, 0);
    } else if (colorStep == 1) {
      setColor(0, brightness, 0);
    } else {
      setColor(0, 0, brightness);
    }

    lastEffectTime = millis();
  }
}

void cycleEffect() {
  unsigned long currentMillis = millis();

  if (currentMillis - lastCycleTime >= cycleDelay) {
    lastCycleTime = currentMillis;

    static int i = 0;
    static int cycleStep = 0;

    switch (cycleStep) {
      case 0:
        analogWrite(redPin, 255 - i);
        analogWrite(greenPin, i);
        analogWrite(bluePin, 0);
        break;
      case 1:
        analogWrite(redPin, 0);
        analogWrite(greenPin, 255 - i);
        analogWrite(bluePin, i);
        break;
      case 2:
        analogWrite(redPin, i);
        analogWrite(greenPin, 0);
        analogWrite(bluePin, 255 - i);
        break;
    }

    if (i < 255) {
      i++;
    } else {
      i = 0;
      cycleStep = (cycleStep + 1) % 3;
      delay(50);
    }
  }
}

void rainbowCycleEffect() {
  static int i = 0;

  if (millis() - lastRainbowTime >= fadeStepDelay) {
    setColor((sin(i * 0.024) * 127 + 128), (sin(i * 0.024 + 2) * 127 + 128), (sin(i * 0.024 + 4) * 127 + 128));
    i = (i + 1) % 256;
    lastRainbowTime = millis();
  }
}

void breathingEffect() {
  static int brightness = 0;
  static bool increasing = true;

  if (millis() - lastBreathingTime >= fadeStepDelay) {
    if (increasing) {
      brightness += fadeAmount;
      if (brightness >= 255) {
        brightness = 255;
        increasing = false;
      }
    } else {
      brightness -= fadeAmount;
      if (brightness <= 0) {
        brightness = 0;
        increasing = true;
      }
    }
    setColor(brightness, brightness, brightness);
    lastBreathingTime = millis();
  }
}

void randomFlashEffect() {
  if (millis() - lastFlashTime >= 100) {
    setColor(random(0, 256), random(0, 256), random(0, 256));
    lastFlashTime = millis();
  }
}
