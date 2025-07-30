# 🏛️ Cemetery Detection Model - Usage Guide

## 🚀 How to Run the Cemetery Detection Model

### **Method 1: Interactive Script (Recommended)**
```bash
python run_cemetery_detector.py
```
This script will:
- ✅ Automatically find all images in your folder
- ✅ Let you choose what to analyze
- ✅ Show detailed results and visualizations
- ✅ Works with any image format (PNG, JPG, etc.)

### **Method 2: Direct Analysis**
```bash
python final_cemetery_detector.py
```
This will analyze the specific images set in the script.

### **Method 3: Command Line (Custom)**
```python
from final_cemetery_detector import RobustCemeteryDetector

detector = RobustCemeteryDetector()
score, features, img = detector.calculate_cemetery_score("your_image.png")
print(f"Cemetery Score: {score:.4f}")
```

## 📋 Step-by-Step Instructions

### **Step 1: Prepare Your Images**
1. Save your satellite images in this folder:
   ```
   C:\Kartikeye\Cemetry-Image-Detection\Cemetery-Image-Detection\
   ```
2. Any image format works: `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`
3. Name them anything you want (e.g., `my_satellite_image.png`)

### **Step 2: Run the Detection**
1. Open terminal in the project folder
2. Run: `python run_cemetery_detector.py`
3. Follow the interactive prompts

### **Step 3: Interpret Results**

**🎯 Cemetery Score Interpretation:**
- **0.7 - 1.0**: 🏆 **HIGH** - Very likely a cemetery
- **0.4 - 0.7**: ⚠️ **MEDIUM** - Some cemetery characteristics
- **0.0 - 0.4**: ❌ **LOW** - Unlikely to be a cemetery

**📊 Feature Analysis:**
- **Regularity Score**: Grid patterns and organization
- **Rectangular Density**: Individual burial plots detected
- **Line Regularity**: Pathways and boundaries
- **Texture Uniformity**: Surface consistency
- **Green Percentage**: Vegetation coverage
- **Color Uniformity**: Color pattern consistency

## 🔧 What the Model Detects

The model analyzes these cemetery characteristics:
- ✅ **Regular grid patterns** (organized layout)
- ✅ **Rectangular structures** (burial plots)
- ✅ **Linear features** (pathways, boundaries)
- ✅ **Texture patterns** (consistent surfaces)
- ✅ **Color distribution** (vegetation vs. paved areas)
- ✅ **Spatial organization** (uniform spacing)

## 📊 Output Files

After running, you'll get:
1. **Console Results** - Scores and analysis summary
2. **Visualization Plots** - `cemetery_analysis_[filename].png`
3. **Feature Breakdown** - Detailed feature scores

## 💡 Tips for Best Results

**✅ Good Images:**
- High-resolution satellite/aerial views
- Clear view of ground details
- Good contrast between features
- Covers sufficient area to show patterns

**❌ Avoid:**
- Very low resolution images
- Heavily zoomed-in close-ups
- Poor quality or blurry images
- Images without clear ground features

## 🛠️ Troubleshooting

**Problem: "No images found"**
- Solution: Make sure images are in the correct folder and have supported extensions

**Problem: "Error loading image"**
- Solution: Check if image file is corrupted or in unsupported format

**Problem: "Low scores for obvious cemetery"**
- Solution: Image might be too zoomed in/out or low quality

**Problem: "ImportError or module not found"**
- Solution: Make sure you've installed requirements: `pip install -r requirements.txt`

## 📞 Quick Start Example

```bash
# 1. Navigate to project folder
cd "C:\Kartikeye\Cemetry-Image-Detection\Cemetery-Image-Detection"

# 2. Add your image (e.g., satellite_image.png)

# 3. Run detection
python run_cemetery_detector.py

# 4. Choose option 1 to analyze your image

# 5. View results and generated visualization plot
```

Your model is ready to detect cemeteries in any satellite image! 🚀
