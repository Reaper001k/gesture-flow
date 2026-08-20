import cv2
import mediapipe as mp
import pyautogui
import time
import math
import ctypes

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
last_act = 0

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time()

    if results.multi_hand_landmarks:
        fists = 0
        for handLms in results.multi_hand_landmarks:
            lms = handLms.landmark
            # 1. Screenshot (Thumb + Index pinch)
            d = math.hypot((lms[8].x - lms[4].x)*w, (lms[8].y - lms[4].y)*h)
            if d < 30 and now - last_act > 3:
                pyautogui.screenshot(f"ss_{int(now)}.png")
                last_act = now
            
            # 2. Count Fists
            if all(lms[tip].y > lms[tip-2].y for tip in [8, 12, 16, 20]):
                fists += 1
            
            mp.solutions.drawing_utils.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

        if fists == 2 and now - last_act > 3:
            # Turn screen off
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
            last_act = now

    cv2.imshow("System Mode - Press Q to Exit", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()