import os
import requests

# OCR API 服务配置
OCR_API_URL = "http://localhost:7862/processOCR"
MODEL_NAME = "deepseek-ocr"


def get_ocr_text(file_path):
    """
    Performs OCR on the given image file using the local OCR API service.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None

        print(f"Running OCR on {os.path.basename(file_path)}...")

        # Prepare the request
        url = f"{OCR_API_URL}?model_name={MODEL_NAME}"

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
                ocr_text = result['data'].get('text', '')
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
