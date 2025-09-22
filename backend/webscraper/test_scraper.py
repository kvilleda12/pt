#!/usr/bin/env python3
"""
Test script for the PT webscraper
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from config import DEFAULT_CRITERIA
from classify import classify_text
from html_utils import html_to_text
from logger import log

def test_html_conversion():
    """Test HTML to text conversion"""
    print("🧪 Testing HTML to text conversion...")
    
    sample_html = """
    <html>
    <head><title>Physical Therapy Exercises</title></head>
    <body>
        <h1>Neck Stretches</h1>
        <p>Here are some effective neck stretches:</p>
        <ol>
            <li>Slowly tilt your head to the right</li>
            <li>Hold for 30 seconds</li>
            <li>Repeat on the left side</li>
        </ol>
        <h2>Safety Notes</h2>
        <p>Stop if you feel pain. Consult a physical therapist for proper form.</p>
    </body>
    </html>
    """
    
    text = html_to_text(sample_html)
    print(f"✅ Converted HTML to {len(text)} characters")
    print(f"Sample text: {text[:200]}...")
    return text

def test_classification():
    """Test content classification"""
    print("\n🧪 Testing content classification...")
    
    # Test with good PT content
    good_content = """
    Physical Therapy Exercises for Neck Pain
    
    Step 1: Neck Stretch
    - Slowly tilt your head to the right
    - Hold for 30 seconds
    - Repeat 3 times on each side
    
    Step 2: Shoulder Rolls
    - Roll shoulders backward 10 times
    - Roll shoulders forward 10 times
    - Maintain proper posture throughout
    
    Safety: Stop if you experience pain. Consult a physical therapist for proper technique.
    """
    
    # Test with bad content
    bad_content = """
    Buy our amazing fitness supplements now!
    Click here for the best deals on protein powder.
    Limited time offer - 50% off!
    """
    
    print("Testing good PT content...")
    result1 = classify_text("test_good", good_content, DEFAULT_CRITERIA)
    print(f"   Viable: {result1['viable']}, Confidence: {result1['confidence']:.2f}")
    
    print("Testing bad content...")
    result2 = classify_text("test_bad", bad_content, DEFAULT_CRITERIA)
    print(f"   Viable: {result2['viable']}, Confidence: {result2['confidence']:.2f}")

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    print(f"✅ Default criteria loaded:")
    print(f"   Keywords: {len(DEFAULT_CRITERIA['keywords_any'])}")
    print(f"   Min text length: {DEFAULT_CRITERIA['min_text_len']}")
    print(f"   Body parts: {len(DEFAULT_CRITERIA['body_parts'])}")

def main():
    """Run all tests"""
    print("🚀 PT Webscraper Test Suite")
    print("=" * 50)
    
    try:
        test_config()
        test_html_conversion()
        test_classification()
        
        print("\n✅ All tests completed successfully!")
        print("\nTo run the scraper:")
        print("   python main.py --labels n,b --results-per-label 5 --verbose")
        print("   python main.py --dry-run  # See what would be scraped")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
