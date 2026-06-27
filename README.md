# Accident Prevention System

## Concept
- Eye Blink Sensor : கண் மூடினா → Alarm → Vehicle Auto Stop
- Alcohol Sensor : Drink பண்ணி வந்தா → Alarm → Vehicle Auto Stop

## Components
- Eye Blink Sensor → Arduino Pin 2
- Alcohol Sensor (MQ-3) → Arduino Pin A0
- Buzzer → Arduino Pin 8
- Relay Module → Arduino Pin 7

## Files
- accident_prevention_system.py → Main Python code
- arduino_sender.ino → Arduino code

## How to Run
1. pip install pyserial
2. Upload arduino_sender.ino to Arduino
3. python accident_prevention_system.py
