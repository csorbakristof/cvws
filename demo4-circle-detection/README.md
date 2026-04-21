# Demo 4 - Circle Detection with Image Preprocessing

This demo demonstrates a complete computer vision pipeline: preprocessing raw images, removing noise, and detecting circular shapes using OpenCV's Hough Circle Transform.

## Features

- **OTSU Thresholding** - Automatic binary conversion
- **Morphological Opening** - Noise removal while preserving shapes
- **Hough Circle Detection** - Find circles of various sizes
- **Multi-View Display** - See all processing steps simultaneously in 2x2 grid
- **Interactive Controls** - Adjust parameters in real-time
- **Real-time Processing** - Live webcam feed

## Requirements

- Python 3.8 or later
- Webcam
- Circular objects to detect (coins, bottle caps, balls, etc.)
- Good lighting and preferably a plain background

## Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `opencv-python` - Computer vision library
- `numpy` - Numerical computing

## Usage

### Basic Usage

Run with webcam (default):

```bash
python circle_detection.py
```

### Command-Line Options

```bash
# Use a video file
python circle_detection.py --source myvideo.mp4

# Adjust initial parameters
python circle_detection.py --kernel 7 --threshold 25 --min-radius 15 --max-radius 80

# For smaller objects
python circle_detection.py --min-radius 5 --max-radius 50

# For more sensitive detection
python circle_detection.py --threshold 20
```

**Parameters explained:**
- `--source`: Camera ID (0, 1, ...) or video file path
- `--kernel`: Morphological kernel size (default: 5, range: 3-15)
- `--threshold`: Detection sensitivity (default: 30, lower = more sensitive, range: 10-100)
- `--min-radius`: Minimum circle radius in pixels (default: 10)
- `--max-radius`: Maximum circle radius in pixels (default: 100)
- `--min-dist`: Minimum distance between circle centers (default: 50)

### Interactive Controls (During Execution)

- **+** or **=** - Increase detection sensitivity (finds more circles)
- **-** or **_** - Decrease detection sensitivity (fewer false positives)
- **k** - Increase kernel size (more noise removal)
- **j** - Decrease kernel size (less noise removal)
- **r** - Reset parameters to defaults
- **s** - Save current frame to file
- **q** or **ESC** - Quit

## Understanding the Display

The application shows 4 views simultaneously:

```
┌─────────────────┬─────────────────┐
│  1. Original    │  2. OTSU        │
│  (Webcam feed)  │  (Threshold)    │
├─────────────────┼─────────────────┤
│  3. Morph Open  │  4. Detected    │
│  (Noise remove) │  (With circles) │
└─────────────────┴─────────────────┘
```

### Quadrant 1: Original
- Raw webcam feed
- What the camera actually sees
- Color image as captured

### Quadrant 2: OTSU Threshold
- Binary image (black and white only)
- OTSU algorithm automatically finds optimal threshold
- Separates foreground (objects) from background
- White = potential objects, Black = background

### Quadrant 3: Morphological Opening
- Result after noise removal
- Small white specs are removed
- Larger shapes (circles) are preserved
- Cleaner than the thresholded image

### Quadrant 4: Detected Circles
- Original image with detected circles overlaid
- Green circles outline detected objects
- Red dots mark centers
- Blue numbers label each circle
- Shows count of detected circles

## How It Works

### The Processing Pipeline

```
Raw Image → Grayscale → OTSU Threshold → Morphological Opening → Circle Detection
```

**Step-by-step:**

1. **Grayscale Conversion**
   ```python
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   ```
   - Reduces 3 channels (RGB) to 1 (grayscale)
   - Simplifies processing
   - Faster computation

2. **OTSU Thresholding**
   ```python
   _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
   ```
   - Automatically finds optimal threshold value
   - Converts grayscale to binary (0 or 255)
   - Separates objects from background
   - OTSU = automatic, no manual threshold needed

3. **Morphological Opening**
   ```python
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
   ```
   - Opening = Erosion followed by Dilation
   - Removes small noise (salt noise)
   - Preserves larger shapes
   - Elliptical kernel works well for circular objects

