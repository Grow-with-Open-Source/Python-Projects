import cv2
import os
import time

# Use OpenCV's built-in Haar cascade (NO local XML file)
cascade_path = cv2.data.haarcascades + "haarcascade_russian_plate_number.xml"
plate_cascade = cv2.CascadeClassifier(cascade_path)

if plate_cascade.empty():
    raise IOError("Error loading Haar cascade")

# Output directory
os.makedirs("plates", exist_ok=True)

# Use webcam by default (NO mp4 file in repo)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

plate_count = 0
last_save_time = 0
save_delay = 0.5  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (960, 540))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    roi = gray[270:540, :]
    plates = plate_cascade.detectMultiScale(
        roi,
        scaleFactor=1.05,
        minNeighbors=7,
        minSize=(60, 20)
    )

    current_time = time.time()

    for (x, y, w, h) in plates:
        y += 270
        aspect_ratio = w / h

        if 2 < aspect_ratio < 5:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if current_time - last_save_time > save_delay:
                plate_count += 1
                plate_img = frame[y:y+h, x:x+w]
                cv2.imwrite(f"plates/plate_{plate_count}.jpg", plate_img)
                last_save_time = current_time

    cv2.imshow("Number Plate Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
