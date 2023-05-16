# Funcionamiento de la aplicación

En términos generales, el endpoint /images de la api se encarga de recibir un json con la información suministrada en los requerimientos de usuario, requiriendo una fecha, hora utc, la imagen en un string base64 y finalmente el id de la cámara que tomó la imagen. Se implementó un modelo Pydantic con los campos anteriores con el fin de validar la información y serializar la respuesta de el endpoint.
Una vez se recibe y se valida la información suministrada, se decodifica la imagen del string base64 a bytes, se crear el blob pertinente, se sube y el registro se guarda en la base de datos implementada en sqlite con el url que retorna el blob client al subir la imagen, la fecha en la que se tomó la imagen y el id de la cámara.

# Cómo correr el programa

Puedes crear un entorno virtual con virtualenv venv, activarlo, si estás en linux sería source venv/bin/activate
luego instalar las librerías necesarias con
pip install -r requirements.txt
y lanzar la aplicación con uvicorn main:app --reload

# Tests

Para correr los tests, ejecuta pytest en la terminal.