4. **Hough Circle Detection**
   ```python
   circles = cv2.HoughCircles(opened, cv2.HOUGH_GRADIENT,
                              dp=1, minDist=50,
                              param1=50, param2=30,
                              minRadius=10, maxRadius=100)
   ```
   - Specialized algorithm for finding circles
   - Uses "voting" mechanism
   - Returns center (x, y) and radius for each circle
   - Parameters control sensitivity and size range

### Key Parameters

**Morphological Kernel Size:**
- Smaller (3x3): Less noise removal, faster
- Larger (7x7, 9x9): More noise removal, but may affect small circles
- Default 5x5 is usually optimal

**HoughCircles param2 (Accumulator Threshold):**
- Lower values (15-25): More sensitive, more detections, more false positives
- Higher values (35-50): Less sensitive, fewer false positives, might miss some circles
- Default 30 is a good starting point

**Radius Range:**
- Set based on expected object size
- Too narrow: miss valid circles
- Too wide: slower processing
- Measure objects in pixels to set appropriately

## Teaching Points

### 1. Image Processing Pipeline
Computer vision tasks often require multiple preprocessing steps. Each step solves a specific problem:
- Thresholding: Simplifies image
- Morphology: Removes noise
- Detection: Finds features

### 2. Why Preprocessing Matters
Try disabling steps to see the difference:
- Without thresholding: Detection is less reliable
- Without morphology: Noise causes false detections
- Together: Clean, accurate results

### 3. OTSU Thresholding
- Automatic threshold selection
- Based on histogram analysis
- Minimizes intra-class variance
- Works well for bimodal distributions (two distinct peaks)

### 4. Morphological Operations
- **Opening** = Erosion + Dilation
- Erosion: Shrinks white regions
- Dilation: Expands white regions
- Net effect: Removes small noise, keeps large shapes

### 5. Hough Transform
- Parametric curve detection
- Each edge point "votes" for possible circles
- Circles with most votes are detected
- Robust to noise and partial occlusion

## Tips for Best Results

### Lighting
- ✅ Good, even lighting
- ✅ Avoid shadows
- ✅ Consistent brightness
- ❌ Avoid backlighting
- ❌ Avoid very bright or very dark conditions

### Background
- ✅ Plain, uniform background (white paper, colored mat)
- ✅ High contrast with objects
- ❌ Avoid cluttered backgrounds
- ❌ Avoid patterns or textures

### Objects
- ✅ Clear, well-defined circles (coins, bottle caps, rings)
- ✅ Good contrast with background
- ✅ Multiple circles for demonstration
- ❌ Avoid overlapping circles
- ❌ Avoid partially visible circles at edges

### Camera
- ✅ Stable camera position
- ✅ Perpendicular view (top-down works great)
- ✅ Focus on object plane
- ❌ Avoid motion blur

## Troubleshooting

### No circles detected

**Problem:** Nothing is detected, even with obvious circles.

**Solutions:**
1. **Increase sensitivity:** Press `+` multiple times or use `--threshold 20`
2. **Check lighting:** Ensure good, even lighting
3. **Verify size range:** Use `--min-radius 5 --max-radius 150` for wider range
4. **Check threshold view:** Look at quadrant 2 - are circles visible as white regions?
5. **Reduce noise removal:** Press `j` to decrease kernel size
6. **Try plain background:** Use white paper under objects

### Too many false circles

**Problem:** Detecting circles that aren't there.

**Solutions:**
1. **Decrease sensitivity:** Press `-` several times or use `--threshold 40`
2. **Increase minimum distance:** Use `--min-dist 70`
3. **Narrow size range:** Set realistic min/max radius
4. **More noise removal:** Press `k` to increase kernel size
5. **Improve background:** Use cleaner, plainer background
6. **Better lighting:** Reduce shadows and reflections

### Circles detected but wrong size

**Problem:** Detection works but circles drawn are wrong size.

**Solutions:**
1. **Adjust radius range:** Measure your objects and set appropriate min/max
2. **Check perspective:** Camera should be perpendicular to objects
3. **Verify in code:** The detected radius is in pixels

### Poor threshold quality (Quadrant 2)

**Problem:** Thresholded image doesn't clearly show objects.

