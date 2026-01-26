import os
import glob
from ocr_utils import get_ocr_text
from pdf_utils import ocr_and_highlight_pdf
from text_renderer import render_text_with_highlights

# Default sensitive words if files are empty
DEFAULT_SENSITIVE_WORDS = [
    "兴业建筑", "祥亿公司", "安州旅游", "中菱钢", "违约金", "质保金", "分包结算书", "安正兴业"
]

def read_sensitive_words(txt_path):
    if not os.path.exists(txt_path):
        return []
    with open(txt_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words

def process_file(file_path):
    print(f"\nProcessing {file_path}...")
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    dir_name = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    
    # Determine sensitive words file
    # Pattern: filename-敏感词.txt or filename-敏感词 .txt
    # We'll try a few variations
    possible_txts = [
        os.path.join(dir_name, f"{base_name}-敏感词.txt"),
        os.path.join(dir_name, f"{base_name}-敏感词 .txt"),
    ]
    
    sensitive_words = []
    for txt in possible_txts:
        if os.path.exists(txt):
            print(f"Found sensitive words file: {txt}")
            sensitive_words = read_sensitive_words(txt)
            break
            
    if not sensitive_words:
        print("No specific sensitive words file found or empty. Using defaults.")
        sensitive_words = DEFAULT_SENSITIVE_WORDS
    else:
        # Merge with defaults or just use file? 
        # Usually file is specific, but if it was empty (which returned []), we used defaults.
        # If it has content, we append defaults? Or replace? 
        # Let's append defaults to be safe for this demo.
        sensitive_words = list(set(sensitive_words + DEFAULT_SENSITIVE_WORDS))

    print(f"Sensitive words: {sensitive_words}")

    if ext == '.pdf':
        output_pdf = os.path.join(dir_name, f"{base_name}_highlighted.pdf")
        # Use the new OCR-based PDF processing logic
        success = ocr_and_highlight_pdf(file_path, sensitive_words, output_pdf)
        if not success:
            print("PDF processing failed.")
    
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
        # Image flow: OCR -> Text -> Render Image
        print("Image detected. Running OCR...")
        text = get_ocr_text(file_path)
        
        if text:
            print("OCR Text retrieved.")
            # print(f"Preview: {text[:100]}...")
            
            output_img = os.path.join(dir_name, f"{base_name}_highlighted.png")
            # We pass output_img path to save it directly
            render_text_with_highlights(text, sensitive_words, output_img)
        else:
            print("OCR failed or returned no text.")

def main():
    # 获取项目根目录（当前脚本所在目录）
    project_root = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(project_root, "data")
    
    # Find all PDFs and Images
    types = ('*.pdf', '*.png', '*.jpg', '*.jpeg')
    files = []
    for t in types:
        files.extend(glob.glob(os.path.join(target_dir, t)))
        
    # Filter out output files (containing _highlighted)
    files = [f for f in files if "_highlighted" not in f]
    
    if not files:
        print("No files found to process.")
        return

    for f in files:
        process_file(f)

if __name__ == "__main__":
    main()
