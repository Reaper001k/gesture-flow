import cv2
import mediapipe as mp
import webbrowser
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
cap = cv2.VideoCapture(0)

last_act = 0
cooldown = 3.0  # Longer cooldown for "event" gestures

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time()

    if results.multi_hand_landmarks:
        lms = results.multi_hand_landmarks[0].landmark
        
        # GESTURE LOGIC: Index and Middle UP, Ring and Pinky DOWN
        # Tip (8, 12, 16, 20) vs PIP joint (6, 10, 14, 18)
        fingers = [1 if lms[tip].y < lms[tip-2].y else 0 for tip in [8, 12, 16, 20]]
        thumb_up = lms[4].x < lms[3].x # Basic thumb check
        
        # [Index=1, Middle=1, Ring=0, Pinky=0]
        if fingers == [1, 1, 0, 0] and now - last_act > cooldown:
            cv2.putText(img, "VICTORY DETECTED!", (50, 200), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            
            # Action: Open a celebration link or your project documentation
            webbrowser.open("https://www.google.com/search?q=Congratulations") 
            
            last_act = now

        mp.solutions.drawing_utils.draw_landmarks(img, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Victory Mode - Press Q to Exit", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()