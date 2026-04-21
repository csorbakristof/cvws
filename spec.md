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

