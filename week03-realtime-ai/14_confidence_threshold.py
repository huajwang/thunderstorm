"""
============================================================
Program 14 — Confidence Threshold
Course: Build Your First AI Computer Vision System
Week 3: Real-Time AI Vision
============================================================

PURPOSE
  Not every detection deserves trust.
  A confidence threshold lets YOU decide how sure YOLO must be
  before a box is shown (and later, before an alarm fires).

LEARNING OBJECTIVE
  After this program, you should understand that:
  - confidence is a score from 0.0 to 1.0
  - a THRESHOLD is a cutoff you choose (example: 0.50)
  - raising the threshold reduces weak / false detections

KEY CONCEPT
  Keep detection only if confidence >= threshold

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 13 measured FPS.
  Program 14 adds a tunable confidence gate (with keyboard control).

WHAT THE COMPUTER CAN DO NOW
  Live person detection that ignores low-confidence guesses.

HOW TO RUN
  1. From this folder, run:  python 14_confidence_threshold.py
  2. Press + / - to raise or lower the threshold
  3. Press Q to quit

CONTROLS
  + or = — raise threshold by 0.05
  - or _ — lower threshold by 0.05
  Q — quit and close the camera cleanly
============================================================
"""

import cv2
from ultralytics import YOLO

# ------------------------------------------------------------
# 1. Settings
# ------------------------------------------------------------
camera_index = 0
allowed_labels = {"person"}

# Start here — students will tune this live for their room
confidence_threshold = 0.50

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

print(f"Starting threshold: {confidence_threshold:.2f}")
print("Press + / - to change threshold. Press Q to quit.")

# ------------------------------------------------------------
# 3. Live loop with confidence filtering
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
    shown = 0
    rejected = 0

    if boxes is not None:
        for box in boxes:
            label = names[int(box.cls[0])]
            confidence = float(box.conf[0])

            if label not in allowed_labels:
                continue

            # --- NEW IDEA: confidence must clear the threshold ---
            if confidence < confidence_threshold:
                rejected = rejected + 1
                continue

            shown = shown + 1
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

    cv2.putText(
        display,
        f"threshold={confidence_threshold:.2f}  shown={shown}  rejected={rejected}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        text_color,
        2,
    )
    cv2.putText(
        display,
        "+/- change threshold   Q quit",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        text_color,
        2,
    )

    cv2.imshow("Program 14 - Confidence Threshold", display)

    key = cv2.waitKey(1) & 0xFF

    # Raise threshold (fewer, stricter detections)
    if key in (ord("+"), ord("=")):
        confidence_threshold = min(0.95, confidence_threshold + 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    # Lower threshold (more detections, including weaker ones)
    if key in (ord("-"), ord("_")):
        confidence_threshold = max(0.05, confidence_threshold - 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 4. Clean up
# ------------------------------------------------------------
camera.release()
cv2.destroyAllWindows()
print(f"Final threshold used: {confidence_threshold:.2f}")
print("Camera released. Done.")
print("Next: Program 15 counts how many allowed objects are visible.")

# ============================================================
# STUDENT CHALLENGE
# 1. Find the best threshold for YOUR room (write it in a comment).
# 2. What happens at 0.10 vs 0.80? Note one difference.
# 3. (Bonus) Flash the HUD text red when rejected > 0 this frame.
#
# EXPECTED RESULT
#  - Person boxes only when confidence >= threshold
#  - HUD shows threshold + shown/rejected counts
#  - + / - changes the cutoff live
#
# COMMON ERRORS
#  - + / - does nothing
#      → Click the VIDEO window first (not the terminal).
#  - Everything disappears at high threshold
#      → Expected if YOLO is unsure; lower the threshold a bit.
#  - Confusing "rejected" with wrong labels
#      → Rejected here means person detections that were too weak.
#
# INSTRUCTOR NOTE
#  Ask: "Would you rather miss a person, or false-alarm on a coat?"
#  That tradeoff is the heart of threshold tuning.
#  Counting comes next — keep decisions/alerts for Program 16.
# ============================================================
