import json
import requests
import boto3
from aws_config import AWS_BUCKET_NAME

s3 = boto3.client('s3')

def lambda_handler(event, context):
    number_of_images = event.get('number_of_images', 1)
    if number_of_images <= 0:
        return {
            'statusCode': 400,
            'body': json.dumps('Número de imágenes debe ser mayor a 0')
        }

    image_urls = []
    for _ in range(number_of_images):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json()
        image_url = data["message"]
        image_urls.append(image_url)

    for i, url in enumerate(image_urls):
        img_data = requests.get(url).content
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=f'image_{i+1}.jpg', Body=img_data)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Se han guardado {number_of_images} imágenes en el bucket de S3")
    }
