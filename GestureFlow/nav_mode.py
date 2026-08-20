import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
cooldown = 0.8
last_act = 0

def get_fingers(lms):
    # Returns list [Index, Middle, Ring, Pinky] (1 = Up, 0 = Down)
    return [1 if lms[tip].y < lms[tip-2].y else 0 for tip in [8, 12, 16, 20]]

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time()

    if results.multi_hand_landmarks:
        lms = results.multi_hand_landmarks[0].landmark
        fingers = get_fingers(lms)
        
        # Action Logic
        if now - last_act > cooldown:
            # 1 Finger: Tab Navigation (Horizontal Swipe)
            if fingers == [1, 0, 0, 0]:
                dx = (lms[8].x - lms[6].x) * w
                if dx > 40: # Right
                    pyautogui.hotkey('ctrl', 'tab')
                    last_act = now
                elif dx < -40: # Left
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                    last_act = now

            # 3 Fingers Down: Minimize
            elif fingers == [0, 0, 0, 0]: # Fist/Downward
                pyautogui.hotkey('win', 'down')
                last_act = now

        mp.solutions.drawing_utils.draw_landmarks(img, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Nav Mode - Press Q to Exit", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()