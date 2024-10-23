# Real-Time 3D Pose Estimation

This project implements real-time 3D pose estimation using MediaPipe and OpenCV. It captures video from a webcam, detects human pose landmarks in 3D, and sends the landmark data to a Unity application via UDP.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [License](#license)

## Features
- Real-time detection of 3D pose landmarks using MediaPipe.
- Visualization of detected landmarks on the webcam feed.
- Sending 3D landmark coordinates to a Unity application via UDP for further processing or visualization.
- Option to terminate the program by pressing the 'q' key.

## Requirements
- Python 3.x
- OpenCV
- MediaPipe
- NumPy
- JSON
- Socket

