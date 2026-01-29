import fitz
import os
from .base import BaseHighlighter

class TextPDFHighlighter(BaseHighlighter):
    @staticmethod
    def apply_highlights_to_page(page, sensitive_words, config):
        """
        Apply highlights to a single PDF page in-place.
        
        Args:
            page (fitz.Page): The page object.
            sensitive_words (list): List of words to highlight.
            config (dict): Configuration dict.
            
        Returns:
            int: Number of highlights added.
        """
        total_highlights = 0
        
        # Get highlight config
        hl_config = config.get('highlight', {})
        padding_x = hl_config.get('padding_x', 0)
        padding_y = hl_config.get('padding_y', 0)
        color = hl_config.get('color', [1, 1, 0])
        
        for word in sensitive_words:
            # Search for text instances
            text_instances = page.search_for(word)
            if not text_instances:
                 text_instances = page.search_for(word, quads=True)
                 
            if text_instances:
                for inst in text_instances:
                    # Apply padding/adjustment to the highlight area
                    if isinstance(inst, fitz.Rect):
                        # It's a Rect
                        inst.x0 -= padding_x
                        inst.y0 -= padding_y
                        inst.x1 += padding_x
                        inst.y1 += padding_y
                    elif isinstance(inst, fitz.Quad):
                        # It's a Quad (ul, ur, ll, lr)
                        inst.ul.y -= padding_y
                        inst.ur.y -= padding_y
                        inst.ll.y += padding_y
                        inst.lr.y += padding_y
                        
                        inst.ul.x -= padding_x
                        inst.ll.x -= padding_x
                        inst.ur.x += padding_x
                        inst.lr.x += padding_x

                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=color) 
                    highlight.update()
                    total_highlights += 1
        return total_highlights

    def process(self, input_path, output_path, config):
        try:
            sensitive_words = config.get('sensitive_words', [])
            
            doc = fitz.open(input_path)
            total_highlights = 0
            
            print(f"Processing Text PDF: {input_path}")
            
            for page in doc:
                total_highlights += self.apply_highlights_to_page(page, sensitive_words, config)
            
            doc.save(output_path)
            doc.close()
            print(f"Saved highlighted PDF to: {output_path} with {total_highlights} highlights")
            return True
            
        except Exception as e:
            print(f"Error processing Text PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
