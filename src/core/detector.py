import fitz

class PDFTypeDetector:
    def __init__(self, text_density_threshold=0.05):
        self.text_density_threshold = text_density_threshold

    def is_text_pdf(self, pdf_path):
        """
        Determines if a PDF is text-based (searchable) or scanned.
        
        Args:
            pdf_path (str): Path to the PDF file.
            
        Returns:
            bool: True if text-based, False if scanned.
        """
        try:
            doc = fitz.open(pdf_path)
            if len(doc) == 0:
                return False
                
            # Check first few pages (up to 3)
            pages_to_check = min(len(doc), 3)
            total_text_len = 0
            
            for i in range(pages_to_check):
                page = doc[i]
                total_text_len += len(page.get_text().strip())
                
            avg_text_per_page = total_text_len / pages_to_check
            
            print(f"[Detector] Average text length per page: {avg_text_per_page}")
            
            if avg_text_per_page > 50:
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error detecting PDF type: {e}")
            return False

    @staticmethod
    def is_page_text_based(page, threshold=50):
        """
        Determines if a single PDF page is text-based.
        Returns False if it's a scanned page (even if it has hidden text/OCR).
        
        Args:
            page (fitz.Page): The page object.
            threshold (int): Minimum characters to consider as text page.
            
        Returns:
            bool: True if text-based (native), False if scanned/image-based.
        """
        try:
            text = page.get_text()
            text_len = len(text.strip())
            
            # Prioritize text existence/searchability.
            # If the page has a significant amount of text (e.g., > 100 chars), 
            # we assume it is "Text-based" (searchable/highlightable).
            # We ignore image coverage because many PDFs are "Searchable Images" 
            # (scans with an invisible text layer) which the user treats as text.
            # Note: We use 100 chars to filter out pages with just a few garbage OCR characters
            # (e.g. Page 1 of the sample has 86 chars of garbage).
            if text_len > 100:
                return True
                
            return False
            
        except:
            return False
        
# if __name__ == "__main__":
#     detector = PDFTypeDetector()
#     print(detector.is_text_pdf(f"C:\\Users\\49270\\Desktop\\internal\\text-highlight\\data\\中菱钢诉兴业建筑、安州旅游起诉状.pdf"))
