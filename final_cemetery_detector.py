import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class RobustCemeteryDetector:
    def __init__(self):
        self.features = {}
        
    def load_image(self, image_path):
        """Load and preprocess the image"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert to RGB for display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Convert to grayscale for analysis
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        return img_rgb, img_gray
    
    def detect_regular_patterns(self, img_gray):
        """Detect regular grid patterns typical of cemeteries"""
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Detect horizontal and vertical lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        
        horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)
        
        # Combine lines
        grid_pattern = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0)
        
        # Calculate regularity score
        regularity_score = np.sum(grid_pattern) / (img_gray.shape[0] * img_gray.shape[1] * 255.0)
        
        return grid_pattern, regularity_score
    
    def analyze_texture_uniformity(self, img_gray):
        """Analyze texture uniformity using local standard deviation"""
        # Calculate local standard deviation
        kernel_size = 9
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        
        # Convert to float for calculations
        img_float = img_gray.astype(np.float32)
        
        # Calculate local mean
        local_mean = cv2.filter2D(img_float, -1, kernel)
        
        # Calculate local variance
        local_sq_mean = cv2.filter2D(img_float * img_float, -1, kernel)
        local_variance = local_sq_mean - local_mean * local_mean
        
        # Calculate uniformity (lower variance = more uniform)
        avg_variance = np.mean(local_variance)
        uniformity = 1.0 / (1.0 + avg_variance / 1000.0)
        
        return local_variance, uniformity
    
    def detect_rectangular_structures(self, img_gray):
        """Detect rectangular structures typical of cemetery plots"""
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangular_count = 0
        
        for contour in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular (4 sides) and has reasonable area
            if len(approx) == 4:
                area = cv2.contourArea(contour)
                if 100 < area < 10000:  # Filter reasonable sizes
                    rectangular_count += 1
        
        # Calculate rectangular density per unit area
        image_area = img_gray.shape[0] * img_gray.shape[1]
        rectangular_density = rectangular_count / (image_area / 100000.0)  # per 100k pixels
        
        return rectangular_count, min(rectangular_density, 1.0)
    
    def analyze_color_patterns(self, img_rgb):
        """Analyze color distribution patterns"""
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
        
        # Focus on vegetation (green areas)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Calculate green vegetation percentage
        green_percentage = np.sum(green_mask > 0) / (img_rgb.shape[0] * img_rgb.shape[1])
        
        # Analyze color uniformity in green regions
        if np.sum(green_mask) > 1000:  # Enough green pixels
            green_pixels = img_rgb[green_mask > 0]
            color_std = np.mean(np.std(green_pixels.astype(np.float32), axis=0))
            color_uniformity = 1.0 / (1.0 + color_std / 50.0)
        else:
            color_uniformity = 0
        
        return green_percentage, color_uniformity
    
    def analyze_line_patterns(self, img_gray):
        """Analyze line patterns using Hough Transform"""
        # Edge detection
        edges = cv2.Canny(img_gray, 50, 150)
        
        # Detect lines using Hough Transform
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        if lines is not None:
            # Count horizontal and vertical lines
            horizontal_lines = 0
            vertical_lines = 0
            
            for line in lines:
                rho, theta = line[0]
                angle = theta * 180 / np.pi
                
                # Check if line is horizontal (around 0° or 180°)
                if (angle < 10) or (angle > 170):
                    horizontal_lines += 1
                # Check if line is vertical (around 90°)
                elif 80 < angle < 100:
                    vertical_lines += 1
            
            # Calculate line regularity (balance of horizontal and vertical)
            total_lines = len(lines)
            if total_lines > 0:
                line_balance = 1.0 - abs(horizontal_lines - vertical_lines) / total_lines
                line_density = min(total_lines / 100.0, 1.0)
                line_regularity = line_balance * line_density
            else:
                line_regularity = 0
        else:
            line_regularity = 0
            
        return line_regularity
    
    def calculate_cemetery_score(self, image_path):
        """Calculate overall cemetery likelihood score"""
        try:
            # Load image
            img_rgb, img_gray = self.load_image(image_path)
            
            # Extract features
            grid_pattern, regularity_score = self.detect_regular_patterns(img_gray)
            variance_map, uniformity = self.analyze_texture_uniformity(img_gray)
            rect_count, rect_density = self.detect_rectangular_structures(img_gray)
            green_pct, color_uniformity = self.analyze_color_patterns(img_rgb)
            line_regularity = self.analyze_line_patterns(img_gray)
            
            # Store features for analysis
            features = {
                'regularity_score': regularity_score,
                'texture_uniformity': uniformity,
                'line_regularity': line_regularity,
                'rectangular_density': rect_density,
                'green_percentage': green_pct,
                'color_uniformity': color_uniformity
            }
            
            # Calculate weighted cemetery score
            cemetery_score = (
                regularity_score * 0.25 +           # Regular grid patterns
                uniformity * 0.20 +                 # Texture uniformity
                line_regularity * 0.20 +            # Line pattern regularity
                rect_density * 0.15 +               # Rectangular structures
                green_pct * 0.10 +                  # Vegetation presence
                color_uniformity * 0.10             # Color uniformity
            )
            
            return cemetery_score, features, img_rgb
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return 0, {}, None
    
    def visualize_analysis(self, image_path, save_plots=True):
        """Visualize the analysis results"""
        try:
            img_rgb, img_gray = self.load_image(image_path)
            
            # Get analysis results
            grid_pattern, regularity_score = self.detect_regular_patterns(img_gray)
            variance_map, uniformity = self.analyze_texture_uniformity(img_gray)
            
            # Create visualization
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            fig.suptitle(f'Cemetery Detection Analysis: {os.path.basename(image_path)}', fontsize=16)
            
            # Original image
            axes[0, 0].imshow(img_rgb)
            axes[0, 0].set_title('Original Image')
            axes[0, 0].axis('off')
            
            # Grayscale
            axes[0, 1].imshow(img_gray, cmap='gray')
            axes[0, 1].set_title('Grayscale Image')
            axes[0, 1].axis('off')
            
            # Grid pattern detection
            axes[0, 2].imshow(grid_pattern, cmap='gray')
            axes[0, 2].set_title(f'Grid Patterns\n(Score: {regularity_score:.4f})')
            axes[0, 2].axis('off')
            
            # Texture variance
            axes[1, 0].imshow(variance_map, cmap='jet')
            axes[1, 0].set_title(f'Texture Variance\n(Uniformity: {uniformity:.4f})')
            axes[1, 0].axis('off')
            
            # Edge detection
            edges = cv2.Canny(img_gray, 50, 150)
            axes[1, 1].imshow(edges, cmap='gray')
            axes[1, 1].set_title('Edge Detection')
            axes[1, 1].axis('off')
            
            # Feature summary
            score, features, _ = self.calculate_cemetery_score(image_path)
            feature_text = f"""Cemetery Score: {score:.4f}
            
