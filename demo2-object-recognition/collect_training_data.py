"""
Training Data Collection Tool
Helps capture images from webcam for training the object recognition model.
"""

import cv2
import os
from datetime import datetime

def collect_images(category, num_images=30, camera_id=0):
    """
    Collect training images from webcam.
    
    Args:
        category: 'positive' or 'negative'
        num_images: number of images to collect
        camera_id: camera device ID (default 0)
    """
    # Create directory for this category
    data_dir = os.path.join('data', category)
    os.makedirs(data_dir, exist_ok=True)
    
    # Count existing images
    existing_images = [f for f in os.listdir(data_dir) if f.endswith(('.jpg', '.png'))]
    start_index = len(existing_images)
    
    print(f"\n{'='*60}")
    print(f"Collecting {category.upper()} examples")
    print(f"{'='*60}")
    print(f"Already have: {start_index} images")
    print(f"Will collect: {num_images} more images")
    print(f"Total will be: {start_index + num_images} images")
    print(f"\nInstructions:")
    print(f"  - Press SPACE to capture an image")
    print(f"  - Press 'q' to quit early")
    print(f"  - Move the object/scene between captures for variety")
    
    if category == 'positive':
        print(f"\n  TIP: Show your TARGET OBJECT from different angles, distances, and lighting")
    else:
        print(f"\n  TIP: Show DIFFERENT objects, backgrounds, or empty scenes (NOT the target)")
    
    print(f"\n{'='*60}\n")
    
    # Open webcam
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    images_collected = 0
    
    while images_collected < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # Display instructions on frame
        display_frame = frame.copy()
        text = f"{category.upper()}: {images_collected}/{num_images} captured"
        cv2.putText(display_frame, text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, "Press SPACE to capture, 'q' to quit", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow('Data Collection', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space bar
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{category}_{start_index + images_collected:04d}_{timestamp}.jpg"
            filepath = os.path.join(data_dir, filename)
            
            cv2.imwrite(filepath, frame)
            images_collected += 1
            print(f"  ✓ Captured: {filename}")
            
            # Brief pause and visual feedback
            cv2.putText(display_frame, "CAPTURED!", (200, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.imshow('Data Collection', display_frame)
            cv2.waitKey(200)  # Show "CAPTURED!" for 200ms
            
        elif key == ord('q'):
            print("\nQuitting early...")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n{'='*60}")
    print(f"Collection complete!")
    print(f"  Collected: {images_collected} new images")
    print(f"  Total in {data_dir}: {start_index + images_collected} images")
    print(f"{'='*60}\n")

def main():
    print("\n" + "="*60)
    print("Object Recognition - Training Data Collection")
    print("="*60)
    
    while True:
        print("\nWhat would you like to collect?")
        print("  1. Positive examples (your target object)")
        print("  2. Negative examples (other objects/backgrounds)")
        print("  3. Both (recommended for new dataset)")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            num = input("How many images? (default: 30): ").strip()
            num = int(num) if num else 30
            collect_images('positive', num)
            
        elif choice == '2':
            num = input("How many images? (default: 30): ").strip()
            num = int(num) if num else 30
            collect_images('negative', num)
            
        elif choice == '3':
            num_pos = input("How many POSITIVE images? (default: 30): ").strip()
            num_pos = int(num_pos) if num_pos else 30
            
            num_neg = input("How many NEGATIVE images? (default: 30): ").strip()
            num_neg = int(num_neg) if num_neg else 30
            
            print("\nFirst, we'll collect POSITIVE examples (target object)")
            input("Press ENTER when ready...")
            collect_images('positive', num_pos)
            
            print("\nNow, we'll collect NEGATIVE examples (other objects/backgrounds)")
            input("Press ENTER when ready...")
            collect_images('negative', num_neg)
            
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
