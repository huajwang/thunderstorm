"""
============================================================
Program 13 — How Fast Is Real-Time?
Course: Build Your First AI Computer Vision System
Week 3: Real-Time AI Vision
============================================================

PURPOSE
  "Real-time" means the computer keeps up with the camera.
  FPS (frames per second) tells you how fast your loop is running.
  AI makes the loop heavier — so we measure it.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - FPS = how many frames you process each second
  - higher FPS feels smoother; lower FPS feels laggy
  - YOLO on every frame has a speed cost

KEY CONCEPT
  Time the loop → calculate FPS → show it on screen

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 12 filtered to people.
  Program 13 keeps that idea and ADDS an FPS readout.

WHAT THE COMPUTER CAN DO NOW
  Live person detection with an on-screen speed meter.

HOW TO RUN
  1. From this folder, run:  python 13_fps_monitor.py
  2. Watch the FPS number in the corner
  3. Press Q to quit

CONTROLS
  Q — quit and close the camera cleanly
============================================================
"""

import time

import cv2
from ultralytics import YOLO

# ------------------------------------------------------------
# 1. Settings
# ------------------------------------------------------------
camera_index = 0
allowed_labels = {"person"}

# Optional speed experiment (Student Challenge):
# set use_half_size = True to run YOLO on a 50% frame
use_half_size = False

# ------------------------------------------------------------
# 2. Open camera + load YOLO once
# ------------------------------------------------------------
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    print("Tips: close other camera apps, or try camera_index = 1")
    raise SystemExit(1)

print("Loading YOLO model (yolov8n)...")
model = YOLO("yolov8n.pt")

box_color = (0, 255, 0)
text_color = (255, 255, 255)

print(f"Half-size mode: {use_half_size}")
print("FPS monitor ready. Press Q to quit.")

# For FPS: remember when the previous frame finished
prev_time = time.time()
fps = 0.0

# ------------------------------------------------------------
# 3. Live loop with FPS measurement
# ------------------------------------------------------------
while True:
    success, frame = camera.read()
    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    detect_frame = frame
    if use_half_size:
        detect_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    results = model(detect_frame, verbose=False)
    result = results[0]
    names = result.names
    boxes = result.boxes

    # Draw on the same image YOLO used (keeps box coordinates aligned)
    display = detect_frame.copy()

    if boxes is not None:
        for box in boxes:
            label = names[int(box.cls[0])]
            if label not in allowed_labels:
                continue

            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(display, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(
                display,
                f"{label} {confidence:.2f}",
                (x1, y1 - 10 if y1 > 20 else y1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                text_color,
                2,
            )

    # --- FPS math ---
    # seconds for this frame = now - previous timestamp
    now = time.time()
    elapsed = now - prev_time
    prev_time = now
    if elapsed > 0:
        fps = 1.0 / elapsed

    cv2.putText(
        display,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        text_color,
        2,
    )
    size_note = "half" if use_half_size else "full"
    cv2.putText(
        display,
        f"size={size_note}  |  Q: quit",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        text_color,
        2,
    )

    cv2.imshow("Program 13 - FPS Monitor", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 4. Clean up
# ------------------------------------------------------------
camera.release()
cv2.destroyAllWindows()
print(f"Last FPS reading: {fps:.1f}")
print("Camera released. Done.")
print("Next: Program 14 adds a confidence threshold.")

# ============================================================
# STUDENT CHALLENGE
# 1. Set use_half_size = True and compare FPS to full size.
# 2. Write your two FPS numbers in a comment at the top.
# 3. (Bonus) Press R later? For now: restart the program to flip modes.
#
# EXPECTED RESULT
#  - Live person boxes (when a person is visible)
#  - HUD shows FPS updating every frame
#  - Half-size mode usually increases FPS on the same computer
#
# COMMON ERRORS
#  - FPS jumps around a lot
#      → Normal; it measures each single frame. Look at the typical range.
#  - Boxes in the wrong place after resizing
#      → Draw on the SAME image you gave to YOLO (this program does).
#  - Thinking higher FPS always means better AI
#      → Faster can mean smaller/less detailed frames (tradeoff).
#
# INSTRUCTOR NOTE
#  Ask: "Is 5 FPS still useful for a doorway alarm?" (Often yes.)
#  Connect to security: smooth video is nice; correct alerts matter more.
#  Thresholds next — do not add them here.
# ============================================================
