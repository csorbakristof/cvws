# Overview

I want to create a 45 minutes, demo-centric class for secondary school students about computer vision. They are IT related students so source code (mainly Python and C#) is important for them.

# Areas covered

Additional ideas: social media effects: kaleidoscope (teach coordinate geometry), hopponálás; cc zaj th morph, és watershet

## Priority-Ordered Topics

### High Priority (Core Demos)

1. **Face Detection and Recognition**
   - Most relatable - students use this daily (phone unlock, social media filters)
   - Highly visual and immediate impact
   - Easy to demonstrate live with webcam
   - Multiple libraries available (OpenCV, dlib, face_recognition)

2. **Object Detection and Classification**
   - Practical applications students understand (autonomous vehicles, surveillance)
   - Can demo with everyday objects in classroom
   - Pre-trained models (YOLO, MobileNet) allow quick setup
   - Real-time detection is very engaging

3. **Image Filters and Effects**
   - Fun and creative - like Instagram/Snapchat/TikTok filters
   - Immediate visual feedback
   - Students can see code-to-result connection clearly
   - Easy to implement basic filters (blur, edge enhancement, color manipulation)

### Medium Priority (Time Permitting)

4. **Text Recognition (OCR)**
   - Clear practical value (digitizing documents, reading signs)
   - Can demo with printed text, handwriting, or signs in classroom
   - Tesseract library makes it accessible
   - Combines with other CV tasks (document scanning apps)

5. **Pose and Gesture Recognition**
   - Highly interactive and engaging
   - Gaming and AR applications resonate with students
   - MediaPipe makes implementation straightforward
   - Good for demonstrating real-time CV applications

6. **Color Detection and Tracking**
   - Simple concept but powerful applications
   - Can build simple games or interactive demos
   - Foundation for more complex tracking systems
   - Easy entry point for understanding CV pipelines

### Lower Priority (Brief Mentions/Future Learning)

7. **Image Segmentation**
   - More technical but impressive results
   - Medical imaging and photo editing applications
   - Can show pre-trained model results without deep technical detail

8. **Edge Detection**
   - Fundamental CV concept
   - Good for understanding how computers "see" shapes
   - Quick to demonstrate with Canny or Sobel operators

9. **Motion Detection and Video Analysis**
   - Security systems, sports analysis applications
   - Can integrate into demos of other topics
   - Background subtraction is conceptually accessible

10. **Augmented Reality Basics**
    - Highly motivating - links to games and social media
    - Combines multiple CV techniques
    - Can show simple marker-based AR examples

## Recommended Demo Flow

For a 45-minute session, focus on **High Priority items (1-3)** with live coding or prepared demos showing:
- Python examples using OpenCV, face_recognition, or MediaPipe
- C# examples using OpenCvSharp or ML.NET
- Real-time webcam demonstrations where possible
- Pre-trained models to avoid lengthy training discussions

# Demo details

## Demo 1 - pre-trained face detection

### Objective
Demonstrate how pre-trained models work in computer vision without needing to train anything yourself. Show real-time face detection to hook students' interest immediately.

### Technology Stack
- **Language**: C# (.NET 6+)
- **Library**: OpenCvSharp4 (OpenCV wrapper for C#)
- **Pre-trained Model**: Haar Cascade classifier (haarcascade_frontalface_default.xml)

### Setup Requirements
- Webcam connected to presentation computer
- Backup: pre-recorded video file with multiple faces (classroom scene, group photo, etc.)
- Prepare for lighting issues - have backup video ready

### Demo Flow (5-7 minutes)

1. **Introduction (30 seconds)**
   - "Let's see if the computer can find faces in real-time"
   - Show the application window before starting

2. **Live Webcam Detection (2-3 minutes)**
   - Start the application with webcam input
   - Show real-time face detection with bounding boxes
   - Move around to show tracking works at different distances
   - Have a student volunteer come up (if willing) to show it works for different people
   - Point out the green rectangles appearing around detected faces

3. **Code Walkthrough (2-3 minutes)**
   - Show the C# code structure:
     - Loading the Haar Cascade classifier
     - Capturing video frames from webcam
     - Converting to grayscale (explain why: faster processing)
     - Calling DetectMultiScale method
     - Drawing rectangles around detected faces
   - Emphasize how little code is needed (20-30 lines)
   - Highlight that the "intelligence" is in the pre-trained model file

4. **Demonstrate Parameters (1 minute)**
   - Adjust scaleFactor parameter to show effect on detection sensitivity
   - Adjust minNeighbors to show false positive reduction
   - Show how these tuning parameters affect performance vs accuracy

5. **Fallback to Video (if webcam fails)**
   - Switch to pre-recorded video input
   - Show the same code works with minimal changes (just source input)

### Key Teaching Points
- Pre-trained models save enormous time and effort
- Computer vision often processes frames in grayscale to reduce complexity
- Real-time processing requires balancing accuracy and speed
- Same code can work with different input sources (webcam, video, images)
- Haar Cascades are older technology but fast and still useful

### Potential Discussion Questions
- Where do you see face detection in daily life? (phones, cameras, social media)
- Why might it fail? (side profiles, occlusion, poor lighting)
- What are privacy implications?

### Technical Notes
- Frame rate target: 20-30 FPS for smooth real-time demo
- If performance issues: reduce webcam resolution or frame size
- Have the cascade XML file in the project resources or local directory

## Demo 2 - training to recognize an object

### Objective
Show students that they can train a computer vision model themselves using simple tools and everyday objects. Demonstrate the complete pipeline from data collection to recognition.

### Technology Stack
- **Language**: Python (more accessible for ML tasks)
- **Library**: OpenCV for image processing, scikit-learn or TensorFlow/Keras for simple classification
- **Alternative**: Teachable Machine by Google (no-code option for quick demo)
- **Object**: A distinctive classroom item (water bottle, specific book, mascot, etc.)

### Setup Requirements
- Collection of 30-50 photos of the target object from different angles
- Collection of 30-50 "negative" photos (other objects, empty background)
- Photos should be prepared beforehand but show students the collection process
- Webcam or phone for demonstrating how photos were captured

### Demo Flow (8-10 minutes)

1. **Introduction: The Problem (1 minute)**
   - "What if we want to detect something specific that isn't in pre-trained models?"
   - Show the target object (e.g., a distinctive water bottle with unique branding)
   - "Let's teach the computer to recognize THIS specific bottle"

2. **Show Training Data (2 minutes)**
   - Display folder with positive examples (object from different angles, lighting, backgrounds)
   - Display folder with negative examples (other objects, empty scenes)
   - Explain why diversity matters: different angles, distances, lighting conditions
   - Show example of taking a new photo with webcam/phone to add to dataset
   - Emphasize: "The more examples, the better the model learns"

3. **Training Process (3-4 minutes)**
   - **Option A - Traditional ML approach:**
     - Show code that extracts features (color histograms, edge patterns)
     - Train a simple classifier (SVM or Random Forest)
     - Display training accuracy metrics
   - **Option B - Transfer Learning approach:**
     - Use pre-trained MobileNet as feature extractor
     - Add simple classifier on top
     - Show training progress (epochs, accuracy improvement)
   - **Option C - Teachable Machine (fastest):**
     - Quickly train model in browser interface
     - Export and use in Python
   - Run training (should complete in 10-30 seconds for quick demo)
   - Show accuracy/confidence metrics

4. **Testing the Model (2-3 minutes)**
   - Hold up the target object to webcam
   - Show real-time classification with confidence score
   - Hold up different objects to show it correctly rejects them
   - Show how confidence changes with object distance/angle
   - Test with a similar but different object (e.g., different bottle) to show discrimination

5. **Discuss Results (1 minute)**
   - When does it work well? When does it struggle?
   - What would improve it? (more training data, better variety)

### Key Teaching Points
- Machine learning models learn from examples, not explicit programming
- Training data quality matters more than quantity (diverse examples)
- Need both positive examples (what to find) and negative examples (what to ignore)
- Confidence scores indicate how "sure" the model is
- Models can be retrained and improved with more data
- Transfer learning lets us use powerful pre-trained models as a foundation

### Potential Discussion Questions
- What objects would be easy vs. hard to recognize? Why?
- How is this different from face detection? (generic vs specific)
- Where could custom object recognition be useful? (manufacturing defects, sorting recyclables, finding lost items)
- What could go wrong? (biased training data, overfitting to backgrounds)

### Technical Notes
- Pre-train the model before class to have a working backup
- Keep training time under 30 seconds for demo purposes
- If using deep learning, use a small model (MobileNet) for speed
- Image size: resize to 224x224 or smaller for faster processing
- Have the trained model saved as a file to show it can be reused

### Variations/Extensions
- Could do live training during class if time permits (more engaging but risky)
- Could prepare multiple models (e.g., recognizing different students' items)
- Could show misclassification examples to discuss limitations

## Demo 3 - video effects

### Objective
Show the creative and fun side of computer vision. Demonstrate how pixel manipulation and geometric transformations create effects students see on social media daily.

### Technology Stack
- **Language**: Python (easier for quick experimentation)
- **Library**: OpenCV (cv2)
- **Key Function**: cv2.remap() for geometric transformations
- **Input**: Webcam feed or video file

### Setup Requirements
- Webcam for live effect application
- Backup pre-recorded video (person moving, talking)
- Simple GUI window to show real-time results

### Demo Flow (7-9 minutes)

1. **Introduction: Effects We Know (1 minute)**
   - "You've all seen filters on Instagram, TikTok, Snapchat..."
   - Show example screenshots of kaleidoscope/mirror effects from social media
   - "Let's create our own video effect from scratch"

2. **Simple Effect First: Mirror Effect (2 minutes)**
   - Start with something simple to build understanding
   - Show live webcam feed split vertically with mirrored right side
   - **Code walkthrough:**
     - Capture frame from webcam
     - Split frame in half
     - Flip one half horizontally
     - Combine them back
   - Show the ~5-10 lines of code needed
   - Let students see themselves in the mirror effect

3. **Main Demo: Kaleidoscope Effect (3-4 minutes)**
   - Apply kaleidoscope transformation to webcam feed
   - Show the mesmerizing, symmetrical pattern effect
   - Move hand/face to show how motion creates dynamic patterns
   - **Explain the concept:**
     - Image is divided into triangular sections
     - Each section is copied, rotated, and mirrored
     - Creates radial symmetry (like looking into a kaleidoscope toy)
   - **Code structure:**
     - Create coordinate maps (mapX, mapY) that define where each output pixel comes from
     - Use cv2.remap() to apply the transformation
     - Process each frame in real-time

4. **Show the Math Behind It (1-2 minutes)**
   - Display the coordinate transformation code
   - Explain in simple terms: "For each pixel in output, we calculate which pixel to copy from input"
   - Show the polar coordinate conversion (cartesian to polar, apply symmetry, back to cartesian)
   - Show parameters that can be adjusted (number of segments, rotation angle)

5. **Live Experimentation (1-2 minutes)**
   - Adjust parameters in real-time if possible:
     - Change number of kaleidoscope segments (4, 6, 8, 12)
     - Rotate the pattern
     - Zoom in/out
   - Show how small code changes create dramatic visual differences

6. **Bonus Effects (if time permits, 1 minute)**
   - Quickly show other geometric effects:
     - Fish-eye lens distortion
     - Barrel distortion
     - Swirl effect
   - All use the same cv2.remap() approach with different coordinate mappings

### Key Teaching Points
- Images are just 2D arrays of numbers (pixels)
- Geometric transformations are about moving pixels around
- cv2.remap() is a powerful general-purpose transformation tool
- Coordinate mapping lets you create any geometric effect
- Real-time video is just processing images very fast (30+ times per second)
- The same techniques power professional video editing and AR filters

### Potential Discussion Questions
- What other effects could you create with pixel manipulation?
- How do apps like Snapchat do face filters? (combination: face detection + geometric transformation)
- What's the difference between geometric effects and color effects?
- Could you apply multiple effects in sequence? (yes - effect pipeline)

### Code Structure Overview
```
1. Setup webcam capture
2. Create transformation maps (pre-computed for efficiency)
   - Calculate for each output pixel: which input pixel to sample
   - Store in mapX and mapY arrays
3. Main loop:
   - Read frame from webcam
   - Apply cv2.remap(frame, mapX, mapY, interpolation)
   - Display result
   - Check for exit key
4. Cleanup
```

### Technical Notes
- Pre-compute the coordinate maps (mapX, mapY) before the loop for performance
- Use cv2.INTER_LINEAR for interpolation (good balance of quality and speed)
- Target 25-30 FPS for smooth real-time effect
- Frame size: 640x480 is sufficient for demo (smaller = faster processing)
- If performance issues: reduce resolution or use cv2.INTER_NEAREST

### Extension Ideas
- Students could modify number of segments as a variable
- Add rotation animation over time
- Combine multiple effects
- Add color filters on top of geometric transforms

### Connection to Real Applications
- Social media filters (Instagram, Snapchat, TikTok)
- Video conferencing backgrounds (Zoom, Teams)
- Video editing software
- Artistic visualization tools
- VR/AR distortion correction (opposite direction)

## Demo 4 - circle detection with image preprocessing

### Objective
Demonstrate a complete image processing pipeline: from raw input through noise removal to feature detection. Show how preprocessing steps (thresholding, morphology) improve detection quality. Teach the importance of each processing stage by visualizing intermediate results.

### Technology Stack
- **Language**: Python (best for image processing demonstrations)
- **Library**: OpenCV (cv2)
- **Key Functions**: 
  - cv2.threshold() with THRESH_OTSU for automatic thresholding
  - cv2.morphologyEx() with MORPH_OPEN for noise removal
  - cv2.HoughCircles() for circle detection
- **Input**: Webcam feed

### Setup Requirements
- Webcam for live detection
- Circular objects to detect (coins, bottle caps, circular stickers, balls)
- Good lighting conditions (important for thresholding)
- Plain background (helps with detection)

### Demo Flow (7-9 minutes)

1. **Introduction: Finding Shapes (1 minute)**
   - "Computers can find specific shapes, not just objects"
   - Show circular objects (coins, bottle cap, ball)
   - "Let's teach the computer to find circles"
   - Explain real-world use: quality control, counting objects, coin recognition

2. **Show Raw Detection First (1 minute)**
   - Run HoughCircles directly on the webcam feed (grayscale only)
   - Show that it detects many false circles due to noise
   - Point out the problem: too many detections, unreliable
   - "We need to clean up the image first!"

3. **Step 1: OTSU Thresholding (2 minutes)**
   - Convert frame to grayscale
   - Apply OTSU thresholding to create binary image (black and white only)
   - **Explain OTSU:**
     - Automatically finds the best threshold value
     - Separates foreground (objects) from background
     - Creates clean binary image
   - Show the thresholded result in a separate window
   - Point out how the image is now only black and white
   - Discuss: "Threshold = separating light from dark"

4. **Step 2: Morphological Opening (2 minutes)**
   - Apply morphological "open" operation (erosion followed by dilation)
   - **Explain morphology:**
     - Opening = erosion + dilation
     - Removes small white noise spots
     - Preserves larger shapes (our circles)
     - Like a filter that removes "salt" noise
   - Show the noise-removed result in another window
   - Compare: thresholded (noisy) vs. opened (clean)
   - Students can see the small specs disappear

5. **Step 3: Circle Detection (2 minutes)**
   - Apply HoughCircles to the cleaned binary image
   - **Explain Hough Transform:**
     - Finds circular patterns in the image
     - Parameters: min/max radius, sensitivity
     - Returns center (x, y) and radius for each circle
   - Draw detected circles on the original color frame
   - Show circles with green outlines and center dots
   - Add text showing number of circles found

6. **Live Multi-View Display (1-2 minutes)**
   - Show all stages simultaneously in a 2x2 grid:
     - Top-left: Original webcam feed
     - Top-right: Thresholded binary image
     - Bottom-left: After morphological opening
     - Bottom-right: Original with detected circles overlaid
   - Move circular objects in and out of frame
   - Show how circles are detected in real-time
   - Demonstrate: covers/uncovers circles, changes positions

### Key Teaching Points

1. **Image Processing Pipeline**
   - Computer vision often needs multiple steps
   - Each step solves a specific problem
   - Pipeline: Input → Preprocessing → Feature Detection → Output
   - Preprocessing quality directly affects detection accuracy

2. **Thresholding Concepts**
   - Converts grayscale to binary (simplifies the image)
   - OTSU method automatically finds optimal threshold
   - Reduces 256 gray levels to just 2 (black/white)
   - Makes shape detection easier and faster

3. **Morphological Operations**
   - Opening = erosion followed by dilation
   - Removes noise while preserving shape
   - Like a smart filter that knows what to remove
   - Essential preprocessing step in many CV applications

4. **Hough Circle Transform**
   - Specialized algorithm for finding circles
   - Works by "voting" for possible circle centers
   - Parameters control sensitivity vs. false positives
   - Can detect multiple circles simultaneously

5. **Visualization for Understanding**
   - Showing intermediate steps is crucial for learning
   - Each window reveals what happens inside the algorithm
   - Helps debug when things don't work
   - Professional CV development uses similar visualization

### Potential Discussion Questions

1. **Why do we need preprocessing?**
   - Raw images have noise, shadows, varying brightness
   - Preprocessing makes detection more reliable
   - Trade-off: processing time vs. accuracy

2. **What happens if we skip steps?**
   - Skip thresholding: detection on grayscale is less reliable
   - Skip morphology: noise causes false detections
   - Show by temporarily disabling each step

3. **What other shapes could we detect?**
   - Lines (Hough Line Transform)
   - Rectangles (contour analysis)
   - Arbitrary shapes (template matching)
   - Faces (back to Demo 1!)

4. **Real-world applications?**
   - Manufacturing: quality control (checking circular parts)
   - Medicine: detecting cells, tumors in microscopy
   - Robotics: ball tracking for robot soccer
   - Coin counting machines
   - Traffic: detecting circular traffic signs

### Code Structure Overview

```python
# 1. Initialize webcam
cap = cv2.VideoCapture(0)

# 2. Main loop
while True:
    # Read frame
    ret, frame = cap.read()
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Step 1: OTSU thresholding
    _, thresh = cv2.threshold(gray, 0, 255, 
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Step 2: Morphological opening (remove noise)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Step 3: Detect circles
    circles = cv2.HoughCircles(opened, cv2.HOUGH_GRADIENT,
                               dp=1, minDist=50,
                               param1=50, param2=30,
                               minRadius=10, maxRadius=100)
    
    # Draw circles on original frame
    if circles is not None:
        for (x, y, r) in circles[0]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
    
    # Create 2x2 grid display
    top_row = np.hstack([frame, cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)])
    bottom_row = np.hstack([cv2.cvtColor(opened, cv2.COLOR_GRAY2BGR), 
                            frame_with_circles])
    display = np.vstack([top_row, bottom_row])
    
    # Show result
    cv2.imshow('Circle Detection Pipeline', display)
```

### Technical Notes

- **Lighting is critical**: Good lighting improves thresholding significantly
- **Kernel size**: 5x5 is good for most cases; adjust based on noise level
- **HoughCircles parameters**:
  - `dp=1`: inverse ratio of accumulator resolution
  - `minDist=50`: minimum distance between circle centers
  - `param1=50`: Canny edge threshold
  - `param2=30`: accumulator threshold (lower = more circles detected)
  - `minRadius/maxRadius`: expected circle size range
- **Performance**: Processing steps add computation time; optimize kernel sizes
- **Alternative**: Can use adaptive thresholding instead of OTSU for varying lighting

### Extension Ideas

**For Students:**
1. **Adjust parameters interactively** - Add trackbars for threshold, kernel size, Hough parameters
2. **Count objects** - Display count of detected circles
3. **Measure circles** - Show diameter/radius in pixels or real-world units
4. **Color-based detection** - Detect only red circles, blue circles, etc.
5. **Track circles over time** - Assign IDs and track movement

**Advanced:**
6. **Compare with other methods** - Try different thresholding (adaptive, simple)
7. **Different shapes** - Modify to detect rectangles, triangles
8. **Size-based filtering** - Classify circles as small/medium/large
9. **Combine with Demo 1** - Detect circles only on detected faces (find eyes!)
10. **Save detections** - Log circle positions and sizes to file

### Troubleshooting

**No circles detected:**
- Check lighting conditions (too bright or too dark)
- Verify circular objects are in frame
- Reduce `param2` parameter (makes detection more sensitive)
- Increase `maxRadius` if objects are large
- Background might be too cluttered - use plain background

**Too many false circles:**
- Increase `param2` parameter (stricter detection)
- Increase `minDist` (prevent overlapping detections)
- Adjust `minRadius/maxRadius` to expected size range
- Improve lighting or increase morphology kernel size

**Thresholding doesn't work well:**
- Try adaptive thresholding instead of OTSU
- Adjust lighting conditions
- Use histogram equalization before thresholding

**Low FPS:**
- Reduce frame resolution
- Use smaller morphology kernel
- Process every other frame instead of every frame
- Limit search range for HoughCircles

### Connection to Real Applications

- **Industrial Quality Control**: Detecting defects in circular parts (bearings, gaskets, washers)
- **Medical Imaging**: Cell counting, tumor detection in microscopy
- **Robotics**: Ball tracking for robot soccer, autonomous navigation
- **Coin Recognition**: Automatic coin counting and sorting machines
- **Traffic Systems**: Detecting circular traffic signs
- **Agriculture**: Counting fruits (oranges, apples) for harvest estimation
- **Sports Analytics**: Ball tracking in tennis, soccer, basketball
- **Scientific Research**: Particle detection and analysis in physics experiments

