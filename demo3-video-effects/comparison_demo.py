"""
Side-by-Side Effect Comparison
Shows original and effect side by side for teaching purposes.
"""

import cv2
import numpy as np

def create_kaleidoscope_map(width, height, segments=6):
    """Create kaleidoscope transformation maps."""
    mapX = np.zeros((height, width), dtype=np.float32)
    mapY = np.zeros((height, width), dtype=np.float32)
    
    center_x = width / 2
    center_y = height / 2
    segment_angle = 2 * np.pi / segments
    
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            
            radius = np.sqrt(dx*dx + dy*dy)
            angle = np.arctan2(dy, dx)
            
            segment_num = int(angle / segment_angle)
            angle_in_segment = angle - segment_num * segment_angle
            
            if segment_num % 2 == 1:
                angle_in_segment = segment_angle - angle_in_segment
            
            new_angle = angle_in_segment
            new_x = center_x + radius * np.cos(new_angle)
            new_y = center_y + radius * np.sin(new_angle)
            
            mapX[y, x] = new_x
            mapY[y, x] = new_y
    
    return mapX, mapY

def run_comparison(video_source=0):
    """
    Show original and kaleidoscope effect side by side.
    """
    print("\n" + "="*70)
    print("Side-by-Side Effect Comparison")
    print("="*70)
    print("\nShowing: Original (left) vs Kaleidoscope (right)")
    print("\nControls:")
    print("  'q' or ESC - Quit")
    print("="*70 + "\n")
    
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source: {video_source}")
        return
    
    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create kaleidoscope maps
    mapX, mapY = create_kaleidoscope_map(frame_width, frame_height, segments=6)
    
    print(f"Video source opened: {frame_width}x{frame_height}\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply kaleidoscope effect
        effect_frame = cv2.remap(frame, mapX, mapY, cv2.INTER_LINEAR)
        
        # Create side-by-side comparison
        comparison = np.hstack([frame, effect_frame])
        
        # Add labels
        cv2.putText(comparison, "Original", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(comparison, "Kaleidoscope", (frame_width + 20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add dividing line
        cv2.line(comparison, (frame_width, 0), (frame_width, frame_height),
                (255, 255, 255), 2)
        
        cv2.imshow('Comparison', comparison)
        
        if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Comparison ended.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Side-by-Side Effect Comparison')
    parser.add_argument('--source', type=str, default='0',
                       help='Video source: camera ID or video file path')
    
    args = parser.parse_args()
    
    try:
        video_source = int(args.source)
    except ValueError:
        video_source = args.source
    
    run_comparison(video_source)
