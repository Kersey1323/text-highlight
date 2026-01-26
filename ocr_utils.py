import os
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor

# Global variables to cache model and processor
_model = None
_processor = None

# Specify GPU device to use (0, 1, or 2)
GPU_ID = 2
_device = f"cuda:{GPU_ID}" if torch.cuda.is_available() else "cpu"

# Set the default CUDA device
if torch.cuda.is_available():
    torch.cuda.set_device(GPU_ID)

def load_model():
    global _model, _processor
    if _model is not None:
        return

    # Resolve absolute path
    # Current file is in .../text-highlight/ocr_utils.py
    # Model is in .../models/PaddleOCR-VL
    # Assuming the structure is:
    # desktop/
    #   实习/
    #     text-highlight/
    #       ocr_utils.py
    #     models/
    #       PaddleOCR-VL/
    
    model_path = "/home/gms/models/PaddleOCR-VL"

    print(f"Loading model from {model_path} on {_device}...")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model directory not found at {model_path}")

    try:
        # Load model with bfloat16 as requested
        # Note: If GPU doesn't support bfloat16, this might need to be float16 or float32
        _model = AutoModelForCausalLM.from_pretrained(
            model_path, 
            trust_remote_code=True, 
            torch_dtype=torch.bfloat16
        ).to(_device).eval()
        
        _processor = AutoProcessor.from_pretrained(
            model_path, 
            trust_remote_code=True
        )
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        raise e

def get_ocr_text(file_path):
    """
    Performs OCR on the given image file using the local PaddleOCR-VL model.
    """
    global _model, _processor

    if _model is None:
        try:
            load_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    # Check if processor was loaded successfully
    if _processor is None:
        print("Error: Processor not loaded. Cannot perform OCR.")
        return None
        
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None

        print(f"Running OCR on {os.path.basename(file_path)}...")
        image = Image.open(file_path).convert("RGB")
        
        CHOSEN_TASK = "ocr"
        PROMPT = "OCR:" 
        
        messages = [
            {"role": "user",
             "content": [
                 {"type": "image", "image": image},
                 {"type": "text", "text": PROMPT},
             ]
            }
        ]
        
        inputs = _processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(_device)
        
        # Generate
        with torch.no_grad():
            outputs = _model.generate(**inputs, max_new_tokens=1024)
            
        generated_text = _processor.batch_decode(outputs, skip_special_tokens=True)[0]
        
        # Post-processing: Try to strip the prompt if it leaks into output
        # Usually apply_chat_template handles the prompt structure, and batch_decode returns full text.
        # We want the assistant's response.
        # Since we don't know the exact chat template format easily, 
        # we can look for "OCR:" or just return as is if it looks okay.
        # Or better, we can just return the generated text.
        
        # Let's try to remove the input prompt part if possible.
        # But for now, returning the raw decoded text is safer than aggressive stripping.
        # However, let's print it to debug in the loop.
        
        return generated_text

    except Exception as e:
        print(f"Error during OCR inference: {e}")
        import traceback
        traceback.print_exc()
        return None
