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
            total_area = 0
            
            for i in range(pages_to_check):
                page = doc[i]
                text = page.get_text()
                total_text_len += len(text.strip())
                # Calculate approximate page area (in points^2)
                # This isn't a perfect density metric but a heuristic
                # A full page of text usually has > 500 characters
                
            # Heuristic: If we have > 50 chars per page on average, it's likely text
            # Or use the threshold from config if we wanted to be more precise about density
            
            avg_text_per_page = total_text_len / pages_to_check
            
            print(f"[Detector] Average text length per page: {avg_text_per_page}")
            
            if avg_text_per_page > 50:
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error detecting PDF type: {e}")
            return False
        
# if __name__ == "__main__":
#     detector = PDFTypeDetector()
#     print(detector.is_text_pdf(f"C:\\Users\\49270\\Desktop\\internal\\text-highlight\\data\\scan.pdf"))
