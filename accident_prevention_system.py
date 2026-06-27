"""
ACCIDENT PREVENTION SYSTEM
===========================
Concept:
  - Eye Blink Sensor : கண் மூடினா → Alarm → Vehicle Auto Stop
  - Alcohol Sensor   : Drink பண்ணி வந்தா → Alarm → Vehicle Auto Stop
  - No LED needed

Hardware:
  - Eye Blink Sensor  → Arduino Pin 2 (Digital)
  - Alcohol Sensor    → Arduino Pin A0 (Analog)
  - Buzzer (Alarm)    → Arduino Pin 8
  - Relay (Car Stop)  → Arduino Pin 7
"""

import serial
import time
import sys
SERIAL_PORT    = 'COM3'
BAUD_RATE      = 9600
ALCOHOL_LIMIT  = 400
EYE_CLOSE_TIME = 2
ALARM_TIME     = 3

def connect():
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("✅ Arduino Connected!")
        return arduino
    except Exception as e:
        print(f"❌ Arduino not found on {SERIAL_PORT}")
        sys.exit(1)

def send(arduino, cmd):
    arduino.write((cmd + '\n').encode())

def read_sensors(arduino):
    eye = None
    alcohol = None
    for _ in range(20):
        try:
            line = arduino.readline().decode('utf-8').strip()
            if line.startswith("EYE:"):
                eye = int(line.split(":")[1])
            elif line.startswith("ALCOHOL:"):
                alcohol = int(line.split(":")[1])
        except:
            pass
        if eye is not None and alcohol is not None:
            break
    return eye, alcohol

def start_alarm(arduino, reason):
    print(f"\n🔔 ALARM! {reason}")
    send(arduino, "BUZZER_ON")

def stop_vehicle(arduino, reason):
    print(f"\n🛑 VEHICLE STOPPED! — {reason}")
    send(arduino, "BUZZER_ON")
    send(arduino, "STOP")
    while True:
        send(arduino, "BUZZER_ON")
        time.sleep(0.5)
        send(arduino, "BUZZER_OFF")
        time.sleep(0.5)

def all_clear(arduino):
    send(arduino, "BUZZER_OFF")
    send(arduino, "START")

def run(arduino):
    print("\n🚗 System Active — Monitoring Driver...")
    print("=" * 45)
    eye_closed_since = None
    alarm_since = None

    while True:
        eye, alcohol = read_sensors(arduino)
        if eye is None or alcohol is None:
            print("[..] Waiting for sensor data", end='\r')
            time.sleep(0.3)
            continue

        eye_status     = "OPEN 👁️ " if eye == 1 else "CLOSED 😴"
        alcohol_status = f"{alcohol} {'⚠️ HIGH' if alcohol > ALCOHOL_LIMIT else '✅ OK'}"
        print(f"Eye: {eye_status} | Alcohol: {alcohol_status}   ", end='\r')

        eye_alert = False
        if eye == 0:
            if eye_closed_since is None:
                eye_closed_since = time.time()
            if time.time() - eye_closed_since >= EYE_CLOSE_TIME:
                eye_alert = True
        else:
            eye_closed_since = None

        alcohol_alert = alcohol > ALCOHOL_LIMIT

        if eye_alert or alcohol_alert:
            reason = []
            if eye_alert:     reason.append("Drowsiness 😴")
            if alcohol_alert: reason.append("Alcohol Detected 🍺")
            reason_str = " + ".join(reason)
            start_alarm(arduino, reason_str)
            if alarm_since is None:
                alarm_since = time.time()
            if time.time() - alarm_since >= ALARM_TIME:
                stop_vehicle(arduino, reason_str)
        else:
            all_clear(arduino)
            alarm_since = None

        time.sleep(0.1)

if __name__ == "__main__":
    arduino = connect()
    try:
        run(arduino)
    except KeyboardInterrupt:
        print("\n\n🔄 System stopped by user.")
        all_clear(arduino)
        arduino.close()
        print("✅ Done.")
