import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Settings
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False 
smoothening = 7
prev_x, prev_y = 0, 0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = handLms.landmark
            # Index (8) and Middle (12) tips
            x1, y1 = int(lm[8].x * w), int(lm[8].y * h)
            x2, y2 = int(lm[12].x * w), int(lm[12].y * h)

            # Move Logic: Index up, Middle down
            if lm[8].y < lm[6].y and lm[12].y > lm[10].y:
                curr_x = prev_x + (int(x1 * screen_w / w) - prev_x) / smoothening
                curr_y = prev_y + (int(y1 * screen_h / h) - prev_y) / smoothening
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y
                cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

            # Click Logic: Index and Middle pinch
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist < 30:
                pyautogui.click()
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                time.sleep(0.2)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Mouse Mode - Press Q to Exit", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()