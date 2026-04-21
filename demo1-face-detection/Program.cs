using OpenCvSharp;

namespace FaceDetectionDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Face Detection Demo");
            Console.WriteLine("===================");
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
                    RunFaceDetection(videoPath);
                }
                else
                {
                    Console.WriteLine("Video file not found. Using webcam instead.");
                    RunFaceDetection();
                }
            }
            else
            {
                RunFaceDetection();
            }
        }

        static void RunFaceDetection(string? videoSource = null)
        {
            // Load the Haar Cascade classifier for face detection
            string cascadePath = "haarcascade_frontalface_default.xml";
            if (!File.Exists(cascadePath))
            {
                Console.WriteLine($"Error: Cascade file not found at {cascadePath}");
                Console.WriteLine("Please download it from:");
                Console.WriteLine("https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml");
                return;
            }

            var faceCascade = new CascadeClassifier(cascadePath);
            if (faceCascade.Empty())
            {
                Console.WriteLine("Error: Failed to load cascade classifier");
                return;
            }

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
            Console.WriteLine("Press 'q' in the video window to quit");
            Console.WriteLine("Press '+' to increase detection sensitivity");
            Console.WriteLine("Press '-' to decrease detection sensitivity");

            // Detection parameters (can be adjusted for tuning)
            double scaleFactor = 1.1;
            int minNeighbors = 4;
            int frameCount = 0;
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            using (var window = new Window("Face Detection Demo"))
            using (var frame = new Mat())
            {
                while (true)
                {
                    // Capture frame
                    capture.Read(frame);
                    if (frame.Empty())
                    {
                        Console.WriteLine("End of video or failed to capture frame");
                        break;
                    }

                    // Convert to grayscale for faster processing
                    using (var gray = new Mat())
                    {
                        Cv2.CvtColor(frame, gray, ColorConversionCodes.BGR2GRAY);
                        Cv2.EqualizeHist(gray, gray); // Improve contrast

                        // Detect faces
                        var faces = faceCascade.DetectMultiScale(
                            gray,
                            scaleFactor: scaleFactor,
                            minNeighbors: minNeighbors,
                            flags: HaarDetectionTypes.ScaleImage,
                            minSize: new Size(30, 30)
                        );

                        // Draw rectangles around detected faces
                        foreach (var face in faces)
                        {
                            Cv2.Rectangle(frame, face, new Scalar(0, 255, 0), 2);
                            
                            // Add label with face count
                            string label = $"Face";
                            Cv2.PutText(frame, label, 
                                new Point(face.X, face.Y - 10),
                                HersheyFonts.HersheySimplex, 0.5, 
                                new Scalar(0, 255, 0), 2);
                        }

                        // Display face count and FPS
                        frameCount++;
                        double elapsed = stopwatch.Elapsed.TotalSeconds;
                        double fps = frameCount / elapsed;
                        
                        string info = $"Faces: {faces.Length} | FPS: {fps:F1} | Scale: {scaleFactor:F2} | MinNeighbors: {minNeighbors}";
                        Cv2.PutText(frame, info,
                            new Point(10, 30),
                            HersheyFonts.HersheySimplex, 0.7,
                            new Scalar(255, 255, 0), 2);
                    }

                    // Show the frame
                    window.ShowImage(frame);

                    // Handle keyboard input
                    int key = Cv2.WaitKey(1);
                    if (key == 'q' || key == 'Q' || key == 27) // 'q' or ESC
                    {
                        break;
                    }
                    else if (key == '+' || key == '=')
                    {
                        // Increase sensitivity (lower minNeighbors)
                        if (minNeighbors > 1)
                        {
                            minNeighbors--;
                            Console.WriteLine($"Detection sensitivity increased (minNeighbors: {minNeighbors})");
                        }
                    }
                    else if (key == '-' || key == '_')
                    {
                        // Decrease sensitivity (higher minNeighbors)
                        if (minNeighbors < 10)
                        {
                            minNeighbors++;
                            Console.WriteLine($"Detection sensitivity decreased (minNeighbors: {minNeighbors})");
                        }
                    }
                }
            }

            capture.Release();
            Console.WriteLine("\nDemo ended.");
            Console.WriteLine($"Total frames processed: {frameCount}");
            Console.WriteLine($"Average FPS: {frameCount / stopwatch.Elapsed.TotalSeconds:F2}");
        }
    }
}
