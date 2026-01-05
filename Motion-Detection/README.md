# 🎥 Motion Detection Using OpenCV 🕵️‍♂️

This project demonstrates a **basic motion detection system** using OpenCV and Python. It captures video from a camera, processes the frames to detect moving objects, and highlights detected motion areas in real-time. 🚀

---

## ✨ Features

- 📹 Capture video feed from the webcam.
- 🎨 Convert frames to grayscale and apply Gaussian blur for noise reduction.
- 🔍 Detect motion by comparing the current frame with the first frame.
- 🔲 Highlight moving objects with bounding rectangles.
- 📝 Display status text indicating whether motion is detected.
- ❌ Press **`q`** to quit the application.

---

## 🛠️ Requirements

- Python 3.x 🐍
- OpenCV (`cv2`) 🖼️
- Imutils 🔧
- Time module (standard Python library) ⏰

---

## 📦 Installation

Install required libraries using pip:

```bash
pip install opencv-python imutils
```

▶️ Usage

Run the script to start the motion detection:

```bash
python motion_detection.py
```

⚙️ How It Works

🥇 The first frame is captured and used as a reference.

🖤 Each new frame is converted to grayscale and blurred.

➖ The absolute difference between the current frame and the reference frame is calculated.

⚫ Thresholding and dilation are applied to highlight differences.

🔎 Contours are detected in the thresholded image.

✅ If contours exceed a minimum area, bounding boxes are drawn, and motion is detected.

📺 The video feed with detected motion highlighted is displayed.
