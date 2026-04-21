# Demo 5 - Motion Detection with MOG2

This demo demonstrates real-time motion detection using OpenCV's MOG2 (Mixture of Gaussians 2) background subtraction algorithm. The system learns what the background looks like and detects anything that moves or changes.

## Features

- **MOG2 Background Subtraction** - Adaptive background modeling
- **Shadow Detection** - Optional shadow filtering
- **Morphological Noise Removal** - Clean detection masks
- **Contour Detection** - Find boundaries of moving objects
- **Bounding Boxes** - Visual indicators around detected motion
- **Multi-View Display** - See all processing steps in 2x2 grid
- **Interactive Controls** - Adjust parameters in real-time
- **Real-time Processing** - Live webcam or video file input

## Prerequisites

- .NET 6.0 or later
- Webcam (for live detection) or video file
- Windows, Linux, or macOS

## Installation

1. **Install .NET SDK** (if not already installed)
   - Download from: https://dotnet.microsoft.com/download
   - Verify: `dotnet --version`

2. **Restore Dependencies**
   ```powershell
   cd demo5-motion-detection
   dotnet restore
   ```

## Running the Demo

### Using Webcam (Default)

```powershell
dotnet run
```

Then press `1` to use webcam.

### Using Video File

```powershell
dotnet run
```

Then press `2` and enter the video file path.

## Understanding the Display

The application shows 4 views simultaneously in a 2x2 grid:

```
┌─────────────────────┬─────────────────────┐
│  1. Original        │  2. Background      │
│  (Webcam feed)      │  (Learned model)    │
├─────────────────────┼─────────────────────┤
│  3. Foreground Mask │  4. Motion Detected │
│  (Motion pixels)    │  (With bounding box)│
└─────────────────────┴─────────────────────┘
```

### Panel 1: Original
- Raw video feed
- What the camera actually sees
- Color image as captured

### Panel 2: Background Model
- What MOG2 learned as the "static" background
- Updates continuously (adaptive learning)
- Shows what the scene looks like without motion

### Panel 3: Foreground Mask
- Binary image (white = motion, black = background)
- After noise removal and morphological operations
- Clean representation of detected motion

### Panel 4: Motion Detected
- Original image with green bounding boxes
- Each moving object gets a box and label
- Shows count, object ID, and area in pixels

## Interactive Controls

During execution, you can adjust parameters:

| Key | Action |
|-----|--------|
| `q` or `ESC` | Quit the application |
| `+` or `=` | Increase sensitivity (detect smaller motions) |
| `-` | Decrease sensitivity (ignore minor changes) |
| `s` | Toggle shadow detection ON/OFF |
| `r` | Reset background model (relearn from scratch) |
| `k` | Increase morphology kernel size (more noise removal) |
| `j` | Decrease morphology kernel size (preserve detail) |
| `m` | Increase minimum contour area (ignore small motions) |
| `n` | Decrease minimum contour area (detect smaller objects) |
| `SPACE` | Pause/Resume processing |

## How It Works

### The Processing Pipeline

```
Raw Frame → MOG2 Background Subtraction → Shadow Removal → Morphological Filtering → Contour Detection → Bounding Boxes
```

**Step-by-step:**

1. **Capture Frame**
   - Read frame from webcam or video file
   - Convert to appropriate format for processing

2. **MOG2 Background Subtraction**
   ```csharp
   var mog2 = BackgroundSubtractorMOG2.Create(
       history: 500,           // Frames used for background model
       varThreshold: 16,       // Sensitivity threshold
       detectShadows: true     // Enable shadow detection
   );
   mog2.Apply(frame, fgMask);
   ```
   - MOG2 maintains a statistical model of each pixel
   - Classifies each pixel as foreground (motion) or background (static)
   - Adapts to gradual changes (lighting, moving objects that stop)

3. **Shadow Removal** (Optional)
   ```csharp
   Cv2.Threshold(fgMask, fgMask, 127, 255, ThresholdTypes.Binary);
   ```
   - MOG2 detects shadows as gray pixels (value 127)
   - Thresholding removes shadows, keeping only real motion

4. **Morphological Filtering**
   ```csharp
   var kernel = Cv2.GetStructuringElement(MorphShapes.Ellipse, new Size(5, 5));
   Cv2.MorphologyEx(fgMask, fgMask, MorphTypes.Open, kernel);  // Remove noise
   Cv2.MorphologyEx(fgMask, fgMask, MorphTypes.Close, kernel); // Fill holes
   ```
   - **Opening**: Removes small white specs (noise)
   - **Closing**: Fills holes inside detected objects
   - Results in cleaner, more solid detection regions

