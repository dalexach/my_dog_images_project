from fastapi import FastAPI, HTTPException
import requests
import boto3
from typing import Optional
from aws_config import AWS_BUCKET_NAME

app = FastAPI()

# AWS S3 client
s3 = boto3.client('s3')

@app.post("/download-images/")
async def download_images(number_of_images: int):
    if number_of_images <= 0:
        raise HTTPException(status_code=400, detail="Número de imágenes debe ser mayor a 0")

    image_urls = []
    for _ in range(number_of_images):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json()
        image_url = data["message"]
        image_urls.append(image_url)

    # Upload images to S3
    for i, url in enumerate(image_urls):
        img_data = requests.get(url).content
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=f'image_{i+1}.jpg', Body=img_data)

    return {"message": f"Se han guardado {number_of_images} imágenes en el bucket de S3"}