Key Features:
• Grid Regularity: {features['regularity_score']:.4f}
• Texture Uniformity: {features['texture_uniformity']:.4f}
• Line Regularity: {features['line_regularity']:.4f}
• Rectangular Density: {features['rectangular_density']:.4f}
• Green Vegetation: {features['green_percentage']:.4f}
• Color Uniformity: {features['color_uniformity']:.4f}

Interpretation:
Score > 0.6: High cemetery likelihood
Score 0.3-0.6: Medium likelihood  
Score < 0.3: Low likelihood"""
            
            axes[1, 2].text(0.05, 0.95, feature_text, fontsize=9, 
                           verticalalignment='top', transform=axes[1, 2].transAxes,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
            axes[1, 2].set_title('Analysis Summary')
            axes[1, 2].axis('off')
            
            plt.tight_layout()
            
            if save_plots:
                plot_name = f"cemetery_analysis_{os.path.splitext(os.path.basename(image_path))[0]}.png"
                plt.savefig(plot_name, dpi=150, bbox_inches='tight')
                print(f"✅ Analysis plot saved as: {plot_name}")
            
            plt.show()
            
        except Exception as e:
            print(f"❌ Error in visualization: {e}")

def compare_images(image1_path, image2_path):
    """Compare two images and determine which is more likely a cemetery"""
    detector = RobustCemeteryDetector()
    
    print("🔍 Analyzing images for cemetery detection...\n")
    
    # Analyze first image
    print(f"📸 Analyzing: {os.path.basename(image1_path)}")
    score1, features1, img1 = detector.calculate_cemetery_score(image1_path)
    
    # Analyze second image  
    print(f"📸 Analyzing: {os.path.basename(image2_path)}")
    score2, features2, img2 = detector.calculate_cemetery_score(image2_path)
    
    # Results
    print("\n" + "="*60)
    print("🏛️  CEMETERY DETECTION RESULTS")
    print("="*60)
    
    print(f"\n📊 {os.path.basename(image1_path)}:")
    print(f"   🎯 Cemetery Score: {score1:.4f}")
    for key, value in features1.items():
        print(f"   • {key.replace('_', ' ').title()}: {value:.4f}")
    
    print(f"\n📊 {os.path.basename(image2_path)}:")
    print(f"   🎯 Cemetery Score: {score2:.4f}")
    for key, value in features2.items():
        print(f"   • {key.replace('_', ' ').title()}: {value:.4f}")
    
    # Conclusion
    print("\n" + "="*60)
    print("🔬 FINAL CONCLUSION")
    print("="*60)
    
    if abs(score1 - score2) < 0.05:
        print("🤔 RESULT: Both images have very similar cemetery likelihood scores")
        print(f"   Difference is only {abs(score1 - score2):.4f} - too close to call definitively")
    elif score1 > score2:
        confidence = ((score1 - score2) / max(score1, 0.001)) * 100
        print(f"🏆 WINNER: {os.path.basename(image1_path)} is more likely a cemetery")
        print(f"   📈 Confidence Level: {confidence:.1f}%")
        
        # Explain why
        if score1 > 0.6:
            print(f"   ✅ High cemetery likelihood (score: {score1:.4f})")
        elif score1 > 0.3:
            print(f"   ⚠️  Medium cemetery likelihood (score: {score1:.4f})")
        else:
            print(f"   ❌ Low cemetery likelihood (score: {score1:.4f})")
            
    elif score2 > score1:
        confidence = ((score2 - score1) / max(score2, 0.001)) * 100
        print(f"🏆 WINNER: {os.path.basename(image2_path)} is more likely a cemetery")
        print(f"   📈 Confidence Level: {confidence:.1f}%")
        
        # Explain why
        if score2 > 0.6:
            print(f"   ✅ High cemetery likelihood (score: {score2:.4f})")
        elif score2 > 0.3:
            print(f"   ⚠️  Medium cemetery likelihood (score: {score2:.4f})")
        else:
            print(f"   ❌ Low cemetery likelihood (score: {score2:.4f})")
    
    print("="*60)
    
    # Key insights
    print("\n🔍 KEY INSIGHTS:")
    if score1 > 0.6 or score2 > 0.6:
        print("• Strong cemetery features detected - regular patterns and organized layout")
    elif score1 > 0.3 or score2 > 0.3:
        print("• Some cemetery-like features present - partial organization visible")
    else:
        print("• Limited cemetery features - may be natural landscape or other structures")
    
    # Generate detailed visualizations
    print(f"\n📊 Generating detailed analysis visualizations...")
    detector.visualize_analysis(image1_path)
    detector.visualize_analysis(image2_path)
    
    print("\n✨ Analysis complete! Check the generated plots for visual details.")
    
    return score1, score2

if __name__ == "__main__":
    # Analyze your cemetery images
    image1 = "cemetry_image_1.png"   # First cemetery image
    image2 = "cemetry_image_2.png"   # Second cemetery image
    
    print("🏛️  CEMETERY DETECTION SYSTEM")
    print("="*50)
    print("Using Traditional Computer Vision + Feature Analysis")
    print("Comprehensive analysis of your cemetery satellite images!")
    print("="*50)
    
    if os.path.exists(image1) and os.path.exists(image2):
        compare_images(image1, image2)
    else:
        print("❌ Missing image files!")
        print("Please make sure both cemetery images are in the current directory:")
        print(f"   📁 {image1}")
        print(f"   📁 {image2}")
        print("\nCurrent directory contents:")
        for file in os.listdir("."):
            if file.endswith(('.png', '.jpg', '.jpeg')):
                print(f"   🖼️  {file}")
