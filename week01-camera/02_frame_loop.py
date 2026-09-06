"""
============================================================
Program 02 — Video Is Frames
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Live video looks smooth — but the computer does not see
  "video." It sees one still image at a time, over and over.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - a VIDEO is a sequence of still images called FRAMES
  - each time the loop runs, we read ONE new frame
  - counting frames proves the loop is really happening

KEY CONCEPT
  Video = Frame + Frame + Frame + Frame + ...

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 01 opened the camera and showed live video.
  Program 02 makes the hidden loop visible by COUNTING frames.

WHAT THE COMPUTER CAN DO NOW
  Track how many frames it has seen, and report frame size.

HOW TO RUN
  1. From this folder, run:  python 02_frame_loop.py
  2. Watch the video window AND the terminal
  3. Press Q to quit and see the total frame count

CONTROLS
  Q — quit and close the camera cleanly
============================================================
"""

import cv2

# ------------------------------------------------------------
# 1. Open the webcam (same idea as Program 01)
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
print("Each loop reads ONE frame. Watch the frame count in this terminal.")
print("Press Q in the video window to quit.")

# ------------------------------------------------------------
# 2. Count frames so students can "see" the loop
# ------------------------------------------------------------
frame_count = 0
printed_size = False

while True:
    # ONE trip through this loop = ONE frame from the camera
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    frame_count = frame_count + 1

    # The first time we get a frame, print its size once.
    # frame.shape is (height, width, color_channels)
    if not printed_size:
        height, width, channels = frame.shape
        print(f"Frame size: {width} x {height} pixels  (channels: {channels})")
        printed_size = True

    # Print progress every 30 frames so the terminal is not flooded.
    # This is proof: the loop is running again and again.
    if frame_count % 30 == 0:
        print(f"Frames so far: {frame_count}")

    cv2.imshow("Program 02 - Video Is Frames", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 3. Clean up
# ------------------------------------------------------------
camera.release()
cv2.destroyAllWindows()
print(f"Total frames shown: {frame_count}")
print("Camera released. Done.")

# ============================================================
# STUDENT CHALLENGE
# 1. Change 30 to 10 so the count prints more often.
# 2. Print the width and height on EVERY frame (warning: spam!).
# 3. (Bonus) Guess: about how many frames appear in 1 second?
#    Quit after watching the clock, then divide total frames by seconds.
#
# EXPECTED RESULT
#  - Live video window (same idea as Program 01)
#  - Terminal prints frame size once
#  - Terminal prints "Frames so far: 30", "60", ... while running
#  - On quit, terminal prints the total frame count
#
# COMMON ERRORS
#  - Watching only the window and missing the terminal output
#      → Place the terminal where you can see both.
#  - Thinking "video" is one special object
#      → Reminder: video is just frames in a loop.
#  - Forgetting camera.release()
#      → Next program may fail to open the camera.
#
# INSTRUCTOR NOTE
#  Ask: "If we stop the loop, what happens to the video?"
#  Answer: It freezes — because new frames stop arriving.
#  Plant the seed for later AI: YOLO will also run ON EACH FRAME.
#  Do NOT introduce saving photos yet — that is Program 03.
# ============================================================
