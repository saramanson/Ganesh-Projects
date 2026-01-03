import requests
import sys
import os
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_image_upload():
    print("Testing Image Upload...")
    
    # 1. Create a dummy image file
    dummy_image_path = "test_image.txt"
    with open(dummy_image_path, "w") as f:
        f.write("This is a test image content.")
    
    # 2. Upload Transaction with Image
    url = f"{BASE_URL}/transactions"
    data = {
        "description": "Test Image Upload",
        "amount": 123.45,
        "type": "debit",
        "date": "2024-05-20",
        "category": "Insurance"
    }
    files = {
        "image": (dummy_image_path, open(dummy_image_path, "rb"), "text/plain")
    }
    
    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        transaction = response.json()
        print("Transaction created successfully.")
    except Exception as e:
        print(f"Failed to create transaction: {e}")
        sys.exit(1)
    finally:
        files["image"][1].close()
        os.remove(dummy_image_path)

    # 3. Verify Image Path in Response
    image_path = transaction.get("image")
    if not image_path:
        print("Error: Image path missing in response.")
        sys.exit(1)
    print(f"Image path in response: {image_path}")

    # 4. Verify Image File Exists on Server (via API)
    image_url = f"{BASE_URL}/storage/{image_path}"
    try:
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        if img_response.text == "This is a test image content.":
            print("Image retrieved successfully via API.")
        else:
            print("Error: Retrieved image content mismatch.")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to retrieve image: {e}")
        sys.exit(1)

    print("Image upload verification successful!")

if __name__ == "__main__":
    test_image_upload()
