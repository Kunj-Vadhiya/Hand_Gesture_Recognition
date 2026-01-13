# Quick Start Guide

## 🚀 Get Started in 2 Steps

### Step 1: Install Dependencies
```bash
cd "G:\ML\Hand Gestures Recognition"
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python hand_gesture_recognition.py
```

Or simply double-click: `run.bat`

## ✅ Compatibility
- Works with Python 3.7+ including Python 3.13
- Automatic compatibility patch for MediaPipe on Python 3.13+
- Requires webcam for hand detection

---

## 📸 What to Expect

### When Running Successfully:

1. **Window Opens**: "Hand Gesture Recognition"
2. **Camera Activates**: Live video feed
3. **Show Your Hand**: Palm facing camera
4. **See Magic Happen**:
   - Green/red dots on your hand (landmarks)
   - Lines connecting dots (hand skeleton)
   - "FPS: 25" (top-left)
   - "Hand 1: Peace" (if you show ✌️)
   - "Command: Next" (below gesture name)

### Console Output:
```
Hand Gesture Recognition System Started
==================================================
Supported Gestures:
  - Fist: All fingers closed
  - Open Palm: All fingers extended
  - Thumbs Up: Only thumb extended
  - Peace: Index and middle fingers extended
  - Pointing: Only index finger extended
==================================================

[Hand 1 - Right] Gesture: Peace -> Command: Next
[Hand 2 - Left] Gesture: Open Palm -> Command: Activate
```

---

## 🎯 Gesture Cheat Sheet

```
FIST            OPEN PALM       THUMBS UP
  👊               🖐️              👍

[0,0,0,0,0]    [1,1,1,1,1]    [1,0,0,0,0]


PEACE           POINTING        ROCK
  ✌️              👆              🤟

[0,1,1,0,0]    [0,1,0,0,0]    [0,1,0,0,1]
```

Legend: [thumb, index, middle, ring, pinky]
- 0 = closed
- 1 = open

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| Q | Quit application |
| E | Toggle low-light enhancement |
| ESC | Also exits |

---

## 🔧 Troubleshooting

### "AttributeError: function 'free' not found"
**Solution**: You're using Python 3.13. Install Python 3.11.

### "Could not open webcam"
**Solutions**:
- Check camera is connected
- Close other apps using camera (Zoom, Teams, etc.)
- Try `camera_index=1` or `2` in code

### "Poor detection / No hand detected"
**Solutions**:
- Press 'E' to enable low-light mode
- Move hand closer (30-100cm)
- Ensure good lighting
- Show palm clearly to camera

### "Low FPS"
**Solutions**:
- Close other applications
- Disable low-light mode
- Reduce `max_hands` to 1

---

## 📂 Files Explained

| File | Purpose | Run It? |
|------|---------|---------|
| `hand_gesture_recognition.py` | Main system | ✅ Yes (needs camera + Python 3.11) |
| `demo_gesture_logic.py` | Simple demo | ✅ Yes (works on any Python) |
| `test_system.py` | Check setup | ✅ Yes |
| `test_gesture_logic.py` | Unit tests | ⚠️ Needs Python 3.11 |
| `README.md` | Full docs | 📖 Read |
| `SETUP_GUIDE.md` | Setup help | 📖 Read if issues |
| `PROJECT_SUMMARY.md` | Overview | 📖 Read for details |
| `requirements.txt` | Dependencies | 📦 For pip install |

---

## 💡 Pro Tips

1. **Best Lighting**: Natural daylight or bright indoor lighting
2. **Hand Position**: 40-60cm from camera, palm facing forward
3. **Background**: Plain wall works best
4. **Stability**: Hold gesture for 2-3 frames for recognition
5. **Multi-Hand**: Both hands work independently

---

## 🎓 Learning Path

### Beginner:
1. Run `demo_gesture_logic.py` - see the algorithm
2. Read the algorithm explanation
3. Understand finger state detection

### Intermediate:
1. Run `hand_gesture_recognition.py` with camera
2. Try different gestures
3. Observe landmark drawing

### Advanced:
1. Modify gesture patterns in `classify_gesture()`
2. Add custom gestures
3. Adjust stability parameters
4. Implement new actions

---

## 🎉 You're All Set!

The system is complete and ready to use. Just need Python 3.11 for full functionality.

**Quick Demo** (works now):
```bash
python demo_gesture_logic.py
```

**Full System** (needs Python 3.11):
```bash
python hand_gesture_recognition.py
```

---

## 📞 Need Help?

1. Check `SETUP_GUIDE.md` for detailed solutions
2. See `README.md` for complete documentation  
3. Run `python test_system.py` to diagnose issues

**Happy Gesture Recognizing! 🖐️✨**
