# Servicio de backend independiente 🔧

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

## 🚀 Instrucciones de configuración local

1. Crear venv para el projecto usando python 3.12:
   ```bash
   pipenv shell
   pipenv install
   ```
2. Crear un archivo `.env` y actualizar los envars (mirar el archivo env.example en el dir raiz)

3. Crear la imagen de postgres:
   ```bash
   # Desde el directorio backend 
   docker build -t fly-postgres-pgvector -f Dockerfile.postgres .
   docker run -d --name fly-postgres-rag -p 5432:5432 -e POSTGRES_DB=pgdb -e POSTGRES_USER=pguser -e POSTGRES_PASSWORD=docker fly-postgres-pgvector
   ```

4. Crear un docker container local para redis:
   ```bash
   docker run -d --name redis-db -p 6379:6379 redis:7-alpine
   ```

5. Agregar su CV y otros textos que quiera para usar para el RAG de "docs" como archivos .md 

6. Iniciar el servidor:
   ```bash
   python3 run_server.py
   ```

7. Visite http://localhost:8000/docs y disfrute! 🎉

## 🐳 Docker Compose

```bash
# Construir los contenedores
docker compose build

# Iniciar los servicios
docker compose up
```

## 🚀 Despliegue en fly.io

1. Instalar el Fly CLI:
   ```bash
   brew install flyctl
   ```

2. Crear una nueva app:
   ```bash
   fly launch --no-deploy --name <your-app-name>
   ```

3. Crear la base de datos Postgres:
   ```bash
   fly postgres create --image-ref andrebrito16/pgvector-fly --name <your-db-name>
   ```
   > Nota: Usar una imagen de comunidad con la extensión pgvector preinstalada.  
   > [Learn more here](https://andrefbrito.medium.com/how-to-add-pgvector-support-on-fly-io-postgres-35b2ca039ab8)

4. Crear una instancia Redis:
   ```bash
   fly redis create --name <your-redis-name>
   ```

5. Configurar los requeridos secrets:
   ```bash
   fly secrets set POSTGRES_PASSWORD=<YOUR_PASSWORD>
   fly secrets set LLM_ROUTER_API_KEY=<YOUR_API_KEY>
   fly secrets set OPENAI_API_KEY=<YOUR_API_KEY>
   fly secrets set REDIS_URL=<YOUR_REDIS_URL>
   ```

6. Update the `fly.toml` file with your app, postgres, and redis details

7. Deploy:
   ```bash
   fly deploy
   ```

8. Visite su app en https://your-app-name.fly.dev/docs 🎉

## 🧪 Pruebas

Este proyecto utiliza PyTest para realizar pruebas. Las pruebas se organizan en el directorio `tests/`, siguiendo la estructura de la aplicación.

### Corriendo pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Correr pruebas con informe de cobertura
pytest --cov=app

# Ejecutar archivo de prueba específico
pytest tests/path/to/test_file.py

# Ejecutar pruebas en modo de observación
pytest-watch
```

### Configuración de prueba

La configuración de la prueba se define en `pytest.ini`. Las variables del entorno de prueba se definen en los accesorios de prueba.

