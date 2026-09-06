"""
============================================================
Program 07 — Draw Boxes & Text
Course: Build Your First AI Computer Vision System
Week 1: Camera + Computer Vision Fundamentals
============================================================

PURPOSE
  Real vision apps do not only process images — they ANNOTATE
  them. Labels and boxes tell humans (and later, AI results)
  what matters on screen.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - you can draw shapes and text ON TOP of a frame
  - a rectangle can mark an ROI on the full image
  - on-screen text is a simple HUD (heads-up display)

KEY CONCEPT
  Frame → draw overlay → annotated frame

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 06 cropped an ROI into a second window.
  Program 07 keeps ONE window and DRAWS the ROI box + title text.

WHAT THE COMPUTER CAN DO NOW
  Look like a basic security camera HUD (box + label).

HOW TO RUN
  1. From this folder, run:  python 07_draw_overlay.py
  2. Adjust ROI numbers to match your room
  3. Press Q to quit

CONTROLS
  Q — quit and close the camera cleanly
============================================================
"""

from datetime import datetime

import cv2

# ------------------------------------------------------------
# 1. ROI box (same idea as Program 06 — now we DRAW it)
# ------------------------------------------------------------
roi_x1 = 200
roi_y1 = 100
roi_x2 = 440
roi_y2 = 360

# OpenCV colors are BGR: (Blue, Green, Red) — not RGB!
box_color = (0, 255, 0)      # green box
text_color = (255, 255, 255)  # white text
title = "SECURITY CAM"

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
print("You should see a title and a green ROI rectangle.")
print("Press Q in the video window to quit.")

# ------------------------------------------------------------
# 3. Frame loop + draw overlay
# ------------------------------------------------------------
while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    # Draw on a copy so we never mix up "camera frame" vs "decorated frame"
    display = frame.copy()

    frame_height, frame_width = display.shape[:2]
    x1 = max(0, min(roi_x1, frame_width - 1))
    x2 = max(0, min(roi_x2, frame_width))
    y1 = max(0, min(roi_y1, frame_height - 1))
    y2 = max(0, min(roi_y2, frame_height))

    # rectangle(image, top-left corner, bottom-right corner, color, thickness)
    # thickness = 2 means a line 2 pixels thick
    cv2.rectangle(display, (x1, y1), (x2, y2), box_color, 2)

    # putText(image, text, bottom-left of text, font, scale, color, thickness)
    cv2.putText(
        display,
        title,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        text_color,
        2,
    )

    # Live clock — useful later for security evidence timestamps
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        display,
        timestamp,
        (20, frame_height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        text_color,
        2,
    )

    cv2.imshow("Program 07 - Draw Boxes & Text", display)

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
# 1. Change title to include your name (example: "MAYA SECURITY CAM").
# 2. Change box_color to blue (255, 0, 0) or red (0, 0, 255).
# 3. (Bonus) Add a second line of text: "ROI: DOORWAY"
#    somewhere near the rectangle.
#
# EXPECTED RESULT
#  - One live video window
#  - Green rectangle marking the ROI
#  - "SECURITY CAM" in the top-left
#  - Updating date/time near the bottom
#
# COMMON ERRORS
#  - Text looks tiny or huge
#      → Change the scale number (1.0 / 0.6) in putText.
#  - Wrong colors (wanted red, got blue)
#      → OpenCV uses BGR, not RGB.
#  - Drawing but not seeing changes
#      → Make sure you imshow(display), not the original frame.
#
# INSTRUCTOR NOTE
#  Say: "Week 2 AI will draw boxes like this — but AI chooses where."
#  Emphasize copy-then-draw so students do not mutate data by accident.
#  Mini-project next: combine overlay + save + earlier Week 1 skills.
# ============================================================
