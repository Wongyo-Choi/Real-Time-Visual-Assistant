from flask import Flask, render_template_string, Response, url_for
import cv2
import os
import numpy as np
from ultralytics import YOLO
from gtts import gTTS
import pygame
import time
import threading
import speech_recognition as sr

# Initialise the Flask application
app = Flask(__name__)

# Initialise the pygame mixer for audio playback (server-side)
pygame.mixer.init()

# Function to generate Text-To-Speech (TTS) audio files for initial alerts
def generate_tts_files():
    # Create an alert for a red traffic signal
    tts_red = gTTS(text="Warning! Please wait, red light.", lang='en')
    tts_red.save("warning_red.mp3")
    
    # Create an alert for a green traffic signal
    tts_green = gTTS(text="You may cross the street. Green light.", lang='en')
    tts_green.save("safe_green.mp3")
    
    # Create an alert for an approaching object
    tts_approach = gTTS(text="Caution! Object approaching.", lang='en')
    tts_approach.save("approaching_alert.mp3")

generate_tts_files()

# Function to play an audio file; runs in a separate thread to avoid blocking
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Load the YOLO model    
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "Models", "yolo8n.pt")
model = YOLO(model_path)

# Initialise the camera capture (using the default camera)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open video device")

# Retrieve camera properties: frames per second, width and height
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define reference points and parameters for detection
SCREEN_CENTER = (width // 2, height // 2)
BOTTOM_CENTER = (width // 2, height)
REFERENCE_VECTOR = np.array(BOTTOM_CENTER) - np.array(SCREEN_CENTER)
LINE_THICKNESS = 4
BOX_THICKNESS = 3  # Thicker bounding box outline
MIN_AREA_THRESHOLD = (width * height) * (1 / 36)

# Dictionary to store tracking history for objects.
# For each object, record 'current_box', 'prev_centroid', 'last_class', 'last_alert_time', 'prev_area', and 'last_seen'.
track_history = {}

def process_frame(frame):
    """Process a single frame using YOLO detection and overlay tracking information."""
    current_time = time.time()
    # Draw the reference line from the screen centre to the bottom centre
    cv2.line(frame, SCREEN_CENTER, BOTTOM_CENTER, (0, 255, 0), 2)
    
    # Perform object tracking detection using the YOLO model
    results = model.track(frame, persist=True, conf=0.3, verbose=False)
    
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        classes = results[0].boxes.cls.int().cpu().tolist()
        confidences = results[0].boxes.conf.float().cpu().tolist()
        
        for i, (box, cls, conf) in enumerate(zip(boxes, classes, confidences)):
            class_name = model.names[cls]
            track_id = track_ids[i]
            
            # Calculate the current object properties: bounding box and centroid
            x1, y1, x2, y2 = map(int, box)
            current_centroid = ((x1 + x2) // 2, (y1 + y2) // 2)
            current_area = max(1, (x2 - x1) * (y2 - y1))
            
            # Initialise or update tracking history for objects
            if track_id not in track_history:
                track_history[track_id] = {
                    'current_box': (x1, y1, x2, y2),
                    'prev_centroid': current_centroid,
                    'last_class': class_name,
                    'last_alert_time': 0,
                    'prev_area': current_area,
                    'last_seen': current_time
                }
                needs_update = False
            else:
                # Update the last seen time
                track_history[track_id]['last_seen'] = current_time
                prev_box = track_history[track_id]['current_box']
                px1, py1, px2, py2 = prev_box
                # Check if the current centroid still lies within the previous bounding box
                if px1 <= current_centroid[0] <= px2 and py1 <= current_centroid[1] <= py2:
                    needs_update = False
                else:
                    needs_update = True
            
            # For non-traffic light objects, compute movement and trigger alerts if appropriate
            if needs_update and class_name not in ['red pedestrian light', 'green pedestrian light']:
                prev_centroid = track_history[track_id]['prev_centroid']
                prev_area = track_history[track_id]['prev_area']
                movement_vector = np.array(current_centroid) - np.array(prev_centroid)
                movement_norm = np.linalg.norm(movement_vector)
                ref_norm = np.linalg.norm(REFERENCE_VECTOR)
                if movement_norm > 0 and ref_norm > 0:
                    cosine_sim = np.dot(movement_vector, REFERENCE_VECTOR) / (movement_norm * ref_norm)
                    if (current_area > prev_area) and (current_area > MIN_AREA_THRESHOLD) and \
                       (cosine_sim > 0.9) and ((current_time - track_history[track_id]['last_alert_time']) > 3):
                        # Trigger the approaching alert sound
                        threading.Thread(target=play_sound, args=("approaching_alert.mp3",), daemon=True).start()
                        track_history[track_id]['last_alert_time'] = current_time
                # Draw an arrow indicating the movement vector
                cv2.arrowedLine(frame, track_history[track_id]['prev_centroid'], current_centroid, (0, 0, 255), LINE_THICKNESS)
            
            # Update tracking information if a significant movement is detected
            if needs_update:
                cv2.arrowedLine(frame, track_history[track_id]['prev_centroid'], current_centroid, (255, 0, 255), LINE_THICKNESS)
                track_history[track_id]['current_box'] = (x1, y1, x2, y2)
                track_history[track_id]['prev_centroid'] = current_centroid
                track_history[track_id]['prev_area'] = current_area
            
            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), BOX_THICKNESS)
            label = f"{class_name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Traffic light alert logic
            if class_name in ['red pedestrian light', 'green pedestrian light']:
                prev_class = track_history[track_id]['last_class']
                if class_name != prev_class:
                    if class_name == 'red pedestrian light' and conf >= 0.6:
                        threading.Thread(target=play_sound, args=("warning_red.mp3",), daemon=True).start()
                        track_history[track_id]['last_alert_time'] = current_time
                    elif class_name == 'green pedestrian light' and conf >= 0.7:
                        threading.Thread(target=play_sound, args=("safe_green.mp3",), daemon=True).start()
                        track_history[track_id]['last_alert_time'] = current_time
                elif (current_time - track_history[track_id]['last_alert_time']) > 10:
                    if class_name == 'red pedestrian light' and conf >= 0.6:
                        threading.Thread(target=play_sound, args=("warning_red.mp3",), daemon=True).start()
                        track_history[track_id]['last_alert_time'] = current_time
                    elif class_name == 'green pedestrian light' and conf >= 0.7:
                        threading.Thread(target=play_sound, args=("safe_green.mp3",), daemon=True).start()
                        track_history[track_id]['last_alert_time'] = current_time
                track_history[track_id]['last_class'] = class_name

    return frame

# Global variable and lock to safely share the latest frame across threads
latest_frame = None
frame_lock = threading.Lock()

def frame_capture_loop():
    """
    Continuously capture frames from the camera and update the global frame variable.
    This function is run in a separate thread.
    """
    global latest_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.05)
            continue
        # Process the captured frame
        processed_frame = process_frame(frame)
        # Update the global frame variable in a thread-safe manner
        with frame_lock:
            latest_frame = processed_frame
        # Wait briefly to match the desired frame capture rate (e.g. 1/30th of a second)
        time.sleep(1/30)

