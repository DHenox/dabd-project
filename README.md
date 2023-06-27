# Proyecto DABD

## Cómo clonar este repositorio

Para clonar este repositorio en tu máquina local, sigue los siguientes pasos:

1. Abre tu terminal o línea de comandos.
2. Navega hasta el directorio en el que deseas clonar este repositorio.
3. Copia el siguiente comando y pégalo en tu terminal:
```
git clone git@github.com:DHenox/dabd-project.git
```

## Antes de empezar

Antes de iniciar el servidor, se necesitará modificar el archivo `django/audi/audi/settings.py` y modificar todos los campos con `XXXXXXXXX` por el valor
que se necesite:

```
'NAME': 'XXXXXXXXX',        # Replace with your psql database name
'USER': 'XXXXXXXXX',        # Replace with your psql username
'PASSWORD': 'XXXXXXXXX',    # Replace with your psql password
```

## Iniciar el servidor web Django

Una vez tengamos clonado el repositorio, instalaremos el framework de Django creando un entorno virtual con Python3:

```
cd dabd-project/django
source bin/activate
pip3 install Django
```

Una vez instalado el framework Django, podmos iniciar el servidor:

```
cd audi
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 8080
```

En caso de realizar cambios en el archivo `django/audi/audi_manager/models.py`, lo indicaremos en nuestro modelo para que se calculen los cambios a realizar en la base de datos mediante una migración (crea un archivo con las instrucciones SQL de los cambios). Después podemos ver las sentencias SQL que se ejecutarían y, si nos convencen, aplicamos la migración (ejecuta las instrucciones SQL anteriores a la base de datos):
```
python3 manage.py makemigrations audi_manager
python3 manage.py sqlmigrate audi_manager 0001
python3 manage.py migrate
```

Para crear un usuario de admin en una linea de terminal (para no poner inputs)
````
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '12345')" | python3 manage.py shell
````

Para crear insertar datos aleatorios:
```
python3 manage.py createdata
```

Para borrar schema:
```
DROP SCHEMA practica CASCADE;
```
También deberemos eliminar los archivos con las migraciones para volver a generarlos de nuevo.
Los archivos 0001xxx.py 0002xxx.py, etc en la carpeta migrations de la aplicación.

Copiar datos a ubiwan (para correr el script de crear datos falsos)
```
rsync -rav dabd-project <user>@ubiwan.epsevg.upc.edu:/home/est/<user>/DABD/
```
Podemos acceder a [http://127.0.0.1:8080](http://127.0.0.1:8080) para visualizar la pagina de inicio de la web.

En [http://127.0.0.1:8080/admin](http://127.0.0.1:8080/admin) tenemos la parte administrativa a la que accederemos con el usuario i contraseña que genermos con `python3 manage.py createsuperuser`.

## Diagrama UML
![UML](https://github.com/DHenox/dabd-project/blob/main/UML/UML.png)