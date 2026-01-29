from abc import ABC, abstractmethod

class BaseHighlighter(ABC):
    @abstractmethod
    def process(self, input_path, output_path, config):
        """
        Process the input file and save the highlighted result to output_path.
        
        Args:
            input_path (str): Path to the input file.
            output_path (str): Path to save the processed file.
            config (dict): Configuration dictionary containing sensitive_words and other settings.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        pass
