"""
============================================================
Program 06 — Crop a Region (ROI)
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Security cameras often care about ONE place — a doorway,
  a desk, or a parking entrance — not the whole room.
  That focused area is called a Region of Interest (ROI).

LEARNING OBJECTIVE
  After this program, you should understand that:
  - every pixel has coordinates (x across, y down)
  - (0, 0) is the TOP-LEFT corner of the image
  - cropping keeps only a rectangle of the frame

KEY CONCEPT
  Full frame → crop ROI → smaller focused image

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 05 scaled the WHOLE image.
  Program 06 keeps only PART of the image (a rectangle).

WHAT THE COMPUTER CAN DO NOW
  Show the full camera view AND a cropped "doorway" zone.

HOW TO RUN
  1. From this folder, run:  python 06_crop_roi.py
  2. Two windows open: full frame + ROI crop
  3. Edit the ROI numbers in the code to match your room
  4. Press Q to quit

CONTROLS
  Q — quit and close the camera cleanly
============================================================
"""

import cv2

# ------------------------------------------------------------
# 1. Define the Region of Interest (ROI)
# ------------------------------------------------------------
# These numbers are PIXEL coordinates in the full frame.
# Change them so the crop matches a real doorway / desk area.
#
#   x1 ----→ x2
#   |
#   y1
#   |
#   ↓
#   y2
#
# Remember: (0, 0) is the TOP-LEFT of the image.
roi_x1 = 200
roi_y1 = 100
roi_x2 = 440
roi_y2 = 360

# ------------------------------------------------------------
# 2. Open the webcam
# ------------------------------------------------------------
camera_index = 0
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    print("Tips:")
    print("  - Is another app already using the webcam?")
    print("  - Try changing camera_index from 0 to 1.")
    print("  - On a laptop, check that the camera privacy switch is on.")
    raise SystemExit(1)

print("Camera is open.")
print(f"ROI box: x={roi_x1}:{roi_x2}, y={roi_y1}:{roi_y2}")
print("Edit roi_x1, roi_y1, roi_x2, roi_y2 in the code to fit your room.")
print("Press Q in either video window to quit.")

printed_size = False

# ------------------------------------------------------------
# 3. Frame loop + crop
# ------------------------------------------------------------
while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    frame_height, frame_width = frame.shape[:2]

    if not printed_size:
        print(f"Full frame size: {frame_width} x {frame_height} pixels")
        printed_size = True

    # Keep ROI inside the image so slicing never crashes
    x1 = max(0, min(roi_x1, frame_width - 1))
    x2 = max(0, min(roi_x2, frame_width))
    y1 = max(0, min(roi_y1, frame_height - 1))
    y2 = max(0, min(roi_y2, frame_height))

    if x2 <= x1 or y2 <= y1:
        print("ERROR: ROI is invalid. Check that x2 > x1 and y2 > y1.")
        break

    # IMPORTANT OpenCV / NumPy crop order:
    #   frame[y1:y2, x1:x2]  →  rows first (y), then columns (x)
    roi = frame[y1:y2, x1:x2]

    cv2.imshow("Program 06 - Full Frame", frame)
    cv2.imshow("Program 06 - ROI Crop", roi)

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

# ============================================================
# STUDENT CHALLENGE
# 1. Change the ROI numbers so the crop shows a real doorway
#    (or your chair / a poster on the wall).
# 2. Make a "narrow hallway" ROI that is tall and thin.
# 3. (Bonus) Save ONLY the ROI when you press S
#    (hint: cv2.imwrite on the `roi` image, like Program 03).
#
# EXPECTED RESULT
#  - Window 1: full webcam view
#  - Window 2: only the cropped rectangle
#  - Terminal prints full frame size once
#  - Moving outside the ROI does not appear in the crop window
#
# COMMON ERRORS
#  - Mixing up x and y (crop looks wrong / empty)
#      → Remember: slice is [y1:y2, x1:x2], not [x, y].
#  - ROI numbers bigger than the camera frame
#      → Print frame size first, then pick numbers inside it.
#  - x2 smaller than x1 (or y2 < y1)
#      → The program stops with an "ROI is invalid" message.
#
# INSTRUCTOR NOTE
#  Walk to a doorway and say: "Later, AI can watch ONLY this zone."
#  Stress coordinate origin at TOP-LEFT (students often assume bottom-left).
#  Drawing a rectangle ON the full frame comes next in Program 07.
# ============================================================
