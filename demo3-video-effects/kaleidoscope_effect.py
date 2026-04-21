"""
Kaleidoscope Video Effect
Creates a mesmerizing kaleidoscope pattern from webcam feed using cv2.remap()
"""

import cv2
import numpy as np
import argparse

def create_kaleidoscope_map(width, height, segments=8, zoom=1.0):
    """
    Create coordinate maps for kaleidoscope effect.
    
    Args:
        width: frame width
        height: frame height
        segments: number of kaleidoscope segments (mirrors)
        zoom: zoom factor (1.0 = normal, >1 = zoom in, <1 = zoom out)
    
    Returns:
        mapX, mapY: coordinate maps for cv2.remap()
    """
    # Create coordinate grids
    center_x = width / 2
    center_y = height / 2
    
    # Create output coordinate arrays
    mapX = np.zeros((height, width), dtype=np.float32)
    mapY = np.zeros((height, width), dtype=np.float32)
    
    # Calculate angle of each segment
    segment_angle = 2 * np.pi / segments
    
    for y in range(height):
        for x in range(width):
            # Convert to coordinates relative to center
            dx = x - center_x
            dy = y - center_y
            
            # Convert to polar coordinates
            radius = np.sqrt(dx*dx + dy*dy)
            angle = np.arctan2(dy, dx)
            
            # Apply zoom
            radius = radius / zoom
            
            # Apply kaleidoscope effect
            # Map angle to first segment and mirror
            segment_num = int(angle / segment_angle)
            angle_in_segment = angle - segment_num * segment_angle
            
            # Mirror every other segment for kaleidoscope effect
            if segment_num % 2 == 1:
                angle_in_segment = segment_angle - angle_in_segment
            
            # Use only the first segment's angle
            new_angle = angle_in_segment
            
            # Convert back to cartesian
            new_x = center_x + radius * np.cos(new_angle)
            new_y = center_y + radius * np.sin(new_angle)
            
            mapX[y, x] = new_x
            mapY[y, x] = new_y
    
    return mapX, mapY

def run_kaleidoscope(video_source=0, segments=8, zoom=1.0):
    """
    Run kaleidoscope effect on video source.
    
    Args:
        video_source: camera ID (int) or video file path (str)
        segments: number of kaleidoscope segments
        zoom: zoom factor
    """
    print("\n" + "="*70)
    print("Kaleidoscope Video Effect")
    print("="*70)
    print(f"Segments: {segments}")
    print(f"Zoom: {zoom}")
    print("\nControls:")
    print("  'q' or ESC - Quit")
    print("  '+' or '=' - Add more segments")
    print("  '-' or '_' - Remove segments")
    print("  'z' - Zoom in")
    print("  'x' - Zoom out")
    print("  'r' - Reset to defaults")
    print("="*70 + "\n")
    
    # Open video source
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source: {video_source}")
        return
    
    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video source opened: {frame_width}x{frame_height}")
    
    # Create initial maps
    mapX, mapY = create_kaleidoscope_map(frame_width, frame_height, segments, zoom)
    
    # FPS calculation
    import time
    fps_start_time = time.time()
    fps_frame_count = 0
    fps = 0
    
    # Main loop
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to capture frame")
            break
        
        # Apply kaleidoscope effect using remap
        kaleidoscope_frame = cv2.remap(frame, mapX, mapY, cv2.INTER_LINEAR)
        
        # Calculate FPS
        fps_frame_count += 1
        if fps_frame_count >= 10:
            fps_end_time = time.time()
            fps = fps_frame_count / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
            fps_frame_count = 0
        
        # Add info overlay
        info_text = f"Segments: {segments} | Zoom: {zoom:.1f}x | FPS: {fps:.1f}"
        cv2.putText(kaleidoscope_frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(kaleidoscope_frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
        
        # Show result
        cv2.imshow('Kaleidoscope Effect', kaleidoscope_frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:  # 'q' or ESC
            break
        elif key == ord('+') or key == ord('='):
            segments = min(segments + 1, 24)
            print(f"Segments increased to {segments}")
            mapX, mapY = create_kaleidoscope_map(frame_width, frame_height, segments, zoom)
        elif key == ord('-') or key == ord('_'):
            segments = max(segments - 1, 2)
            print(f"Segments decreased to {segments}")
            mapX, mapY = create_kaleidoscope_map(frame_width, frame_height, segments, zoom)
        elif key == ord('z'):
            zoom = min(zoom + 0.1, 3.0)
            print(f"Zoom increased to {zoom:.1f}x")
            mapX, mapY = create_kaleidoscope_map(frame_width, frame_height, segments, zoom)
        elif key == ord('x'):
            zoom = max(zoom - 0.1, 0.5)
            print(f"Zoom decreased to {zoom:.1f}x")
            mapX, mapY = create_kaleidoscope_map(frame_width, frame_height, segments, zoom)
        elif key == ord('r'):
            segments = 8
            zoom = 1.0
            print(f"Reset to defaults: segments={segments}, zoom={zoom}")
            mapX, mapY = create_kaleidoscope_map(frame_width, frame_height, segments, zoom)
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nKaleidoscope effect ended.")

def main():
    parser = argparse.ArgumentParser(description='Kaleidoscope Video Effect')
    parser.add_argument('--source', type=str, default='0',
                       help='Video source: camera ID (0, 1, ...) or video file path')
    parser.add_argument('--segments', type=int, default=8,
                       help='Number of kaleidoscope segments (default: 8)')
    parser.add_argument('--zoom', type=float, default=1.0,
                       help='Zoom factor (default: 1.0)')
    
    args = parser.parse_args()
    
    # Parse video source
    try:
        video_source = int(args.source)
    except ValueError:
        video_source = args.source
    
    run_kaleidoscope(video_source, args.segments, args.zoom)

if __name__ == "__main__":
    main()
