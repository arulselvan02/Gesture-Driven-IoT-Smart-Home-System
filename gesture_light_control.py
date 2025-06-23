import cv2
import mediapipe as mp
import time
import serial
import threading
import tkinter as tk
from tkinter import messagebox

# ===== Serial Communication =====
ser = serial.Serial('COM7', 9600, timeout=1)  # Change 'COM7' to your port

# ===== MediaPipe Setup =====
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# ===== Global States =====
last_action_time = 0
action_delay = 5  # seconds

def count_fingers(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    finger_states = []

    # Thumb
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        finger_states.append(1)
    else:
        finger_states.append(0)


    # Other fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
            finger_states.append(1)
        else:
            finger_states.append(0)

    return sum(finger_states)

def send_command(cmd):
    if cmd in ['1', '2', '3', '4', '5']:
        ser.write(cmd.encode())
        print(f"Sent: {cmd}")

def read_serial():
    while ser.in_waiting > 0:
        msg = ser.readline().decode().strip()
        print("From NodeMCU:", msg)

# ===== GUI =====
def create_gui():
    root = tk.Tk()
    root.title("Light Control Panel")

    tk.Label(root, text="Manual Light Controls", font=("Arial", 14)).pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack()

    def make_toggle_button(light_num):
        def toggle():
            send_command(str(light_num))
        return toggle

    for i in range(1, 5):
        btn = tk.Button(btn_frame, text=f"Toggle Light {i}", width=20,
                        command=make_toggle_button(i))
        btn.grid(row=(i-1)//2, column=(i-1)%2, padx=10, pady=5)

    tk.Button(root, text="Toggle ALL Lights", command=lambda: send_command('5')).pack(pady=10)

    tk.Button(root, text="Exit", command=root.destroy).pack()

    root.mainloop()

# ===== Gesture Thread =====
def gesture_control():
    global last_action_time
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        read_serial()
        now = time.time()

        cv2.putText(frame, "Gesture Control Active", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
                count = count_fingers(lm)
                cv2.putText(frame, f"Fingers: {count}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

                if now - last_action_time > action_delay and 1 <= count <= 5:
                    send_command(str(count))
                    last_action_time = now

        cv2.imshow("Gesture Window", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

# ===== Main Execution =====
# Run gesture and GUI in parallel threads
threading.Thread(target=gesture_control, daemon=True).start()
create_gui()
