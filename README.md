# Cemetery Detection Using Computer Vision

This project implements traditional computer vision techniques to detect cemeteries in satellite images. It analyzes various visual features that are characteristic of cemetery locations.

## 🎯 What This Does

The system analyzes satellite images and identifies cemetery locations by detecting:

- **Regular Grid Patterns**: Cemeteries have organized, geometric layouts
- **Texture Uniformity**: Consistent patterns from gravestones and pathways  
- **Rectangular Structures**: Individual burial plots and tomb structures
- **Vegetation Patterns**: Maintained grass areas with regular spacing
- **Color Distribution**: Uniform green areas with pathway networks

## 🔧 Features Analyzed

### 1. **Regular Pattern Detection**
- Uses Canny edge detection and morphological operations
- Detects horizontal and vertical line patterns
- Calculates regularity score based on grid-like structures

### 2. **Texture Analysis (Local Binary Patterns)**
- Analyzes micro-texture patterns in the image
- Measures uniformity of surface textures
- Higher uniformity indicates organized cemetery layouts

### 3. **Gabor Filter Analysis**
- Detects oriented patterns at different frequencies
- Analyzes pattern consistency across different orientations
- Measures how regular and repetitive the patterns are

### 4. **Rectangular Structure Detection**
- Uses contour detection to find rectangular shapes
- Counts and measures density of rectangular plots
- Filters out noise by size thresholding

### 5. **Color Pattern Analysis**
- Analyzes vegetation (green areas) distribution
- Measures color uniformity in green regions
- Calculates vegetation percentage

## 📁 Project Structure

```
Cemetery-Image-Detection/
├── cemetery_detector.py      # Main detection algorithm
├── run_analysis.py          # Quick start script
├── requirements.txt         # Python dependencies
├── cemetry_image_1.png     # Your first satellite image
├── cemetry_image_2.png     # Your second satellite image
└── README.md               # This file
```

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Add Your Images
Place your satellite images in the project folder:
- `cemetry_image_1.png` - First satellite image
- `cemetry_image_2.png` - Second satellite image

### Step 3: Run Analysis
```bash
python run_analysis.py
```

## 📊 Understanding the Results

The system generates:

1. **Cemetery Score** (0.0 to 1.0): Overall likelihood of being a cemetery
2. **Feature Breakdown**: Individual scores for each analyzed feature
3. **Visual Analysis**: Generated plots showing detected patterns
4. **Comparison**: Which image is more likely a cemetery

### Score Interpretation:
- **0.0 - 0.3**: Low probability of cemetery
- **0.3 - 0.6**: Medium probability of cemetery  
- **0.6 - 1.0**: High probability of cemetery

## 🔬 Technical Details

### Algorithm Weights:
- Regular Grid Patterns: 25%
- Texture Uniformity: 20%
- Pattern Consistency: 20%
- Rectangular Density: 15%
- Vegetation Presence: 10%
- Color Uniformity: 10%

### Key Parameters:
```python
# Edge detection
canny_low = 50, canny_high = 150

# LBP texture analysis
radius = 3, n_points = 24

# Gabor filters
angles = [0°, 45°, 90°, 135°]
frequencies = [0.1, 0.3, 0.5]

# Color analysis (HSV)
green_range = [35-85, 40-255, 40-255]
```

## 📈 Sample Output

```
==================================================
CEMETERY DETECTION RESULTS
==================================================

cemetry_image_1.png:
  Cemetery Score: 0.7234
  Regularity Score: 0.0456
  Texture Uniformity: 0.8123
  Pattern Consistency: 0.6789
  Rectangular Density: 0.3456
  Green Percentage: 0.5678
  Color Uniformity: 0.7890

cemetry_image_2.png:
  Cemetery Score: 0.4567
  ...

==================================================
CONCLUSION: cemetry_image_1.png is more likely a cemetery
Confidence: 85.3%
==================================================
```

## 🛠️ Customization

### Adjusting Sensitivity:
Edit `cemetery_detector.py` to modify:

```python
# Line 160: Adjust score weights
cemetery_score = (
    regularity_score * 0.25 +      # Increase for more grid sensitivity
    uniformity * 0.20 +            # Increase for texture importance
    pattern_consistency * 0.20 +   # Increase for pattern regularity
    min(rect_density, 1.0) * 0.15 + # Rectangular structure importance
    green_pct * 0.10 +             # Vegetation importance
    color_uniformity * 0.10        # Color uniformity importance
)
```

### Adding New Features:
You can extend the `CemeteryDetector` class with additional analysis methods:

```python
def your_custom_analysis(self, img_gray):
    # Your custom feature detection
    return feature_score
```

## 📸 Image Requirements

- **Format**: PNG, JPG, or similar
- **Type**: Satellite or aerial imagery
- **Resolution**: At least 500x500 pixels recommended
- **Content**: Should show ground-level details clearly

## 🔍 Troubleshooting

### Common Issues:

1. **Import Errors**: Run `pip install -r requirements.txt`
2. **Image Not Loading**: Check file paths and formats
3. **Low Scores**: Images might be too zoomed out or unclear
4. **Similar Scores**: Both images might have similar characteristics

### Tips for Better Results:

- Use high-resolution satellite images
- Ensure images show clear ground details
- Avoid very zoomed-out or very zoomed-in images
- Images should have good contrast and clarity

## 📝 Next Steps

After running this analysis, you can:

1. **Collect More Data**: Use the insights to gather more cemetery images
2. **Refine Parameters**: Adjust weights based on your specific imagery
3. **Add Deep Learning**: Use this as preprocessing for CNN models
4. **Extend Features**: Add more sophisticated analysis methods

## 🤝 Contributing

Feel free to extend this project by:
- Adding new feature detection methods
- Improving the scoring algorithm
- Adding support for different image formats
- Creating a GUI interface

---

**Note**: This is a traditional computer vision approach. For production use with larger datasets, consider combining with deep learning methods for improved accuracy.
