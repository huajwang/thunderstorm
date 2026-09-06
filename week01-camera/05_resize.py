"""
============================================================
Program 05 — Resize the Image
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Big images look nice — but they are slower to process.
  Later, AI detection will run faster on smaller frames.
  Today we learn how to SCALE an image.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - resize changes width and height in pixels
  - a scale factor like 0.5 means "half size"
  - smaller frames are useful when speed matters

KEY CONCEPT
  Full-size frame → resize → smaller frame

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 04 changed COLOR (to grayscale).
  Program 05 changes SIZE (width and height).

WHAT THE COMPUTER CAN DO NOW
  Show a live resized webcam view and print the new size.

HOW TO RUN
  1. From this folder, run:  python 05_resize.py
  2. Try different scale keys (see Controls)
  3. Press Q to quit

CONTROLS
  1 — show 100% size (original)
  2 — show 50% size
  3 — show 25% size
  Q — quit and close the camera cleanly
============================================================
"""

import cv2

# ------------------------------------------------------------
# 1. Open the webcam
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

# 1.0 = full size, 0.5 = half, 0.25 = quarter
scale = 0.5

print("Camera is open.")
print("Starting at 50% size. Press 1 / 2 / 3 to change. Press Q to quit.")

# ------------------------------------------------------------
# 2. Frame loop + resize
# ------------------------------------------------------------
while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    # Original size (before resize)
    original_height, original_width = frame.shape[:2]

    # New size = original size * scale
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Guard: OpenCV needs width and height of at least 1
    if new_width < 1:
        new_width = 1
    if new_height < 1:
        new_height = 1

    # Resize the frame for display / later processing
    display_frame = cv2.resize(frame, (new_width, new_height))

    cv2.imshow("Program 05 - Resize the Image", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("1"):
        scale = 1.0
        print(f"Scale: 100%  | camera {original_width}x{original_height} → display ~{int(original_width * scale)}x{int(original_height * scale)}")

    if key == ord("2"):
        scale = 0.5
        print(f"Scale: 50%  | camera {original_width}x{original_height} → display ~{int(original_width * scale)}x{int(original_height * scale)}")

    if key == ord("3"):
        scale = 0.25
        print(f"Scale: 25%  | camera {original_width}x{original_height} → display ~{int(original_width * scale)}x{int(original_height * scale)}")

    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 3. Clean up
# ------------------------------------------------------------
camera.release()
cv2.destroyAllWindows()
print("Camera released. Done.")

# ============================================================
# STUDENT CHALLENGE
# 1. Add a key 4 that sets scale = 0.10 (10% size).
# 2. Print the RESIZED size every 60 frames (reuse Program 02 idea).
# 3. (Bonus) Why might AI run faster on a smaller frame?
#    Write one sentence as a comment at the top of this file.
#
# EXPECTED RESULT
#  - Window opens smaller than full camera size (50% by default)
#  - Key 1 makes the window content larger (100%)
#  - Keys 2 and 3 make it smaller (50% / 25%)
#  - Terminal prints the chosen scale
#
# COMMON ERRORS
#  - Thinking the physical camera changed resolution
#      → Only the IMAGE we process/show changed size.
#  - Scale 0 or negative
#      → Width/height must stay positive integers.
#  - Comparing window chrome to image size
#      → Look at printed pixel sizes, not only window borders.
#
# INSTRUCTOR NOTE
#  Plant the Week 2/3 seed: "YOLO on a huge frame can feel laggy."
#  Emphasize: resize is a deliberate tradeoff (detail vs speed).
#  Do NOT introduce crop/ROI yet — that is Program 06.
# ============================================================
