"""
============================================================
Program 16 — AI Makes a Decision
Course: Build Your First AI Computer Vision System
Week 3: Real-Time AI Vision
============================================================

PURPOSE
  Drawing boxes is not the end goal.
  A smart system DECIDES: should we alert, or is everything clear?

LEARNING OBJECTIVE
  After this program, you should understand that:
  - AI output can drive an if/then decision
  - ALERT vs CLEAR is a simple rule you write in Python
  - this decision is what Week 4 will send to hardware

KEY CONCEPT
  Camera → YOLO → count → Decision (ALERT / CLEAR)

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 15 counted people.
  Program 16 uses that count to choose ALERT or ALL CLEAR.

WHAT THE COMPUTER CAN DO NOW
  Act like a basic on-screen security decision engine.

HOW TO RUN
  1. From this folder, run:  python 16_ai_decision_alert.py
  2. Step into view → ALERT; step out → ALL CLEAR
  3. Press Q to quit

CONTROLS
  + or = — raise confidence threshold
  - or _ — lower confidence threshold
  Q — quit and close the camera cleanly
============================================================
"""

import cv2
from ultralytics import YOLO

# ------------------------------------------------------------
# 1. Settings
# ------------------------------------------------------------
camera_index = 0
allowed_labels = {"person"}
confidence_threshold = 0.50

# Challenge idea: require a person for several frames in a row
# before ALERT (reduces flicker). Start at 1 = decide immediately.
frames_required_for_alert = 1

# ------------------------------------------------------------
# 2. Open camera + load YOLO once
# ------------------------------------------------------------
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print("ERROR: Could not open the camera.")
    print("Tips: close other camera apps, or try camera_index = 1")
    raise SystemExit(1)

print("Loading YOLO model (yolov8n)...")
model = YOLO("yolov8n.pt")

print("Decision engine ready. Press Q to quit.")

person_streak = 0  # how many frames in a row we have seen a person

# ------------------------------------------------------------
# 3. Live loop: detect → count → decide
# ------------------------------------------------------------
while True:
    success, frame = camera.read()
    if not success:
        print("ERROR: Could not read a frame from the camera.")
        break

    results = model(frame, verbose=False)
    result = results[0]
    names = result.names
    boxes = result.boxes

    display = frame.copy()
    people_count = 0

    if boxes is not None:
        for box in boxes:
            label = names[int(box.cls[0])]
            confidence = float(box.conf[0])

            if label not in allowed_labels:
                continue
            if confidence < confidence_threshold:
                continue

            people_count = people_count + 1

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                display,
                f"{label} {confidence:.2f}",
                (x1, y1 - 10 if y1 > 20 else y1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

    # Track consecutive frames with at least one person
    if people_count > 0:
        person_streak = person_streak + 1
    else:
        person_streak = 0

    # --- NEW IDEA: turn AI results into a DECISION ---
    if person_streak >= frames_required_for_alert:
        decision = "ALERT"
        decision_color = (0, 0, 255)  # red (BGR)
    else:
        decision = "ALL CLEAR"
        decision_color = (0, 200, 0)  # green

    # Soft background bar so the decision is easy to read
    cv2.rectangle(display, (0, 0), (display.shape[1], 110), (0, 0, 0), -1)
    cv2.putText(
        display,
        decision,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.6,
        decision_color,
        3,
    )
    cv2.putText(
        display,
        f"People: {people_count}   streak: {person_streak}/{frames_required_for_alert}   thr={confidence_threshold:.2f}",
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2,
    )

    cv2.imshow("Program 16 - AI Decision Alert", display)

    key = cv2.waitKey(1) & 0xFF

    if key in (ord("+"), ord("=")):
        confidence_threshold = min(0.95, confidence_threshold + 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    if key in (ord("-"), ord("_")):
        confidence_threshold = max(0.05, confidence_threshold - 0.05)
        print(f"Threshold → {confidence_threshold:.2f}")

    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed. Closing camera...")
        break

# ------------------------------------------------------------
# 4. Clean up
# ------------------------------------------------------------
camera.release()
cv2.destroyAllWindows()
print("Camera released. Done.")
print("Week 3 complete — your program can DECIDE.")
print("Next week: send that decision to Arduino (LED / buzzer).")

# ============================================================
# STUDENT CHALLENGE
# 1. Set frames_required_for_alert = 8 (or 10) to reduce flicker.
# 2. Change ALERT text to "INTRUDER" or "VISITOR DETECTED".
# 3. (Bonus) Beep in the terminal on ALERT using print("\a")
#    (may not beep on all computers).
#
# EXPECTED RESULT
#  - No person → green ALL CLEAR
#  - Person (for enough frames) → red ALERT
#  - HUD shows people count + streak progress
#
# COMMON ERRORS
#  - ALERT flickers on/off every frame
#      → Raise frames_required_for_alert.
#  - Never reaches ALERT with a high frames_required value
#      → Stand still in clear view; check threshold.
#  - Thinking the model "decides"
#      → YOLO detects; YOUR if/then decides.
#
# INSTRUCTOR NOTE
#  Exit ticket: "Detection is not the same as decision."
#  Preview Week 4: replace red text with LED/buzzer action.
#  Keep serial/hardware out of this file on purpose.
# ============================================================
