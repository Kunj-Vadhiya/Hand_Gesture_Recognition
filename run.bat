@echo off
echo ========================================
echo Hand Gesture Recognition - Quick Start
echo ========================================
echo.
echo Starting Hand Gesture Recognition...
echo (Python 3.13 Compatible)
echo.
python hand_gesture_recognition.py
pause
) else if "%choice%"=="2" (
    echo.
    echo Starting OpenCV version...
    echo ========================================
    python hand_gesture_recognition_opencv.py
) else if "%choice%"=="3" (
    echo.
    echo Starting MediaPipe original version...
    echo Note: This requires Python 3.11
    echo ========================================
    python hand_gesture_recognition.py
) else if "%choice%"=="4" (
    echo.
    echo Starting demo...
    echo ========================================
    python demo_gesture_logic.py
    pause
) else if "%choice%"=="5" (
    echo Exiting...
) else (
    echo Invalid choice!
    pause
)
