import fitz  # PyMuPDF
import os
import io
import time
from PIL import Image
from ocr_utils import get_ocr_text
from text_renderer import render_text_with_highlights

def ocr_and_highlight_pdf(pdf_path, sensitive_words, output_path):
    """
    Process PDF by converting pages to images, running OCR, 
    re-rendering text with highlights, and saving as a new PDF.
    """
    try:
        doc = fitz.open(pdf_path)
        output_doc = fitz.open()
        
        print(f"Processing PDF: {pdf_path} ({len(doc)} pages)")
        
        for page_num, page in enumerate(doc):
            print(f"  Processing page {page_num + 1}/{len(doc)}...")
            
            # 1. Convert Page to Image
            # Use higher DPI for better OCR accuracy
            pix = page.get_pixmap(dpi=300)
            
            # Save to a temporary file because our OCR utils expects a file path
            temp_img_path = f"temp_page_{page_num}.png"
            pix.save(temp_img_path)
            
            try:
                # 2. OCR the image
                text = get_ocr_text(temp_img_path)
                
                print(f"--- Page {page_num + 1} OCR Result Start ---")
                print(text)
                print(f"--- Page {page_num + 1} OCR Result End ---")
                
                if not text:
                    print(f"    Warning: No text found on page {page_num + 1}.")
                    text = "[OCR Failed or Empty Page]"
                
                # 3. Render text to new image with highlights
                # We don't save to file immediately, we get the PIL Image
                highlighted_img = render_text_with_highlights(text, sensitive_words, output_image_path=None)
                
                # 4. Convert PIL Image to bytes for PyMuPDF
                img_byte_arr = io.BytesIO()
                highlighted_img.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                
                # 5. Create a new page in output PDF
                # We use the dimensions of the generated image
                output_page = output_doc.new_page(width=highlighted_img.width, height=highlighted_img.height)
                output_page.insert_image(output_page.rect, stream=img_bytes)
                
            finally:
                # Cleanup temp file
                if os.path.exists(temp_img_path):
                    try:
                        os.remove(temp_img_path)
                    except:
                        pass # Ignore cleanup errors
        
        # Save final PDF with retry logic for permission errors
        try:
            output_doc.save(output_path)
            print(f"Saved highlighted PDF to {output_path}")
        except Exception as e:
            if "Permission denied" in str(e) or "cannot remove file" in str(e):
                print(f"Warning: Could not save to {output_path} (File might be open).")
                # Try a new filename
                base, ext = os.path.splitext(output_path)
                timestamp = int(time.time())
                new_path = f"{base}_{timestamp}{ext}"
                print(f"Attempting to save to {new_path} instead...")
                output_doc.save(new_path)
                print(f"Saved highlighted PDF to {new_path}")
            else:
                raise e
                
        return True

    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
