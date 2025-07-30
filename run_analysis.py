#!/usr/bin/env python3
"""
Cemetery Detection - Quick Start Script
Run this script to analyze your cemetery images
"""

from cemetery_detector import compare_images
import os
import sys

def main():
    print("="*60)
    print("    CEMETERY DETECTION USING COMPUTER VISION")
    print("="*60)
    print()
    
    # Check if images exist
    image1 = "cemetry_image_1.png"
    image2 = "cemetry_image_2.png"
    
    if not os.path.exists(image1):
        print(f"❌ Error: {image1} not found!")
        print("Please make sure your first cemetery image is named 'cemetry_image_1.png'")
        return
    
    if not os.path.exists(image2):
        print(f"❌ Error: {image2} not found!")
        print("Please make sure your second cemetery image is named 'cemetry_image_2.png'")
        return
    
    print("✅ Found both images!")
    print(f"📸 Image 1: {image1}")
    print(f"📸 Image 2: {image2}")
    print()
    
    try:
        # Run the analysis
        score1, score2 = compare_images(image1, image2)
        
        print("\n🎯 Analysis complete!")
        print("📊 Check the generated visualization plots for detailed analysis.")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Ensure your images are valid PNG files")
        print("3. Check that your images are satellite/aerial views")

if __name__ == "__main__":
    main()
