"""
============================================================
Program 10 — Boxes, Labels, Confidence
Course: Build Your First AI Computer Vision System
Week 2: Object Detection with YOLO
============================================================

PURPOSE
  Program 09 showed YOLO results with a built-in plot helper.
  Now we unpack WHAT a detection really is — so you can draw
  it yourself (just like Program 07 overlays).

LEARNING OBJECTIVE
  After this program, you should understand that each detection has:
  - a BOUNDING BOX (where the object is)
  - a LABEL (what YOLO thinks it is)
  - a CONFIDENCE SCORE (how sure YOLO is, from 0.0 to 1.0)

KEY CONCEPT
  Detection = box + label + confidence

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 09 used result.plot() (automatic drawing).
  Program 10 reads the numbers and draws boxes/text manually.

WHAT THE COMPUTER CAN DO NOW
  Explain and draw each detection from the raw YOLO outputs.

HOW TO RUN
  1. From this folder, run:  python 10_boxes_labels_confidence.py
  2. Read the terminal list of detections
  3. View the window, then press any key to close

CONTROLS
  Any key in the result window — close and exit
============================================================
"""

from pathlib import Path

import cv2
from ultralytics import YOLO

# ------------------------------------------------------------
# 1. Load the image (same idea as Program 09)
# ------------------------------------------------------------
image_path = Path("../assets/images/bus.jpg")

if not image_path.exists():
    print(f"ERROR: Could not find image: {image_path}")
    print("Change image_path to a real photo, then try again.")
    raise SystemExit(1)

image = cv2.imread(str(image_path))
if image is None:
    print(f"ERROR: OpenCV could not read: {image_path}")
    raise SystemExit(1)

print(f"Loaded image: {image_path.resolve()}")

# ------------------------------------------------------------
# 2. Run YOLO
# ------------------------------------------------------------
print("Loading YOLO model (yolov8n)...")
model = YOLO("yolov8n.pt")
results = model(image, verbose=False)
result = results[0]
names = result.names
boxes = result.boxes

# Draw on a copy (Program 07 habit)
display = image.copy()

box_color = (0, 255, 0)       # green box (BGR)
text_color = (255, 255, 255)  # white text

print()
if boxes is None or len(boxes) == 0:
    print("No objects detected.")
else:
    print(f"Found {len(boxes)} detection(s). Each one has box + label + confidence:")
    print("-" * 60)

    for index, box in enumerate(boxes, start=1):
        # --- LABEL ---
        class_id = int(box.cls[0])
        label = names[class_id]

        # --- CONFIDENCE (0.0 = unsure, 1.0 = very sure) ---
        confidence = float(box.conf[0])

        # --- BOX corners in pixels: x1,y1 = top-left; x2,y2 = bottom-right ---
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        print(
            f"{index:2d}. label={label:12s}  "
            f"confidence={confidence:.2f}  "
            f"box=({x1},{y1})-({x2},{y2})"
        )

        # Draw the box (Program 07 skill)
        cv2.rectangle(display, (x1, y1), (x2, y2), box_color, 2)

        # Draw label + confidence above the box
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

print("-" * 60)
print("Tip: confidence closer to 1.00 means YOLO is more sure.")

cv2.imshow("Program 10 - Boxes, Labels, Confidence", display)
print("Press any key in the image window to close...")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Done. Next: Program 11 runs YOLO on your live camera.")

# ============================================================
# STUDENT CHALLENGE
# 1. Only DRAW detections with confidence >= 0.50
#    (still PRINT every detection — compare what gets skipped).
# 2. Change box_color to red (0, 0, 255).
# 3. (Bonus) Count how many detections are "person".
#
# EXPECTED RESULT
#  - Terminal prints label, confidence, and box corners for each find
#  - Window shows manually drawn green boxes + captions
#  - You can match each terminal line to a box on screen
#
# COMMON ERRORS
#  - Forgetting int(...) on box coordinates
#      → OpenCV rectangle needs whole-number pixel positions.
#  - Confusing confidence with a percentage
#      → 0.87 means "pretty sure," not 87 as a separate unit.
#  - Text drawn off-screen near the top edge
#      → This program moves text below the top if y1 is too small.
#
# INSTRUCTOR NOTE
#  Ask: "If confidence is 0.20, should a security alarm trust it?"
#  Plant the seed for Program 14 (thresholds) and security filtering.
#  Do NOT go live-camera yet — that is Program 11.
# ============================================================
