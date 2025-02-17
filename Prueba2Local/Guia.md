# **Guía Rápida para Desplegar la App en Local con Docker y Docker Compose**

Esta guía detalla el proceso para ejecutar la aplicación en local utilizando Docker y Docker Compose, sin necesidad de modificar código en el backend ni en el frontend.

---

## **Paso 1: Instalar Dependencias**

Antes de continuar, asegurarse de que Docker y Docker Compose están instalados.

### **Instalar Docker y Docker Compose**

**En Ubuntu/Debian:**
```sh
sudo apt update && sudo apt install -y docker.io docker-compose
```

**En macOS con Homebrew:**
```sh
brew install docker docker-compose
```

**Verificar la instalación:**
```sh
docker --version
docker-compose --version
```

---

## **Paso 2: Clonar el Repositorio**
Si el código aún no está en local, clonarlo:
```sh
git clone https://github.com/ramiaguero/CraftechTest.git
cd CraftechTest
```

---

## **Paso 3: Configurar Variables de Entorno**

El backend y el frontend ya están configurados para funcionar en local sin cambios de código.

### **Backend**
Crear el archivo `.env` en la carpeta `backend`:
```sh
touch backend/.env
nano backend/.env
```
Agregar lo siguiente:
```ini
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=django_db
SQL_USER=admin
SQL_PASSWORD=supersecret
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

### **Frontend**
Verificar que el archivo `.env` en `frontend` tiene la URL correcta:
```sh
touch frontend/.env
nano frontend/.env
```
Debe contener:
```ini
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## **Paso 4: Levantar la Aplicación con Docker Compose**

El archivo `docker-compose.yml` ya está configurado para levantar la base de datos, el backend y el frontend.

### **Construir las Imágenes**
```sh
docker-compose build
```

### **Iniciar los Contenedores**
```sh
docker-compose up -d
```

Para ver logs en tiempo real:
```sh
docker-compose logs -f
```

---

## **Paso 5: Verificar el Funcionamiento**

### **Verificar Contenedores Activos**
```sh
docker ps
```
Se deberían ver tres contenedores ejecutándose:
```
CONTAINER ID   IMAGE             STATUS          PORTS
12345abcde     backend           Up 10 seconds  0.0.0.0:8000->8000/tcp
67890fghij     frontend          Up 10 seconds  0.0.0.0:3000->3000/tcp
abcde12345     postgres:latest   Up 10 seconds  5432/tcp
```

### **Acceder a la Aplicación**

- **Backend (Django REST API)**:  
  http://localhost:8000/api/

- **Frontend (React)**:  
  http://localhost:3000

---

## **Paso 6: Debugging y Acceso a Contenedores**

### **Ver logs**
Backend:
```sh
docker-compose logs backend
```
Frontend:
```sh
docker-compose logs frontend
```
Base de datos:
```sh
docker-compose logs db
```

### **Acceder a los Contenedores**
Backend:
```sh
docker exec -it backend sh
```
Abrir shell de Django:
```sh
docker exec -it backend python manage.py shell
```

---

## **Paso 7: Detener la App**

Para apagar los contenedores:
```sh
docker-compose down
```

Para eliminar volúmenes de la base de datos:
```sh
docker-compose down -v
```

---

## **Notas Finales**
- Cada vez que se quiera levantar la aplicación:
  ```sh
  docker-compose up -d
  ```
- Si se realizan cambios en el código:
  ```sh
  docker-compose build
  docker-compose up -d
  ```
- Para detener la aplicación:
  ```sh
  docker-compose down
  ```