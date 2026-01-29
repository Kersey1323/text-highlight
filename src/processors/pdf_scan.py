import fitz
import os
import time
import re
from .base import BaseHighlighter
from ..utils.ocr import get_ocr_text
from ..utils.docx_formatter import parse_markdown_to_docx, convert_docx_to_pdf
from .pdf_text import TextPDFHighlighter

class ScannedPDFHighlighter(BaseHighlighter):
    def process(self, input_path, output_path, config):
        try:
            sensitive_words = config.get('sensitive_words', [])
            ocr_config = config.get('ocr', {})
            
            doc_pdf = fitz.open(input_path)
            
            print(f"Processing Scanned PDF: {input_path} ({len(doc_pdf)} pages)")
            
            docx_document = None
            
            # Create a temp directory for OCR images
            temp_dir = os.path.join(os.path.dirname(input_path), "temp_ocr_images")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir, exist_ok=True)
                
            try:
                for page_num, page in enumerate(doc_pdf):
                    print(f"  Processing page {page_num + 1}/{len(doc_pdf)}...")
                    
                    # 1. Convert Page to Image
                    pix = page.get_pixmap(dpi=300)
                    temp_img_path = os.path.join(temp_dir, f"temp_page_{page_num}_{int(time.time())}.png")
                    pix.save(temp_img_path)
                    
                    try:
                        # 2. OCR the image
                        text = get_ocr_text(
                            temp_img_path,
                            api_url=ocr_config.get('api_url'),
                            model_name=ocr_config.get('model_name'),
                            prompt=ocr_config.get('prompt')
                        )
                        
                        if not text:
                            print(f"    Warning: No text found on page {page_num + 1}.")
                            text = ""
                        else:
                            # Remove "识别结果：" prefix if present using regex
                            text = re.sub(r'^识别结果：', '', str(text)).strip()
                            # Remove markdown code block markers (```markdown and ```)
                            text = re.sub(r'^```(?:markdown)?\s*', '', text).strip()
                            text = re.sub(r'\s*```$', '', text).strip()
                        
                        # 3. Add to docx (WITHOUT HIGHLIGHTS)
                        # We use sensitive_words=[] to prevent highlighting in the Docx stage
                        if docx_document is None:
                            docx_document = parse_markdown_to_docx(text, sensitive_words=[])
                        else:
                            docx_document.add_page_break()
                            parse_markdown_to_docx(text, sensitive_words=[], doc=docx_document)
                            
                    finally:
                        if os.path.exists(temp_img_path):
                            try:
                                os.remove(temp_img_path)
                            except:
                                pass
                                
                # 4. Save docx and convert to PDF
                if docx_document:
                    temp_docx_path = output_path + ".temp.docx"
                    docx_document.save(temp_docx_path)
                    
                    print(f"Converting intermediate DOCX to PDF: {output_path}")
                    temp_pdf_path = output_path + ".temp.pdf"
                    convert_docx_to_pdf(temp_docx_path, temp_pdf_path)
                    
                    # 5. Apply highlights to the clean PDF using TextPDFHighlighter
                    if os.path.exists(temp_pdf_path):
                        text_highlighter = TextPDFHighlighter()
                        # Use the original output_path for the final result
                        success = text_highlighter.process(temp_pdf_path, output_path, config)
                        
                        # Clean up temp PDF
                        try:
                            os.remove(temp_pdf_path)
                        except:
                            pass
                            
                        if not success:
                            print("Error: Failed to apply highlights to intermediate PDF")
                            return False
                    else:
                        print("Error: Intermediate PDF generation failed")
                        return False
                    
                    if os.path.exists(temp_docx_path):
                        try:
                            os.remove(temp_docx_path)
                        except:
                            pass
                    
                    return True
                else:
                    print("Error: No document created (maybe empty PDF?)")
                    return False

            finally:
                # Cleanup temp dir
                if os.path.exists(temp_dir):
                    try:
                        os.rmdir(temp_dir) # Only removes if empty
                    except:
                        pass
                        
        except Exception as e:
            print(f"Error processing Scanned PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
