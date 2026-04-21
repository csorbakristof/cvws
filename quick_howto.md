# Computer Vision Demos - Quick Start Guide

## Demo 1: Face Detection (C#)
**Setup:** `dotnet restore` → `dotnet build`  
**Run:** `dotnet run` (choose webcam or video)  
**Controls:** q=quit, +/- adjust sensitivity  
**Note:** Requires `haarcascade_frontalface_default.xml` in project dir

## Demo 2: Custom Object Recognition (Python)
**Setup:** `pip install -r requirements.txt`  
**Workflow:**
1. `python collect_training_data.py` - Capture 30+ images (SPACE to capture)
2. `python train_model.py` - Train model on collected data
3. `python detect_object.py` - Test real-time detection

**Tips:** Collect positive (target object) and negative (other objects) examples

## Demo 3: Video Effects (Python)
**Setup:** `pip install -r requirements.txt`  
**Run Options:**
- `python kaleidoscope_effect.py` - Main demo (+/- segments, z/x zoom, r reset)
- `python simple_effects.py` - Multi-effect switcher (0-4 switch effects, +/- strength)
- `python comparison_demo.py` - Side-by-side view

**Controls:** q=quit, numbers=switch effects

## Demo 4: Circle Detection (Python)
**Setup:** `pip install -r requirements.txt`  
**Run:** `python circle_detection.py` (optional: `--source video.mp4`)  
**Controls:** +/- sensitivity, k/j kernel size, r reset, s save, q quit  
**Best with:** Coins, bottle caps, balls on plain background

## Demo 5: Motion Detection (C#)
**Setup:** `dotnet restore`  
**Run:** `dotnet run` (choose webcam or video)  
**Controls:** +/- sensitivity, s toggle shadows, r reset background, k/j kernel, m/n min area, q quit  
**Views:** 2x2 grid showing original, background model, foreground mask, detected motion

---
**General Tips:**
- C# demos: Require .NET 6.0+, use `dotnet run`
- Python demos: Require Python 3.8+, install via `pip install -r requirements.txt`
- All demos: Press 'q' or ESC to quit
- Webcam required for most demos (except where video file option available)
