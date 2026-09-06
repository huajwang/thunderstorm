"""
============================================================
Program 20 — Smart Security Starter Kit
Course: Build Your First AI Computer Vision System
Week 5: Student AI Project
============================================================

PURPOSE
  This is your remixable final starter.
  Customize the SETTINGS block to build YOUR project variant
  (security, pet detector, visitor counter, recycling watch, ...).

LEARNING OBJECTIVE
  After this program, you should understand that:
  - one pipeline can become many products by changing settings
  - Camera → AI → Decision → Action is now YOUR system
  - good projects start from working code, then change one thing

KEY CONCEPT
  Configurable AI vision system (edit settings, not everything)

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 19 was a fixed security alarm lesson.
  Program 20 is the same pipeline with clear SETTINGS for remixing.

WHAT THE COMPUTER CAN DO NOW
  Run a complete smart vision project you can personalize.

HOW TO RUN
  1. Edit SETTINGS below (title, labels, port, ROI, etc.)
  2. If using Arduino: upload week04 firmware; close Serial Monitor
  3. From this folder, run:  python 20_smart_security_starter.py
  4. A = arm, D = disarm, S = snapshot, Q = quit

CONTROLS
  A — arm
  D — disarm / silence
  S — save a snapshot now
  + / - — confidence threshold
  Q — quit
============================================================
"""

import os
import time
from datetime import datetime

import cv2
from ultralytics import YOLO

# ============================================================
# SETTINGS — change these for YOUR project
# ============================================================
project_title = "AI SMART SECURITY"
alert_text = "ALERT"
clear_text = "ALL CLEAR"

camera_index = 0
allowed_labels = {"person"}      # try {"dog", "cat"} or {"bottle"}
confidence_threshold = 0.50
frames_required_for_alert = 5
alarm_cooldown_seconds = 3.0

# ROI (doorway zone). Set use_roi = True after adjusting coordinates.
use_roi = False
roi_x1, roi_y1 = 200, 100
roi_x2, roi_y2 = 440, 360

# Hardware: set False for on-screen-only demos
use_arduino = True
serial_port = "COM3"             # change to your port
baud_rate = 9600

# Save a photo automatically when alarm triggers
save_on_alarm = True
output_folder = "output"
filename_prefix = "alarm"
# ============================================================

os.makedirs(output_folder, exist_ok=True)

board = None
if use_arduino:
    try:
        import serial
        from serial.tools import list_ports
    except ImportError:
        print("ERROR: pyserial is not installed. Fix: pip install pyserial")
        raise SystemExit(1)

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
        print("Tip: set use_arduino = False to demo without hardware.")
        raise SystemExit(1)
    time.sleep(2)
    board.write(b"DISARM\n")
    print("Arduino connected.")
else:
    print("Arduino disabled (on-screen decisions only).")

camera = cv2.VideoCapture(camera_index)
if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    if board is not None:
        board.close()
    raise SystemExit(1)

print("Loading YOLO model (yolov8n)...")
model = YOLO("yolov8n.pt")
print(f"Project: {project_title}")
print(f"Watching for: {sorted(allowed_labels)}")
print("Controls: A=arm  D=disarm  S=snapshot  Q=quit")

armed = False
alarm_active = False
person_streak = 0
last_alarm_time = 0.0
photo_number = 1


def box_center_in_roi(x1, y1, x2, y2):
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    return roi_x1 <= center_x <= roi_x2 and roi_y1 <= center_y <= roi_y2


def save_snapshot(image):
    global photo_number
    filename = f"{filename_prefix}_{photo_number:02d}.jpg"
    filepath = os.path.join(output_folder, filename)
    if cv2.imwrite(filepath, image):
        print(f"Saved: {filepath}")
        photo_number = photo_number + 1
    else:
        print(f"ERROR: Could not save {filepath}")


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
    target_count = 0

    if use_roi:
        cv2.rectangle(display, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 255, 0), 2)

    if boxes is not None:
        for box in boxes:
            label = names[int(box.cls[0])]
            confidence = float(box.conf[0])
            if label not in allowed_labels:
                continue
            if confidence < confidence_threshold:
                continue

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            if use_roi and not box_center_in_roi(x1, y1, x2, y2):
                continue

            target_count = target_count + 1
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

    if target_count > 0:
        person_streak = person_streak + 1
    else:
        person_streak = 0

    target_confirmed = person_streak >= frames_required_for_alert
    now = time.time()

    if armed and target_confirmed and not alarm_active:
        if now - last_alarm_time >= alarm_cooldown_seconds:
            alarm_active = True
            last_alarm_time = now
            print(f"{alert_text} triggered")
            if board is not None:
                board.write(b"ALARM\n")
            if save_on_alarm:
                save_snapshot(display)

    if alarm_active and not target_confirmed:
        alarm_active = False
        print("Target gone → alarm cleared")
        if board is not None:
            board.write(b"DISARM\n")

    if not armed:
        mode_text = f"{project_title}  |  DISARMED"
        mode_color = (160, 160, 160)
    elif alarm_active:
        mode_text = f"{project_title}  |  {alert_text}"
        mode_color = (0, 0, 255)
    else:
        mode_text = f"{project_title}  |  {clear_text}"
        mode_color = (0, 200, 0)

    cv2.rectangle(display, (0, 0), (display.shape[1], 125), (0, 0, 0), -1)
    cv2.putText(display, mode_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.85, mode_color, 2)
    cv2.putText(
        display,
        f"Count: {target_count}  streak: {person_streak}/{frames_required_for_alert}  thr={confidence_threshold:.2f}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        display,
        f"{timestamp}   A:arm D:disarm S:snap Q:quit",
        (20, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (200, 200, 200),
        1,
    )

    cv2.imshow("Program 20 - Smart Security Starter", display)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("a") or key == ord("A"):
        armed = True
        print("System ARMED")

    if key == ord("d") or key == ord("D"):
        armed = False
        alarm_active = False
        if board is not None:
            board.write(b"DISARM\n")
        print("System DISARMED")

    if key == ord("s") or key == ord("S"):
        save_snapshot(display)

    if key in (ord("+"), ord("=")):
        confidence_threshold = min(0.95, confidence_threshold + 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    if key in (ord("-"), ord("_")):
        confidence_threshold = max(0.05, confidence_threshold - 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed.")
        break

if board is not None:
    board.write(b"DISARM\n")
    board.close()
camera.release()
cv2.destroyAllWindows()
print("Done. Customize SETTINGS and make it yours.")
print("Next: Week 6 Demo Day — tell the Camera → AI → Decision → Action story.")

# ============================================================
# STUDENT CHALLENGE
# 1. Pick a project from project_ideas.md and change SETTINGS.
# 2. Turn on use_roi = True and align the doorway box.
# 3. (Bonus) Write notes.md in student_template/ explaining your changes.
#
# EXPECTED RESULT
#  - Full pipeline with your project title on screen
#  - Optional Arduino alarm when armed + target confirmed
#  - Optional auto-snapshot on alarm + manual S snapshots
#
# COMMON ERRORS
#  - Hardware fails on Demo Day
#      → Set use_arduino = False and continue with on-screen demo.
#  - Wrong labels (no boxes)
#      → Check YOLO names are lowercase: person, dog, cat, bottle, car.
#  - ROI filters everyone out
#      → Widen ROI or temporarily set use_roi = False.
#
# INSTRUCTOR NOTE
#  Grade the story + intentional SETTINGS changes, not code elegance.
#  Encourage one clear theme per student/team.
# ============================================================
