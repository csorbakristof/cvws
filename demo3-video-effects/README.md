# Demo 3 - Video Effects with cv2.remap()

This demo shows creative video effects using OpenCV's powerful `cv2.remap()` function in Python, demonstrating how geometric transformations create effects similar to those seen on social media platforms.

## Features

- **Kaleidoscope Effect** - Mesmerizing radial symmetry pattern
- **Mirror Effect** - Simple vertical mirroring
- **Fisheye Effect** - Wide-angle lens distortion
- **Swirl Effect** - Spiral twist transformation
- **Barrel Distortion** - Camera lens-style warping
- **Interactive Controls** - Adjust parameters in real-time
- **Side-by-Side Comparison** - See original and effect together

## Requirements

- Python 3.8 or later
- Webcam (or video file)
- OpenCV and NumPy (see requirements.txt)

## Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `opencv-python` - Computer vision library
- `numpy` - Numerical computing

## Usage

### 1. Kaleidoscope Effect (Main Demo)

The star of the show - creates a beautiful kaleidoscope pattern:

```bash
python kaleidoscope_effect.py
```

**Interactive Controls:**
- **+** or **=** - Add more segments (more mirrors)
- **-** or **_** - Remove segments
- **z** - Zoom in
- **x** - Zoom out
- **r** - Reset to defaults
- **q** or **ESC** - Quit

**Command-line options:**
```bash
# Use a video file instead of webcam
python kaleidoscope_effect.py --source myvideo.mp4

# Start with 12 segments
python kaleidoscope_effect.py --segments 12

# Start zoomed in 1.5x
python kaleidoscope_effect.py --zoom 1.5
```

**Tips for best results:**
- Move your hand slowly in front of the camera
- Try different numbers of segments (6, 8, 12 work great)
- Colorful objects create stunning patterns
- Works amazingly with faces!

### 2. Multi-Effect Demo

Switch between multiple effects interactively:

```bash
python simple_effects.py
```

**Interactive Controls:**
- **0** - Original (no effect)
- **1** - Mirror effect
- **2** - Fisheye effect
- **3** - Swirl effect
- **4** - Barrel distortion
- **+/-** - Adjust effect strength
- **q** or **ESC** - Quit

**Great for teaching:** Shows different transformation types side by side.

### 3. Comparison Demo

See original and kaleidoscope side by side:

```bash
python comparison_demo.py
```

Perfect for presentations - clearly shows the transformation in real-time.

## How It Works

### The Magic of cv2.remap()

All geometric effects use OpenCV's `cv2.remap()` function:

```python
# For each pixel in the output image,
# remap tells it which pixel to copy from the input image

output = cv2.remap(input_image, mapX, mapY, interpolation)
```

**Key concepts:**
- `mapX` - Array saying "for each output pixel, get X coordinate from input"
- `mapY` - Array saying "for each output pixel, get Y coordinate from input"
- By creating different maps, we create different effects

### Example: Mirror Effect (Simple)

```python
# Just flip one half of the image
left_half = frame[:, :width//2]
flipped = cv2.flip(left_half, 1)
result[:, width//2:] = flipped
```

### Example: Kaleidoscope Effect (Using remap)

```python
# 1. Create coordinate maps
mapX = np.zeros((height, width))
mapY = np.zeros((height, width))

# 2. For each output pixel...
for y in range(height):
    for x in range(width):
        # Convert to polar coordinates (radius, angle)
        radius = distance_from_center(x, y)
        angle = angle_from_center(x, y)
        
        # Apply symmetry - map to first segment
        segment_angle = 2*pi / num_segments
        new_angle = angle % segment_angle
        
        # Mirror alternating segments
        if segment_number is odd:
            new_angle = segment_angle - new_angle
        
        # Convert back to cartesian
        mapX[y, x], mapY[y, x] = polar_to_cartesian(radius, new_angle)

# 3. Apply transformation
kaleidoscope = cv2.remap(frame, mapX, mapY, cv2.INTER_LINEAR)
```

### Coordinate Transformation Pipeline

```
Input Pixel (x, y)
    ↓
Convert to Polar Coordinates (radius, angle)
    ↓
Apply Effect (modify radius and/or angle)
    ↓
Convert back to Cartesian (new_x, new_y)
    ↓
Store in mapX[y,x] and mapY[y,x]
    ↓
Use cv2.remap() to create output
```

## Teaching Points for Class

### Core Concepts

1. **Images are 2D Arrays**
   - Each pixel has a position (x, y) and color (R, G, B)
   - We can move pixels around to create effects
   - The image content doesn't change, just where it appears

2. **Coordinate Systems**
   - **Cartesian**: (x, y) - usual screen coordinates
   - **Polar**: (radius, angle) - distance and direction from center
   - Converting between them enables circular effects

3. **Pre-computation for Speed**
   - Maps are computed once, then reused
   - Real-time effects need 30+ FPS
   - Pre-computing maps makes it fast enough

4. **Interpolation**
   - Maps often specify fractional coordinates (e.g., 125.7, 89.3)
   - Interpolation blends nearby pixels for smooth results
   - `INTER_LINEAR` is good balance of quality and speed

### Discussion Questions

1. **Where do you see these effects?**
   - Instagram, Snapchat, TikTok filters
   - Video conferencing (Zoom backgrounds)
   - VR headset lens correction
   - 360° video players
   - Photo editing apps

2. **Why use polar coordinates?**
   - Easier to create circular/radial effects
   - Natural for rotation and mirroring around a center
   - Kaleidoscope needs radial symmetry

