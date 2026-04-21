# Demo 2 - Object Recognition with Training

This demo shows how to train a custom machine learning model to recognize a specific object of your choice using Python and scikit-learn.

## Overview

Unlike Demo 1 (which uses pre-trained models), this demo teaches students how to:
1. Collect their own training data
2. Train a custom model
3. Use the model for real-time object detection

## Features

- **Data Collection Tool**: Easy webcam-based image capture
- **Training Pipeline**: Simple but effective ML training
- **Real-time Detection**: Live object recognition with confidence scores
- **Visual Feedback**: Color-coded results and probability visualization

## Requirements

- Python 3.8 or later
- Webcam
- A distinctive object to recognize (water bottle, book, toy, etc.)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `opencv-python` - For image processing and webcam access
- `numpy` - For numerical operations
- `scikit-learn` - For machine learning
- `pillow` - For additional image support

### 2. Project Structure

```
demo2-object-recognition/
├── collect_training_data.py   # Step 1: Collect images
├── train_model.py             # Step 2: Train the model
├── detect_object.py           # Step 3: Test the model
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── data/                      # Created automatically
│   ├── positive/              # Images of target object
│   └── negative/              # Images of other objects
└── models/                    # Created automatically
    └── object_model_latest.pkl  # Trained model
```

## Usage - Complete Workflow

### Step 1: Collect Training Data

Run the data collection tool:

```bash
python collect_training_data.py
```

**What to do:**
1. Choose option 3 (collect both positive and negative examples)
2. You'll be prompted for how many images (30 each is a good start)

**Positive Examples** (target object):
- Show your chosen object from different angles
- Vary the distance (close, medium, far)
- Try different lighting conditions
- Rotate the object
- Press SPACE to capture each image

**Negative Examples** (not the target):
- Show different objects
- Show empty backgrounds
- Show similar but different items
- Again, press SPACE for each capture

**Tips for good training data:**
- Diversity is key! More variety = better model
- Avoid too much background clutter initially
- Make sure object is clearly visible
- 30-50 images per category is a good starting point

### Step 2: Train the Model

Once you have collected data, train the model:

```bash
python train_model.py
```

**What happens:**
1. Loads all images from `data/positive/` and `data/negative/`
2. Extracts features (color histograms) from each image
3. Trains a Random Forest classifier
4. Evaluates accuracy on a test set
5. Saves the trained model to `models/object_model_latest.pkl`

**Training output:**
```
Step 1: Loading training data...
  Positive examples (target object): 30
  Negative examples (other objects): 30
  
Step 2: Splitting data (80% train, 20% test)...
  Training set: 48 images
  Test set: 12 images
  
Step 3: Training Random Forest classifier...
  ✓ Training complete!
  
Step 4: Evaluating model performance...
  Training accuracy: 98.00%
  Test accuracy: 92.00%
```

**Good accuracy:**
- 85-95% on test set is excellent for this simple approach
- If test accuracy is below 70%, collect more diverse training data

### Step 3: Real-time Detection

Test your trained model with live webcam:

```bash
python detect_object.py
```

**What you'll see:**
- Live webcam feed
- "TARGET OBJECT DETECTED!" in green when object is found
- "No object detected" in red otherwise
- Confidence percentage
- Visual probability bar
- FPS counter

**Controls:**
- Press 'q' to quit

**Testing tips:**
- Show the target object - should detect it
- Show different objects - should NOT detect them
- Try different angles and distances
- See how confidence changes

## How It Works

### Feature Extraction

Instead of using raw pixels, we extract meaningful features:

```python
# Color histogram features
for each color channel (Red, Green, Blue):
    Calculate histogram of color values (32 bins)
    Add to feature vector

# Result: 96 features (3 channels × 32 bins)
```

**Why color histograms?**
- Captures color distribution
- Invariant to small position changes
- Much faster than deep learning
- Sufficient for simple object recognition

### Training Process

```python
# 1. Load and preprocess images
X_positive = load_images('data/positive', label=1)
X_negative = load_images('data/negative', label=0)

# 2. Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y)

# 3. Train Random Forest
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# 4. Evaluate
accuracy = clf.score(X_test, y_test)

# 5. Save model
pickle.dump(clf, 'model.pkl')
```

### Detection Process

```python
# 1. Capture frame from webcam
frame = webcam.read()

# 2. Extract features
features = extract_features(frame)

# 3. Predict
prediction = model.predict(features)
confidence = model.predict_proba(features)

# 4. Display result
if prediction == 1:
    show("TARGET DETECTED!")
```

