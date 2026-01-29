import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import Pipeline

def test_pipeline():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipeline = Pipeline()
    
    # Test cases
    files = [
        "text.pdf", # Text PDF
        "中菱钢诉兴业建筑、安州旅游起诉状.pdf", # Scanned PDF
        "答辩状.PNG" # Image
    ]
    
    for filename in files:
        f = os.path.join(project_root, "data", filename)
        if os.path.exists(f):
            print(f"\n{'='*50}")
            print(f"Testing {filename}...")
            print(f"{'='*50}")
            pipeline.process_file(f)
        else:
            print(f"File not found: {filename}")

if __name__ == "__main__":
    test_pipeline()