5. **Contour Detection**
   ```csharp
   Cv2.FindContours(fgMask, out contours, out hierarchy,
                    RetrievalModes.External,
                    ContourApproximationModes.ApproxSimple);
   ```
   - Finds boundaries of white regions in the mask
   - Each contour represents one detected moving object

6. **Bounding Boxes and Visualization**
   ```csharp
   foreach (var contour in contours)
   {
       double area = Cv2.ContourArea(contour);
       if (area > minContourArea)
       {
           Rect bbox = Cv2.BoundingRect(contour);
           Cv2.Rectangle(result, bbox, new Scalar(0, 255, 0), 2);
       }
   }
   ```
   - Calculate area to filter out tiny motions
   - Draw green rectangles around each moving object
   - Add labels with object information

## Key Concepts

### 1. Background Subtraction
Motion detection works by comparing current frame to a background model:
- **Background**: What the scene normally looks like (static)
- **Foreground**: Anything different from the background (moving)
- MOG2 learns background over time, doesn't need pre-training

### 2. Mixture of Gaussians (MOG2)
- Each pixel modeled as mixture of Gaussian distributions
- Handles complex backgrounds (waving trees, water, reflections)
- Adapts to lighting changes automatically
- More robust than simple frame differencing

### 3. Adaptive Learning
- Background model updates continuously
- Objects that stop moving gradually become background
- Lighting changes are absorbed into the model
- **History parameter**: How many frames to remember (500 = ~16 seconds at 30fps)

### 4. Shadow Detection
- Shadows often trigger false motion detections
- MOG2 can identify shadows (appear darker than background but not completely different)
- Shadows marked as gray (127) in mask, real motion as white (255)
- Can be filtered out for cleaner results

### 5. Morphological Operations
- **Opening** = Erosion followed by Dilation
  - Removes small noise while preserving large shapes
- **Closing** = Dilation followed by Erosion
  - Fills small holes inside detected objects
- Essential for clean, reliable detection

### 6. Contour Analysis
- Contours = boundaries of connected regions
- Each contour typically represents one object
- Area filtering removes noise (tiny motions)
- Bounding rectangles simplify visualization

## Parameter Tuning

### Sensitivity (varThreshold)
- **Lower values (8-12)**: Very sensitive, detects small motions
  - Pro: Catches everything
  - Con: More false positives from noise
- **Medium values (16-20)**: Balanced (default = 16)
  - Good for most scenarios
- **Higher values (25+)**: Less sensitive, only obvious motion
  - Pro: Fewer false positives
  - Con: May miss subtle movements

### History (frames for background model)
- **Lower values (100-300)**: Fast adaptation
  - Quickly forgets old background
  - Good for dynamic scenes
- **Medium values (500)**: Standard adaptation (default)
  - ~16 seconds at 30fps
- **Higher values (1000+)**: Slow adaptation
  - Takes longer to learn/update background
  - Good for very static scenes

### Morphology Kernel Size
- **Smaller (3x3)**: Preserves detail
  - Good for detecting small objects
  - May leave some noise
- **Medium (5x5)**: Balanced (default)
- **Larger (9x9+)**: Strong noise removal
  - Very clean masks
  - May lose small objects

### Minimum Contour Area
- **Smaller (100-300)**: Detect tiny motions
  - Picks up finger movements, small objects
  - More false positives
- **Medium (500)**: Balanced (default)
- **Larger (1000+)**: Only large objects
  - Ignore small motions
  - Good for people/vehicle detection

## Troubleshooting

### Everything is Detected as Motion
- **Cause**: Background model not initialized yet
- **Solution**: Wait 2-3 seconds for the model to learn
- **Alternative**: Ensure camera is stable (not shaking)

### Nothing is Detected
- **Cause**: Sensitivity too low, motion too slow, or object color similar to background
- **Solution**: 
  - Press `+` to increase sensitivity
  - Verify object is actually moving
  - Check lighting conditions

### Too Many False Detections
- **Cause**: Noise, lighting changes, or shadows
- **Solution**:
  - Press `-` to decrease sensitivity
  - Press `k` to increase kernel size (more noise removal)
  - Press `m` to increase minimum area
  - Press `s` to enable shadow detection
  - Improve lighting conditions

### Shadows Detected as Motion
- **Cause**: Shadow detection disabled or shadows very strong
- **Solution**:
  - Press `s` to enable shadow detection
  - Improve lighting (diffuse light, no harsh shadows)
  - Increase varThreshold to ignore weak differences

