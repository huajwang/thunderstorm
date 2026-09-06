"""
============================================================
Program 11 — Live Camera + YOLO
Course: Build Your First AI Computer Vision System
Week 2: Object Detection with YOLO
============================================================

PURPOSE
  Still photos were Step 1. Now AI watches LIVE video —
  detecting objects on every new camera frame.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - the Week 1 camera loop and Week 2 YOLO can work together
  - YOLO runs once per frame (over and over)
  - live detection is the same idea as photo detection, just continuous

KEY CONCEPT
  Camera frame → YOLO → live boxes + labels

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 10 explained detections on one still image.
  Program 11 runs that idea on your webcam in real time.

WHAT THE COMPUTER CAN DO NOW
  Open the webcam and draw YOLO detections live.

HOW TO RUN
  1. From this folder, run:  python 11_yolo_on_camera.py
  2. Point the camera at people / objects / a busy desk
  3. Press Q to quit

CONTROLS
  Q — quit and close the camera cleanly
============================================================
"""

import cv2
from ultralytics import YOLO

# ------------------------------------------------------------
# 1. Open the webcam (Week 1 skill)
# ------------------------------------------------------------
camera_index = 0
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    print("Tips:")
    print("  - Close Zoom/Teams if they are using the webcam")
    print("  - Try camera_index = 1")
    raise SystemExit(1)

# ------------------------------------------------------------
# 2. Load YOLO once (do NOT reload inside the loop!)
# ------------------------------------------------------------
print("Loading YOLO model (yolov8n)...")
model = YOLO("yolov8n.pt")

box_color = (0, 255, 0)
text_color = (255, 255, 255)

print("Camera + YOLO ready. Press Q in the video window to quit.")
print("Tip: good lighting helps detection.")

# ------------------------------------------------------------
# 3. Live loop: read frame → detect → draw → show
# ------------------------------------------------------------
while True:
    success, frame = camera.read()
    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    # Run YOLO on this frame (one AI pass per loop)
    results = model(frame, verbose=False)
    result = results[0]
    names = result.names
    boxes = result.boxes

    display = frame.copy()

    if boxes is not None:
        for box in boxes:
            class_id = int(box.cls[0])
            label = names[class_id]
            confidence = float(box.conf[0])
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

    cv2.putText(
        display,
        "LIVE YOLO  |  Q: quit",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        text_color,
        2,
    )

    cv2.imshow("Program 11 - Live Camera + YOLO", display)

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
print("Next: Program 12 filters detections to people only (security mode).")

# ============================================================
# STUDENT CHALLENGE
# 1. Speed boost: resize the frame BEFORE YOLO, then draw on
#    the small frame (Program 05 skill), for example:
#      small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
#      results = model(small, verbose=False)
# 2. Change the HUD title to include your name.
# 3. (Bonus) Print how many objects were found every 30 frames
#    (Program 02 counting skill).
#
# EXPECTED RESULT
#  - Live webcam window with boxes/labels updating as you move
#  - HUD text: LIVE YOLO
#  - Q quits and releases the camera
#
# COMMON ERRORS
#  - Loading YOLO inside the while loop
#      → Extremely slow / may re-download. Load ONCE before the loop.
#  - Video feels laggy
#      → Normal on some laptops; try the 50% resize challenge.
#  - Few detections
#      → Add light, step back, include clear everyday objects.
#
# INSTRUCTOR NOTE
#  Celebrate: "The camera loop + AI are now one system."
#  If machines are slow, do the resize challenge as a class demo.
#  Privacy: students should not film others without permission.
#  Person-only filtering is Program 12 — keep all classes for now.
# ============================================================
