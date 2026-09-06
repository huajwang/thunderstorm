"""
============================================================
Program 04 — Grayscale Vision
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Until now we only DISPLAYED camera frames.
  Now we PROCESS them — change the image data itself.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - a frame is data you can transform
  - grayscale removes color and keeps brightness
  - OpenCV can convert color frames with one function call

KEY CONCEPT
  Color frame → convert → grayscale frame

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 03 saved frames to disk.
  Program 04 changes how a frame LOOKS (color → gray).

WHAT THE COMPUTER CAN DO NOW
  Show a live grayscale view of the webcam (and toggle back).

HOW TO RUN
  1. From this folder, run:  python 04_grayscale.py
  2. Press G to toggle grayscale on/off
  3. Press Q to quit

CONTROLS
  G — toggle grayscale mode
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

# Start in grayscale mode so the NEW idea is obvious immediately
use_grayscale = True

print("Camera is open.")
print("Grayscale is ON. Press G to toggle. Press Q to quit.")

# ------------------------------------------------------------
# 2. Frame loop + optional grayscale conversion
# ------------------------------------------------------------
while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    # Decide what to SHOW this time through the loop
    if use_grayscale:
        # BGR = Blue, Green, Red (OpenCV's usual color order)
        # GRAY = one brightness value per pixel (no color)
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        display_frame = frame

    cv2.imshow("Program 04 - Grayscale Vision", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("g") or key == ord("G"):
        use_grayscale = not use_grayscale
        mode = "ON" if use_grayscale else "OFF"
        print(f"Grayscale: {mode}")

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
# 1. Start with use_grayscale = False instead of True.
# 2. Save a grayscale photo when you press S
#    (hint: reuse cv2.imwrite from Program 03 on display_frame).
# 3. (Bonus) Print frame.shape for color vs gray.
#    Gray frames have 2 numbers (height, width).
#    Color frames have 3 (height, width, channels).
#
# EXPECTED RESULT
#  - Window opens in grayscale (black / white / gray tones)
#  - Pressing G switches between gray and full color
#  - Terminal prints Grayscale: ON / OFF when you toggle
#
# COMMON ERRORS
#  - Expecting "gray" to look like a filter app with fancy looks
#      → True grayscale is only brightness — that is the point.
#  - Forgetting that the ORIGINAL frame is still in `frame`
#      → We convert a copy for display; the camera frame stays color.
#  - Trying to draw colored text on a gray image later
#      → Gray images have no color channels (we will handle this later).
#
# INSTRUCTOR NOTE
#  Say out loud: "We did not get a new camera — we CHANGED the data."
#  This is the bridge to all later vision: process each frame.
#  Mention briefly: many classic CV steps start from gray.
#  Do NOT introduce resize yet — that is Program 05.
# ============================================================
