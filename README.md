# my_dog_images_project

## Descripción

Este proyecto proporciona una API REST que descarga imágenes aleatorias de perros y las guarda en un bucket de AWS S3. La API está construida con FastAPI y utiliza AWS Lambda para el procesamiento de imágenes.

## Estructura del Proyecto

- `main.py`: Código de la API REST con FastAPI.
- `lambda_function.py`: Función Lambda para procesar imágenes y subirlas a S3.
- `aws_config.py`: Configuración de AWS.
- `tests/`: Carpeta que contiene las pruebas unitarias.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd my_dog_images_project
   ```

## Uso de la API

Envía una solicitud POST a /download-images/ con un cuerpo JSON que especifique el número de imágenes a descargar.

Ejemplo de Solicitud

```
{
    "number_of_images": 5
}
```

Ejemplo de Respuesta

```
{
    "message": "Se han guardado 5 imágenes en el bucket de S3"
}
```
