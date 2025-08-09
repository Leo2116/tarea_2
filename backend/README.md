# Backend - Gestión de Alumnos

## Requisitos
- Python 3.8+
- PostgreSQL

## Instalación
1. Clona el repositorio o copia los archivos en tu máquina.
2. Instala las dependencias:
   ```pwsh
   pip install -r requirements.txt
   ```
3. Crea la base de datos y la tabla:
   ```sql
   CREATE DATABASE tu_basededatos;
   \c tu_basededatos
   CREATE TABLE alumnos (
       id SERIAL PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL,
       apellido VARCHAR(100) NOT NULL,
       edad INTEGER NOT NULL
   );
   ```
4. Copia `.env.example` a `.env` y completa tus credenciales de PostgreSQL.

## Ejecución
```pwsh
python app.py
```
El backend estará disponible en `http://localhost:5000`.

## Endpoints
- `GET /alumnos` - Lista todos los alumnos
- `GET /alumnos/<id>` - Obtiene un alumno por id
- `POST /alumnos` - Agrega un nuevo alumno
- `PUT /alumnos/<id>` - Modifica un alumno existente
- `DELETE /alumnos/<id>` - Elimina un alumno