# Start the frame capture loop in a separate thread
capture_thread = threading.Thread(target=frame_capture_loop, daemon=True)
capture_thread.start()

def generate_frames():
    """
    Continuously encode the latest frame as JPEG and yield it for streaming.
    """
    while True:
        with frame_lock:
            frame = latest_frame.copy() if latest_frame is not None else None
        if frame is None:
            time.sleep(0.01)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        # Brief pause to regulate the streaming rate (e.g. 1/30th of a second)
        time.sleep(1/30)

# HTML template for the index page
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Precision Monitoring System</title>
    <style>
        body { background-colour: #222; colour: #eee; text-align: centre; }
        h1 { colour: #eee; }
        img { width: 80%%; border: 5px solid #444; }
    </style>
</head>
<body>
    <h1>Precision Monitoring System</h1>
    <img src="{{ url_for('video_feed') }}" alt="Live Camera Feed">
</body>
</html>
"""

@app.route('/')
def index():
    # Render the index page using the HTML template
    return render_template_string(INDEX_HTML)

@app.route('/video_feed')
def video_feed():
    # Return a streaming response containing the video frames
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ----------------- Voice Command Handling ----------------- #
def get_traffic_summary():
    """
    Analyse the current tracking history and generate a summary.
    Only objects updated within the last 3 seconds are included.
    The function compares each object's current and previous centroids to determine movement.
    """
    current_time = time.time()
    summary_lines = []
    # Remove outdated objects from tracking history
    stale_keys = []
    for track_id, info in track_history.items():
        if current_time - info.get('last_seen', current_time) > 3:
            stale_keys.append(track_id)
            continue
        # Determine the horizontal position of the object's centroid
        x1, y1, x2, y2 = info['current_box']
        centroid = ((x1 + x2) // 2, (y1 + y2) // 2)
        if centroid[0] < width / 3:
            position = "on the left"
        elif centroid[0] < 2 * width / 3:
            position = "in the centre"
        else:
            position = "on the right"
        # Determine movement direction by comparing current and previous centroids
        prev_centroid = info['prev_centroid']
        dx = centroid[0] - prev_centroid[0]
        dy = centroid[1] - prev_centroid[1]
        if abs(dx) < 5 and abs(dy) < 5:
            movement = "stationary"
        else:
            if dx > 0:
                movement = "moving right"
            elif dx < 0:
                movement = "moving left"
            else:
                movement = "stationary"
        summary_lines.append(f"{info['last_class']} detected {position} is {movement}.")
    
    # Remove outdated data from tracking history
    for key in stale_keys:
        del track_history[key]
        
    if not summary_lines:
        return "No objects are currently detected."
    return " ".join(summary_lines)

def listen_for_commands():
    """
    Continuously listen for voice commands.
    When the command "traffic situation" is detected, generate a summary based on the latest object data and provide audio feedback.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    while True:
        with microphone as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("Heard command:", command)
            if "traffic" in command.lower() and "situation" in command.lower():
                summary = get_traffic_summary()
                print("Traffic Summary:", summary)
                # Generate TTS audio for the summary
                tts = gTTS(text=summary, lang='en')
                tts.save("traffic_summary.mp3")
                play_sound("traffic_summary.mp3")
        except Exception as e:
            print("Command not recognised:", e)

# Start the voice command listener in a separate thread
command_thread = threading.Thread(target=listen_for_commands, daemon=True)
command_thread.start()
# ---------------------------------------------------------- #

if __name__ == '__main__':
    try:
        # Run the Flask application on all interfaces at port 5001 without debug mode
        app.run(host='0.0.0.0', port=5001, debug=False)
    finally:
        # Release the camera resource and quit the pygame mixer upon termination
        cap.release()
        pygame.mixer.quit()
