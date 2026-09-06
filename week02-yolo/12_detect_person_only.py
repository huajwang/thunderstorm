"""
============================================================
Program 12 — Filter: Person Detector
Course: Build Your First AI Computer Vision System
Week 2: Object Detection with YOLO
============================================================

PURPOSE
  A security system usually does not care about every object.
  It cares about PEOPLE (or pets, cars, bottles — your choice).
  Today we FILTER detections to keep only what matters.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - YOLO can detect many classes, but your app can ignore most
  - filtering by LABEL turns generic AI into a focused tool
  - this is the start of the "smart security" story

KEY CONCEPT
  Many detections → keep only allowed labels → person detector

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 11 drew EVERY class YOLO found.
  Program 12 draws only labels in an allow-list (default: person).

WHAT THE COMPUTER CAN DO NOW
  Live webcam detection focused on people (security mode).

HOW TO RUN
  1. From this folder, run:  python 12_detect_person_only.py
  2. Stand in view — you should get a box; chairs/bottles should not
  3. Press Q to quit

CONTROLS
  Q — quit and close the camera cleanly
============================================================
"""

import cv2
from ultralytics import YOLO

# ------------------------------------------------------------
# 1. Which labels should we KEEP?
# ------------------------------------------------------------
# YOLO knows many COCO classes (person, dog, cat, bottle, ...).
# Security starter mode: people only.
allowed_labels = {"person"}

# Student challenge idea (pet mode):
# allowed_labels = {"person", "dog", "cat"}

# ------------------------------------------------------------
# 2. Open camera + load YOLO once
# ------------------------------------------------------------
camera_index = 0
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    print("Tips:")
    print("  - Close Zoom/Teams if they are using the webcam")
    print("  - Try camera_index = 1")
    raise SystemExit(1)

print("Loading YOLO model (yolov8n)...")
model = YOLO("yolov8n.pt")

box_color = (0, 255, 0)
text_color = (255, 255, 255)

print(f"Allowed labels: {sorted(allowed_labels)}")
print("Person detector ready. Press Q to quit.")

# ------------------------------------------------------------
# 3. Live loop with filtering
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
    kept = 0
    skipped = 0

    if boxes is not None:
        for box in boxes:
            class_id = int(box.cls[0])
            label = names[class_id]
            confidence = float(box.conf[0])

            # --- THIS IS THE NEW IDEA: filter by label ---
            if label not in allowed_labels:
                skipped = skipped + 1
                continue

            kept = kept + 1
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(display, (x1, y1), (x2, y2), box_color, 2)
            caption = f"{label} {confidence:.2f}"
            text_y = y1 - 10 if y1 > 20 else y1 + 20
            cv2.putText(
                display,
                caption,
                (x1, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                text_color,
                2,
            )

    status = f"PERSON FILTER  |  shown={kept}  ignored={skipped}  |  Q: quit"
    cv2.putText(
        display,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        text_color,
        2,
    )

    cv2.imshow("Program 12 - Person Detector", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 4. Clean up
# ------------------------------------------------------------
camera.release()
cv2.destroyAllWindows()
print("Camera released. Done.")
print("Week 2 complete — AI can find people in live video.")
print("Next week: FPS, thresholds, counting, and ALERT decisions.")

# ============================================================
# STUDENT CHALLENGE
# 1. Pet mode: allow dog and cat too
#      allowed_labels = {"person", "dog", "cat"}
# 2. Classroom monitor mode: try {"person", "book", "laptop"}
# 3. (Bonus) Change the HUD title based on your mode name.
#
# EXPECTED RESULT
#  - People get boxes; most other objects are ignored
#  - HUD shows how many detections were shown vs ignored
#  - Q quits cleanly
#
# COMMON ERRORS
#  - Typo in label ("Person" vs "person")
#      → YOLO labels are lowercase (person, dog, cat).
#  - Empty boxes when a person is clearly visible
#      → Lighting / distance; or confidence is low (Week 3 topic).
#  - Thinking filtering changes the model
#      → The model still sees everything; YOUR code chooses what to keep.
#
# INSTRUCTOR NOTE
#  Exit ticket: "AI detects many things; our app decides what matters."
#  Connect to final project: change allowed_labels = project theme.
#  Ethics: do not use person detection to secretly monitor classmates.
# ============================================================
