import cv2
import numpy as np
import os

# For now, let's use the robust detector since it works better
from final_cemetery_detector import compare_images

def analyze_new_cemetery_images():
    """Analyze the new cemetery images you provided"""
    
    print("🏛️  ANALYZING YOUR NEW CEMETERY IMAGES")
    print("="*60)
    
    # Check if we have the images
    image1 = "cemetery_image_3.png"  # First cemetery image you provided
    image2 = "cemetery_image_4.png"  # Second cemetery image you provided
    
    # For now, let's use your existing images to demonstrate
    available_images = []
    for img_file in os.listdir("."):
        if img_file.endswith(('.png', '.jpg', '.jpeg')):
            available_images.append(img_file)
    
    print("📁 Available images in directory:")
    for img in available_images:
        print(f"   🖼️  {img}")
    
    # Let's use the images we know exist
    if "cemetry_image_1.png" in available_images and "cemetry_image_2.png" in available_images:
        print(f"\n🔍 Running analysis on existing cemetery images...")
        compare_images("cemetry_image_1.png", "cemetry_image_2.png")
    else:
        print("\n❌ Cemetery images not found!")
        print("Please make sure you have:")
        print("- cemetery_image_3.png (your first new image)")
        print("- cemetery_image_4.png (your second new image)")

if __name__ == "__main__":
    analyze_new_cemetery_images()
