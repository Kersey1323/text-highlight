import os
import re
from .base import BaseHighlighter
from ..utils.ocr import get_ocr_text
from ..utils.docx_formatter import parse_markdown_to_docx, convert_docx_to_pdf
from .pdf_text import TextPDFHighlighter

class ImageHighlighter(BaseHighlighter):
    def process(self, input_path, output_path, config):
        try:
            print(f"Processing Image: {input_path}")
            print(f"Output Path: {repr(output_path)}")
            
            sensitive_words = config.get('sensitive_words', [])
            ocr_config = config.get('ocr', {})
            
            # 1. OCR the image
            text = get_ocr_text(
                input_path,
                api_url=ocr_config.get('api_url'),
                model_name=ocr_config.get('model_name'),
                prompt=ocr_config.get('prompt')
            )
            
            if not text:
                print("Warning: No text found in image.")
                text = ""
            else:
                # Remove "识别结果：" prefix if present using regex
                text = re.sub(r'^识别结果：', '', str(text)).strip()
                # Remove markdown code block markers (```markdown and ```)
                text = re.sub(r'^```(?:markdown)?\s*', '', text).strip()
                text = re.sub(r'\s*```$', '', text).strip()
                
            # 2. Create clean docx (without highlights)
            # Create a temporary docx path
            temp_docx_path = output_path + ".temp.docx"
            
            # Pass empty list for sensitive_words to avoid highlighting in Docx
            doc = parse_markdown_to_docx(text, sensitive_words=[])
            doc.save(temp_docx_path)
            
            # 3. Convert docx to clean PDF
            temp_pdf_path = output_path + ".temp.pdf"
            convert_docx_to_pdf(temp_docx_path, temp_pdf_path)
            
            # 4. Apply highlights to the clean PDF using TextPDFHighlighter
            # This ensures consistent highlighting style (padding, color)
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
            
            # 5. Clean up temp docx
            if os.path.exists(temp_docx_path):
                try:
                    os.remove(temp_docx_path)
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"Error processing Image: {e}")
            import traceback
            traceback.print_exc()
            return False
