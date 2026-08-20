import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
cap = cv2.VideoCapture(0)

last_act = 0
cooldown = 1.0

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time()

    if results.multi_hand_landmarks:
        lms = results.multi_hand_landmarks[0].landmark
        
        # Get coordinates for Index tip (8) and wrist (0)
        index_x = lms[8].x
        
        # GESTURE: Pointing Index Finger Only
        fingers = [1 if lms[tip].y < lms[tip-2].y else 0 for tip in [8, 12, 16, 20]]
        
        if fingers == [1, 0, 0, 0] and now - last_act > cooldown:
            # Swipe Right (Index tip moves to the right side of screen)
            if index_x > 0.7:
                pyautogui.press("right")
                cv2.putText(img, "NEXT SLIDE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                last_act = now
            # Swipe Left (Index tip moves to the left side of screen)
            elif index_x < 0.3:
                pyautogui.press("left")
                cv2.putText(img, "PREV SLIDE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                last_act = now

        mp.solutions.drawing_utils.draw_landmarks(img, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Presentation Mode - Press Q to Exit", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()