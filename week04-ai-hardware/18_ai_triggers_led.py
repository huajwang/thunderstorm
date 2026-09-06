"""
============================================================
Program 18 — AI Turns On an LED
Course: Build Your First AI Computer Vision System
Week 4: AI + Physical Hardware
============================================================

PURPOSE
  Connect the full pipeline for the first time:
  Camera → YOLO → Decision → Hardware Action

LEARNING OBJECTIVE
  After this program, you should understand that:
  - an on-screen ALERT can become a physical LED
  - Python sends serial commands only when the decision changes
  - AI + hardware together make an interactive system

KEY CONCEPT
  Person detected → send LED_ON / else → send LED_OFF

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 17 controlled the LED with keys only.
  Program 18 lets AI (person detection) control the LED.

WHAT THE COMPUTER CAN DO NOW
  Light an Arduino LED when a person is visible.

HOW TO RUN
  1. Upload arduino_alarm.ino (same as Program 17)
  2. Close Arduino Serial Monitor
  3. Set serial_port below
  4. From this folder, run:  python 18_ai_triggers_led.py
  5. Step into view → LED ON; step out → LED OFF
  6. Press Q to quit

CONTROLS
  + / - — change confidence threshold
  Q — quit (also sends LED_OFF)
============================================================
"""

import time

import cv2
from ultralytics import YOLO

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("ERROR: pyserial is not installed.")
    print("Fix:  pip install pyserial")
    raise SystemExit(1)

# ------------------------------------------------------------
# 1. Settings
# ------------------------------------------------------------
camera_index = 0
serial_port = "COM3"  # change to your port
baud_rate = 9600

allowed_labels = {"person"}
confidence_threshold = 0.50
frames_required_for_alert = 3  # small streak reduces LED flicker

# ------------------------------------------------------------
# 2. Connect to Arduino
# ------------------------------------------------------------
def print_available_ports():
    ports = list(list_ports.comports())
    if not ports:
        print("  (No serial ports found.)")
        return
    print("Available serial ports:")
    for port in ports:
        print(f"  - {port.device}: {port.description}")


print(f"Opening serial port {serial_port}...")
try:
    board = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.SerialException as error:
    print(f"ERROR: Could not open {serial_port}")
    print(f"Details: {error}")
    print_available_ports()
    raise SystemExit(1)

time.sleep(2)  # wait for Arduino USB reset
board.write(b"LED_OFF\n")
print("Arduino connected.")

# ------------------------------------------------------------
# 3. Open camera + load YOLO
# ------------------------------------------------------------
camera = cv2.VideoCapture(camera_index)
if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    board.close()
    raise SystemExit(1)

print("Loading YOLO model (yolov8n)...")
model = YOLO("yolov8n.pt")
print("AI → LED ready. Press Q to quit.")

person_streak = 0
led_is_on = False  # remember last command so we do not spam serial

# ------------------------------------------------------------
# 4. Live loop: detect → decide → maybe send serial command
# ------------------------------------------------------------
while True:
    success, frame = camera.read()
    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    results = model(frame, verbose=False)
    result = results[0]
    names = result.names
    boxes = result.boxes

    display = frame.copy()
    people_count = 0

    if boxes is not None:
        for box in boxes:
            label = names[int(box.cls[0])]
            confidence = float(box.conf[0])
            if label not in allowed_labels:
                continue
            if confidence < confidence_threshold:
                continue

            people_count = people_count + 1
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                display,
                f"{label} {confidence:.2f}",
                (x1, y1 - 10 if y1 > 20 else y1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

    if people_count > 0:
        person_streak = person_streak + 1
    else:
        person_streak = 0

    person_confirmed = person_streak >= frames_required_for_alert

    # --- NEW IDEA: decision controls HARDWARE ---
    if person_confirmed and not led_is_on:
        board.write(b"LED_ON\n")
        led_is_on = True
        print("AI decision: person → LED_ON")
    elif (not person_confirmed) and led_is_on:
        board.write(b"LED_OFF\n")
        led_is_on = False
        print("AI decision: clear → LED_OFF")

    decision = "ALERT / LED ON" if led_is_on else "CLEAR / LED OFF"
    decision_color = (0, 0, 255) if led_is_on else (0, 200, 0)

    cv2.rectangle(display, (0, 0), (display.shape[1], 110), (0, 0, 0), -1)
    cv2.putText(display, decision, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, decision_color, 3)
    cv2.putText(
        display,
        f"People: {people_count}  streak: {person_streak}/{frames_required_for_alert}  thr={confidence_threshold:.2f}",
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    cv2.imshow("Program 18 - AI Triggers LED", display)
    key = cv2.waitKey(1) & 0xFF

    if key in (ord("+"), ord("=")):
        confidence_threshold = min(0.95, confidence_threshold + 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    if key in (ord("-"), ord("_")):
        confidence_threshold = max(0.05, confidence_threshold - 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed.")
        break

# ------------------------------------------------------------
# 5. Clean up
# ------------------------------------------------------------
board.write(b"LED_OFF\n")
board.close()
camera.release()
cv2.destroyAllWindows()
print("Camera + serial closed. Done.")
print("Next: Program 19 adds buzzer alarm + armed/disarmed mode.")

# ============================================================
# STUDENT CHALLENGE
# 1. Only turn the LED on if confidence > 0.70 (stricter than boxes).
# 2. Raise frames_required_for_alert to 8 to reduce flicker.
# 3. (Bonus) Also send BUZZ_ON while ALERT (if buzzer is wired).
#
# EXPECTED RESULT
#  - Step into the camera → on-screen ALERT + Arduino LED ON
#  - Leave the view → CLEAR + LED OFF
#  - Serial commands print only when the LED state changes
#
# COMMON ERRORS
#  - LED flickers rapidly
#      → Increase frames_required_for_alert; improve lighting.
#  - AI works on screen but LED never moves
#      → Recheck Program 17 first; confirm serial_port.
#  - Port busy
#      → Close Serial Monitor / other Python serial programs.
#
# INSTRUCTOR NOTE
#  Celebrate the first full Camera → AI → Decision → Action win.
#  Emphasize: send serial only on CHANGE (this program does).
#  Armed mode + buzzer patterns are Program 19.
# ============================================================
