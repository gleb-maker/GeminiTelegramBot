import requests
import json

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
api_key = "AIzaSyC1WpX65DjRRvk-VNtpV37fLVCdFlMsaXM"

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": api_key
}

data = {
    "contents": [
        {"parts": [{"text": "Hello from Python!"}]}
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.text)
