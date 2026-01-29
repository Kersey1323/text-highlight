import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import Pipeline

def test_image_highlight():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, "data", "答辩状.PNG")
    
    if not os.path.exists(input_path):
        print(f"Test image not found: {input_path}")
        return

    print("Testing Image Highlight...")
    pipeline = Pipeline()
    success = pipeline.process_file(input_path)
    
    if success:
        print("Image highlight test passed!")
    else:
        print("Image highlight test failed!")

if __name__ == "__main__":
    test_image_highlight()
