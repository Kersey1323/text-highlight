import fitz
import sys

def debug_page_detection(pdf_path):
    print(f"Analyzing: {pdf_path}")
    doc = fitz.open(pdf_path)
    
    for i, page in enumerate(doc):
        print(f"\n--- Page {i+1} ---")
        
        # 1. Check Text Content
        text = page.get_text()
        text_len = len(text.strip())
        print(f"Text length: {text_len}")
        sample = text[:50].replace('\n', ' ')
        print(f"Text sample: {sample}...")
        
        # 2. Check Images
        image_list = page.get_images()
        print(f"Number of images: {len(image_list)}")
        
        page_area = page.rect.width * page.rect.height
        total_image_area = 0
        
        for img in image_list:
            xref = img[0]
            try:
                rects = page.get_image_rects(xref)
                for r in rects:
                    area = r.width * r.height
                    total_image_area += area
                    print(f"  Image rect: {r}, Area: {area}")
            except Exception as e:
                print(f"  Error getting rects for image {xref}: {e}")
                
        coverage = (total_image_area / page_area) * 100 if page_area > 0 else 0
        print(f"Total Image Area: {total_image_area}")
        print(f"Page Area: {page_area}")
        print(f"Image Coverage: {coverage:.2f}%")
        
        # 3. Apply Detector Logic (Simulated)
        threshold = 50
        has_text = text_len > threshold
        is_text_based = False
        
        if not has_text:
            print("Logic: Not text based (Not enough text)")
        else:
            if total_image_area > (page_area * 0.8):
                 print("Logic: Not text based (Image coverage > 80%)")
            else:
                 print("Logic: Text based")
                 is_text_based = True
                 
        print(f"Result: {'TEXT' if is_text_based else 'SCANNED'}")

if __name__ == "__main__":
    pdf_path = r"c:\Users\49270\Desktop\internal\text-highlight\data\中菱钢诉兴业建筑、安州旅游起诉状.pdf"
    debug_page_detection(pdf_path)
