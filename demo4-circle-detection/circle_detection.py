"""
Circle Detection with Image Preprocessing
Demonstrates a complete image processing pipeline: thresholding, noise removal, edge detection, and circle detection.
"""

import cv2
import numpy as np
import argparse

def create_2x3_grid(img1, img2, img3, img4, img5):
    """
    Create a 2x3 grid display from 5 images.
    
    Args:
        img1: Top-left image
        img2: Top-middle image
        img3: Top-right image
        img4: Bottom-left image
        img5: Bottom-middle image (bottom-right will be blank)
    
    Returns:
        Combined grid image
    """
    # Ensure all images are same size and color (BGR)
    h, w = img1.shape[:2]
    
    # Convert grayscale images to BGR if needed
    for i, img in enumerate([img2, img3, img4, img5]):
        if len(img.shape) == 2:
            if i == 0:
                img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif i == 1:
                img3 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif i == 2:
                img4 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif i == 3:
                img5 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    # Resize all to same size
    img2 = cv2.resize(img2, (w, h))
    img3 = cv2.resize(img3, (w, h))
    img4 = cv2.resize(img4, (w, h))
    img5 = cv2.resize(img5, (w, h))
    
    # Create blank image for bottom-right
    img6 = np.zeros_like(img1)
    
    # Stack horizontally and vertically
    top_row = np.hstack([img1, img2, img3])
    bottom_row = np.hstack([img4, img5, img6])
    grid = np.vstack([top_row, bottom_row])
    
    return grid

