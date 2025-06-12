# Visual Assistant Web

Visual Assistant is a Flask web application that provides real‐time visual feedback using advanced object detection, tracking, and voice command recognition. The app processes live video from a connected camera using a YOLO model from the Models folder, overlays detection information on the video stream, and issues auditory alerts based on scene analysis.

---

## Features

- **Real‐Time Object Detection & Tracking:**  
  Utilises a YOLO model (choose from `yolo8n.pt`, `yolo8m.pt`, or `yolo8x.pt` available in the Models folder) with the ultralytics package to detect and track objects in real time.

- **Live Video Streaming:**  
  Captures video frames using OpenCV and streams the processed video via a Flask web server.

- **Auditory Alerts:**  
  Generates Text-To-Speech (TTS) audio alerts for red/green traffic signals and approaching objects using gTTS, with audio playback handled by pygame.

- **Voice Command Recognition:**  
  Continuously listens for voice commands (e.g. "traffic situation") and provides a spoken summary of the current scene.

- **Customisable Detection Parameters:**  
  Adjusts detection thresholds (e.g. confidence, area) and uses visual cues (bounding boxes, movement arrows) to indicate object status.

---

## Code Structure

- **Flask_Web.py**  
  This is the main application file that:
  - Sets up the Flask web server and routes.
  - Captures and processes video frames from the camera.
  - Implements object detection and tracking using a selectable YOLO model.
  - Generates and plays TTS audio alerts.
  - Listens for voice commands on a separate thread.

- **Models Folder:**  
  Contains the following YOLO model files:
  - `yolo8n.pt`
  - `yolo8m.pt`
  - `yolo8x.pt`  
  You can choose the appropriate model file by updating the model path in the code.

- **Embedded HTML Template:**  
  The application uses an HTML template (via `render_template_string`) to display the live video feed with detection overlays.

---

## Requirements

- **Python:** 3.7 or later  
- **Flask:** For serving the web application  
- **OpenCV:** For video capture and processing  
- **NumPy:** For numerical operations  
- **Ultralytics YOLO:** For object detection and tracking  
- **gTTS:** For generating TTS audio alerts  
- **Pygame:** For audio playback  
- **SpeechRecognition:** For processing voice commands  
- **PyAudio:** (required by SpeechRecognition for microphone input)

---

## Installation & Setup

1. **Install Dependencies:**  
   In the project directory, run the following command to install all packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**  
   Open your terminal in the project directory and execute the following command:
   ```bash
   python Flask_Web.py
   ```

3. **Access the Web Interface**:
   Once the Flask server starts (default port: 5001), open your web browser and navigate to: 
   `http://localhost:5001`
