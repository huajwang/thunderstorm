"""
============================================================
Program 15 — Count What AI Sees
Course: Build Your First AI Computer Vision System
Week 3: Real-Time AI Vision
============================================================

PURPOSE
  Detection boxes are useful. NUMBERS are powerful.
  Counting turns AI output into something a security system
  (or classroom monitor) can report: "People: 2".

LEARNING OBJECTIVE
  After this program, you should understand that:
  - you can count filtered detections each frame
  - a count is a simple summary of what AI sees right now
  - counts change as people enter or leave the view

KEY CONCEPT
  Filtered detections → count → show "People: N"

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 14 filtered by confidence.
  Program 15 keeps that filter and ADDS a live people count.

WHAT THE COMPUTER CAN DO NOW
  Show how many people are visible (above the threshold).

HOW TO RUN
  1. From this folder, run:  python 15_object_counter.py
  2. Walk in/out of view and watch the count change
  3. Press Q to quit

CONTROLS
  + or = — raise confidence threshold
  - or _ — lower confidence threshold
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

print("Object counter ready. Press Q to quit.")

# ------------------------------------------------------------
# 3. Live loop with counting
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

            # --- NEW IDEA: each kept detection adds 1 to the count ---
            people_count = people_count + 1

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

    # Big readable count — this is the new headline skill
    cv2.putText(
        display,
        f"People: {people_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.4,
        text_color,
        3,
    )
    cv2.putText(
        display,
        f"threshold={confidence_threshold:.2f}  |  +/- change  |  Q quit",
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        text_color,
        2,
    )

    cv2.imshow("Program 15 - Object Counter", display)

    key = cv2.waitKey(1) & 0xFF

    if key in (ord("+"), ord("=")):
        confidence_threshold = min(0.95, confidence_threshold + 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

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
print("Camera released. Done.")
print("Next: Program 16 turns the count into an ALERT / CLEAR decision.")

# ============================================================
# STUDENT CHALLENGE
# 1. Count ONLY inside an ROI (Program 06 + 07 skills):
#    - draw a doorway rectangle
#    - count a person only if the BOX CENTER is inside the ROI
#      center_x = (x1 + x2) // 2
#      center_y = (y1 + y2) // 2
# 2. Rename the HUD to "Visitors: N" for a visitor-counter project.
# 3. (Bonus) Print the count to the terminal whenever it changes.
#
# EXPECTED RESULT
#  - Live boxes for people above the threshold
#  - Large on-screen "People: N" that updates as people move
#  - +/- still adjusts the threshold
#
# COMMON ERRORS
#  - Count flickers between numbers
#      → Normal when YOLO is unsure near the edge of the frame.
#  - Count seems high (one person → 2 boxes)
#      → Raise threshold, improve lighting, or step farther back.
#  - Forgetting to reset people_count = 0 each frame
#      → Then the number would grow forever (this program resets).
#
# INSTRUCTOR NOTE
#  Emphasize: count is PER FRAME, not "total visitors today"
#  (true visitor totals need tracking — advanced / later challenge).
#  Decision logic is next: if people_count > 0 → ALERT.
# ============================================================