## Teaching Points for Class

### Key Concepts

1. **Supervised Learning**
   - Model learns from labeled examples
   - Needs both positive and negative examples
   - "Training" means finding patterns in the data

2. **Feature Engineering**
   - Raw pixels aren't always the best input
   - Color histograms capture "what colors are present"
   - Good features make learning easier

3. **Train/Test Split**
   - Never test on training data!
   - Test set simulates "new, unseen data"
   - Gap between train and test accuracy indicates overfitting

4. **Confidence Scores**
   - Not just yes/no, but "how sure?"
   - Probability from 0 to 1 (0% to 100%)
   - Useful for setting thresholds

### Discussion Questions

1. **What makes good training data?**
   - Diverse examples
   - Representative of real-world use
   - Balanced classes (similar number of positive/negative)

2. **When might the model fail?**
   - Object in unusual lighting
   - Extreme angles not in training data
   - Partial occlusion
   - Similar-looking objects

3. **How is this different from Demo 1?**
   - Demo 1: Pre-trained, general purpose (any face)
   - Demo 2: Custom-trained, specific object (your bottle)
   - Trade-off: specificity vs. generality

4. **Real-world applications?**
   - Manufacturing: defect detection
   - Agriculture: crop disease identification
   - Recycling: sorting materials
   - Retail: product recognition

## Troubleshooting

### Low Accuracy (< 70%)

**Possible causes:**
- Not enough training data
- Training data not diverse enough
- Positive and negative examples too similar
- Poor lighting in training images

**Solutions:**
- Collect more images (50-100 per category)
- Ensure variety in angles, distances, lighting
- Make sure object is clearly visible
- Re-train after adding more data

### False Positives (detects wrong objects)

**Solutions:**
- Add more diverse negative examples
- Include images of similar-looking objects in negative set
- Increase confidence threshold in code

### False Negatives (misses the target object)

**Solutions:**
- Add more positive examples from different angles
- Check if lighting/angle in test is very different from training
- Ensure object is clearly visible and not too small

### Model file not found

```
Error: Model file not found at models/object_model_latest.pkl
```

**Solution:** Run `train_model.py` first to create the model.

### No training data

```
Error: Training data not found!
```

**Solution:** Run `collect_training_data.py` first to collect images.

## Extensions and Improvements

Ideas for students to explore:

### Beginner Level
1. **Collect more data** - See how accuracy improves
2. **Try different objects** - Compare easy vs. hard objects
3. **Adjust confidence threshold** - Trade-off sensitivity vs. false positives

### Intermediate Level
4. **Multiple objects** - Train to recognize 3+ different objects
5. **Save snapshots** - Capture images when object is detected
6. **Add sound alerts** - Play sound on detection
7. **Data augmentation** - Flip, rotate, adjust brightness of training images

### Advanced Level
8. **Deep learning** - Replace Random Forest with a CNN (TensorFlow/Keras)
9. **Transfer learning** - Use MobileNet or ResNet as feature extractor
10. **Object localization** - Draw bounding box around detected object
11. **Web interface** - Create a Flask app for browser-based detection

## Comparison: Traditional ML vs. Deep Learning

**This demo (Traditional ML + Color Histograms):**
- ✅ Fast to train (seconds)
- ✅ Works with small datasets (30-50 images)
- ✅ Easy to understand
- ✅ No GPU needed
- ❌ Limited accuracy for complex objects
- ❌ Struggles with different backgrounds

**Deep Learning Alternative (CNN):**
- ✅ Higher accuracy possible
- ✅ Better at generalizing
- ✅ Can learn spatial features
- ❌ Needs more training data (hundreds of images)
- ❌ Slower to train
- ❌ Harder to understand
- ❌ Benefits from GPU

**For this demo:** Traditional ML is perfect! It's fast, understandable, and effective for teaching the core concepts.

## Additional Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Random Forest Explained](https://www.youtube.com/watch?v=J4Wdy0Wc_xQ)
- [Feature Engineering Guide](https://www.kaggle.com/learn/feature-engineering)

## Alternative: Google Teachable Machine

For an even simpler approach (no code), try:
- [Teachable Machine](https://teachablemachine.withgoogle.com/)
- Web-based, drag-and-drop interface
- Can export model for use in Python/JavaScript
- Great for quick demos!

---

**Happy Training!** 🎯
