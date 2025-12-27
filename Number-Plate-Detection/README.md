# Number Plate Detection 🚘🔍

This project is a simple Number Plate Detection system built using **OpenCV** and **Python**. It uses image processing techniques and a pre-trained Haar Cascade classifier to detect number plates in real-time from video streams or static images.

## 📸 Demo

![Screenshot 2025-05-21 160620](https://github.com/user-attachments/assets/fd6d233e-a948-4015-aab3-50ec09ac9f75)


## 🧠 Features

- Real-time number plate detection using webcam
- Uses OpenCV's Haar Cascade Classifier
- Highlights detected number plates with rectangles
- Can be extended for OCR (Optical Character Recognition)

## 🛠️ Technologies Used

- Python 3.x
- OpenCV
- Haar Cascade Classifier

## 📁 Project Structure

Number-Plate-Detection/

│

├── Numberplatedetection.py # Main script for plate detection

├── haarcascade_russian_plate_number.xml # Haar Cascade model for number plates

└── README.md # Project documentation

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/iamdevdhanush/Number-Plate-Detection.git
cd Number-Plate-Detection
```

2. Install Requirements

```bash
pip install opencv-python
```

3. Run the Script

```bash
python Numberplatedetection.py
```

📦 Dependencies
```
opencv-python
```
You can install them using pip:

```
pip install -r requirements.txt
```

📌 Notes

Make sure you have the correct Haar Cascade XML file (haarcascade_russian_plate_number.xml).

This project is a basic implementation and doesn't perform OCR. You can extend it using pytesseract for extracting plate text.

🤖 Future Improvements

Add OCR to extract text from number plates

Improve accuracy with deep learning-based detection (YOLO, SSD)

Support detection in images and video files


🙋‍♂️ Author

Dhanush

GitHub
