# QR Code Generator (Flask)

A small web app that turns any URL into a downloadable QR code image.

## Features
- Enter a URL and generate a QR code instantly
- Automatically adds `https://` if you forget it
- Download the QR code as a PNG

## Requirements
- Python 3.8+
- Flask, qrcode, Pillow

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python app.py
```
Then open http://127.0.0.1:5000 in your browser, enter a URL, and click download.

## Project Structure
```
QR-Code-Flask-App/
├── app.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```