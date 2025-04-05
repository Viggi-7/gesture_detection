import subprocess
import time
import cv2
import mediapipe as mp
import pyautogui
import os

# Step 1: Launch Notepad
blpath = r"C:\Users\vigna\OneDrive\Desktop\SubwaySurf.lnk"
subprocess.Popen(blpath, shell=True)
print("Notepad opened. Starting webcam and gesture detection...")

# Optional delay (in case system needs to load Notepad first)
time.sleep(2)

# Step 2: Initialize MediaPipe and webcam
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
gesture_cooldown = 1  # in seconds
last_gesture_time = time.time()
SWIPE_THRESHOLD = 40  # pixel difference to detect gesture

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Webcam started. Swipe your hand to send arrow keys.")
print("Press ESC to exit.")

# Step 3: Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get coordinates of index finger tip
            x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            y = int(hand_landmarks.landmark[8].y * frame.shape[0])

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            dx = x - prev_x
            dy = y - prev_y
            current_time = time.time()

            if current_time - last_gesture_time > gesture_cooldown:
                if abs(dx) > SWIPE_THRESHOLD:
                    if dx > 0:
                        pyautogui.press('right')
                        print("Swipe Right")
                    else:
                        pyautogui.press('left')
                        print("Swipe Left")
                    last_gesture_time = current_time
                elif abs(dy) > SWIPE_THRESHOLD:
                    if dy < 0:
                        pyautogui.press('up')
                        print("Swipe Up")
                    else:
                        pyautogui.press('down')
                        print("Swipe Down")
                    last_gesture_time = current_time

            prev_x, prev_y = x, y

    cv2.imshow("Hand Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

# Step 4: Clean up
cap.release()
cv2.destroyAllWindows()
print("Webcam closed. Exiting...")

# Optional: Close Notepad automatically
os.system("taskkill /im notepad.exe /f")
print("Notepad closed.")
