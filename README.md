# Proyecto Unidad 2 - SysAdmin 2025 I

## 🌟 Objetivo General

Contenerizar y orquestar una aplicación funcional de microservicios para la gestión de tareas colaborativas. Se implementan dos servicios:

* **user-service**: para registrar y consultar usuarios.
* **task-service**: para crear y gestionar tareas asociadas a usuarios existentes.

Ambos microservicios se conectan vía red interna Docker y se despliegan con Docker Compose. Se utilizan variables de entorno para manejar configuraciones sensibles y reutilizables.

---

## 📦 Instalación y ejecución rápida

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/robobaile-sysadmin-2025.git
cd robobaile-sysadmin-2025

# Construir y ejecutar los servicios
docker compose up --build

# Accede a los servicios
# http://localhost:8000/docs (user-service)
# http://localhost:8001/docs (task-service)
```

---

## 📅 Estructura del Proyecto

```
robobaile-sysadmin-2025/
├── docker-compose.yml
├── .env
├── README.md
├── user-service/
│   ├── .env
│   ├── app/
│   │   ├── main.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── database.py
│   ├── Dockerfile
│   └── requirements.txt
└── task-service/
    ├── .env
    ├── app/
    │   ├── main.py
    │   ├── crud.py
    │   ├── models.py
    │   ├── schemas.py
    │   └── database.py
    ├── Dockerfile
    └── requirements.txt
```

---

## 🚀 Servicios Desarrollados

### 1. user-service

**Responsabilidad**: Registro, consulta y validación de usuarios.

* Base de datos: SQLite (`users.db` especificado en `.env`)
* Endpoints:

  * `POST /users`: Registrar nuevo usuario
  * `GET /users`: Listar usuarios
  * `GET /users/{id}`: Consultar usuario específico
  * `GET /health`: Estado del servicio

### 2. task-service

**Responsabilidad**: Crear, consultar y actualizar tareas de usuarios.

* Base de datos: SQLite (`tasks.db` especificado en `.env`)
* Verifica la existencia del usuario antes de crear la tarea (`USER_SERVICE_URL` desde `.env`)
* Endpoints:

  * `POST /tasks`
  * `GET /tasks`
  * `GET /tasks/{id}`
  * `PUT /tasks/{id}`
  * `GET /tasks?user_id=X`
  * `GET /health`

---

## 🔐 Variables de Entorno

### 📁 `.env` (raíz)

```env
USER_SERVICE_PORT=8000
TASK_SERVICE_PORT=8001
```

### 📁 `user-service/.env`

```env
DB_NAME=users.db
```

### 📁 `task-service/.env`

```env
DB_NAME=tasks.db
USER_SERVICE_URL=http://user-service:8000/users/
```

### 🧠 ¿Cómo se utilizan?

En `database.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = f"sqlite:///./{os.getenv('DB_NAME')}"
```

En `main.py` de task-service:

```python
from dotenv import load_dotenv
import os

load_dotenv()
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
```

Docker Compose los carga con `env_file:` y los pasa automáticamente al entorno del contenedor.

---

## 🚜 Docker Compose explicado línea por línea

```yaml
version: '3.8'                      # Define la versión del esquema de Docker Compose

services:
  user-service:                     # Define el primer servicio (contenedor)
    build: ./user-service           # Usa el Dockerfile ubicado en ./user-service
    container_name: user-service   # Le asigna un nombre al contenedor
    ports:
      - "${USER_SERVICE_PORT}:8000" # Mapea el puerto del host al contenedor (usa .env)
    volumes:
      - ./user-service/app:/app/app # Monta el código local para desarrollo en caliente
    env_file:
      - ./user-service/.env        # Carga variables de entorno específicas del servicio
    networks:
      - micro_net                  # Conecta este servicio a una red interna
    restart: unless-stopped        # Reinicia automáticamente si se cae

  task-service:
    build: ./task-service
    container_name: task-service
    ports:
      - "${TASK_SERVICE_PORT}:8001"
    volumes:
      - ./task-service/app:/app/app
    env_file:
      - ./task-service/.env
    networks:
      - micro_net
    depends_on:
      - user-service               # Espera a que user-service esté arriba antes de arrancar
    restart: unless-stopped

networks:
  micro_net:                        # Define una red interna llamada micro_net
    driver: bridge                  # Usa el driver de red bridge predeterminado
```

---

## 📊 Validación de Requisitos de la Unidad 2

| Requisito                                  | Estado |
| ------------------------------------------ | ------ |
| Contenerización de ambos servicios         | ✅      |
| API REST funcionales y documentadas        | ✅      |
| Validación de datos y comunicación interna | ✅      |
| Uso de Docker Compose                      | ✅      |
| Red interna y dependencia entre servicios  | ✅      |
| Uso de variables de entorno                | ✅      |

---

## 🌟 Resultado Final

Sistema de microservicios **funcional, orquestado, validado y parametrizado con variables de entorno** según los criterios de la Unidad 2.

✔️ Código portable y reutilizable
✔️ Configurable mediante `.env`
✔️ Desplegable en cualquier entorno compatible con Docker

Listo para avanzar a la Unidad 3: Seguridad y Alta Disponibilidad 🚀