def add_label(img, text, position='top'):
    """
    Add a label to an image.
    
    Args:
        img: Input image
        text: Label text
        position: 'top' or 'bottom'
    """
    h, w = img.shape[:2]
    
    if position == 'top':
        y = 30
    else:
        y = h - 10
    
    # Add background rectangle for text
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
    cv2.rectangle(img, (5, y - 25), (text_size[0] + 15, y + 5), (0, 0, 0), -1)
    
    # Add text
    cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def run_circle_detection(video_source=0, kernel_size=5, param2=30, min_radius=10, max_radius=100, min_dist=50):
    """
    Run circle detection with preprocessing pipeline.
    
    Args:
        video_source: Camera ID or video file path
        kernel_size: Morphological kernel size
        param2: HoughCircles accumulator threshold
        min_radius: Minimum circle radius
        max_radius: Maximum circle radius
        min_dist: Minimum distance between circle centers
    """
    print("\n" + "="*70)
    print("Circle Detection with Image Preprocessing")
    print("="*70)
    print(f"Initial Parameters:")
    print(f"  Kernel Size: {kernel_size}x{kernel_size}")
    print(f"  Detection Threshold (param2): {param2}")
    print(f"  Radius Range: {min_radius} - {max_radius} pixels")
    print(f"  Minimum Distance: {min_dist} pixels")
    print("\nControls:")
    print("  'q' or ESC - Quit")
    print("  '+' or '=' - Increase detection sensitivity (lower param2)")
    print("  '-' or '_' - Decrease detection sensitivity (higher param2)")
    print("  'k' - Increase kernel size (more noise removal)")
    print("  'j' - Decrease kernel size (less noise removal)")
    print("  'r' - Reset to defaults")
    print("  's' - Save current frame")
    print("="*70 + "\n")
    
    # Open video source
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source: {video_source}")
        return
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video source opened: {frame_width}x{frame_height}")
    print("\nTip: Use circular objects like coins, bottle caps, or balls!")
    print("Tip: Plain background and good lighting work best.\n")
    
    # FPS calculation
    import time
    fps_start_time = time.time()
    fps_frame_count = 0
    fps = 0
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to capture frame")
            break
        
        frame_count += 1
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Step 1: OTSU Thresholding
        # OTSU automatically finds the optimal threshold value
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Step 2: Morphological Opening (erosion followed by dilation)
        # Removes small noise while preserving larger shapes
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        # Step 3: Canny Edge Detection
        # Detects edges in the cleaned binary image
        edges = cv2.Canny(opened, 50, 150)
        
        # Step 4: Circle Detection using Hough Transform
        # Applied to the edge-detected image
        circles = cv2.HoughCircles(
            edges,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=min_dist,
            param1=50,
            param2=param2,
            minRadius=min_radius,
            maxRadius=max_radius
        )
        
        # Create result frame with detected circles
        result_frame = frame.copy()
        circle_count = 0
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            circle_count = len(circles[0])
            
            for i, (x, y, r) in enumerate(circles[0, :]):
                # Draw the outer circle
                cv2.circle(result_frame, (x, y), r, (0, 255, 0), 2)
                # Draw the center
                cv2.circle(result_frame, (x, y), 2, (0, 0, 255), 3)
                # Add circle number
                cv2.putText(result_frame, str(i+1), (x-10, y-r-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Calculate FPS
        fps_frame_count += 1
        if fps_frame_count >= 10:
            fps_end_time = time.time()
            fps = fps_frame_count / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
            fps_frame_count = 0
        
        # Create display images with labels
        img1 = frame.copy()
        img2 = thresh.copy()
        img3 = opened.copy()
        img4 = edges.copy()
        img5 = result_frame.copy()
        
        # Add labels to each image
        add_label(img1, "1. Original", 'top')
        add_label(img2, "2. OTSU Threshold", 'top')
        add_label(img3, f"3. Morph Open (K={kernel_size})", 'top')
        add_label(img4, "4. Canny Edges", 'top')
        add_label(img5, f"5. Detected: {circle_count} circles", 'top')
        
        # Add parameters info to result frame
        param_text = f"Threshold: {param2} | MinDist: {min_dist} | Radius: {min_radius}-{max_radius}"
        cv2.putText(img5, param_text, (10, img5.shape[0] - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Create 2x3 grid
        grid = create_2x3_grid(img1, img2, img3, img4, img5)
        
        # Add overall info
        info_text = f"FPS: {fps:.1f} | Frame: {frame_count}"
        cv2.putText(grid, info_text, (10, grid.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        # Show the grid
        cv2.imshow('Circle Detection Pipeline', grid)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:  # 'q' or ESC
            break
        elif key == ord('+') or key == ord('='):
            # Increase sensitivity (lower threshold)
            param2 = max(param2 - 5, 10)
            print(f"Detection sensitivity increased (param2: {param2})")
        elif key == ord('-') or key == ord('_'):
            # Decrease sensitivity (higher threshold)
            param2 = min(param2 + 5, 100)
            print(f"Detection sensitivity decreased (param2: {param2})")
        elif key == ord('k'):
            # Increase kernel size
            kernel_size = min(kernel_size + 2, 15)
            print(f"Kernel size increased: {kernel_size}x{kernel_size}")
        elif key == ord('j'):
            # Decrease kernel size
            kernel_size = max(kernel_size - 2, 3)
            print(f"Kernel size decreased: {kernel_size}x{kernel_size}")
        elif key == ord('r'):
            # Reset to defaults
            kernel_size = 5
            param2 = 30
            print(f"Reset to defaults: kernel={kernel_size}, param2={param2}")
        elif key == ord('s'):
            # Save current frame
            filename = f'circle_detection_{frame_count}.png'
            cv2.imwrite(filename, grid)
            print(f"Saved: {filename}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nCircle detection ended.")
    print(f"Total frames processed: {frame_count}")

def main():
    parser = argparse.ArgumentParser(description='Circle Detection with Image Preprocessing')
    parser.add_argument('--source', type=str, default='0',
                       help='Video source: camera ID (0, 1, ...) or video file path')
    parser.add_argument('--kernel', type=int, default=5,
                       help='Morphological kernel size (default: 5)')
    parser.add_argument('--threshold', type=int, default=30,
                       help='HoughCircles param2 threshold (default: 30, lower=more sensitive)')
    parser.add_argument('--min-radius', type=int, default=10,
                       help='Minimum circle radius in pixels (default: 10)')
    parser.add_argument('--max-radius', type=int, default=100,
                       help='Maximum circle radius in pixels (default: 100)')
    parser.add_argument('--min-dist', type=int, default=50,
                       help='Minimum distance between circle centers (default: 50)')
    
    args = parser.parse_args()
    
    # Parse video source
    try:
        video_source = int(args.source)
    except ValueError:
        video_source = args.source
    
    run_circle_detection(
        video_source=video_source,
        kernel_size=args.kernel,
        param2=args.threshold,
        min_radius=args.min_radius,
        max_radius=args.max_radius,
        min_dist=args.min_dist
    )

if __name__ == "__main__":
    main()
