# Acerca de este proyecto
Se trata de una API de gestión de Órdenes para un ecomercce , :
* Endpoints para CRUD de Órdenes
* Detalles de cada orden
* Estados
* Validaciones 
* Y más
  
# INFO
  *De las 3 APIs de mi Repo esta es la menos trabajada, aún así es utilizable*

# Instrucciones para ejecutar el proyecto

* Crear un entorno virtual para aislar dependencias:
    * `python -m venv mi_entorno`
   
    * Luego activarlo con:
      * `mi_entorno/Scripts/activate`
  
  
* Ejecutar el siguiente comando para instalar dependencias:
    * `pip install -r requirements.txt`

* Una vez instaladas las dependencias , posicionarse en la carpeta contenedora de el archivo **main.py**, en este caso la carpeta *Orders*

* Es necesario crear un archivo .env para establecer las variables de entorno, para eso mirar el archivo *.env.example* para tener una idea de como hacerlo

* Una vez hecho esto , ejecutar el siguiente comando para correr el servidor en el servidor local:
    * `fastapi dev main.py`

* Para leer la documentación de la API y saber como consumirla entrar en:
    * (http://127.0.0.1:8000/docs)
  
  
