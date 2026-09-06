"""
============================================================
Program 01 — Open the Camera
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Your computer vision journey starts with one skill:
  get a live picture from the webcam into Python.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - a webcam is an INPUT device for your program
  - OpenCV can open the camera and show a window
  - you must release the camera when you are done

KEY CONCEPT
  Camera → Python → Window on screen

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  This is the first program. Nothing came before it.

WHAT THE COMPUTER CAN DO NOW
  Open your webcam and show live video until you quit.

HOW TO RUN
  1. Install OpenCV once:  pip install opencv-python
  2. Plug in / enable your webcam
  3. From this folder, run:  python 01_open_camera.py
  4. Look at the window, then press Q to quit

CONTROLS
  Q — quit and close the camera cleanly
============================================================
"""

import cv2

# ------------------------------------------------------------
# 1. Open the webcam
# ------------------------------------------------------------
# Camera index 0 usually means "the default webcam".
# If you have more than one camera, try 1 or 2 later.
camera_index = 0
camera = cv2.VideoCapture(camera_index)

# Always check: did the camera actually open?
if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    print("Tips:")
    print("  - Is another app already using the webcam?")
    print("  - Try changing camera_index from 0 to 1.")
    print("  - On a laptop, check that the camera privacy switch is on.")
    raise SystemExit(1)

print("Camera is open. Press Q in the video window to quit.")

# ------------------------------------------------------------
# 2. Keep showing live video until the student presses Q
# ------------------------------------------------------------
# We need a loop so the window updates again and again.
# Next program (02) will zoom in on what a "frame" really is.
while True:
    # Read one image from the camera.
    # success is True if we got an image.
    # frame is the image itself (a big grid of color values).
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    # Show the image in a window titled "Program 01 - Open Camera"
    cv2.imshow("Program 01 - Open Camera", frame)

    # waitKey(1) waits 1 millisecond for a key press.
    # We convert to a letter with chr(...) so we can check for "q".
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 3. Clean up (very important!)
# ------------------------------------------------------------
# If you forget this, the camera may stay "busy"
# and the next program will fail to open it.
camera.release()
cv2.destroyAllWindows()
print("Camera released. Done.")

# ============================================================
# STUDENT CHALLENGE
# 1. Change the window title to include your name.
# 2. If camera_index = 0 does not work, try 1.
# 3. (Bonus) Print a friendly welcome message before the loop.
#
# EXPECTED RESULT
#  - A window appears showing live video from your webcam.
#  - When you move, the video moves.
#  - Pressing Q closes the window and prints a goodbye message.
#
# COMMON ERRORS
#  - "Could not open the camera"
#      → Camera in use by Zoom/Teams, wrong index, or permission off.
#  - Window opens then instantly closes
#      → The loop broke because read() failed; check the camera.
#  - Pressing Q in the terminal does nothing
#      → Click the VIDEO WINDOW first, then press Q.
#
# INSTRUCTOR NOTE
#  Celebrate the first win: "The computer can see you."
#  Emphasize INPUT (camera) → OUTPUT (window).
#  Mention cleanup now so students never skip camera.release().
#  Do NOT introduce frames theory yet — that is Program 02.
# ============================================================
