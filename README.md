# Real-time Hand Gesture Recognition System

A sophisticated hand gesture recognition system built with Python, OpenCV, and MediaPipe that detects and recognizes hand gestures in real-time from webcam feed.

## Features

### Core Features
- **Real-time Hand Detection**: Tracks up to 2 hands simultaneously
- **21 Landmark Extraction**: Detects all 21 hand landmarks with pixel-perfect accuracy
- **Multiple Gesture Recognition**: Recognizes 5 different hand gestures
- **Visual Feedback**: Color-coded landmarks and connections for each gesture
- **FPS Display**: Shows real-time performance metrics

### Advanced Features
- **Multi-Hand Support**: Tracks and recognizes gestures from both hands independently
- **Gesture Stability**: Frame-based smoothing to prevent flickering (5-frame buffer)
- **Action Mapping**: Maps gestures to specific commands/actions
- **Python 3.13 Compatibility**: Automatic patching for MediaPipe on Python 3.13+

## Recognized Gestures

| Gesture | Color | Description | Action |
|---------|-------|-------------|--------|
| **Open Palm** | 🟢 Green | All 5 fingers extended | Command: Activate |
| **Fist** | 🔴 Red | All fingers closed | Command: Stop |
| **Peace** | 🔵 Cyan | Index and middle fingers | Command: Next |
| **Pointing** | 🟣 Magenta | Only index finger extended | Command: Select |
| **Thumbs Up** | 🟠 Orange | Only thumb extended | Command: Approve |


### Processing Pipeline

1. **Frame Capture**: Webcam input via OpenCV
2. **Hand Detection**: MediaPipe detects hands and extracts 21 landmarks
3. **Finger State Analysis**: Determines which fingers are extended
4. **Gesture Classification**: Matches finger patterns to known gestures
5. **Stability Filter**: 60% consensus from last 5 frames
6. **Visual Feedback**: Color-coded rendering based on gesture


### Gesture Detection Logic

The system uses geometric rules based on landmark positions:

1. **Finger State Detection**: Compares fingertip position with lower joints
   - For fingers: Tip Y < PIP Y = Extended
   - For thumb: Horizontal comparison based on handedness

2. **Gesture Classification**: Pattern matching on finger states
   ```
   Fist:       [0, 0, 0, 0, 0]  (all closed)
   Open Palm:  [1, 1, 1, 1, 1]  (all open)
   Thumbs Up:  [1, 0, 0, 0, 0]  (thumb only)
   Peace:      [0, 1, 1, 0, 0]  (index + middle)
   Pointing:   [0, 1, 0, 0, 0]  (index only)
   ```

3. **Stability Filter**: Uses 60% consensus from last 5 frames

## Technical Details

### MediaPipe Hand Landmarks

The system tracks 21 landmarks per hand:
- **Wrist**: Landmark 0
- **Thumb**: Landmarks 1-4
- **Index**: Landmarks 5-8
- **Middle**: Landmarks 9-12
- **Ring**: Landmarks 13-16
- **Pinky**: Landmarks 17-20

## Technical Stack

- **opencv-python**: Video capture and image processing
- **mediapipe**: Hand detection and landmark tracking  
- **numpy**: Numerical operations
- **protobuf**: MediaPipe dependencies