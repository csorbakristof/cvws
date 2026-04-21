using OpenCvSharp;

namespace MotionDetectionDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Motion Detection Demo - MOG2");
            Console.WriteLine("=============================");
            Console.WriteLine("Press 'q' to quit");
            Console.WriteLine();
            Console.WriteLine("Choose input source:");
            Console.WriteLine("1. Webcam (default)");
            Console.WriteLine("2. Video file");
            Console.Write("Enter choice (1 or 2): ");
            
            string? choice = Console.ReadLine();
            
            if (choice == "2")
            {
                Console.Write("Enter video file path: ");
                string? videoPath = Console.ReadLine();
                if (!string.IsNullOrEmpty(videoPath) && File.Exists(videoPath))
                {
                    RunMotionDetection(videoPath);
                }
                else
                {
                    Console.WriteLine("Video file not found. Using webcam instead.");
                    RunMotionDetection();
                }
            }
            else
            {
                RunMotionDetection();
            }
        }

        static Mat CreateGridDisplay(Mat original, Mat background, Mat fgMask, Mat result)
        {
            // Ensure all images are same size
            int width = original.Width;
            int height = original.Height;

            // Convert grayscale images to BGR for consistent display
            Mat backgroundBgr = new Mat();
            if (background.Channels() == 1)
                Cv2.CvtColor(background, backgroundBgr, ColorConversionCodes.GRAY2BGR);
            else
                backgroundBgr = background.Clone();

            Mat fgMaskBgr = new Mat();
            Cv2.CvtColor(fgMask, fgMaskBgr, ColorConversionCodes.GRAY2BGR);

            // Resize all to same dimensions
            Cv2.Resize(original, original, new Size(width, height));
            Cv2.Resize(backgroundBgr, backgroundBgr, new Size(width, height));
            Cv2.Resize(fgMaskBgr, fgMaskBgr, new Size(width, height));
            Cv2.Resize(result, result, new Size(width, height));

            // Add labels to each image
            AddLabel(original, "1. Original", 10, 30);
            AddLabel(backgroundBgr, "2. Background Model", 10, 30);
            AddLabel(fgMaskBgr, "3. Foreground Mask", 10, 30);
            AddLabel(result, "4. Motion Detected", 10, 30);

            // Create 2x2 grid
            Mat topRow = new Mat();
            Mat bottomRow = new Mat();
            Cv2.HConcat(new[] { original, backgroundBgr }, topRow);
            Cv2.HConcat(new[] { fgMaskBgr, result }, bottomRow);

            Mat grid = new Mat();
            Cv2.VConcat(new[] { topRow, bottomRow }, grid);

            return grid;
        }

        static void AddLabel(Mat image, string text, int x, int y)
        {
            // Add black background for text
            var textSize = Cv2.GetTextSize(text, HersheyFonts.HersheySimplex, 0.7, 2, out int baseline);
            Cv2.Rectangle(image, new Point(x - 5, y - textSize.Height - 5),
                         new Point(x + textSize.Width + 5, y + baseline + 5),
                         new Scalar(0, 0, 0), -1);
            
            // Add white text
            Cv2.PutText(image, text, new Point(x, y),
                       HersheyFonts.HersheySimplex, 0.7, new Scalar(255, 255, 255), 2);
        }

        static void RunMotionDetection(string? videoSource = null)
        {
            // Open video capture (webcam or video file)
            VideoCapture capture;
            if (videoSource == null)
            {
                capture = new VideoCapture(0); // 0 = default webcam
                Console.WriteLine("Opening webcam...");
            }
            else
            {
                capture = new VideoCapture(videoSource);
                Console.WriteLine($"Opening video file: {videoSource}");
            }

            if (!capture.IsOpened())
            {
                Console.WriteLine("Error: Could not open video source");
                return;
            }

            Console.WriteLine("Video source opened successfully!");
            Console.WriteLine("\nControls:");
            Console.WriteLine("  q        - Quit");
            Console.WriteLine("  +        - Increase sensitivity (lower threshold)");
            Console.WriteLine("  -        - Decrease sensitivity (higher threshold)");
            Console.WriteLine("  s        - Toggle shadow detection");
            Console.WriteLine("  r        - Reset background model");
            Console.WriteLine("  k/j      - Increase/decrease morphology kernel size");
            Console.WriteLine("  m/n      - Increase/decrease minimum contour area");
            Console.WriteLine("  SPACE    - Pause/Resume");

            // Initialize MOG2 background subtractor
            int history = 500;              // Number of frames for background model
            double varThreshold = 16;       // Threshold for foreground/background classification
            bool detectShadows = true;      // Enable shadow detection
            
            var mog2 = BackgroundSubtractorMOG2.Create(history, varThreshold, detectShadows);

            // Morphological operation parameters
            int kernelSize = 5;
            double minContourArea = 500;

            // Statistics
            int frameCount = 0;
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            bool paused = false;

            using (var window = new Window("Motion Detection - MOG2"))
            using (var frame = new Mat())
            {
                Console.WriteLine("\nInitializing background model (this takes a few seconds)...");
                
                while (true)
                {
                    if (!paused)
                    {
                        // Capture frame
                        capture.Read(frame);
                        if (frame.Empty())
                        {
                            Console.WriteLine("End of video or failed to capture frame");
                            break;
                        }

                        frameCount++;

                        // Apply MOG2 to get foreground mask
                        Mat fgMask = new Mat();
                        mog2.Apply(frame, fgMask);

                        // Remove shadows (they appear as gray pixels - value 127)
                        if (detectShadows)
                        {
                            // Set shadow pixels to black (0)
                            Cv2.Threshold(fgMask, fgMask, 127, 255, ThresholdTypes.Binary);
                        }

                        // Morphological operations to remove noise
                        Mat kernel = Cv2.GetStructuringElement(MorphShapes.Ellipse, 
                                                               new Size(kernelSize, kernelSize));
                        
                        // Opening: removes small white noise spots
                        Cv2.MorphologyEx(fgMask, fgMask, MorphTypes.Open, kernel);
                        
                        // Closing: fills small holes in detected objects
                        Cv2.MorphologyEx(fgMask, fgMask, MorphTypes.Close, kernel);

                        // Find contours (boundaries of moving objects)
                        Point[][] contours;
                        HierarchyIndex[] hierarchy;
                        Cv2.FindContours(fgMask, out contours, out hierarchy,
                                       RetrievalModes.External,
                                       ContourApproximationModes.ApproxSimple);

                        // Draw bounding boxes around detected motion
                        Mat result = frame.Clone();
                        int motionCount = 0;

                        foreach (var contour in contours)
                        {
                            double area = Cv2.ContourArea(contour);
                            
                            // Filter small contours (noise)
                            if (area > minContourArea)
                            {
                                motionCount++;
                                Rect bbox = Cv2.BoundingRect(contour);
                                
                                // Draw bounding box
                                Cv2.Rectangle(result, bbox, new Scalar(0, 255, 0), 2);
                                
                                // Draw label with object number and area
                                string label = $"#{motionCount} ({area:F0}px)";
                                Cv2.PutText(result, label, new Point(bbox.X, bbox.Y - 10),
                                          HersheyFonts.HersheySimplex, 0.5, new Scalar(0, 255, 0), 2);
                            }
                        }

                        // Add motion count and parameters info
                        string infoText = $"Objects: {motionCount} | Kernel: {kernelSize}x{kernelSize} | MinArea: {minContourArea} | Threshold: {varThreshold:F1}";
                        Cv2.PutText(result, infoText, new Point(10, result.Height - 15),
                                  HersheyFonts.HersheySimplex, 0.5, new Scalar(255, 255, 255), 1);
                        
                        // Add shadow detection status
                        string shadowText = detectShadows ? "Shadows: ON" : "Shadows: OFF";
                        Cv2.PutText(result, shadowText, new Point(10, result.Height - 35),
                                  HersheyFonts.HersheySimplex, 0.5, new Scalar(255, 255, 255), 1);

                        // Get background model image
                        Mat background = new Mat();
                        mog2.GetBackgroundImage(background);
                        
                        // If background not ready yet, use black image
                        if (background.Empty())
                        {
                            background = Mat.Zeros(frame.Rows, frame.Cols, MatType.CV_8UC3);
                            AddLabel(background, "Learning...", background.Width / 2 - 50, background.Height / 2);
                        }

                        // Create and display grid
                        Mat grid = CreateGridDisplay(frame, background, fgMask, result);
                        window.ShowImage(grid);

                        // Calculate and display FPS every 30 frames
                        if (frameCount % 30 == 0)
                        {
                            double fps = frameCount / stopwatch.Elapsed.TotalSeconds;
                            Console.Write($"\rFPS: {fps:F1} | Frames: {frameCount} | Motion objects: {motionCount}   ");
                        }
                    }
                    else
                    {
                        // Paused - just wait for key
                        window.ShowImage(frame);
                    }

                    // Handle keyboard input
                    int key = Cv2.WaitKey(30);
                    if (key == 'q' || key == 'Q' || key == 27) // q or ESC
                    {
                        break;
                    }
                    else if (key == '+' || key == '=')
                    {
                        varThreshold = Math.Max(1, varThreshold - 2);
                        mog2.VarThreshold = varThreshold;
                        Console.WriteLine($"\nSensitivity increased (threshold: {varThreshold})");
                    }
                    else if (key == '-' || key == '_')
                    {
                        varThreshold += 2;
                        mog2.VarThreshold = varThreshold;
                        Console.WriteLine($"\nSensitivity decreased (threshold: {varThreshold})");
                    }
                    else if (key == 's' || key == 'S')
                    {
                        detectShadows = !detectShadows;
                        Console.WriteLine($"\nShadow detection: {(detectShadows ? "ON" : "OFF")}");
                    }
                    else if (key == 'r' || key == 'R')
                    {
                        // Reset background model
                        mog2.Dispose();
                        mog2 = BackgroundSubtractorMOG2.Create(history, varThreshold, detectShadows);
                        Console.WriteLine("\nBackground model reset");
                    }
                    else if (key == 'k' || key == 'K')
                    {
                        kernelSize = Math.Min(21, kernelSize + 2);
                        Console.WriteLine($"\nKernel size increased: {kernelSize}x{kernelSize}");
                    }
                    else if (key == 'j' || key == 'J')
                    {
                        kernelSize = Math.Max(3, kernelSize - 2);
                        Console.WriteLine($"\nKernel size decreased: {kernelSize}x{kernelSize}");
                    }
                    else if (key == 'm' || key == 'M')
                    {
                        minContourArea += 100;
                        Console.WriteLine($"\nMin contour area increased: {minContourArea}");
                    }
                    else if (key == 'n' || key == 'N')
                    {
                        minContourArea = Math.Max(100, minContourArea - 100);
                        Console.WriteLine($"\nMin contour area decreased: {minContourArea}");
                    }
                    else if (key == ' ')
                    {
                        paused = !paused;
                        Console.WriteLine($"\n{(paused ? "PAUSED" : "RESUMED")}");
                    }
                }
            }

            Console.WriteLine("\n\nMotion detection stopped.");
            Console.WriteLine($"Total frames processed: {frameCount}");
            Console.WriteLine($"Average FPS: {frameCount / stopwatch.Elapsed.TotalSeconds:F1}");

            capture.Release();
        }
    }
}
