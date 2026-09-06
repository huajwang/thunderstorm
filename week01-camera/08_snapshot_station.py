"""
============================================================
Program 08 — Mini Project: Snapshot Station
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Put Week 1 skills together into one tiny real tool:
  a security-style Snapshot Station.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - big projects are built by COMBINING small skills
  - the same frame can be shown, annotated, filtered, and saved
  - you are ready for AI object detection in Week 2

KEY CONCEPT
  Camera → process → overlay → save evidence

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Programs 01–07 each taught ONE idea.
  Program 08 reuses many of those ideas in ONE program.

WHAT THE COMPUTER CAN DO NOW
  Live security HUD + optional gray view + numbered photo saves.

WEEK 1 SKILLS REUSED
  - camera + frame loop (01, 02)
  - save photos (03)
  - grayscale (04)
  - ROI idea (06)
  - draw box + text (07)

HOW TO RUN
  1. From this folder, run:  python 08_snapshot_station.py
  2. Try G (gray), S (save), Q (quit)
  3. Open the output folder to see your snapshots

CONTROLS
  G — toggle grayscale preview
  S — save a numbered snapshot (with overlay burned in)
  Q — quit and close the camera cleanly
============================================================
"""

import os
from datetime import datetime

import cv2

# ------------------------------------------------------------
# 1. Settings students can customize
# ------------------------------------------------------------
camera_index = 0
output_folder = "output"
filename_prefix = "snapshot"

roi_x1 = 200
roi_y1 = 100
roi_x2 = 440
roi_y2 = 360

box_color = (0, 255, 0)       # green (BGR)
text_color = (255, 255, 255)  # white
title = "SNAPSHOT STATION"

os.makedirs(output_folder, exist_ok=True)

# ------------------------------------------------------------
# 2. Open the webcam
# ------------------------------------------------------------
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    print("Tips:")
    print("  - Is another app already using the webcam?")
    print("  - Try changing camera_index from 0 to 1.")
    print("  - On a laptop, check that the camera privacy switch is on.")
    raise SystemExit(1)

use_grayscale = False
photo_number = 1

print("Camera is open. Welcome to Snapshot Station!")
print(f"Photos save to: {os.path.abspath(output_folder)}")
print("Controls: G = grayscale, S = save, Q = quit")

# ------------------------------------------------------------
# 3. Main loop — combine Week 1 skills
# ------------------------------------------------------------
while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    # Start from a copy (from Program 07)
    display = frame.copy()

    # Optional grayscale (from Program 04)
    # Convert back to BGR afterward so we can still draw COLOR overlays.
    if use_grayscale:
        gray = cv2.cvtColor(display, cv2.COLOR_BGR2GRAY)
        display = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    frame_height, frame_width = display.shape[:2]
    x1 = max(0, min(roi_x1, frame_width - 1))
    x2 = max(0, min(roi_x2, frame_width))
    y1 = max(0, min(roi_y1, frame_height - 1))
    y2 = max(0, min(roi_y2, frame_height))

    # ROI rectangle + HUD text (from Program 07)
    cv2.rectangle(display, (x1, y1), (x2, y2), box_color, 2)

    mode_label = "GRAY" if use_grayscale else "COLOR"
    cv2.putText(
        display,
        f"{title}  [{mode_label}]",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        text_color,
        2,
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        display,
        timestamp,
        (20, frame_height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        text_color,
        2,
    )

    # Help line so students remember keys without leaving the window
    cv2.putText(
        display,
        "G: gray   S: save   Q: quit",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        text_color,
        1,
    )

    cv2.imshow("Program 08 - Snapshot Station", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("g") or key == ord("G"):
        use_grayscale = not use_grayscale
        print(f"Grayscale preview: {'ON' if use_grayscale else 'OFF'}")

    # Save the annotated frame (from Program 03 + overlays)
    if key == ord("s") or key == ord("S"):
        filename = f"{filename_prefix}_{photo_number:02d}.jpg"
        filepath = os.path.join(output_folder, filename)
        saved = cv2.imwrite(filepath, display)

        if saved:
            print(f"Saved: {filepath}")
            photo_number = photo_number + 1
        else:
            print(f"ERROR: Could not save photo to {filepath}")

    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 4. Clean up
# ------------------------------------------------------------
camera.release()
cv2.destroyAllWindows()
print("Camera released. Done.")
print("Week 1 complete — you taught the computer to see and save.")
print("Next up (Week 2): AI object detection with YOLO.")

# ============================================================
# STUDENT CHALLENGE
# 1. Add ARMED / DISARMED status:
#    - start with armed = False
#    - press A to toggle armed/disarmed
#    - draw the status on screen (example: "STATUS: ARMED")
# 2. Change title and filename_prefix to your project name.
# 3. (Bonus) When you press S, ALSO save a cropped ROI image
#    using display[y1:y2, x1:x2] (Program 06 skill).
#
# EXPECTED RESULT
#  - Security-style live HUD with ROI box + timestamp
#  - G toggles gray/color preview
#  - S saves numbered photos into output/
#  - Saved photos include the overlays you saw on screen
#
# COMMON ERRORS
#  - Drawing colored text fails after grayscale
#      → Convert gray back to BGR before drawing (this program does that).
#  - Saved photo has no box/text
#      → Save `display` (annotated), not the original `frame`.
#  - ROI box in the wrong place
#      → Edit roi_x1/y1/x2/y2 to match your room.
#
# INSTRUCTOR NOTE
#  Celebrate Week 1 as a finished TOOL, not just demos.
#  Exit ticket: "A video is frames. We can process, annotate, and save them."
#  Preview Week 2: "Next, AI will choose the boxes for us."
#  Optional gallery walk: students show one saved snapshot.
# ============================================================
