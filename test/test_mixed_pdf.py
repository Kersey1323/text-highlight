import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.pipeline import Pipeline

def test_mixed_pdf():
    config_path = "config.yaml"
    pipeline = Pipeline(config_path)
    
    input_pdf = r"c:\Users\49270\Desktop\internal\text-highlight\data\中菱钢诉兴业建筑、安州旅游起诉状.pdf"
    
    if not os.path.exists(input_pdf):
        print(f"File not found: {input_pdf}")
        return
        
    output_dir = r"c:\Users\49270\Desktop\internal\text-highlight\data\output"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "mixed_highlighted.pdf")
    
    # Remove existing output
    if os.path.exists(output_path):
        os.remove(output_path)
        
    print(f"Processing Mixed PDF: {input_pdf}")
    pipeline.process_file(input_pdf, output_path)
    
    if os.path.exists(output_path):
        print("Success! Output generated.")
    else:
        print("Failure! No output.")

if __name__ == "__main__":
    test_mixed_pdf()
