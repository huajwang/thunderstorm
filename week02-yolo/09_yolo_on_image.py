"""
============================================================
Program 09 — AI Detects Objects in a Photo
Course: Build Your First AI Computer Vision System
Week 2: Object Detection with YOLO
============================================================

PURPOSE
  Week 1 taught YOU to process images.
  Week 2 introduces AI that can FIND objects in an image
  using a pretrained model called YOLO.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - a MODEL is a pretrained "brain" that already knows many objects
  - you do not train YOLO today — you RUN it
  - YOLO looks at a photo and reports what it thinks is there

KEY CONCEPT
  Image → YOLO model → detected objects

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 08 was a Snapshot Station (no AI).
  Program 09 runs AI object detection on a still image.

WHAT THE COMPUTER CAN DO NOW
  Load a photo, detect objects, show a labeled result window.

HOW TO RUN
  1. Install deps (if needed):  pip install -r ../requirements.txt
  2. From this folder, run:  python 09_yolo_on_image.py
  3. Wait for the model the first time (download may happen)
  4. View the result window, then press any key to close

CONTROLS
  Any key in the result window — close and exit
============================================================
"""

from pathlib import Path

import cv2
from ultralytics import YOLO

# ------------------------------------------------------------
# 1. Which photo should AI look at?
# ------------------------------------------------------------
# Default sample ships with the course (a busy street / bus scene).
# Challenge: point this at YOUR photo from Week 1, for example:
#   image_path = Path("../week01-camera/output/capture_01.jpg")
image_path = Path("../assets/images/bus.jpg")

if not image_path.exists():
    print(f"ERROR: Could not find image: {image_path}")
    print("Tips:")
    print("  - Check that assets/images/bus.jpg exists")
    print("  - Or change image_path to one of your Week 1 photos")
    raise SystemExit(1)

print(f"Loading image: {image_path.resolve()}")

# ------------------------------------------------------------
# 2. Load the pretrained YOLO model (YOLOv8n = "nano" = small/fast)
# ------------------------------------------------------------
# The first run may download yolov8n.pt automatically.
print("Loading YOLO model (yolov8n)... first run may download the model.")
model = YOLO("yolov8n.pt")

# ------------------------------------------------------------
# 3. Run AI detection on the image
# ------------------------------------------------------------
# model(...) returns a results list. We used one image, so use results[0].
print("Running detection...")
results = model(str(image_path), verbose=False)
result = results[0]

# Print what YOLO found (names + how many)
names = result.names  # id → label, like 0:"person", 5:"bus"
boxes = result.boxes

if boxes is None or len(boxes) == 0:
    print("No objects detected. Try a different photo with clearer objects.")
else:
    print(f"Detected {len(boxes)} object(s):")
    for box in boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        label = names[class_id]
        print(f"  - {label:12s}  confidence={confidence:.2f}")

# ------------------------------------------------------------
# 4. Show an annotated image (YOLO can draw boxes for us)
# ------------------------------------------------------------
# result.plot() returns an image with boxes + labels already drawn.
annotated = result.plot()

cv2.imshow("Program 09 - YOLO on an Image", annotated)
print("Press any key in the image window to close...")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Done. Next: Program 10 will explain boxes, labels, and confidence.")

# ============================================================
# STUDENT CHALLENGE
# 1. Run again on a second photo (change image_path).
# 2. Run on one of YOUR Week 1 captures:
#      image_path = Path("../week01-camera/output/snapshot_01.jpg")
# 3. (Bonus) Which objects did YOLO miss? Which were wrong?
#    Write 2 sentences — AI is helpful, but not perfect.
#
# EXPECTED RESULT
#  - Terminal lists detected objects and confidence scores
#  - A window shows the photo with boxes and labels
#  - First run may pause while yolov8n.pt downloads
#
# COMMON ERRORS
#  - ModuleNotFoundError: ultralytics
#      → pip install ultralytics
#  - Image path not found
#      → Use a real path; start with ../assets/images/bus.jpg
#  - Very slow first launch
#      → Normal while the model downloads / loads once
#  - No detections on a selfie / blank wall
#      → Try bus.jpg or a photo with clear everyday objects
#
# INSTRUCTOR NOTE
#  Say: "We did not train this model — we borrowed a pretrained brain."
#  Keep boxes/confidence deep-dive for Program 10.
#  Privacy reminder: only use photos students consent to share.
# ============================================================
