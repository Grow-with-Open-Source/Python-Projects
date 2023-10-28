# QRCODE
QRCODE generator using python

# QR Code Generator with GUI

This Python application allows you to generate QR codes for website URLs with a graphical user interface (GUI). Users can input a URL, and the program generates and displays the QR code in the GUI. Additionally, clicking on the generated QR code will open the URL in the default web browser.

## Prerequisites

To run this application, you need to have Python installed on your system. The code relies on the following Python libraries:

- `qrcode`: For generating QR codes.
- `tkinter`: For creating the GUI.
- `Pillow` (PIL Fork): For image processing and displaying the QR code.
- `webbrowser`: For opening URLs in the default web browser.

You can install the required libraries using `pip`:

## shell
`pip install qrcode[pil] pillow`

## Usage
Clone this repository or download the main.py file.
Run the application by executing the main.py script.

## shell

Copy code
python main.py
A GUI window will open with the following elements:

A label and text entry field for entering a URL.
A button to generate the QR code.
A label to display the generated QR code.
Enter a URL in the text entry field and click the "Generate QR Code" button.

The program will generate the QR code and display it in the GUI.

Click on the generated QR code, and it will open the URL in your default web browser.

## OUTPUT

<div align= "center">

<img src="assets/img/imgg1.png">
<img src="assets/img/imgg2.png">

</div>
Contributing
Feel free to contribute to this project by submitting issues, feature requests, or pull requests.