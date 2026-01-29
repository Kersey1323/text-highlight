import os
import requests

# OCR API 服务配置
# 这些配置现在应该通过参数传入，但保留默认值作为后备
DEFAULT_OCR_API_URL = "http://localhost:7862/processVL"
DEFAULT_MODEL_NAME = "qwen3-vl-8b-instruct"
DEFAULT_PROMPT = "请识别这张图片的内容并以markdown的格式给出。"


def get_ocr_text(file_path, api_url=None, model_name=None, prompt=None):
    """
    Performs OCR on the given image file using the local OCR API service.
    
    Args:
        file_path (str): Path to the image file.
        api_url (str): OCR API URL.
        model_name (str): Model name to use.
        prompt (str): Prompt for the model.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None

        # Use provided config or defaults
        api_url = api_url or DEFAULT_OCR_API_URL
        model_name = model_name or DEFAULT_MODEL_NAME
        prompt = prompt or DEFAULT_PROMPT

        print(f"Running OCR on {os.path.basename(file_path)}...")

        # Prepare the request
        url = f"{api_url}?model_name={model_name}&prompt={prompt}"

        # Open and send the image file
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {
                'accept': 'application/json'
            }

            response = requests.post(url, headers=headers, files=files, timeout=60)

        # Check if request was successful
        if response.status_code == 200:
            result = response.json()

            if result.get('success') and result.get('data'):
                ocr_text = result['data'].get('response', '')
                return ocr_text
            else:
                print(f"OCR API returned error: {result.get('error', 'Unknown error')}")
                return None
        else:
            print(f"OCR API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("Error: OCR API request timed out")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to OCR API service. Please check if the service is running.")
        return None
    except Exception as e:
        print(f"Error during OCR API call: {e}")
        import traceback
        traceback.print_exc()
        return None
