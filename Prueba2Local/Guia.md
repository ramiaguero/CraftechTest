# **Guía de Despliegue Local con Docker Compose**

Esta guía explica cómo ejecutar la aplicación en tu entorno local utilizando Docker y Docker Compose. 

---

## **1. Instalar Dependencias**
Antes de iniciar el despliegue, asegurate de tener instalados:

- **Docker**  
  [Instrucciones de instalación](https://docs.docker.com/get-docker/)

- **Docker Compose**  
  [Instrucciones de instalación](https://docs.docker.com/compose/install/)

- e.g. para ubuntu 

    ```bash
  sudo apt update && sudo apt install -y docker.io docker-compose
  
  sudo usermod -aG docker $USER  # Añade el usuario actual al grupo de Docker para permitir ejecutar comandos Docker sin `sudo`

    ```



Para verificar que están correctamente instalados:

```bash
docker --version
docker-compose --version
```

---

## **2. Clonar el Repositorio y Configurar el Entorno**
Si aún no lo tenés, clona el repositorio:

```bash
git clone https://github.com/ramiaguero/CraftechTest.git
cd CraftechTest
cd Prueba2Local
```

Asegurate de que el archivo `.env` esté en su lugar y configurado correctamente.

---

## **3. Construir y Levantar los Contenedores**
Desde la raíz del proyecto, ejecutar:

```bash
docker-compose up --build -d
```

Esto:
- Construye las imágenes de los servicios (`backend`, `frontend`, `db`).
- Inicia los contenedores en modo `detached` (en segundo plano).

Si ya habías levantado los contenedores antes y querés reconstruir desde cero, podés correr:

```bash
docker-compose down
docker-compose up --build -d
```

---

## **4. Verificar que Todo Está Corriendo**
Para comprobar que los contenedores están activos:

```bash
docker ps
```

Para ver logs de los contenedores:

```bash
docker-compose logs -f
```

---

## **5. Acceder a la Aplicación**
- **Frontend (React):**  
  `http://localhost:3000`

- **registrarse y logear**

Si la base de datos se está usando en otro servicio, verificar que la configuración en `.env` apunte correctamente al contenedor `db` en lugar de `localhost`.

---

## **6. Detener los Contenedores**
Para detener y eliminar los contenedores sin borrar volúmenes ni imágenes:

```bash
docker-compose down
```

Si querés borrar todo, incluyendo volúmenes:

```bash
docker-compose down -v
```
