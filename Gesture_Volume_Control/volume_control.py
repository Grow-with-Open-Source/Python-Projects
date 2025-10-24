import cv2
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

# Mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()  # minVol, maxVol, step

# Phone camera
cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=30)
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Resize to 360x360
    frame = cv2.resize(frame, (640, 480))

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Thumb and index finger tips
            thumb_tip = handLms.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            h, w, _ = frame.shape
            x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

            cv2.circle(frame, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Distance between fingers → volume
            length = math.hypot(x2 - x1, y2 - y1)
            min_vol, max_vol, _ = vol_range
            vol = (length / 200) * (max_vol - min_vol) + min_vol
            vol = max(min(vol, max_vol), min_vol)
            volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Hand Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
