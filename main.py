import sys
import os
from src.core.pipeline import Pipeline

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file_or_directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    pipeline = Pipeline()
    
    if os.path.isdir(input_path):
        # Process all supported files in directory
        print(f"Processing directory: {input_path}")
        supported_exts = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        for filename in os.listdir(input_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in supported_exts:
                file_path = os.path.join(input_path, filename)
                print(f"\nProcessing {filename}...")
                pipeline.process_file(file_path)
    else:
        pipeline.process_file(input_path)

if __name__ == "__main__":
    main()
