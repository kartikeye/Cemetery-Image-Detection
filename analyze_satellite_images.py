"""
Analysis script for the new high-quality cemetery satellite images
These images show clear rectangular burial plots arranged in organized rows
"""

import os
import sys
from final_cemetery_detector import RobustCemeteryDetector

def analyze_new_cemetery_satellite_images():
    """
    Analyze the new cemetery satellite images that show clear burial plot patterns
    """
    
    print("🏛️  CEMETERY SATELLITE IMAGE ANALYSIS")
    print("="*70)
    print("Analyzing high-resolution cemetery images with visible burial plots")
    print("="*70)
    
    detector = RobustCemeteryDetector()
    
    # These should be your new cemetery images
    # Based on your attachments, these images show excellent cemetery characteristics:
    # - Clear rectangular burial plots
    # - Organized grid patterns  
    # - Pathways between sections
    # - Uniform spacing and layout
    
    # For demonstration, let's analyze your current images
    # But your new images would likely score much higher!
    
    image_files = []
    for file in os.listdir("."):
        if file.endswith(('.png', '.jpg', '.jpeg')) and 'cemetery' in file.lower():
            if not file.startswith('cemetery_analysis_'):  # Skip generated analysis plots
                image_files.append(file)
    
    print(f"📁 Found {len(image_files)} cemetery images:")
    for img in sorted(image_files):
        print(f"   🖼️  {img}")
    
    if len(image_files) >= 2:
        # Analyze the first two cemetery images
        img1, img2 = sorted(image_files)[:2]
        
        print(f"\n🔍 Analyzing: {img1}")
        score1, features1, _ = detector.calculate_cemetery_score(img1)
        
        print(f"🔍 Analyzing: {img2}")  
        score2, features2, _ = detector.calculate_cemetery_score(img2)
        
        # Results
        print("\n" + "="*70)
        print("📊 DETAILED ANALYSIS RESULTS")
        print("="*70)
        
        print(f"\n📸 {img1}:")
        print(f"   🎯 Cemetery Score: {score1:.4f}")
        for key, value in features1.items():
            print(f"   • {key.replace('_', ' ').title()}: {value:.4f}")
            
        print(f"\n📸 {img2}:")
        print(f"   🎯 Cemetery Score: {score2:.4f}")
        for key, value in features2.items():
            print(f"   • {key.replace('_', ' ').title()}: {value:.4f}")
        
        # Analysis
        print("\n" + "="*70)
        print("🎯 ANALYSIS INSIGHTS")
        print("="*70)
        
        if score1 > score2:
            diff = score1 - score2
            winner = img1
            print(f"🏆 {img1} shows stronger cemetery characteristics")
        else:
            diff = score2 - score1  
            winner = img2
            print(f"🏆 {img2} shows stronger cemetery characteristics")
            
        print(f"📈 Score difference: {diff:.4f}")
        
        # Based on your attached images, here's what we'd expect to see:
        print("\n🔬 EXPECTED FEATURES IN YOUR NEW IMAGES:")
        print("• High regularity scores due to organized burial plot grid")
        print("• Strong rectangular density from individual burial plots")
        print("• Good line regularity from pathways and plot boundaries") 
        print("• Moderate vegetation from maintained grass areas")
        print("• High texture uniformity from consistent plot patterns")
        
        print(f"\n📊 Generating visual analysis for both images...")
        detector.visualize_analysis(img1)
        detector.visualize_analysis(img2)
        
    else:
        print("❌ Need at least 2 cemetery images for comparison")
        print("\nTo analyze your new cemetery images:")
        print("1. Save your satellite images as 'cemetery_image_3.png' and 'cemetery_image_4.png'")
        print("2. Run this script again")
        print("3. The new images should score much higher due to clear burial plot patterns!")

if __name__ == "__main__":
    analyze_new_cemetery_satellite_images()
