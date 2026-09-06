# Demo Day Checklist

## Before you present

- [ ] Program runs without errors on your computer
- [ ] Camera permission / index is correct
- [ ] If using Arduino: sketch uploaded, correct COM port, Serial Monitor closed
- [ ] You know your **A** (arm) / **D** (disarm) / **Q** (quit) keys
- [ ] Lighting is good enough for YOLO to see your target object
- [ ] You can point to the line(s) you changed in SETTINGS

## During the demo (in order)

- [ ] 1. Show the live camera view
- [ ] 2. Show AI boxes / labels
- [ ] 3. Show the decision (ALERT / CLEAR or your custom text)
- [ ] 4. Show the action (LED/buzzer or on-screen mode)
- [ ] 5. Say what YOU changed (labels, title, ROI, threshold, etc.)

## Backup plan

- [ ] If Arduino fails: set `use_arduino = False` and demo on-screen decision only
- [ ] If YOLO is slow: enable half-size / lower resolution in settings if you added it
- [ ] If detections fail: lower `confidence_threshold` slightly