### Stationary Objects Not in Background
- **Cause**: Learning rate too slow or background recently reset
- **Solution**:
  - Wait longer (object becomes background after ~history frames)
  - Press `r` to reset and rebuild background model
  - Ensure camera is completely stable

### Low FPS / Slow Performance
- **Cause**: High resolution video or slow hardware
- **Solution**:
  - Use lower resolution webcam or resize frames
  - Reduce morphology kernel size
  - Process every other frame instead of every frame
  - Close other applications

## Real-World Applications

This technology is used in:

- **Security Systems**: Detect intruders, monitor restricted areas, trigger alarms
- **Smart Buildings**: Automatic lighting, occupancy detection, energy management
- **Retail Analytics**: Count customers, analyze foot traffic, dwell time measurement
- **Traffic Monitoring**: Vehicle counting, congestion detection, accident alerts
- **Parking Systems**: Detect available spots, enforce parking rules, automated gates
- **Wildlife Research**: Camera traps for animal detection, conservation studies
- **Industrial Safety**: Detect unauthorized access to dangerous zones
- **Healthcare**: Fall detection for elderly, patient movement monitoring
- **Sports Analysis**: Track player movement, automatic camera following
- **Home Automation**: Smart doorbells, security cameras, pet detection

## Extension Ideas

### For Learning
1. **Object Counting** - Count how many objects cross a virtual line
2. **Motion History** - Show trail of motion over time (heat map)
3. **Zone Monitoring** - Define specific regions, alert only for motion in those zones
4. **Direction Detection** - Determine if objects moving left/right/up/down
5. **Size Classification** - Categorize detected objects by size (small/medium/large)

### Advanced
6. **Object Tracking** - Assign persistent IDs, track same object across frames
7. **Speed Estimation** - Calculate velocity of moving objects
8. **Multi-Camera System** - Combine feeds from multiple cameras
9. **Event Recording** - Save video clips only when motion detected (save storage)
10. **Alert System** - Send notifications/emails when motion detected

## Comparison with Other Methods

### MOG2 vs. Simple Frame Differencing
- **Frame Diff**: Subtract consecutive frames
  - Pro: Very fast and simple
  - Con: Detects edges of motion, not entire object; sensitive to camera shake
- **MOG2**: Statistical background model
  - Pro: Detects entire moving object; robust to lighting changes
  - Con: Slightly slower; requires initialization period

### MOG2 vs. MOG (Original)
- **MOG**: Original Mixture of Gaussians algorithm
  - Older, simpler version
- **MOG2**: Improved version (recommended)
  - Better performance and accuracy
  - Adaptive learning rate
  - Built-in shadow detection

### MOG2 vs. Object Detection (YOLO, etc.)
- **MOG2**: "Is something moving?" (doesn't identify what)
  - Pro: Fast, simple, real-time on any hardware
  - Con: Can't identify object types
- **Object Detection**: "What objects are present?" (identifies specific things)
  - Pro: Knows what objects are (person, car, dog, etc.)
  - Con: Slower, requires more processing power
- **Best Practice**: Combine both - use MOG2 to detect motion, then run object detection only on moving regions

## Educational Value

This demo teaches:

1. **Background Subtraction** - Core concept in video analysis
2. **Statistical Modeling** - How algorithms learn patterns
3. **Adaptive Systems** - Systems that adjust to changing conditions
4. **Real-time Processing** - Handling continuous video streams
5. **Morphological Operations** - Image processing fundamentals
6. **Contour Analysis** - Shape detection and measurement
7. **Parameter Tuning** - Balancing sensitivity vs. false positives

## Technical Notes

- **Performance**: MOG2 is efficient, runs real-time on modern hardware
- **Memory**: Background model stored in memory, relatively lightweight
- **Initialization**: First ~2 seconds build initial background model
- **Thread Safety**: Create separate MOG2 instance for each thread/video stream
- **Video Codecs**: Supports any video format OpenCV can read

## References

- [OpenCV Documentation - BackgroundSubtractorMOG2](https://docs.opencv.org/master/d7/d7b/classcv_1_1BackgroundSubtractorMOG2.html)
- [Original MOG2 Paper](https://www.zoranz.net/Publications/zivkovic2006.pdf) - Zivkovic, Z. (2006)
- [Background Subtraction Tutorial](https://docs.opencv.org/master/d1/dc5/tutorial_background_subtraction.html)

## License

This demo is for educational purposes. Feel free to modify and experiment!
