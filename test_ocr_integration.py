"""
Test OCR Integration
Demonstrates how the system extracts text from images
"""

import requests
from PIL import Image, ImageDraw, ImageFont
import os

print("=" * 60)
print("🖼️  Testing OCR Integration")
print("=" * 60)
print()

# Create a test image with text
print("📝 Step 1: Creating test image with claim text")
print("-" * 60)

# Create image
img = Image.new('RGB', (800, 200), color='white')
draw = ImageDraw.Draw(img)

# Add text
text = "COVID vaccines contain microchips"
try:
    # Try to use a nice font
    font = ImageFont.truetype("arial.ttf", 40)
except:
    # Fallback to default font
    font = ImageFont.load_default()

# Draw text
draw.text((50, 80), text, fill='black', font=font)

# Save image
os.makedirs("./test_images", exist_ok=True)
image_path = "./test_images/test_claim.png"
img.save(image_path)

print(f"✓ Image created: {image_path}")
print(f"✓ Text in image: '{text}'")
print()

# Test OCR extraction directly
print("📝 Step 2: Testing OCR extraction")
print("-" * 60)

from app.agents.extract import extraction_agent

result = extraction_agent.run('image', image_path)

print(f"✓ Extraction success: {result['success']}")
print(f"✓ Extracted from: {result['extracted_from']}")
print(f"✓ Claim text: {result['claim_text']}")
print(f"✓ Raw OCR text: {result['raw_content'][:100]}...")
print()

# Test via API
print("📝 Step 3: Testing via API (full pipeline)")
print("-" * 60)

API_URL = "http://localhost:8000"

# Submit image
with open(image_path, 'rb') as f:
    response = requests.post(
        f"{API_URL}/check",
        files={"file": f}
    )

if response.status_code == 200:
    result = response.json()
    submission_id = result['submission_id']
    
    print(f"✓ Submission ID: {submission_id}")
    print(f"✓ Status: {result['status']}")
    print()
    
    print("⏳ Waiting 60 seconds for processing...")
    import time
    time.sleep(60)
    
    # Get result
    response = requests.get(f"{API_URL}/result/{submission_id}")
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Final status: {result['status']}")
        print(f"✓ Extracted claim: {result.get('claim', 'N/A')}")
        print(f"✓ Confidence: {result.get('confidence', 'N/A')}")
        print()
else:
    print(f"❌ API error: {response.status_code}")
    print(response.text)

print("=" * 60)
print("✅ OCR Integration Test Complete!")
print("=" * 60)
print()
print("📋 OCR Features:")
print("  ✓ OCR.space API integration")
print("  ✓ Automatic text extraction from images")
print("  ✓ Intelligent claim selection")
print("  ✓ Full pipeline support (all 8 agents)")
print("  ✓ Supports PNG, JPG, and other image formats")
