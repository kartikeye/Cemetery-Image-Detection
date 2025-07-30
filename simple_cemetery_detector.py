import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import ndimage

class SimpleCemeteryDetector:
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
        
        # Detect horizontal and vertical lines using morphological operations
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        
        horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)
        
        # Combine lines
        grid_pattern = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0)
        
        # Calculate regularity score
        regularity_score = np.sum(grid_pattern) / (img_gray.shape[0] * img_gray.shape[1])
        
        return grid_pattern, regularity_score
    
    def analyze_texture_variance(self, img_gray):
        """Analyze texture using local variance"""
        # Calculate local variance using a sliding window
        kernel = np.ones((9, 9), np.float32) / 81
        mean = cv2.filter2D(img_gray.astype(np.float32), -1, kernel)
        sq_mean = cv2.filter2D((img_gray.astype(np.float32))**2, -1, kernel)
        variance = sq_mean - mean**2
        
        # Calculate uniformity (inverse of variance)
        avg_variance = np.mean(variance)
        uniformity = 1.0 / (1.0 + avg_variance / 100.0)
        
        return variance, uniformity
    
    def detect_rectangular_structures(self, img_gray):
        """Detect rectangular structures typical of cemetery plots"""
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangular_count = 0
        total_area = 0
        
        for contour in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular (4 sides)
            if len(approx) == 4:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter out very small rectangles
                    rectangular_count += 1
                    total_area += area
        
        # Calculate rectangular density
        image_area = img_gray.shape[0] * img_gray.shape[1]
        rectangular_density = rectangular_count / (image_area / 10000)  # per 100x100 pixels
        
        return rectangular_count, rectangular_density
    
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
        if np.sum(green_mask) > 0:
            green_pixels = img_rgb[green_mask > 0]
            color_std = np.mean(np.std(green_pixels, axis=0))
            color_uniformity = 1.0 / (1.0 + color_std)
        else:
            color_uniformity = 0
        
        return green_percentage, color_uniformity
    
    def detect_periodic_patterns(self, img_gray):
        """Detect periodic patterns using frequency analysis"""
        # Apply FFT to detect periodic patterns
        f_transform = np.fft.fft2(img_gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.log(np.abs(f_shift) + 1)
        
        # Analyze the frequency domain for regular patterns
        h, w = magnitude_spectrum.shape
        center_h, center_w = h // 2, w // 2
        
        # Look for peaks away from center (indicating periodicity)
        mask = np.zeros_like(magnitude_spectrum, dtype=np.uint8)
        cv2.circle(mask, (center_w, center_h), min(h, w) // 8, 1, -1)
        
        # Calculate pattern regularity
        periodic_energy = np.sum(magnitude_spectrum * mask)
        total_energy = np.sum(magnitude_spectrum)
        pattern_regularity = periodic_energy / total_energy if total_energy > 0 else 0
        
        return magnitude_spectrum, pattern_regularity
    
    def calculate_cemetery_score(self, image_path):
        """Calculate overall cemetery likelihood score"""
        try:
            # Load image
            img_rgb, img_gray = self.load_image(image_path)
            
            # Extract features
            grid_pattern, regularity_score = self.detect_regular_patterns(img_gray)
            variance_map, uniformity = self.analyze_texture_variance(img_gray)
            rect_count, rect_density = self.detect_rectangular_structures(img_gray)
            green_pct, color_uniformity = self.analyze_color_patterns(img_rgb)
            freq_spectrum, pattern_regularity = self.detect_periodic_patterns(img_gray)
            
            # Store features for analysis
            features = {
                'regularity_score': regularity_score,
                'texture_uniformity': uniformity,
                'pattern_regularity': pattern_regularity,
                'rectangular_density': rect_density,
                'green_percentage': green_pct,
                'color_uniformity': color_uniformity
            }
            
            # Calculate weighted cemetery score
            cemetery_score = (
                regularity_score * 0.25 +           # Regular grid patterns
                uniformity * 0.20 +                 # Texture uniformity
                pattern_regularity * 0.20 +         # Frequency domain patterns
                min(rect_density, 1.0) * 0.15 +     # Rectangular structures
                green_pct * 0.10 +                  # Vegetation presence
                color_uniformity * 0.10              # Color uniformity
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
            variance_map, uniformity = self.analyze_texture_variance(img_gray)
            freq_spectrum, pattern_regularity = self.detect_periodic_patterns(img_gray)
            
            # Create visualization
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            fig.suptitle(f'Cemetery Detection Analysis: {os.path.basename(image_path)}', fontsize=16)
            
            # Original image
            axes[0, 0].imshow(img_rgb)
            axes[0, 0].set_title('Original Image')
            axes[0, 0].axis('off')
            
            # Grayscale
            axes[0, 1].imshow(img_gray, cmap='gray')
            axes[0, 1].set_title('Grayscale')
            axes[0, 1].axis('off')
            
            # Grid pattern detection
            axes[0, 2].imshow(grid_pattern, cmap='gray')
            axes[0, 2].set_title(f'Grid Patterns (Score: {regularity_score:.4f})')
            axes[0, 2].axis('off')
            
            # Texture variance
            axes[1, 0].imshow(variance_map, cmap='jet')
            axes[1, 0].set_title(f'Texture Variance (Uniformity: {uniformity:.4f})')
            axes[1, 0].axis('off')
            
            # Edge detection
            edges = cv2.Canny(img_gray, 50, 150)
            axes[1, 1].imshow(edges, cmap='gray')
            axes[1, 1].set_title('Edge Detection')
            axes[1, 1].axis('off')
            
            # Feature summary
            score, features, _ = self.calculate_cemetery_score(image_path)
            feature_text = f"""Cemetery Score: {score:.4f}
            
Features:
• Regularity: {features['regularity_score']:.4f}
• Texture Uniformity: {features['texture_uniformity']:.4f}
• Pattern Regularity: {features['pattern_regularity']:.4f}
• Rectangular Density: {features['rectangular_density']:.4f}
• Green Vegetation: {features['green_percentage']:.4f}
• Color Uniformity: {features['color_uniformity']:.4f}"""
            
            axes[1, 2].text(0.1, 0.5, feature_text, fontsize=10, 
                           verticalalignment='center', transform=axes[1, 2].transAxes)
            axes[1, 2].set_title('Feature Summary')
            axes[1, 2].axis('off')
            
            plt.tight_layout()
            
            if save_plots:
                plot_name = f"analysis_{os.path.splitext(os.path.basename(image_path))[0]}.png"
                plt.savefig(plot_name, dpi=300, bbox_inches='tight')
                print(f"Analysis plot saved as: {plot_name}")
            
            plt.show()
            
        except Exception as e:
            print(f"Error in visualization: {e}")

def compare_images(image1_path, image2_path):
    """Compare two images and determine which is more likely a cemetery"""
    detector = SimpleCemeteryDetector()
    
    print("Analyzing images for cemetery detection...\n")
    
    # Analyze first image
    print(f"Analyzing: {os.path.basename(image1_path)}")
    score1, features1, img1 = detector.calculate_cemetery_score(image1_path)
    
    # Analyze second image
    print(f"Analyzing: {os.path.basename(image2_path)}")
    score2, features2, img2 = detector.calculate_cemetery_score(image2_path)
    
    # Results
    print("\n" + "="*50)
    print("CEMETERY DETECTION RESULTS")
    print("="*50)
    
    print(f"\n{os.path.basename(image1_path)}:")
    print(f"  Cemetery Score: {score1:.4f}")
    for key, value in features1.items():
        print(f"  {key.replace('_', ' ').title()}: {value:.4f}")
    
    print(f"\n{os.path.basename(image2_path)}:")
    print(f"  Cemetery Score: {score2:.4f}")
    for key, value in features2.items():
        print(f"  {key.replace('_', ' ').title()}: {value:.4f}")
    
    # Conclusion
    print("\n" + "="*50)
    if score1 > score2:
        confidence = (score1 - score2) / max(score1, 0.001) * 100
        print(f"CONCLUSION: {os.path.basename(image1_path)} is more likely a cemetery")
        print(f"Confidence: {confidence:.1f}%")
    elif score2 > score1:
        confidence = (score2 - score1) / max(score2, 0.001) * 100
        print(f"CONCLUSION: {os.path.basename(image2_path)} is more likely a cemetery")
        print(f"Confidence: {confidence:.1f}%")
    else:
        print("CONCLUSION: Both images have similar cemetery likelihood scores")
    
    print("="*50)
    
    # Generate detailed visualizations
    print("\nGenerating detailed analysis visualizations...")
    detector.visualize_analysis(image1_path)
    detector.visualize_analysis(image2_path)
    
    return score1, score2

if __name__ == "__main__":
    # Example usage
    image1 = "cemetry_image_1.png"
    image2 = "cemetry_image_2.png"
    
    if os.path.exists(image1) and os.path.exists(image2):
        compare_images(image1, image2)
    else:
        print("Please make sure both cemetery images are in the current directory:")
        print("- cemetry_image_1.png")
        print("- cemetry_image_2.png")
