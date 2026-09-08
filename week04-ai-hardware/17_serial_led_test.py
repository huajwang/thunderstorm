"""
============================================================
Program 17 — Talk to Hardware (Serial LED Test)
Course: Build Your First AI Computer Vision System
Week 4: AI + Physical Hardware
============================================================

PURPOSE
  Before connecting AI to hardware, prove the wire works:
  Python sends a message → Arduino turns an LED on or off.

LEARNING OBJECTIVE
  After this program, you should understand that:
  - Python can talk to Arduino over a USB serial port
  - a simple text command can control a physical LED
  - hardware testing should happen WITHOUT YOLO first

KEY CONCEPT
  Keyboard → Python → Serial command → Arduino → LED

WHAT CHANGED FROM THE PREVIOUS PROGRAM
  Program 16 decided ALERT / CLEAR on screen.
  Program 17 controls a REAL LED (no AI yet).

WHAT THE COMPUTER CAN DO NOW
  Turn an Arduino LED on and off with keypresses.

HOW TO RUN
  1. pip install pyserial   (or: pip install -r requirements.txt)
  2. Upload firmware/arduino_alarm/arduino_alarm.ino
  3. Close Arduino Serial Monitor
  4. Set serial_port below (example: "COM3" on Windows)
  5. From this folder, run:  python 17_serial_led_test.py
  6. Press O (on), F (off), Q (quit)

CONTROLS
  O — LED ON   (sends LED_ON)
  F — LED OFF  (sends LED_OFF)
  Q — quit
============================================================
"""

import cv2
import numpy as np

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("ERROR: pyserial is not installed.")
    print("Fix:  pip install pyserial")
    raise SystemExit(1)

# ------------------------------------------------------------
# 1. SETTINGS — change this to YOUR Arduino port
# ------------------------------------------------------------
# Windows examples: "COM3", "COM4"
# Mac examples: "/dev/cu.usbmodem1101"
# Linux examples: "/dev/ttyACM0"
serial_port = "COM6"
baud_rate = 9600

# ------------------------------------------------------------
# 2. Helper: list ports if connection fails
# ------------------------------------------------------------
def print_available_ports():
    ports = list(list_ports.comports())
    if not ports:
        print("  (No serial ports found. Is the Arduino plugged in?)")
        return
    print("Available serial ports:")
    for port in ports:
        print(f"  - {port.device}: {port.description}")


# ------------------------------------------------------------
# 3. Open serial connection to Arduino
# ------------------------------------------------------------
print(f"Opening serial port {serial_port} at {baud_rate} baud...")
try:
    board = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.SerialException as error:
    print(f"ERROR: Could not open {serial_port}")
    print(f"Details: {error}")
    print_available_ports()
    print("Edit serial_port near the top of this file, then try again.")
    raise SystemExit(1)

# Give Arduino a moment after the port opens (many boards reset on connect)
cv2.waitKey(2000)

print("Connected. Press O=LED on, F=LED off, Q=quit.")
print("Click the window first so keypresses are received.")

led_is_on = False

# ------------------------------------------------------------
# 4. Simple window for keyboard focus (no camera / no YOLO)
# ------------------------------------------------------------
while True:
    canvas = np.zeros((260, 520, 3), dtype=np.uint8)
    status = "LED: ON" if led_is_on else "LED: OFF"
    color = (0, 255, 0) if led_is_on else (0, 0, 255)

    cv2.putText(canvas, "SERIAL LED TEST", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(canvas, status, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.4, color, 3)
    cv2.putText(canvas, "O: on   F: off   Q: quit", (20, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    cv2.putText(canvas, f"port: {serial_port}", (20, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (160, 160, 160), 1)

    cv2.imshow("Program 17 - Serial LED Test", canvas)
    key = cv2.waitKey(30) & 0xFF

    if key == ord("o") or key == ord("O"):
        board.write(b"LED_ON\n")
        led_is_on = True
        print("Sent: LED_ON")

    if key == ord("f") or key == ord("F"):
        board.write(b"LED_OFF\n")
        led_is_on = False
        print("Sent: LED_OFF")

    if key == ord("q") or key == ord("Q"):
        print("Quit key pressed.")
        break

# ------------------------------------------------------------
# 5. Clean up
# ------------------------------------------------------------
board.write(b"LED_OFF\n")
board.close()
cv2.destroyAllWindows()
print("Serial port closed. Done.")
print("Next: Program 18 turns the LED on when AI sees a person.")

# ============================================================
# STUDENT CHALLENGE
# 1. Add key B that sends BUZZ_ON and key N that sends BUZZ_OFF
#    (needs buzzer wired to pin 9).
# 2. Add key Space that toggles the LED each time.
# 3. (Bonus) Blink pattern: key 1 sends ON/OFF/ON/OFF with waits.
#
# EXPECTED RESULT
#  - Window shows LED: ON / OFF
#  - Arduino LED lights when you press O
#  - Arduino LED turns off when you press F
#
# COMMON ERRORS
#  - Port busy / access denied
#      → Close Arduino Serial Monitor; unplug/replug USB.
#  - Wrong COM port
#      → Use the printed available ports list; edit serial_port.
#  - Nothing happens on the board
#      → Confirm the sketch uploaded; look for READY in Serial Monitor once, then close it.
#  - Keys do nothing
#      → Click the OpenCV window first.
#
# INSTRUCTOR NOTE
#  Do NOT add YOLO until Program 17 works for every station.
#  Separate "wire problems" from "AI problems" on purpose.
# ============================================================
