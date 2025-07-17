import cv2   
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(0)


index_finger = 8
middle_finger = 12

distance_threshold = 30  

click_detected = False
last_click_time = 0  
debounce_threshold = 0.3  

expression = ""  
button_size = 60  
buttons = [
    ('7', (50, 100)), ('8', (110, 100)), ('9', (170, 100)), ('/', (230, 100)),
    ('4', (50, 160)), ('5', (110, 160)), ('6', (170, 160)), ('*', (230, 160)),
    ('1', (50, 220)), ('2', (110, 220)), ('3', (170, 220)), ('-', (230, 220)),
    ('C', (50, 280)), ('0', (110, 280)), ('=', (170, 280)), ('+', (230, 280)),
    ('Close', (400, 280))  # Close button
]

button_colors = {button[0]: (255, 255, 255) for button in buttons}  
button_colors['Close'] = (0, 0, 255)  # Red close button

def draw_calculator(frame):
    overlay = frame.copy()
    for label, position in buttons:
        x, y = position
        button_color = button_colors[label]
        cv2.rectangle(overlay, (x, y), (x + button_size, y + button_size), button_color, -1)
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        label_x = x + (button_size - label_size[0]) // 2
        label_y = y + (button_size + label_size[1]) // 2
        cv2.putText(overlay, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

def handle_click(x, y):
    global expression
    for label, position in buttons:
        bx, by = position
        if bx < x < bx + button_size and by < y < by + button_size:
            if label == 'C':
                expression = ""
            elif label == '=':
                try:
                    expression = str(eval(expression))
                except:
                    expression = "Error"
            elif label == 'Close':
                return True  # Indicate to close window
            else:
                expression += label  
            return False  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape
            index_x, index_y = int(hand_landmarks.landmark[index_finger].x * w), int(hand_landmarks.landmark[index_finger].y * h)
            middle_x, middle_y = int(hand_landmarks.landmark[middle_finger].x * w), int(hand_landmarks.landmark[middle_finger].y * h)
            distance = ((index_x - middle_x) ** 2 + (index_y - middle_y) ** 2) ** 0.5

            if distance < distance_threshold and not click_detected and (time.time() - last_click_time > debounce_threshold):  
                if handle_click((index_x + middle_x) // 2, (index_y + middle_y) // 2):  
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()  
                click_detected = True
                last_click_time = time.time()
            
            if distance > distance_threshold:
                click_detected = False  

    draw_calculator(frame)
    cv2.putText(frame, expression, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.imshow("Hand Tracking Calculator", frame)
    if cv2.waitKey(1) == 27:  
        break

cap.release()
cv2.destroyAllWindows()
