import os
import yaml
from ..processors.pdf_text import TextPDFHighlighter
from ..processors.pdf_scan import ScannedPDFHighlighter
from ..processors.image import ImageHighlighter
from .detector import PDFTypeDetector

class Pipeline:
    def __init__(self, config_path="config.yaml"):
        self.project_root = os.getcwd()
        if not os.path.isabs(config_path):
            config_path = os.path.join(self.project_root, config_path)
            
        self.config = self._load_config(config_path)
        self.detector = PDFTypeDetector(
            text_density_threshold=self.config.get('pdf', {}).get('text_density_threshold', 0.05)
        )
        self.processors = {
            'pdf_text': TextPDFHighlighter(),
            'pdf_scan': ScannedPDFHighlighter(),
            'image': ImageHighlighter()
        }

    def _load_config(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config from {path}: {e}")
            return {}

    def process_file(self, input_path, output_path=None):
        if not os.path.isabs(input_path):
            input_path = os.path.abspath(input_path)
            
        if not os.path.exists(input_path):
            print(f"Error: Input file not found: {input_path}")
            return False

        ext = os.path.splitext(input_path)[1].lower()
        sensitive_words = self.config.get('sensitive_words', [])

        if not output_path:
            # Generate default output path
            filename = os.path.basename(input_path)
            name, _ = os.path.splitext(filename)
            output_dir = self.config['paths']['output_dir']
            if not os.path.isabs(output_dir):
                output_dir = os.path.join(self.project_root, output_dir)
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Always output as PDF
            output_path = os.path.join(output_dir, f"{name}_highlighted.pdf")

        processor = None
        
        if ext == '.pdf':
            is_text = self.detector.is_text_pdf(input_path)
            if is_text:
                print("Detected Text PDF")
                processor = self.processors['pdf_text']
            else:
                print("Detected Scanned PDF")
                processor = self.processors['pdf_scan']
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            print("Detected Image")
            processor = self.processors['image']
        else:
            print(f"Unsupported file type: {ext}")
            return False

        return processor.process(input_path, output_path, self.config)
