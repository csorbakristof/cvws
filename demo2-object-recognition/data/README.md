# Training Data Directory

This directory will contain your training images.

## Structure

```
data/
├── positive/     # Images of your target object
└── negative/     # Images of other objects/backgrounds
```

## How to Populate

Run the data collection tool:

```bash
python collect_training_data.py
```

## Guidelines

### Positive Examples (target object)
- 30-50 images recommended
- Different angles (front, side, top)
- Different distances (close, medium, far)
- Different lighting conditions
- Rotate the object between captures
- Keep the object clearly visible

### Negative Examples (not the target)
- 30-50 images recommended
- Different objects (not your target)
- Empty backgrounds
- Similar but different items
- Various scenes without the target object

## Tips for Best Results

1. **Diversity matters** - More variety in your training data = better model
2. **Balance classes** - Similar number of positive and negative examples
3. **Clear images** - Make sure object is visible and in focus
4. **Representative data** - Include conditions you'll test under
5. **Avoid bias** - Don't always have the same background or lighting

## Example

If training to recognize a blue water bottle:
- **Positive**: Blue bottle from 20+ angles, on desk, in hand, different lighting
- **Negative**: Red bottle, coffee mug, empty desk, other objects, plain backgrounds

---

After collecting data, run: `python train_model.py`
