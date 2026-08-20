import cv2
import mediapipe as mp
import pyautogui
import math
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
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
        lms = results.multi_hand_landmarks[0].landmark
        
        # 1. VOLUME CONTROL (Distance between Thumb and Index)
        x1, y1 = int(lms[4].x * w), int(lms[4].y * h)
        x2, y2 = int(lms[8].x * w), int(lms[8].y * h)
        dist = math.hypot(x2 - x1, y2 - y1)

        # Draw a line between fingers to visualize volume level
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        if dist > 100:
            pyautogui.press("volumeup")
        elif dist < 30:
            pyautogui.press("volumedown")

        # 2. PLAY/PAUSE (Palm Open to Stop/Play)
        fingers = [1 if lms[tip].y < lms[tip-2].y else 0 for tip in [8, 12, 16, 20]]
        if sum(fingers) == 4 and now - last_act > 1.5:
            pyautogui.press("playpause")
            last_act = now
            cv2.putText(img, "PLAY/PAUSE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        mp.solutions.drawing_utils.draw_landmarks(img, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Media Mode - Press Q to Exit", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()