3. **What other effects could you create?**
   - Ripple effect (like dropping stone in water)
   - Tunnel effect (zooming inward spiral)
   - Pixelation (map multiple output pixels to same input pixel)
   - Time delay (mix current and past frames)

4. **Real-world applications beyond fun?**
   - Lens distortion correction (cameras, VR headsets)
   - Image registration (aligning medical scans)
   - Panorama stitching
   - Augmented reality transformations

### Code Structure Walkthrough

For a 45-minute class, walk through this progression:

**Step 1: Show the mirror effect (5 min)**
- Simplest example
- No remap needed
- Shows the core idea: "move pixels around"

**Step 2: Explain cv2.remap() concept (5 min)**
- Draw on whiteboard: input image, output image, mapping
- "For each output pixel, which input pixel do we copy?"
- Show mapX and mapY as "instruction sheets"

**Step 3: Live kaleidoscope demo (5 min)**
- Run with webcam
- Adjust segments interactively (+ and -)
- Let students see themselves in the effect
- Move objects for "wow factor"

**Step 4: Code walkthrough (10 min)**
- Show the polar coordinate conversion
- Explain the segment angle calculation
- Highlight the mirroring logic
- Show how it all becomes mapX and mapY

**Step 5: Experimentation (10 min)**
- Let students try different parameters
- Show other effects (swirl, fisheye)
- Discuss how each is different mathematically

**Step 6: Connections and extensions (10 min)**
- Link to social media filters
- Discuss face detection + effects (combines demos 1 and 3!)
- Show how professionals create filters
- Ideas for student projects

## Performance Tips

### For Smooth Real-time Effects

1. **Pre-compute maps** - Do this once, not every frame
2. **Reduce resolution** - 640x480 is plenty for demos
3. **Use efficient interpolation** - `INTER_LINEAR` is fast
4. **Limit frame processing** - 30 FPS is smooth enough

### If experiencing lag:

```python
# Reduce webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Or use faster interpolation
output = cv2.remap(frame, mapX, mapY, cv2.INTER_NEAREST)
```

## Extension Ideas

### For Students to Try

**Beginner:**
1. **Change kaleidoscope colors** - Add color filters (HSV adjustments)
2. **Combine effects** - Apply swirl, then kaleidoscope
3. **Adjust default parameters** - Start with 12 segments instead of 8
4. **Add more keyboard controls** - Rotate the pattern

**Intermediate:**
5. **Animated effects** - Slowly rotate kaleidoscope over time
6. **Face-centered kaleidoscope** - Use face detection to center effect on face
7. **Record output** - Save effect video to file
8. **Multiple simultaneous effects** - Show 4 different effects in a grid

**Advanced:**
9. **Custom mathematical transformations** - Create your own unique effect
10. **Real-time parameter sliders** - Use trackbars for controls
11. **Combine with Demo 1** - Apply effects only to detected faces
12. **AR marker-based effects** - Trigger different effects based on detected markers

## Troubleshooting

### Webcam not working
- Check if another app is using it
- Try `--source 1` for different camera
- Use a video file: `--source myvideo.mp4`

### Low FPS / Laggy
- Reduce resolution (edit code to use smaller frame size)
- Use `cv2.INTER_NEAREST` instead of `cv2.INTER_LINEAR`
- Close other applications
- Reduce number of segments (for kaleidoscope)

### Image looks distorted at edges
- This is expected - the effect wraps around
- Try different zoom levels
- Some distortion is inherent to the transformation

### "Module not found" error
```
ModuleNotFoundError: No module named 'cv2'
```
**Solution:** Run `pip install -r requirements.txt`

## Understanding the Math

### Polar Coordinates

```
Cartesian (x, y) → Polar (r, θ)

r = sqrt(x² + y²)         # Distance from center
θ = atan2(y, x)           # Angle from center

Polar (r, θ) → Cartesian (x, y)

x = r * cos(θ)
y = r * sin(θ)
```

### Kaleidoscope Segments

For `N` segments, each segment spans `2π/N` radians:

```
N = 6 segments
segment_angle = 2π/6 = π/3 ≈ 60°

Input angle: 45° → Segment 0 → Output: 45°
Input angle: 90° → Segment 1 → Output: 60° (mirrored)
Input angle: 135° → Segment 2 → Output: 45°
...
```

The mirroring creates the kaleidoscope symmetry!

## Connection to Professional Tools

### Social Media Filters

Professional filters (Snapchat Lenses, Instagram AR) combine:
- **Face detection** (Demo 1) - Find the face
- **Face landmarks** (68 facial points) - Track eyes, nose, mouth
- **Geometric transforms** (Demo 3) - Warp, distort, add effects
- **3D rendering** - Add masks, objects
- **Particle systems** - Sparkles, animations

This demo teaches the geometric transformation foundation!

### Video Editing Software

Adobe After Effects, Final Cut Pro, etc. use similar techniques:
- Lens correction tools
- Warp/distort effects
- Optical flow for motion
- All based on pixel remapping!

## Resources

- [OpenCV cv2.remap() Documentation](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gab75ef31ce5cdfb5c44b6da5f3b908ea4)
- [Coordinate Systems Explained](https://mathworld.wolfram.com/PolarCoordinates.html)
- [Lens Distortion Models](https://en.wikipedia.org/wiki/Distortion_(optics))
- [Creating Instagram-like Filters](https://www.youtube.com/results?search_query=create+instagram+filters)

---

**Have fun creating visual magic!** ✨🎨
