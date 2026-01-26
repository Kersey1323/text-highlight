import os
import glob
import fitz  # PyMuPDF
from pdf_utils import ocr_and_highlight_pdf, ocr_and_highlight_pdf_docx

# Default sensitive words if files are empty
DEFAULT_SENSITIVE_WORDS = [
    "兴业建筑", "祥亿公司", "安州旅游", "中菱钢", "违约金", "质保金", "分包结算书", "安正兴业"
]

def highlight_text_pdf(input_pdf_path, output_pdf_path, search_words, debug=True):
    """
    在文本型PDF中搜索敏感词并添加黄色高亮注释
    
    Args:
        input_pdf_path: 输入PDF文件路径
        output_pdf_path: 输出PDF文件路径
        search_words: 要搜索并高亮的敏感词列表
        debug: 是否输出调试信息
        
    Returns:
        bool: 成功返回True，失败返回False
    """
    try:
        # 打开PDF文档
        doc = fitz.open(input_pdf_path)

        print(f"Processing Text PDF: {input_pdf_path} ({len(doc)} pages)")
        if debug:
            print(f"Search words: {search_words}")

        total_highlights = 0

        # 遍历每一页
        for page_num, page in enumerate(doc):
            if debug:
                print(f"  Processing page {page_num + 1}/{len(doc)}...")

            page_highlights = 0

            # 遍历每个敏感词，使用多种搜索策略
            for word in search_words:
                text_instances = []

                # 策略1: 标准搜索（默认）
                if not text_instances:
                    text_instances = page.search_for(word)

                # 策略2: 使用 quads 参数搜索
                if not text_instances:
                    text_instances = page.search_for(word, quads=True)

                if text_instances:
                    # 为每个匹配的文本区域添加高亮注释
                    for inst in text_instances:
                        # 添加黄色高亮注释
                        # 颜色格式: (R, G, B, Alpha) 范围 0-1
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=(1, 1, 0))  # 黄色边框
                        highlight.update()

                        page_highlights += 1
                        total_highlights += 1
            
            if debug and page_highlights > 0:
                print(f"    Page {page_num + 1}: {page_highlights} highlights added")

        # 保存修改后的PDF
        doc.save(output_pdf_path)
        doc.close()

        print(f"✓ Saved highlighted Text PDF to: {output_pdf_path}")
        print(f"✓ Total highlights added: {total_highlights}")

        return True

    except Exception as e:
        print(f"Error processing Text PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def is_text_pdf(pdf_path, threshold=50, check_pages=3):
    """
    Detects if a PDF is text-based or scanned (image-based).
    Checks the first `check_pages` pages. If any has text length > threshold, 
    consider it a text PDF.
    """
    try:
        doc = fitz.open(pdf_path)
        text_found = False
        count = 0
        for page in doc:
            if count >= check_pages:
                break
            text = page.get_text()
            # If text is substantial, we assume it's a text PDF
            if len(text.strip()) > threshold:
                text_found = True
                break
            count += 1
        doc.close()
        return text_found
    except Exception as e:
        print(f"Error checking PDF type: {e}")
        # Default to False (treat as scanned) if we can't read it
        return False

def process_pdf_pipeline(input_path, output_path, sensitive_words):
    """
    Unified pipeline to process PDF files.
    Detects if PDF is text-based or scanned, and applies appropriate highlighting method.
    """
    print(f"\nAnalyzing PDF type for: {input_path}")
    
    if is_text_pdf(input_path):
        print(">> Detected TEXT-BASED PDF. Using PyMuPDF direct text search.")
        return highlight_text_pdf(input_path, output_path, sensitive_words)
    else:
        print(">> Detected SCANNED/IMAGE PDF. Using OCR -> Docx -> PDF conversion.")
        print("   Note: This method creates a formatted Word document first.")
        
        # Create intermediate docx path
        docx_path = os.path.splitext(output_path)[0] + ".docx"
        
        return ocr_and_highlight_pdf_docx(input_path, sensitive_words, docx_path, output_path)

def read_sensitive_words(txt_path):
    if not os.path.exists(txt_path):
        return []
    with open(txt_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words

def main():
    # Get project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, "data")
    
    print(f"Searching for files in: {target_dir}")
    
    # Find all PDFs
    pdf_files = glob.glob(os.path.join(target_dir, "*.pdf"))
    
    # Filter out output files
    pdf_files = [f for f in pdf_files if "_highlighted" not in f and "扫描版PDF高亮示例" not in f]
    
    if not pdf_files:
        print("No PDF files found to process.")
        return

    for file_path in pdf_files:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        dir_name = os.path.dirname(file_path)
        
        # Determine output path
        # Using a distinct suffix to indicate it went through the pipeline
        output_pdf = os.path.join(os.path.dirname(dir_name), "outputs", f"{base_name}_highlighted.pdf")
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
        
        # Determine sensitive words
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
            print("Using default sensitive words.")
            sensitive_words = DEFAULT_SENSITIVE_WORDS
        else:
             # Merge with defaults
            sensitive_words = list(set(sensitive_words + DEFAULT_SENSITIVE_WORDS))
            
        # Run pipeline
        process_pdf_pipeline(file_path, output_pdf, sensitive_words)

if __name__ == "__main__":
    main()
