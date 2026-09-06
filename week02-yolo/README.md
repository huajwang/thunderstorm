# Week 2 — Object Detection with YOLO

**Big idea:** A pretrained AI model can look at an image and find objects — boxes, labels, and confidence scores — without you writing rules for every object.

**This week’s pipeline:**

```text
Image → YOLO → objects
Camera → YOLO → live objects
Filter → person-only (security story)
```

## Setup (once)

```bash
pip install -r requirements.txt
```

The first YOLO run may download `yolov8n.pt` (small pretrained model). That can take a minute.

## Programs

| # | File | What you learn |
|---|------|----------------|
| 09 | `09_yolo_on_image.py` | AI detects objects in a still photo |
| 10 | `10_boxes_labels_confidence.py` | Boxes, labels, and confidence scores |
| 11 | `11_yolo_on_camera.py` | Live camera + YOLO |
| 12 | `12_detect_person_only.py` | Keep only people (security filter) |

**Week 2 complete** when Program 12 works and students can explain:

> A pretrained model finds objects. Each detection has a box, label, and confidence. Our program can filter labels to build a person detector.

**Ready now:** Programs 09–12 (all of Week 2).
