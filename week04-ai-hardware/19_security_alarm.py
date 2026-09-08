"""
============================================================
Program 19 — Security Alarm Behavior
Course: Build Your First AI Computer Vision System
Week 4: AI + Physical Hardware
============================================================

PURPOSE
  Real security tools have modes and actions.
  This program adds ARMED / DISARMED control, an ALARM command
  (LED + buzzer), and a cooldown so the alarm does not spam.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - systems can be armed or disarmed by a human
  - AI should only trigger hardware when the system is armed
  - cooldowns prevent noisy repeat alarms

KEY CONCEPT
  Armed + person detected → ALARM  |  Disarm key → stop

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 18 turned an LED on for any confirmed person.
  Program 19 adds armed mode, buzzer alarm pattern, and cooldown.

WHAT THE COMPUTER CAN DO NOW
  Act like a simple AI doorway alarm with physical outputs.

HOW TO RUN
  1. Upload arduino_alarm.ino (LED pin 13/8, buzzer pin 9)
  2. Close Serial Monitor; set serial_port below
  3. From this folder, run:  python 19_security_alarm.py
  4. Press A to ARM, then step into view
  5. Press D to DISARM / silence
  6. Press Q to quit

CONTROLS
  A — arm the system
  D — disarm / silence alarm
  + / - — confidence threshold
  Q — quit
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
serial_port = "COM6"  # change to your port
baud_rate = 9600

allowed_labels = {"person"}
confidence_threshold = 0.50
frames_required_for_alert = 5

# Do not re-send ALARM too often (seconds)
alarm_cooldown_seconds = 3.0

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

time.sleep(2)
board.write(b"DISARM\n")
print("Arduino connected. System starts DISARMED.")

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
print("Controls: A=arm  D=disarm  Q=quit")

armed = False
alarm_active = False
person_streak = 0
last_alarm_time = 0.0

# ------------------------------------------------------------
# 4. Live security loop
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
    now = time.time()

    # --- NEW IDEAS: armed mode + ALARM + cooldown ---
    if armed and person_confirmed and not alarm_active:
        if now - last_alarm_time >= alarm_cooldown_seconds:
            board.write(b"ALARM\n")
            alarm_active = True
            last_alarm_time = now
            print("ALARM triggered (armed + person)")

    # If people leave while alarming, stop the hardware pattern
    if alarm_active and not person_confirmed:
        board.write(b"DISARM\n")
        alarm_active = False
        print("Person gone → alarm silenced (still armed)" if armed else "Alarm silenced")
        # Re-arm state: if still armed, DISARM command also clears outputs;
        # keep `armed` True so a new person can trigger again after cooldown.
        if armed:
            # Firmware DISARM clears outputs; we remain armed in Python.
            pass

    # HUD
    if not armed:
        mode_text = "DISARMED"
        mode_color = (160, 160, 160)
    elif alarm_active:
        mode_text = "ALARM!"
        mode_color = (0, 0, 255)
    else:
        mode_text = "ARMED - ALL CLEAR"
        mode_color = (0, 200, 0)

    cv2.rectangle(display, (0, 0), (display.shape[1], 120), (0, 0, 0), -1)
    cv2.putText(display, mode_text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, mode_color, 3)
    cv2.putText(
        display,
        f"People: {people_count}  streak: {person_streak}/{frames_required_for_alert}  thr={confidence_threshold:.2f}",
        (20, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        display,
        "A: arm   D: disarm   Q: quit",
        (20, 112),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (200, 200, 200),
        1,
    )

    cv2.imshow("Program 19 - Security Alarm", display)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("a") or key == ord("A"):
        armed = True
        print("System ARMED")

    if key == ord("d") or key == ord("D"):
        armed = False
        alarm_active = False
        board.write(b"DISARM\n")
        print("System DISARMED")

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
board.write(b"DISARM\n")
board.close()
camera.release()
cv2.destroyAllWindows()
print("Camera + serial closed. Done.")
print("Week 4 complete — AI can trigger real-world alarms.")
print("Next: Week 5 starter project you can remix.")

# ============================================================
# STUDENT CHALLENGE
# 1. Change alarm_cooldown_seconds to 5.0 and test rapid walk-ins.
# 2. Require a higher streak (frames_required_for_alert = 10).
# 3. (Bonus) Save a snapshot automatically when ALARM triggers
#    (reuse Program 03 / 08 save skills).
#
# EXPECTED RESULT
#  - Starts DISARMED (person visible does nothing to buzzer)
#  - Press A, then person → ALARM (LED blink + buzzer if wired)
#  - Press D → silence and disarm
#  - Cooldown prevents immediate re-spam
#
# COMMON ERRORS
#  - Alarm never fires
#      → Press A first; check streak/threshold; confirm Program 17/18 work.
#  - Buzzer silent but LED works
#      → Check pin 9 wiring / active buzzer polarity.
#  - DISARM on Arduino also meant "leave armed" confusion
#      → Python `armed` is the mode; firmware DISARM clears outputs.
#
# INSTRUCTOR NOTE
#  Demo the arming ritual — students love the "security system" feel.
#  Discuss ethics: classroom alarms need consent and clear purpose.
#  Week 5 will wrap this into a configurable starter project.
# ============================================================