**Solutions:**
1. **Improve lighting:** More even, consistent lighting
2. **Try adaptive threshold:** Modify code to use `cv2.ADAPTIVE_THRESH_GAUSSIAN_C`
3. **Histogram equalization:** Add `gray = cv2.equalizeHist(gray)` before thresholding
4. **Adjust camera exposure:** Manual camera settings if available

### Low FPS / Slow performance

**Problem:** Processing is too slow, laggy display.

**Solutions:**
1. **Reduce resolution:** Camera captures smaller images (edit code)
2. **Smaller kernel:** Use 3x3 instead of 5x5 or larger
3. **Narrow search range:** Reduce min/max radius range
4. **Process every Nth frame:** Skip some frames (modify code)
5. **Close other applications:** Free up CPU resources

### Circles merge or split incorrectly

**Problem:** One circle detected as multiple or vice versa.

**Solutions:**
1. **Adjust minDist:** Increase if merging, decrease if splitting
2. **Better separation:** Physically separate objects more
3. **Tune param2:** Adjust threshold for better discrimination

## Real-World Applications

### Manufacturing & Quality Control
- **Bearing inspection:** Verify size and roundness
- **Gasket testing:** Check for defects in O-rings
- **Bottle cap counting:** Automated inventory
- **Hole detection:** PCB manufacturing verification

### Medical & Scientific
- **Cell counting:** Microscopy analysis
- **Particle detection:** Physics experiments
- **Tumor detection:** Circular lesions in medical imaging
- **Microorganism identification:** Circular bacteria colonies

### Robotics & Automation
- **Ball tracking:** Robot soccer, sports analysis
- **Coin sorting:** Vending machines, counting machines
- **Object grasping:** Identify circular objects to pick up
- **Navigation:** Detect circular markers or targets

### Agriculture
- **Fruit counting:** Estimate harvest (oranges, apples)
- **Plant disease:** Circular lesions on leaves
- **Seed counting:** Quality control in packaging

### Traffic & Safety
- **Traffic sign detection:** Circular speed limit signs
- **Wheel detection:** Vehicle counting and classification
- **Safety markers:** Detect circular warning markers

### Entertainment & Sports
- **Ball tracking:** Tennis, basketball, soccer analytics
- **Target detection:** Archery, darts scoring systems
- **Pool/billiards:** Ball tracking and game analysis

## Extension Ideas

### Beginner
1. **Add circle counter:** Display total count prominently
2. **Color-code circles:** Different colors for different sizes
3. **Measure diameters:** Show diameter/radius values
4. **Sound alerts:** Beep when circles detected/lost
5. **Save detections:** Log circle positions to CSV file

### Intermediate
6. **Track circles over time:** Assign IDs, track movement
7. **Size classification:** Small/medium/large categories
8. **Multiple video sources:** Compare different cameras
9. **Histogram display:** Show threshold histogram
10. **Parameter sliders:** GUI trackbars for all parameters

### Advanced
11. **Color-based filtering:** Detect only red circles, blue circles, etc.
12. **Ellipse detection:** Extend to detect ellipses/ovals
13. **3D position estimation:** Calculate real-world coordinates
14. **Machine learning classification:** CNN to verify circles
15. **Multi-shape detection:** Combine circles, rectangles, triangles
16. **Adaptive parameters:** Auto-tune based on scene conditions

## Code Customization Examples

### Change detection color

```python
# In the circle drawing section, replace:
cv2.circle(result_frame, (x, y), r, (0, 255, 0), 2)  # Green
# With:
cv2.circle(result_frame, (x, y), r, (255, 0, 255), 2)  # Magenta
```

### Add size filtering

```python
if circles is not None:
    for (x, y, r) in circles[0]:
        # Only draw circles with radius between 20-50
        if 20 <= r <= 50:
            cv2.circle(result_frame, (x, y), r, (0, 255, 0), 2)
```

### Try adaptive thresholding

```python
# Replace OTSU thresholding with:
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)
```

## Additional Resources

- [OpenCV Hough Circle Tutorial](https://docs.opencv.org/4.x/d4/d70/tutorial_hough_circle.html)
- [Morphological Operations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
- [OTSU Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
- [Understanding Hough Transform](https://en.wikipedia.org/wiki/Hough_transform)

---

**Happy Circle Hunting!** 🔵⭕🟢
