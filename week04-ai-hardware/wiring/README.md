# Week 4 Wiring (Arduino Uno)

## Minimum for Program 17 (easiest)

Use the **built-in LED on pin 13** — no extra parts required.

```text
Arduino Uno  →  built-in LED (pin 13)
USB cable    →  computer
```

## Recommended classroom kit (Programs 17–19)

| Part | Arduino pin | Notes |
|------|-------------|--------|
| External LED (+) | D8 | Use a ~220Ω resistor in series |
| External LED (−) | GND | |
| Active buzzer (+) | D9 | Passive buzzers are simplest for beginners |
| Active buzzer (−) | GND | |
| USB | computer | Powers board + serial link |

```text
        220Ω
   D8 ----/\/\----|>|---- GND     (external LED)
   D9 ---------------(((---- GND  (active buzzer)
```

The firmware drives **both** pin 13 (built-in) and pin 8 (external LED) together, so either setup works.

## Safety

- Never connect LED pins directly to 5V without a resistor.
- Disconnect USB before changing wires.
- Ask an instructor before using a passive piezo that needs tone code variants.
