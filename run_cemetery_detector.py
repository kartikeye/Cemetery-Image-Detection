"""
🏛️ CEMETERY DETECTION MODEL - EASY TO USE
=============================================

This script will help you detect cemeteries in satellite images using computer vision.

HOW TO USE:
1. Place your image(s) in this folder
2. Run this script
3. Get results showing cemetery likelihood scores
"""

import os
import sys
from final_cemetery_detector import RobustCemeteryDetector

def detect_cemetery_in_image(image_path):
    """
    Detect cemetery in a single image
    """
    detector = RobustCemeteryDetector()
    
    print(f"🔍 Analyzing: {os.path.basename(image_path)}")
    print("-" * 50)
    
    try:
        # Run the detection
        score, features, img = detector.calculate_cemetery_score(image_path)
        
        # Display results
        print(f"🎯 CEMETERY LIKELIHOOD SCORE: {score:.4f}")
        print(f"📊 INTERPRETATION:")
        
        if score >= 0.7:
            print("   ✅ HIGH - Very likely a cemetery!")
        elif score >= 0.4:
            print("   ⚠️  MEDIUM - Some cemetery characteristics detected")
        else:
            print("   ❌ LOW - Unlikely to be a cemetery")
            
        print(f"\n📈 DETAILED FEATURES:")
        for key, value in features.items():
            feature_name = key.replace('_', ' ').title()
            print(f"   • {feature_name}: {value:.4f}")
            
        # Generate visualization
        print(f"\n📊 Generating visual analysis...")
        detector.visualize_analysis(image_path)
        
        return score, features
        
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        return 0, {}

def compare_two_images(image1, image2):
    """
    Compare two images to see which is more likely a cemetery
    """
    detector = RobustCemeteryDetector()
    
    print("🔍 COMPARING TWO IMAGES FOR CEMETERY DETECTION")
    print("=" * 60)
    
    # Analyze first image
    print(f"\n📸 Analyzing Image 1: {os.path.basename(image1)}")
    score1, features1, _ = detector.calculate_cemetery_score(image1)
    
    # Analyze second image
    print(f"\n📸 Analyzing Image 2: {os.path.basename(image2)}")
    score2, features2, _ = detector.calculate_cemetery_score(image2)
    
    # Show results
    print("\n" + "=" * 60)
    print("🏆 COMPARISON RESULTS")
    print("=" * 60)
    
    print(f"\n📊 {os.path.basename(image1)}:")
    print(f"   🎯 Cemetery Score: {score1:.4f}")
    
    print(f"\n📊 {os.path.basename(image2)}:")
    print(f"   🎯 Cemetery Score: {score2:.4f}")
    
    # Determine winner
    if score1 > score2:
        diff = score1 - score2
        confidence = (diff / max(score1, 0.001)) * 100
        print(f"\n🏆 WINNER: {os.path.basename(image1)}")
        print(f"📈 Confidence: {confidence:.1f}% higher")
    elif score2 > score1:
        diff = score2 - score1
        confidence = (diff / max(score2, 0.001)) * 100
        print(f"\n🏆 WINNER: {os.path.basename(image2)}")
        print(f"📈 Confidence: {confidence:.1f}% higher")
    else:
        print(f"\n🤝 TIE: Both images have similar cemetery likelihood")
    
    # Generate visualizations
    print(f"\n📊 Generating visual analysis for both images...")
    detector.visualize_analysis(image1)
    detector.visualize_analysis(image2)
    
    return score1, score2

def main():
    """
    Main function to run cemetery detection
    """
    print("🏛️  CEMETERY DETECTION MODEL")
    print("=" * 50)
    print("Detecting cemeteries in satellite images using Computer Vision")
    print("=" * 50)
    
    # Find available images
    image_files = []
    for file in os.listdir("."):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            if not file.startswith('cemetery_analysis_'):  # Skip generated plots
                image_files.append(file)
    
    if not image_files:
        print("❌ No images found!")
        print("\n📋 TO USE THIS MODEL:")
        print("1. Place your satellite image(s) in this folder")
        print("2. Supported formats: PNG, JPG, JPEG, TIFF, BMP")
        print("3. Run this script again")
        return
    
    print(f"📁 Found {len(image_files)} image(s):")
    for i, img in enumerate(image_files, 1):
        print(f"   {i}. {img}")
    
    if len(image_files) == 1:
        print(f"\n🔍 SINGLE IMAGE ANALYSIS")
        detect_cemetery_in_image(image_files[0])
        
    elif len(image_files) >= 2:
        print(f"\n🔍 Choose analysis mode:")
        print("   1. Analyze single image")
        print("   2. Compare two images")
        print("   3. Analyze all images")
        
        try:
            choice = input("\nEnter your choice (1, 2, or 3): ").strip()
            
            if choice == "1":
                print("\nAvailable images:")
                for i, img in enumerate(image_files, 1):
                    print(f"   {i}. {img}")
                img_choice = int(input("Choose image number: ")) - 1
                detect_cemetery_in_image(image_files[img_choice])
                
            elif choice == "2":
                print("\nSelect two images to compare:")
                for i, img in enumerate(image_files, 1):
                    print(f"   {i}. {img}")
                img1_idx = int(input("Choose first image number: ")) - 1
                img2_idx = int(input("Choose second image number: ")) - 1
                compare_two_images(image_files[img1_idx], image_files[img2_idx])
                
            elif choice == "3":
                print(f"\n🔍 ANALYZING ALL {len(image_files)} IMAGES")
                print("=" * 50)
                results = []
                for img in image_files:
                    score, features = detect_cemetery_in_image(img)
                    results.append((img, score))
                    print("-" * 50)
                
                # Show summary
                print(f"\n📊 SUMMARY - ALL IMAGES RANKED:")
                results.sort(key=lambda x: x[1], reverse=True)
                for i, (img, score) in enumerate(results, 1):
                    status = "🏆" if score >= 0.7 else "⚠️" if score >= 0.4 else "❌"
                    print(f"   {i}. {status} {img}: {score:.4f}")
            
        except (ValueError, IndexError):
            print("❌ Invalid choice. Running default analysis...")
            compare_two_images(image_files[0], image_files[1])
        except KeyboardInterrupt:
            print("\n\n👋 Analysis cancelled by user")
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print("📊 Check the generated visualization plots for detailed analysis.")

if __name__ == "__main__":
    main()
