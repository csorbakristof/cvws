"""
Simple Video Effects
Demonstrates various geometric transformations using cv2.remap()
"""

import cv2
import numpy as np
import argparse

def create_mirror_effect(frame):
    """
    Simple vertical mirror effect - split frame and mirror one side.
    """
    h, w = frame.shape[:2]
    result = frame.copy()
    
    # Take left half and flip it
    left_half = frame[:, :w//2]
    flipped = cv2.flip(left_half, 1)
    
    # Replace right half with flipped left half
    result[:, w//2:] = flipped
    
    return result

def create_fisheye_map(width, height, strength=0.5):
    """
    Create coordinate maps for fisheye lens effect.
    
    Args:
        width, height: frame dimensions
        strength: distortion strength (0 = none, 1 = extreme)
    """
    mapX = np.zeros((height, width), dtype=np.float32)
    mapY = np.zeros((height, width), dtype=np.float32)
    
    center_x = width / 2
    center_y = height / 2
    max_radius = min(center_x, center_y)
    
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            
            radius = np.sqrt(dx*dx + dy*dy)
            angle = np.arctan2(dy, dx)
            
            if radius < max_radius:
                # Apply fisheye distortion
                normalized_radius = radius / max_radius
                distorted_radius = normalized_radius ** (1 + strength)
                new_radius = distorted_radius * max_radius
            else:
                new_radius = radius
            
            new_x = center_x + new_radius * np.cos(angle)
            new_y = center_y + new_radius * np.sin(angle)
            
            mapX[y, x] = new_x
            mapY[y, x] = new_y
    
    return mapX, mapY

def create_swirl_map(width, height, strength=1.0):
    """
    Create coordinate maps for swirl/twist effect.
    
    Args:
        width, height: frame dimensions
        strength: swirl strength (radians per pixel)
    """
    mapX = np.zeros((height, width), dtype=np.float32)
    mapY = np.zeros((height, width), dtype=np.float32)
    
    center_x = width / 2
    center_y = height / 2
    max_radius = min(center_x, center_y)
    
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            
            radius = np.sqrt(dx*dx + dy*dy)
            angle = np.arctan2(dy, dx)
            
            # Add rotation based on distance from center
            if radius < max_radius:
                rotation = strength * (1 - radius / max_radius)
                new_angle = angle + rotation
            else:
                new_angle = angle
            
            new_x = center_x + radius * np.cos(new_angle)
            new_y = center_y + radius * np.sin(new_angle)
            
            mapX[y, x] = new_x
            mapY[y, x] = new_y
    
    return mapX, mapY

def create_barrel_map(width, height, strength=0.3):
    """
    Create coordinate maps for barrel distortion effect.
    
    Args:
        width, height: frame dimensions
        strength: distortion strength
    """
    mapX = np.zeros((height, width), dtype=np.float32)
    mapY = np.zeros((height, width), dtype=np.float32)
    
    center_x = width / 2
    center_y = height / 2
    max_radius = np.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            
            radius = np.sqrt(dx*dx + dy*dy)
            normalized_radius = radius / max_radius
            
            # Barrel distortion formula
            distortion = 1 + strength * normalized_radius**2
            
            new_x = center_x + dx * distortion
            new_y = center_y + dy * distortion
            
            mapX[y, x] = new_x
            mapY[y, x] = new_y
    
    return mapX, mapY

def run_effects_demo(video_source=0):
    """
    Run interactive demo with multiple effects.
    """
    print("\n" + "="*70)
    print("Video Effects Demo")
    print("="*70)
    print("\nControls:")
    print("  '1' - Mirror effect")
    print("  '2' - Fisheye effect")
    print("  '3' - Swirl effect")
    print("  '4' - Barrel distortion")
    print("  '0' - Original (no effect)")
    print("  '+/-' - Adjust effect strength")
    print("  'q' or ESC - Quit")
    print("="*70 + "\n")
    
    # Open video source
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source: {video_source}")
        return
    
    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video source opened: {frame_width}x{frame_height}\n")
    
    # Current effect and strength
    current_effect = 0  # 0 = none, 1 = mirror, 2 = fisheye, 3 = swirl, 4 = barrel
    strength = 0.5
    
    # Pre-compute initial maps
    mapX = None
    mapY = None
    
    effect_names = {
        0: "Original",
        1: "Mirror",
        2: "Fisheye",
        3: "Swirl",
        4: "Barrel"
    }
    
    print(f"Current effect: {effect_names[current_effect]}")
    
    # FPS calculation
    import time
    fps_start_time = time.time()
    fps_frame_count = 0
    fps = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to capture frame")
            break
        
        # Apply current effect
        if current_effect == 0:  # Original
            output = frame
        elif current_effect == 1:  # Mirror
            output = create_mirror_effect(frame)
        else:  # Effects using remap
            if mapX is None or mapY is None:
                # Create maps based on current effect
                if current_effect == 2:  # Fisheye
                    mapX, mapY = create_fisheye_map(frame_width, frame_height, strength)
                elif current_effect == 3:  # Swirl
                    mapX, mapY = create_swirl_map(frame_width, frame_height, strength)
                elif current_effect == 4:  # Barrel
                    mapX, mapY = create_barrel_map(frame_width, frame_height, strength)
            
            output = cv2.remap(frame, mapX, mapY, cv2.INTER_LINEAR)
        
        # Calculate FPS
        fps_frame_count += 1
        if fps_frame_count >= 10:
            fps_end_time = time.time()
            fps = fps_frame_count / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
            fps_frame_count = 0
        
        # Add info overlay
        effect_name = effect_names[current_effect]
        if current_effect > 1:
            info_text = f"{effect_name} | Strength: {strength:.2f} | FPS: {fps:.1f}"
        else:
            info_text = f"{effect_name} | FPS: {fps:.1f}"
        
        cv2.putText(output, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(output, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
        
        # Instructions
        cv2.putText(output, "Press 1-4 for effects, 0 for original", (10, frame_height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Video Effects', output)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:  # 'q' or ESC
            break
        elif key == ord('0'):
            current_effect = 0
            mapX, mapY = None, None
            print(f"Effect: {effect_names[current_effect]}")
        elif key == ord('1'):
            current_effect = 1
            mapX, mapY = None, None
            print(f"Effect: {effect_names[current_effect]}")
        elif key == ord('2'):
            current_effect = 2
            mapX, mapY = create_fisheye_map(frame_width, frame_height, strength)
            print(f"Effect: {effect_names[current_effect]} | Strength: {strength:.2f}")
        elif key == ord('3'):
            current_effect = 3
            mapX, mapY = create_swirl_map(frame_width, frame_height, strength)
            print(f"Effect: {effect_names[current_effect]} | Strength: {strength:.2f}")
        elif key == ord('4'):
            current_effect = 4
            mapX, mapY = create_barrel_map(frame_width, frame_height, strength)
            print(f"Effect: {effect_names[current_effect]} | Strength: {strength:.2f}")
        elif key == ord('+') or key == ord('='):
            if current_effect > 1:
                strength = min(strength + 0.1, 2.0)
                # Recreate maps with new strength
                if current_effect == 2:
                    mapX, mapY = create_fisheye_map(frame_width, frame_height, strength)
                elif current_effect == 3:
                    mapX, mapY = create_swirl_map(frame_width, frame_height, strength)
                elif current_effect == 4:
                    mapX, mapY = create_barrel_map(frame_width, frame_height, strength)
                print(f"Strength increased to {strength:.2f}")
        elif key == ord('-') or key == ord('_'):
            if current_effect > 1:
                strength = max(strength - 0.1, 0.0)
                # Recreate maps with new strength
                if current_effect == 2:
                    mapX, mapY = create_fisheye_map(frame_width, frame_height, strength)
                elif current_effect == 3:
                    mapX, mapY = create_swirl_map(frame_width, frame_height, strength)
                elif current_effect == 4:
                    mapX, mapY = create_barrel_map(frame_width, frame_height, strength)
                print(f"Strength decreased to {strength:.2f}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nEffects demo ended.")

def main():
    parser = argparse.ArgumentParser(description='Video Effects Demo')
    parser.add_argument('--source', type=str, default='0',
                       help='Video source: camera ID (0, 1, ...) or video file path')
    
    args = parser.parse_args()
    
    # Parse video source
    try:
        video_source = int(args.source)
    except ValueError:
        video_source = args.source
    
    run_effects_demo(video_source)

if __name__ == "__main__":
    main()
