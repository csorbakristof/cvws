"""
Object Recognition Model Training
Trains a simple machine learning model to recognize a specific object.
"""

import cv2
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from datetime import datetime

def load_images_from_folder(folder, label, img_size=(128, 128)):
    """
    Load and preprocess images from a folder.
    
    Args:
        folder: path to folder containing images
        label: class label (0 or 1)
        img_size: resize images to this size
    
    Returns:
        images: list of preprocessed images
        labels: list of corresponding labels
    """
    images = []
    labels = []
    
    if not os.path.exists(folder):
        print(f"Warning: Folder {folder} does not exist")
        return images, labels
    
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(valid_extensions)]
    
    print(f"Loading {len(image_files)} images from {folder}...")
    
    for filename in image_files:
        img_path = os.path.join(folder, filename)
        try:
            # Load image
            img = cv2.imread(img_path)
            if img is None:
                print(f"  Warning: Could not load {filename}")
                continue
            
            # Resize to standard size
            img = cv2.resize(img, img_size)
            
            # Convert to feature vector
            # Method 1: Color histogram features (simple and fast)
            hist_features = []
            for i in range(3):  # For each color channel
                hist = cv2.calcHist([img], [i], None, [32], [0, 256])
                hist_features.extend(hist.flatten())
            
            # Method 2: Flatten the resized image (alternative)
            # features = img.flatten()
            
            images.append(hist_features)
            labels.append(label)
            
        except Exception as e:
            print(f"  Error processing {filename}: {e}")
    
    print(f"  Successfully loaded {len(images)} images")
    return images, labels

def extract_features(img, img_size=(128, 128)):
    """
    Extract features from a single image (used for inference).
    This must match the feature extraction in load_images_from_folder.
    """
    img = cv2.resize(img, img_size)
    
    # Extract color histogram features
    hist_features = []
    for i in range(3):
        hist = cv2.calcHist([img], [i], None, [32], [0, 256])
        hist_features.extend(hist.flatten())
    
    return hist_features

def train_model():
    """
    Train the object recognition model.
    """
    print("\n" + "="*70)
    print("Object Recognition - Model Training")
    print("="*70 + "\n")
    
    # Check if data directories exist
    positive_dir = os.path.join('data', 'positive')
    negative_dir = os.path.join('data', 'negative')
    
    if not os.path.exists(positive_dir) or not os.path.exists(negative_dir):
        print("Error: Training data not found!")
        print(f"Expected directories:")
        print(f"  - {positive_dir}")
        print(f"  - {negative_dir}")
        print(f"\nPlease run collect_training_data.py first to collect training images.")
        return
    
    # Load training data
    print("Step 1: Loading training data...")
    print("-" * 70)
    
    X_positive, y_positive = load_images_from_folder(positive_dir, label=1)
    X_negative, y_negative = load_images_from_folder(negative_dir, label=0)
    
    if len(X_positive) == 0 or len(X_negative) == 0:
        print("\nError: Not enough training data!")
        print(f"  Positive examples: {len(X_positive)}")
        print(f"  Negative examples: {len(X_negative)}")
        print(f"\nYou need at least some images in both categories.")
        return
    
    # Combine datasets
    X = np.array(X_positive + X_negative)
    y = np.array(y_positive + y_negative)
    
    print(f"\nDataset summary:")
    print(f"  Positive examples (target object): {len(X_positive)}")
    print(f"  Negative examples (other objects): {len(X_negative)}")
    print(f"  Total examples: {len(X)}")
    print(f"  Feature dimensions: {X.shape[1]}")
    
    # Split into training and testing sets
    print(f"\nStep 2: Splitting data (80% train, 20% test)...")
    print("-" * 70)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  Training set: {len(X_train)} images")
    print(f"  Test set: {len(X_test)} images")
    
    # Train the model
    print(f"\nStep 3: Training Random Forest classifier...")
    print("-" * 70)
    
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1  # Use all CPU cores
    )
    
    clf.fit(X_train, y_train)
    print("  ✓ Training complete!")
    
    # Evaluate the model
    print(f"\nStep 4: Evaluating model performance...")
    print("-" * 70)
    
    # Training accuracy
    y_train_pred = clf.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    print(f"  Training accuracy: {train_accuracy * 100:.2f}%")
    
    # Test accuracy
    y_test_pred = clf.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"  Test accuracy: {test_accuracy * 100:.2f}%")
    
    if train_accuracy - test_accuracy > 0.15:
        print(f"\n  ⚠ Warning: Large gap between training and test accuracy!")
        print(f"  This might indicate overfitting. Consider collecting more diverse data.")
    
    # Detailed classification report
    print(f"\nDetailed Performance Report:")
    print("-" * 70)
    target_names = ['Not Object (Negative)', 'Target Object (Positive)']
    print(classification_report(y_test, y_test_pred, target_names=target_names))
    
    # Save the model
    print(f"\nStep 5: Saving model...")
    print("-" * 70)
    
    os.makedirs('models', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f'models/object_model_{timestamp}.pkl'
    
    model_data = {
        'classifier': clf,
        'img_size': (128, 128),
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'num_training_samples': len(X_train),
        'num_positive': len(X_positive),
        'num_negative': len(X_negative),
        'trained_on': timestamp
    }
    
    with open(model_filename, 'wb') as f:
        pickle.dump(model_data, f)
    
    # Also save as "latest" for easy access
    latest_filename = 'models/object_model_latest.pkl'
    with open(latest_filename, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"  ✓ Model saved to: {model_filename}")
    print(f"  ✓ Model saved to: {latest_filename} (for easy loading)")
    
    print("\n" + "="*70)
    print("Training Complete!")
    print("="*70)
    print(f"\nYou can now run detect_object.py to test the model with your webcam.")
    print(f"\nModel Performance Summary:")
    print(f"  • Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"  • Trained on {len(X)} total images")
    print(f"  • Ready to detect your object!")
    print("="*70 + "\n")

if __name__ == "__main__":
    train_model()
