# Demo 1 - Pre-trained Face Detection

This demo shows real-time face detection using OpenCV's Haar Cascade classifier in C#.

## Features

- Real-time face detection from webcam
- Alternative: Load and process video files
- Interactive parameter adjustment (+ and - keys)
- Display of FPS and detection statistics
- Visual feedback with green bounding boxes

## Requirements

- .NET 6.0 SDK or later
- Webcam (optional, can use video file instead)
- Windows OS (OpenCvSharp4.runtime.win package)

## Setup Instructions

### 1. Download the Haar Cascade File

Download the pre-trained face detection model:

```
https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
```

Save it as `haarcascade_frontalface_default.xml` in the same directory as the project.

Or use this direct download link:
```
https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
```

### 2. Restore NuGet Packages

```bash
dotnet restore
```

### 3. Build the Project

```bash
dotnet build
```

### 4. Run the Demo

```bash
dotnet run
```

## Usage

When you run the program:

1. Choose input source:
   - Option 1: Webcam (default)
   - Option 2: Video file (you'll be prompted for the path)

2. Once the video window opens:
   - **Press 'q'** or **ESC** to quit
   - **Press '+'** to increase detection sensitivity (more detections, possible false positives)
   - **Press '-'** to decrease detection sensitivity (fewer false positives, might miss some faces)

## How It Works

### Key Concepts

1. **Haar Cascade Classifier**: A pre-trained machine learning model that can detect faces. It was trained on thousands of positive (faces) and negative (non-faces) images.

2. **Grayscale Conversion**: The image is converted to grayscale before processing because:
   - Reduces data to process (1 channel instead of 3)
   - Face detection doesn't need color information
   - Faster processing = higher FPS

3. **Detection Parameters**:
   - `scaleFactor` (1.1): How much the image size is reduced at each scale. Lower = more thorough but slower.
   - `minNeighbors` (4): How many neighbors each candidate rectangle should have to retain it. Higher = fewer false positives but might miss faces.

### Code Structure

```csharp
// 1. Load the pre-trained Haar Cascade classifier
var faceCascade = new CascadeClassifier("haarcascade_frontalface_default.xml");

// 2. Open video capture (webcam or file)
var capture = new VideoCapture(0); // 0 = default webcam

// 3. Process each frame
while (true)
{
    // Read frame
    capture.Read(frame);
    
    // Convert to grayscale
    Cv2.CvtColor(frame, gray, ColorConversionCodes.BGR2GRAY);
    
    // Detect faces
    var faces = faceCascade.DetectMultiScale(gray, scaleFactor, minNeighbors);
    
    // Draw rectangles around detected faces
    foreach (var face in faces)
    {
        Cv2.Rectangle(frame, face, new Scalar(0, 255, 0), 2);
    }
    
    // Display result
    window.ShowImage(frame);
}
```

## Teaching Points for Class

### Discussion Questions

1. **Where do you see face detection in daily life?**
   - Phone unlock (Face ID)
   - Camera auto-focus
   - Social media (auto-tagging friends)
   - Zoom/Teams virtual backgrounds

2. **Why might face detection fail?**
   - Side profiles (Haar Cascades work best on frontal faces)
   - Poor lighting conditions
   - Occlusion (face partially covered)
   - Extreme angles or distances

3. **What are the privacy implications?**
   - Surveillance concerns
   - Consent for facial recognition
   - Data storage and usage

### Technical Insights

- **Pre-trained models** save enormous time - training this from scratch would require thousands of labeled images
- The same code works for both webcam and video files with minimal changes
- Real-time processing requires balancing **accuracy vs. speed**
- OpenCV provides many other pre-trained cascades (eyes, smile, full body, etc.)

## Troubleshooting

### Webcam not working
- Check if another application is using the webcam
- Try the video file option instead
- Check Windows privacy settings (Camera access)

### Low FPS
- Reduce webcam resolution in code: `capture.Set(VideoCaptureProperties.FrameWidth, 640);`
- Increase `scaleFactor` to 1.2 or higher
- Process every other frame instead of every frame

### Too many false detections
- Increase `minNeighbors` parameter (try 5-7)
- Add minimum size constraint (already set to 30x30)

### No faces detected
- Decrease `minNeighbors` parameter (try 2-3)
- Ensure good lighting
- Face the camera more directly

## Extensions

Ideas for students to try:

1. **Add eye detection** - Use `haarcascade_eye.xml` to detect eyes within detected faces
2. **Count unique faces** - Track faces across frames
3. **Take snapshots** - Save images when faces are detected
4. **Add sound alerts** - Play a sound when a face is detected
5. **Face blur** - Blur detected faces for privacy (like Google Street View)
6. **Multiple cascades** - Detect faces, eyes, and smiles simultaneously

## Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [OpenCvSharp GitHub](https://github.com/shimat/opencvsharp)
- [Haar Cascade Training](https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html)
- [More Haar Cascades](https://github.com/opencv/opencv/tree/master/data/haarcascades)
