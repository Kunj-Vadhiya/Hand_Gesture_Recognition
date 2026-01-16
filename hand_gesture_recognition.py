""" Hand Gesture Recognition System """

import mediapipe_patch

import cv2
import numpy as np
import time
from collections import deque
import urllib.request
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandGestureRecognizer:
    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8
    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12
    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20
    
    HAND_CONNECTIONS = [
        # Thumb
        (0, 1), (1, 2), (2, 3), (3, 4),
        # Index finger
        (0, 5), (5, 6), (6, 7), (7, 8),
        # Middle finger
        (0, 9), (9, 10), (10, 11), (11, 12),
        # Ring finger
        (0, 13), (13, 14), (14, 15), (15, 16),
        # Pinky
        (0, 17), (17, 18), (18, 19), (19, 20),
        # Palm
        (5, 9), (9, 13), (13, 17)
    ]
    
    GESTURE_COLORS = {
        'Open Palm': (0, 255, 0),      # Green
        'Fist': (0, 0, 255),            # Red
        'Peace': (255, 255, 0),         # Cyan
        'Pointing': (255, 0, 255),      # Magenta
        'Thumbs Up': (0, 165, 255),     # Orange
        'Rock': (255, 0, 127),          # Purple
        'OK Sign': (0, 255, 255),       # Yellow
        'Unknown': (128, 128, 128)      # Gray
    }
    
    def __init__(self, max_hands=2, detection_confidence=0.7):
        """Initialize the recognizer"""
        print("Initializing Hand Gesture Recognizer...")
        
        self.model_path = 'hand_landmarker.task'
        if not os.path.exists(self.model_path):
            print("Downloading hand landmarker model...")
            model_url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
            urllib.request.urlretrieve(model_url, self.model_path)
            print("Model downloaded!")
        
        try:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.HandLandmarkerOptions(
                base_options=base_options,
                num_hands=max_hands,
                min_hand_detection_confidence=detection_confidence,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.detector = vision.HandLandmarker.create_from_options(options)
            print("✓ MediaPipe HandLandmarker initialized successfully!")
        except Exception as e:
            print(f"Error initializing detector: {e}")
            raise

        self.gesture_history = [deque(maxlen=5), deque(maxlen=5)]
        
        self.prev_time = 0
        self.fps = 0

        self.gesture_actions = {
            'Fist': 'Command: Stop',
            'Open Palm': 'Command: Activate',
            'Thumbs Up': 'Command: Approve',
            'Peace': 'Command: Next',
            'Pointing': 'Command: Select'
        }
    
    def extract_landmarks(self, hand_landmarks, frame_width, frame_height):
        """Extract 21 hand landmarks in pixel coordinates"""
        landmarks = []
        for landmark in hand_landmarks:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            landmarks.append((x, y))
        return landmarks
    
    def is_finger_open(self, landmarks, finger_tip_idx, finger_pip_idx):
        """Check if finger is extended"""
        return landmarks[finger_tip_idx][1] < landmarks[finger_pip_idx][1]
    
    def is_thumb_open(self, landmarks, hand_type):
        """Check if thumb is extended (horizontal)"""
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        if hand_type == 'Right':
            return thumb_tip[0] > thumb_ip[0]
        else:
            return thumb_tip[0] < thumb_ip[0]
    
    def get_fingers_state(self, landmarks, hand_type):
        """Get state of all 5 fingers"""
        fingers = []
        fingers.append(self.is_thumb_open(landmarks, hand_type))
        fingers.append(self.is_finger_open(landmarks, 8, 6))   # Index
        fingers.append(self.is_finger_open(landmarks, 12, 10))  # Middle
        fingers.append(self.is_finger_open(landmarks, 16, 14))  # Ring
        fingers.append(self.is_finger_open(landmarks, 20, 18))  # Pinky
        return fingers
    
    def classify_gesture(self, landmarks, hand_type):
        """Classify gesture based on finger states"""
        fingers = self.get_fingers_state(landmarks, hand_type)
        fingers_up = sum(fingers)
        
        if fingers_up == 0:
            return 'Fist'
        elif fingers_up == 5:
            return 'Open Palm'
        elif fingers_up == 1 and fingers[0]:
            return 'Thumbs Up'
        elif fingers_up == 2 and fingers[1] and fingers[2]:
            return 'Peace'
        elif fingers_up == 1 and fingers[1]:
            return 'Pointing'
        elif fingers_up == 2 and fingers[1] and fingers[4]:
            return 'Rock'
        elif fingers_up == 3 and fingers[0] and fingers[2] and fingers[3]:
            return 'OK Sign'
        else:
            return 'Unknown'
    
    def get_stable_gesture(self, gesture, hand_idx):
        """Apply stability filter"""
        self.gesture_history[hand_idx].append(gesture)
        
        if len(self.gesture_history[hand_idx]) > 0:
            gesture_counts = {}
            for g in self.gesture_history[hand_idx]:
                gesture_counts[g] = gesture_counts.get(g, 0) + 1
            
            stable_gesture = max(gesture_counts, key=gesture_counts.get)
            
            if gesture_counts[stable_gesture] >= len(self.gesture_history[hand_idx]) * 0.6:
                return stable_gesture
        
        return gesture
    
    def calculate_fps(self):
        """Calculate FPS"""
        current_time = time.time()
        self.fps = 1 / (current_time - self.prev_time) if self.prev_time > 0 else 0
        self.prev_time = current_time
        return int(self.fps)
    
    def draw_landmarks(self, frame, landmarks, gesture, hand_idx=0):
        """Draw 21 landmarks and connections with gesture-specific colors"""
        h, w = frame.shape[:2]
    
        color = self.GESTURE_COLORS.get(gesture, (255, 255, 255))
        
        for connection in self.HAND_CONNECTIONS:
            start_idx, end_idx = connection
            if start_idx < len(landmarks) and end_idx < len(landmarks):
                start_point = landmarks[start_idx]
                end_point = landmarks[end_idx]
                cv2.line(frame, start_point, end_point, color, 3)
    
        for i, point in enumerate(landmarks):
            # Larger circles for fingertips and wrist
            if i in [0, 4, 8, 12, 16, 20]:
                radius = 9
                
                cv2.circle(frame, point, radius + 3, (255, 255, 255), 3)
                cv2.circle(frame, point, radius, color, -1)
            else:
                radius = 6

                cv2.circle(frame, point, radius + 2, (255, 255, 255), 2)

                cv2.circle(frame, point, radius, color, -1)
    
    def draw_info(self, frame, gestures, fps):
        """Draw UI information"""
        
        cv2.putText(frame, f'FPS: {fps}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        y_offset = 70
        for i, gesture in enumerate(gestures):
            color = self.GESTURE_COLORS.get(gesture, (255, 255, 255))
            
            cv2.putText(frame, f'Hand {i+1}: {gesture}',
                        (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, color, 2)
            
            if gesture in self.gesture_actions:
                cv2.putText(frame, self.gesture_actions[gesture],
                            (10, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (255, 255, 0), 2)
                y_offset += 70
            else:
                y_offset += 40
    
    def process_frame(self, frame):
        """Process single frame"""
        # Flip for mirror view
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect hands
        detection_result = self.detector.detect(mp_image)
        
        gestures = []
        h, w, _ = frame.shape
        
        # Process detected hands
        if detection_result.hand_landmarks and detection_result.handedness:
            for hand_idx, (hand_landmarks, handedness) in enumerate(
                zip(detection_result.hand_landmarks, detection_result.handedness)
            ):
                # Get hand type
                hand_label = handedness[0].category_name
                
                # Extract landmarks
                landmarks = self.extract_landmarks(hand_landmarks, w, h)
                
                # Classify gesture based on landmarks and hand type
                gesture = self.classify_gesture(landmarks, hand_label)
                
                # Ensure we have enough history buffers
                if hand_idx >= len(self.gesture_history):
                    self.gesture_history.append(deque(maxlen=5))
                
                stable_gesture = self.get_stable_gesture(gesture, hand_idx)
                gestures.append(stable_gesture)
                
                self.draw_landmarks(frame, landmarks, stable_gesture, hand_idx)
                
                if stable_gesture in self.gesture_actions:
                    print(f"[Hand {hand_idx+1} - {hand_label}] {stable_gesture} -> {self.gesture_actions[stable_gesture]}")
        
        # Calculate FPS
        fps = self.calculate_fps()
        
        # Draw info
        self.draw_info(frame, gestures, fps)
        
        return frame, gestures
    
    def run(self, camera_index=0):
        """Run the recognition system"""
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
            
        print("Hand Gesture Recognition System Started")
        print("Gestures:")
        print("Open Palm - All fingers extended")
        print("Fist - All fingers closed")
        print("Peace - Index + middle fingers")
        print("Pointing - Index finger only")
        print("Thumbs Up - Thumb only")

        print("Press 'q' to quit")
        
        while True:
            success, frame = cap.read()
            
            if not success:
                print("Error: Failed to capture frame")
                break
            
            processed_frame, gestures = self.process_frame(frame)
            
            cv2.imshow('Hand Gesture Recognition - 21 Landmarks', processed_frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nExiting...")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("System shutdown complete")


def main():
    try:
        recognizer = HandGestureRecognizer(max_hands=2, detection_confidence=0.7)
        recognizer.run(camera_index=0)
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nIf you see ctypes errors, MediaPipe may not be compatible with Python 3.13")
        print("Solution: Install Python 3.11 or use hand_gesture_recognition_opencv.py")


if __name__ == "__main__":
    main()
