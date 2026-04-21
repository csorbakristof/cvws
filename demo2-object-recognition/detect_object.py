"""
Object Detection - Real-time Inference
Uses the trained model to detect objects in real-time via webcam.
"""

import cv2
import numpy as np
import pickle
import os

def extract_features(img, img_size=(128, 128)):
    """
    Extract features from an image.
    Must match the feature extraction used during training.
    """
    img = cv2.resize(img, img_size)
    
    # Extract color histogram features
    hist_features = []
    for i in range(3):
        hist = cv2.calcHist([img], [i], None, [32], [0, 256])
        hist_features.extend(hist.flatten())
    
    return hist_features

def load_model(model_path='models/object_model_latest.pkl'):
    """
    Load the trained model from file.
    """
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        print("Please train the model first using train_model.py")
        return None
    
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    print("\n" + "="*70)
    print("Model Information:")
    print("="*70)
    print(f"  Trained on: {model_data.get('trained_on', 'unknown')}")
    print(f"  Training samples: {model_data.get('num_training_samples', 'unknown')}")
    print(f"  Positive examples: {model_data.get('num_positive', 'unknown')}")
    print(f"  Negative examples: {model_data.get('num_negative', 'unknown')}")
    print(f"  Test accuracy: {model_data.get('test_accuracy', 0) * 100:.2f}%")
    print("="*70 + "\n")
    
    return model_data

def run_detection(model_path='models/object_model_latest.pkl', camera_id=0):
    """
    Run real-time object detection using webcam.
    """
    # Load the trained model
    model_data = load_model(model_path)
    if model_data is None:
        return
    
    clf = model_data['classifier']
    img_size = model_data.get('img_size', (128, 128))
    
    print("Starting webcam detection...")
    print("Press 'q' to quit\n")
    
    # Open webcam
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # For FPS calculation
    import time
    fps_start_time = time.time()
    fps_frame_count = 0
    fps = 0
    
    # Detection history for smoothing
    history = []
    history_size = 5
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # Extract features from current frame
        features = extract_features(frame, img_size)
        features_array = np.array([features])
        
        # Predict
        prediction = clf.predict(features_array)[0]
        probabilities = clf.predict_proba(features_array)[0]
        confidence = probabilities[prediction]
        
        # Add to history for smoothing
        history.append(prediction)
        if len(history) > history_size:
            history.pop(0)
        
        # Smoothed prediction (majority vote)
        smoothed_prediction = 1 if sum(history) > len(history) / 2 else 0
        
        # Calculate FPS
        fps_frame_count += 1
        if fps_frame_count >= 10:
            fps_end_time = time.time()
            fps = fps_frame_count / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
            fps_frame_count = 0
        
        # Prepare display
        display_frame = frame.copy()
        h, w = display_frame.shape[:2]
        
        # Determine result and color
        if smoothed_prediction == 1:
            result_text = "TARGET OBJECT DETECTED!"
            result_color = (0, 255, 0)  # Green
            box_color = (0, 255, 0)
            # Draw detection box
            cv2.rectangle(display_frame, (50, 50), (w-50, h-50), box_color, 3)
        else:
            result_text = "No object detected"
            result_color = (0, 0, 255)  # Red
        
        # Display result text
        cv2.putText(display_frame, result_text, (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, result_color, 2)
        
        # Display confidence
        confidence_text = f"Confidence: {confidence * 100:.1f}%"
        cv2.putText(display_frame, confidence_text, (20, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Display FPS
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(display_frame, fps_text, (20, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display probabilities bar
        bar_width = 300
        bar_height = 20
        bar_x = 20
        bar_y = 95
        
        # Background
        cv2.rectangle(display_frame, (bar_x, bar_y), 
                     (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
        
        # Confidence bar
        confidence_width = int(bar_width * probabilities[1])
        if probabilities[1] > 0.5:
            bar_fill_color = (0, 255, 0)  # Green for positive
        else:
            bar_fill_color = (0, 0, 255)  # Red for negative
        
        cv2.rectangle(display_frame, (bar_x, bar_y),
                     (bar_x + confidence_width, bar_y + bar_height), 
                     bar_fill_color, -1)
        
        # Border
        cv2.rectangle(display_frame, (bar_x, bar_y),
                     (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 1)
        
        # Threshold line (50%)
        cv2.line(display_frame, (bar_x + bar_width//2, bar_y),
                (bar_x + bar_width//2, bar_y + bar_height), (255, 255, 255), 1)
        
        # Instructions
        cv2.putText(display_frame, "Press 'q' to quit", (w - 180, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Show frame
        cv2.imshow('Object Detection', display_frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nDetection ended.")

def main():
    print("\n" + "="*70)
    print("Object Recognition - Real-time Detection")
    print("="*70)
    
    # Check for model file
    model_path = 'models/object_model_latest.pkl'
    
    if not os.path.exists(model_path):
        print("\n⚠ No trained model found!")
        print(f"Expected model at: {model_path}")
        print("\nPlease follow these steps:")
        print("  1. Run collect_training_data.py to collect images")
        print("  2. Run train_model.py to train the model")
        print("  3. Then run this script again")
        print()
        return
    
    # Run detection
    run_detection(model_path)

if __name__ == "__main__":
    main()
