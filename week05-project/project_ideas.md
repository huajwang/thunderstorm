# Project Ideas (Week 5)

Start from Program 20. Change **labels**, **ROI**, **messages**, and **hardware behavior**.

| Project | Change `allowed_labels` to… | Extra twist |
|---------|-----------------------------|-------------|
| AI Smart Security System | `{"person"}` | Armed mode + alarm (default starter) |
| AI Visitor Detector | `{"person"}` | Save a snapshot for every new visitor alert |
| AI Pet Detector | `{"dog", "cat"}` | Different HUD text: "PET DETECTED" |
| AI Object Counter | `{"bottle"}` or `{"cup"}` | Show count big; optional LED if count >= 1 |
| AI Classroom Monitor | `{"person", "book", "laptop"}` | Count people only; ignore other classes for alarm |
| AI Recycling Detector | `{"bottle"}` | Alert when a bottle appears in the ROI |
| AI Parking / Entry Detector | `{"car", "person"}` | Watch a driveway ROI |

## Tips

- Change **one setting at a time**, then test.
- If hardware is unavailable, set `use_arduino = False` and demo on-screen only.
- Write 3 sentences: what you changed, why, and what the system does now.
