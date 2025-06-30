# Guía de Despliegue para Microservicios de Tareas y Usuarios

---

## Resumen
Este proyecto implementa una arquitectura de microservicios basada en Docker para gestionar tareas y usuarios, conforme a las Unidades 2 y 3 del curso SysAdmin 2025. Los servicios `user-service` y `task-service` están orquestados con Docker Compose, con Nginx Proxy Manager como API Gateway para enrutamiento y seguridad. A continuación, se detalla el despliegue con un enfoque profundo en los componentes subyacentes.

---

## Requisitos Previos
- Docker y Docker Compose instalados
- Git para clonar el repositorio
- Variables de entorno configuradas (ver archivo `.env`)

---

## Estructura del Proyecto
| Directorio/Archivo         | Descripción                                  |
|----------------------------|----------------------------------------------|
| `app/`                     | Código fuente para `user-service` y `task-service` |
| `env/`                     | Archivos de configuración de entorno         |
| `nginx/`                   | Configuración de Nginx Proxy Manager         |
| `task-service/`, `user-service/` | Directorios específicos de los servicios  |
| `Dockerfile`               | Instrucciones de compilación                 |
| `docker-compose.yml`       | Archivo de orquestación                      |
| `requirements.txt`         | Dependencias de Python                       |
| `.gitignore`               | Archivos excluidos                           |
| `README.md`                | Este archivo                                 |

---

## Pasos de Despliegue

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd <directorio-del-repositorio>
```

### 2. Configurar Variables de Entorno
- Copia `.env.example` a `.env` y configura:
  - `DB_NAME`: Nombre de la base de datos SQLite (e.g., `tasks.db`)
  - `USER_SERVICE_URL`: URL del servicio de usuarios (e.g., `http://user-service:8000/users/`)
- Este archivo se carga en los scripts Python mediante `python-dotenv`.

### 3. Compilar y Ejecutar con Docker Compose
```bash
docker-compose up --build
```
- Compila las imágenes Docker y las inicia con Nginx Proxy Manager.

### 4. Verificar los Servicios
- Endpoints de salud:
  - `http://localhost:8000/api/users/health` (user-service)
  - `http://localhost:8001/api/tasks/health` (task-service)
- API Gateway: `http://localhost/admin`

### 5. Endpoints de la API
| Método | Ruta             | Descripción                  |
|--------|------------------|-------------------------------|
| `POST` | `/api/users`     | Crear usuario                 |
| `GET`  | `/api/users`     | Listar usuarios               |
| `GET`  | `/api/users/{user_id}` | Obtener usuario         |
| `POST` | `/api/tasks`     | Crear tarea                   |
| `GET`  | `/api/tasks`     | Listar tareas                 |
| `GET`  | `/api/tasks/{task_id}` | Obtener tarea         |
| `PUT`  | `/api/tasks/{task_id}` | Actualizar estado       |
| `GET`  | `/api/tasks?user_id={user_id}` | Filtrar por usuario |

---

## Detalle Técnico de los Componentes

### El Rol del Dockerfile
El `Dockerfile` define la construcción de las imágenes. Ejemplo:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data
COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", 8000]
```
- **Pasos**: Copia dependencias, instala librerías, crea directorio de datos, expone puertos y ejecuta Uvicorn.

### Lógica Interna en los Archivos `.py`
- **database.py**: Configura SQLAlchemy con SQLite:
  ```python
  SQLALCHEMY_DATABASE_URL = "sqlite:///./data/tasks.db"
  engine = create_engine(SQLALCHEMY_DATABASE_URL)
  SessionLocal = sessionmaker(bind=engine)
  ```
- **models.py**: Define tablas:
  ```python
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True)
      email = Column(String, unique=True)
  ```
- **schemas.py**: Valida datos con Pydantic:
  ```python
  class TaskCreate(BaseModel):
      title: str
      user_id: int
  ```
- **crud.py**: Opera la base de datos:
  ```python
  def create_task(db: Session, task: schemas.TaskCreate):
      db_task = models.Task(**task.dict(), status="pendiente")
      db.add(db_task)
      db.commit()
      return db_task
  ```
- **main.py**: Define rutas de FastAPI:
  ```python
  @app.post("/tasks")
  async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
      async with httpx.AsyncClient() as client:
          response = await client.get(f"{USER_SERVICE_URL}{task.user_id}")
          if response.status_code != 200:
              raise HTTPException(status_code=404, detail="Usuario no encontrado")
      return crud.create_task(db, task)
  ```

### Rol de Nginx Proxy Manager
Nginx redirige el tráfico. Ejemplo de configuración:
```
location /api/users/ {
    proxy_pass http://user-service:8000/;
}
location /api/tasks/ {
    proxy_pass http://task-service:8001/;
}
```
- En Unidad 3, se añade SSL/TLS y redirección HTTPS.

### Volúmenes y Persistencia
Ejemplo en `docker-compose.yml`:
```yaml
volumes:
  - ./app/data:/app/data
```
- Monta `./app/data` para persistir `tasks.db`.

### Enrutamiento y Comunicación
- **Red interna**: Definida en `docker-compose.yml`:
  ```yaml
  networks:
    app-network:
      driver: bridge
  ```
- **Llamadas HTTP**: `task-service` consulta `user-service` internamente.

---

## Notas
- SQLite es usado por simplicidad; considera PostgreSQL en producción.
- Para Unidad 3, configura SSL/TLS y mitigación DoS.

---

## Solución de Problemas
- Verifica puertos (8000, 8001, 80, 443).
- Revisa logs con `docker-compose logs`.

---

*Última actualización: 29 de junio de 2025, 10:10 PM -04*