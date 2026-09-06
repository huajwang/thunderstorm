"""
============================================================
Program 03 — Save a Photo
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Live video disappears when you quit. Sometimes you want to
  KEEP one moment — a snapshot saved as an image file.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - a frame in memory can be written to disk as a photo
  - a keyboard key can trigger an action (not only quit)
  - image files (like .jpg) store what the camera saw

KEY CONCEPT
  Frame in memory → save → photo file on disk

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 02 counted frames as they passed by.
  Program 03 lets you FREEZE one frame by saving it.

WHAT THE COMPUTER CAN DO NOW
  Press a key to capture and save a webcam photo.

HOW TO RUN
  1. From this folder, run:  python 03_capture_photo.py
  2. Pose in front of the camera
  3. Press S to save a photo into the output folder
  4. Press Q to quit

CONTROLS
  S — save the current frame as a .jpg photo
  Q — quit and close the camera cleanly
============================================================
"""

import os

import cv2

# ------------------------------------------------------------
# 1. Where should saved photos go?
# ------------------------------------------------------------
# os.path.join works on Windows, Mac, and Linux.
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Filename pieces — change these in the student challenge!
filename_prefix = "capture"
photo_number = 1

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
print(f"Photos will be saved in: {os.path.abspath(output_folder)}")
print("Press S to save a photo. Press Q to quit.")

# ------------------------------------------------------------
# 3. Frame loop + save on keypress
# ------------------------------------------------------------
while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    cv2.imshow("Program 03 - Save a Photo", frame)

    key = cv2.waitKey(1) & 0xFF

    # Save the CURRENT frame when the student presses S
    if key == ord("s") or key == ord("S"):
        # Example name: output/capture_01.jpg, capture_02.jpg, ...
        filename = f"{filename_prefix}_{photo_number:02d}.jpg"
        filepath = os.path.join(output_folder, filename)

        # cv2.imwrite writes the image data to a file
        saved = cv2.imwrite(filepath, frame)

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
print(f"Open the '{output_folder}' folder to see your photos.")

# ============================================================
# STUDENT CHALLENGE
# 1. Change filename_prefix from "capture" to your name.
# 2. Change output_folder to "my_photos".
# 3. (Bonus) Also save when the student presses SPACE
#    (space bar key code is 32:  if key == 32:).
#
# EXPECTED RESULT
#  - Live video window
#  - Pressing S creates a .jpg file in the output folder
#  - Terminal prints the saved filepath
#  - Each new save uses a higher number (01, 02, 03, ...)
#
# COMMON ERRORS
#  - Pressing S in the terminal instead of the video window
#      → Click the video window first.
#  - Looking for photos in the wrong folder
#      → Check the absolute path printed when the program starts.
#  - Photo looks black / wrong
#      → Wait a second after opening so the camera can adjust.
#
# INSTRUCTOR NOTE
#  Show students the output folder in File Explorer / Finder.
#  Connect to the final project: security systems SAVE evidence.
#  Keep overlays / on-screen "Saved!" text for Program 07+.
#  Do NOT introduce grayscale yet — that is Program 04.
# ============================================================
