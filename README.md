
# 💡 Gesture-Controlled Smart Light System

## 📌 Overview
This project is a smart home automation system that allows users to **control lights using hand gestures** and a **manual GUI interface**. It integrates computer vision, serial communication, and microcontroller-based hardware control to enhance accessibility and convenience.

## 🎯 Features
- **Gesture-Based Light Control** using a webcam and MediaPipe:
  - Raise fingers (1–5) to toggle individual or all lights.
- **Tkinter GUI** for manual control:
  - Toggle Light 1 to Light 4 or all lights with a button click.
- **Real-Time Feedback** via Serial Monitor:
  - The NodeMCU responds with light ON/OFF messages.
- **Multithreaded Execution**:
  - Simultaneously runs gesture detection and GUI control.

## 🛠️ Technologies Used
- **Python** (OpenCV, MediaPipe, Tkinter)
- **Arduino (ESP8266/NodeMCU)**
- **Serial Communication**
- **Multithreading**

## 🖥️ Software Components
- `gesture_light_control.py`:  
  Detects hand gestures using the webcam and controls lights through serial communication. Also provides a GUI for manual operation.

- `nodemcu_light_controller.ino`:  
  Receives serial commands and toggles GPIO pins connected to relays or LEDs for lights.

## 🔌 Hardware Requirements
- NodeMCU (ESP8266)
- 4-channel Relay module (or LEDs for testing)
- Jumper wires and breadboard
- Webcam
- PC with Python installed

## ⚙️ How It Works
1. The Python program captures the webcam feed.
2. MediaPipe processes the video and counts raised fingers.
3. Based on the finger count (1–5), a command is sent to the NodeMCU via serial.
4. NodeMCU toggles the respective light and sends feedback via serial.
5. Users can also use the GUI to manually control the lights.
