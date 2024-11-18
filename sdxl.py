from PIL import Image
import io
import base64
import requests

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


def generate_image(text):

    image_bytes = query({"inputs": text})

    # image = Image.open(io.BytesIO(image_bytes))

    # return image
    
    return image_bytes