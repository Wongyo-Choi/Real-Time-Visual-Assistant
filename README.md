# Real‑Time Visual Assistant

## Overview

This repository comprises three integrated components aimed at providing a comprehensive visual assistance solution:

1. **Neural Network Training Models** – Jupyter notebooks demonstrating the preparation, training and export of YOLOv8 models for traffic light and vehicle detection.
2. **Visual Assistant Web** – A Flask application offering real‑time object detection, tracking and audio alerts via a web interface.
3. **Visual Assistant iOS App** – An iOS application utilising CoreML and Vision frameworks for on‑device detection, visual overlays and voice command recognition.

Each component can be used independently or combined to form a flexible end‑to‑end pipeline for real‑time visual analysis.

## Table of Contents

* [Neural Network Training Models](#neural-network-training-models)
* [Visual Assistant Web](#visual-assistant-web)
* [Visual Assistant iOS App](#visual-assistant-ios-app)
* [Repository Structure](#repository-structure)
* [Requirements](#requirements)
* [Installation & Setup](#installation--setup)
* [Usage](#usage)
* [References](#references)

## Neural Network Training Models

Three Jupyter notebooks illustrate the full workflow for training YOLOv8 models (n, m and x variants) on a combined custom and COCO dataset:

1. **Neural\_Network(yolov8n).ipynb**
2. **Neural\_Network(yolov8m).ipynb**
3. **Neural\_Network(yolov8x).ipynb**

Each notebook guides you through:

* Installing dependencies (Ultralytics YOLOv8, pycocotools, Albumentations, OpenCV, etc.)
* Downloading and organising a Roboflow traffic light dataset
* Filtering and relabelling relevant classes from COCO (bicycle, car, motorcycle, bus)
* Merging datasets and creating `data.yaml`
* Training the selected YOLOv8 model variant
* Saving the best model weights (`best.pt`) into the **Models/** directory as:

  * `yolo8n.pt`
  * `yolo8m.pt`
  * `yolo8x.pt`

## Visual Assistant Web

The **Visual Assistant Web** component is a Flask‑based application that:

* Captures live video via OpenCV and processes frames using a chosen YOLOv8 model
* Overlays bounding boxes, labels and movement vectors on the video stream
* Generates auditory alerts (traffic light states, approaching objects) using gTTS and pygame
* Listens for voice commands (e.g. "traffic situation") on a separate thread, responding with a spoken scene summary

Main file: `Flask_Web.py`
Embedded HTML template serves as the web interface, defaulting to port 5001.

## Visual Assistant iOS App

The **Visual Assistant iOS App** delivers on‑device real‑time detection and alerts:

* Utilises CoreML, Vision and AVFoundation frameworks to run YOLO8n/m/x models
* Displays dynamic bounding boxes and confidence labels via `BoundingBoxView.swift`
* Implements custom threshold adjustments through `ThresholdProvider.swift`
* Captures and streams live camera feed in `ViewController.swift`
* Integrates speech recognition and synthesis for voice commands and audio feedback
* Supports photo capture, sharing, pinch‑to‑zoom and orientation changes

Open the `YOLO.xcodeproj` in Xcode to build and run on iOS 13+ devices.

## Repository Structure

```
.
├── Models/
│   ├── yolo8n.pt
│   ├── yolo8m.pt
│   └── yolo8x.pt
├── Neural_Network(yolov8n).ipynb
├── Neural_Network(yolov8m).ipynb
├── Neural_Network(yolov8x).ipynb
├── Visual_Assistant_Flask_Web/
│   └── Flask_Web.py
├── Visual_Assistant_iOS_App/
│   ├── YOLO.xcodeproj/
│   ├── ViewController.swift
│   ├── ThresholdProvider.swift
│   └── BoundingBoxView.swift
└── README.md
```

## Requirements

* **Python 3.7+** with GPU‑enabled PyTorch
* **Ultralytics YOLOv8**
* **COCO API** (`pycocotools`)
* **Albumentations, OpenCV, Matplotlib, Pandas, Requests, TQDM**
* **Flask, gTTS, pygame, SpeechRecognition, PyAudio** (for Web component)
* **Xcode (iOS 13+)**, Swift, CoreML, Vision, AVFoundation (for iOS App)

## Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Wongyo-Choi/Real-Time-Visual-Assistant.git
   cd Real-Time-Visual-Assistant
   ```

2. **Set up Python environment**:

   ```bash
   pip install pycocotools requests albumentations ultralytics matplotlib pandas tqdm flask gtts pygame SpeechRecognition pyaudio
   ```

3. **Train models (optional)**:
   Open any training notebook in Jupyter or Colab:

   ```bash
   jupyter lab Neural_Network(yolov8n).ipynb
   ```

4. **Run the Web application**:

   ```bash
   cd Visual_Assistant_Flask_Web
   python Flask_Web.py
   # Open http://localhost:5001 in your browser
   ```

5. **Build and run iOS App**:

   * Open `Visual_Assistant_iOS_App/YOLO.xcodeproj` in Xcode
   * Connect your device, enable Developer Mode, select your team for signing
   * Build and run

## Usage

* **Models**: Use the exported `.pt` files in your own Ultralytics code for inference.
* **Web**: Navigate to the Flask web page to view live detections and hear alerts.
* **iOS App**: Launch the app on your device to experience on‑device detection, voice commands and photo capture.

## References

* [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com)
* [Roboflow Dataset Management](https://roboflow.com)
* [COCO Dataset](https://cocodataset.org)
