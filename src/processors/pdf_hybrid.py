import fitz
import os
import time
import re
from .base import BaseHighlighter
from .pdf_text import TextPDFHighlighter
from ..core.detector import PDFTypeDetector
from ..utils.ocr import get_ocr_text
from ..utils.docx_formatter import parse_markdown_to_docx, convert_docx_to_pdf

class HybridPDFHighlighter(BaseHighlighter):
    def process(self, input_path, output_path, config):
        try:
            print(f"Processing Hybrid PDF: {input_path}")
            
            sensitive_words = config.get('sensitive_words', [])
            ocr_config = config.get('ocr', {})
            
            # Open input document
            input_doc = fitz.open(input_path)
            # Create output document
            output_doc = fitz.open()
            
            temp_dir = os.path.join(os.path.dirname(input_path), "temp_hybrid_processing")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir, exist_ok=True)
                
            try:
                for i, page in enumerate(input_doc):
                    print(f"  Processing page {i + 1}/{len(input_doc)}...")
                    
                    # Detect page type
                    if PDFTypeDetector.is_page_text_based(page):
                        print(f"    [Page {i+1}] Detected as Text. Applying text highlighting.")
                        # Apply highlighting in-place to the input page
                        TextPDFHighlighter.apply_highlights_to_page(page, sensitive_words, config)
                        # Copy to output
                        output_doc.insert_pdf(input_doc, from_page=i, to_page=i)
                    else:
                        print(f"    [Page {i+1}] Detected as Scanned. Running OCR pipeline.")
                        # Handle Scanned Page
                        self._process_scanned_page(page, output_doc, temp_dir, sensitive_words, ocr_config, config, i)
                        
                # Save final result
                output_doc.save(output_path)
                output_doc.close()
                input_doc.close()
                print(f"Saved hybrid highlighted PDF to: {output_path}")
                return True
                
            except Exception as e:
                print(f"Error during page processing loop: {e}")
                raise e
            finally:
                # Cleanup temp dir
                if os.path.exists(temp_dir):
                    try:
                        # Simple cleanup of files in dir
                        for f in os.listdir(temp_dir):
                            try:
                                os.remove(os.path.join(temp_dir, f))
                            except:
                                pass
                        os.rmdir(temp_dir)
                    except:
                        pass

        except Exception as e:
            print(f"Error processing Hybrid PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _process_scanned_page(self, page, output_doc, temp_dir, sensitive_words, ocr_config, config, page_index):
        """
        Process a single scanned page: Image -> OCR -> Docx -> PDF -> Highlight -> Append to output_doc
        """
        # 1. Render to image
        pix = page.get_pixmap(dpi=300)
        temp_img_path = os.path.join(temp_dir, f"page_{page_index}_{int(time.time())}.png")
        pix.save(temp_img_path)
        
        try:
            # 2. OCR
            text = get_ocr_text(
                temp_img_path,
                api_url=ocr_config.get('api_url'),
                model_name=ocr_config.get('model_name'),
                prompt=ocr_config.get('prompt')
            )
            
            if not text:
                print(f"    Warning: No text found on page {page_index + 1}.")
                text = ""
            else:
                text = re.sub(r'^识别结果：', '', str(text)).strip()
                text = re.sub(r'^```(?:markdown)?\s*', '', text).strip()
                text = re.sub(r'\s*```$', '', text).strip()
            
            # 3. Create Clean Docx (sensitive_words=[])
            doc = parse_markdown_to_docx(text, sensitive_words=[])
            temp_docx_path = os.path.join(temp_dir, f"page_{page_index}.docx")
            doc.save(temp_docx_path)
            
            try:
                # 4. Convert to Clean PDF
                temp_pdf_path = os.path.join(temp_dir, f"page_{page_index}.pdf")
                convert_docx_to_pdf(temp_docx_path, temp_pdf_path)
                
                if os.path.exists(temp_pdf_path):
                    # 5. Highlight the clean PDF
                    temp_pdf_doc = fitz.open(temp_pdf_path)
                    for temp_page in temp_pdf_doc:
                        TextPDFHighlighter.apply_highlights_to_page(temp_page, sensitive_words, config)
                    
                    # 6. Append to main output doc
                    # We insert the processed PDF pages (could be 1 or more if text overflowed)
                    output_doc.insert_pdf(temp_pdf_doc)
                    temp_pdf_doc.close()
                else:
                    print(f"    Error: Failed to generate PDF for page {page_index + 1}")
                    
            finally:
                if os.path.exists(temp_docx_path):
                    try:
                        os.remove(temp_docx_path)
                    except:
                        pass
        finally:
            if os.path.exists(temp_img_path):
                try:
                    os.remove(temp_img_path)
                except:
                    pass
