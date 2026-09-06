# Week 4 — AI + Physical Hardware (Arduino)

**Big idea:** When AI decides ALERT, the real world can react — lights, buzzers, and more.

**This week’s pipeline:**

```text
Python decision → Serial message → Arduino → LED / buzzer
```

**Primary board:** Arduino Uno (or compatible).

## Setup

1. Install Python serial support:

```bash
pip install -r requirements.txt
```

2. Wire hardware (see `wiring/README.md`).
3. Upload the sketch in `firmware/arduino_alarm/` with the Arduino IDE.
4. Note your serial port (Windows example: `COM3`).
5. Run Program 17 and set `serial_port` in the Python file.

## Programs

| # | File | What you learn |
|---|------|----------------|
| 17 | `17_serial_led_test.py` | Python talks to Arduino; LED on/off |
| 18 | `18_ai_triggers_led.py` | Person detected → LED ON |
| 19 | `19_security_alarm.py` | Full alarm (LED + buzzer + armed) |

**Week 4 complete** when Program 19 works and students can explain:

> Armed + AI person detection → hardware alarm. Disarm stops it.

**Ready now:** Programs 17–19 (all of Week 4).

## Serial command list (plain text lines)

| Command | Meaning |
|---------|---------|
| `LED_ON` | Turn LED on |
| `LED_OFF` | Turn LED off |
| `BUZZ_ON` | Turn buzzer on |
| `BUZZ_OFF` | Turn buzzer off |
| `ALARM` | LED + buzzer alarm pattern |
| `DISARM` | Stop alarm / turn outputs off |
