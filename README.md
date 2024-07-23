# PICO USB SWITCHBOX

# Introduction

This project programs a Raspberry Pi Pico to act as a USB input device. I use it with Microsoft Flight Simulator.

The hardware is a simple button box consisting of 4 buttons and 4 rotary encoders. There is also a potentiometer attached to an analog input which mimics a Cessna ignition key. The key has 5 positions which are Off, Right Magneto, Left Magneto, Both Magnetos and Start. The Start position is spring loaded so the key returns to the Both position once released.

To ensure no clicks get skipped on the rotary encoders I decided to map each encoder to a joystick axis. An absolute position is then sent depending on how much the encoder is rotated (positive or negative).

I used Edward Wright's excellent JoystickXL library for CircuitPython and added the mod to make the joystick values  16-bit instead of 8-bit. This means you can rotate the encoders many many times and won't reach the axis extremities.

# Instructions

1. Flash the Pico with the latest CircuitPython firmware
2. Add the files from this repo
3. Unplug and replug the Pico to pick up the new boot.py
4. Run Game Controllers (in Windows) to confirm the joystick inputs are working. Note that the axis inputs will be tiny when you rotate the encoders as it only adds or subtracts 1 for each click of the encoder.

# A table summarizing the inputs mentioned in the code and their corresponding pins

| Input Type | Pins on RPI PICO Board |
| ---------- | ----------------------------- |
| Rotary Encoder 1 | GP1, GP0 |
| Rotary Encoder 2 | GP4, GP5 |
| Rotary Encoder 3 | GP8, GP9 |
| Rotary Encoder 4 | GP13, GP12 |
| Button 1 (with Encoder) | GP15 |
| Button 2 (with Encoder) | GP3 |
| Button 3 (with Encoder) | GP7 |
| Button 4 (with Encoder) | GP11 |
| Button 5 | GP2 |
| Button 6 | GP10 |
| Button 7 | GP6 |
| Button 8 | GP14 |
| Analog Input (Potentiometer) | GP28 |
