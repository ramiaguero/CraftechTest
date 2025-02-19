### **Guía de Despliegue: App Django + React con Docker en EC2**  

### **luego de clonar el repositorio y pararse en el directorio Prueba2VM**

el proyecto debería verse así:

```
.
├── app
│   ├── backend
│   │   ├── Dockerfile
│   │   ├── Dockerfile.prod
│   │   └── .env.prod
│   └── frontend
│       ├── Dockerfile
│       └── Dockerfile.prod
├── deployment
│   ├── docker-compose.prod.yml
│   └── nginx.conf
└── docker-compose.yml
```

---

### **1. Crear la Instancia EC2**  

#### a. Configuración inicial  

- **AMI:** Ubuntu 22.04  
- **Tipo de instancia:** t2.micro o superior  
- **User Data:** Agregar este script en el campo *User Data* al crear la instancia  

```bash
#!/bin/bash
apt-get update
apt-get upgrade -y

apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    docker.io

systemctl start docker
systemctl enable docker

curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

mkdir -p /opt/myapp
```

#### b. Configuración del Security Group  

- **HTTP (puerto 80):** Permitir desde `0.0.0.0/0`  
- **SSH (puerto 22):** Permitir solo desde tu IP  

---

### **2. Preparar el Entorno Local**  

Antes de subir el proyecto a la instancia EC2, verifica que tu configuración esté correcta:  

1. **Archivo de entorno:** Edita `/app/backend/.env.prod` con los valores adecuados.  

   ```env
   DEBUG=0
   SECRET_KEY=clave-secreta
   DJANGO_ALLOWED_HOSTS=ip de la instancia aqui
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=dbname
   SQL_USER=craftech
   SQL_PASSWORD=craftech1234
   SQL_HOST=db
   SQL_PORT=5432
   DATABASE=postgres
   POSTGRES_USER=craftech
   POSTGRES_PASSWORD=craftech1234
   POSTGRES_DB=dbname
   ```

2. **Configurar Nginx para el frontend:**  

   ```bash
   cp deployment/nginx.conf app/frontend/nginx.conf
   ```

---

### **3. Subir el Proyecto a la Instancia EC2**  

Desde tu máquina local, ejecuta:  

```bash
scp -i tu-clave.pem -r ./* ubuntu@tu-ip-ec2:/opt/myapp/
```

Reemplaza `tu-clave.pem` con la clave privada y `tu-ip-ec2` con la dirección pública de tu instancia.  

---

### **4. Conectarse a la Instancia**  

```bash
ssh -i tu-clave.pem ubuntu@tu-ip-ec2
```

Una vez dentro:  

```bash
cd /opt/myapp
```

---

### **5. Instalar Dependencias (si es necesario)**  

Si el script de *User Data* no instaló Docker y Docker Compose:  

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common docker.io

sudo systemctl start docker
sudo systemctl enable docker

sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo usermod -aG docker ubuntu
newgrp docker
```

---

### **6. Construir y Ejecutar los Contenedores**  

Desde `/opt/myapp`:  

```bash
docker-compose -f deployment/docker-compose.prod.yml down && docker-compose -f deployment/docker-compose.prod.yml up -d --build
```

Esto detiene los contenedores antiguos, reconstruye las imágenes y levanta el stack en modo *detached*.

---

### **7. Aplicar Migraciones**  

```bash
docker-compose -f deployment/docker-compose.prod.yml exec backend python manage.py migrate
```

Si es necesario, generar migraciones antes:  

```bash
docker-compose -f deployment/docker-compose.prod.yml exec backend python manage.py makemigrations
docker-compose -f deployment/docker-compose.prod.yml exec backend python manage.py migrate
```

---

### **8. Verificar el Despliegue**  

- **Ver contenedores corriendo:**  

  ```bash
  docker ps
  ```

- **Ver logs en caso de errores:**  

  ```bash
  docker-compose -f deployment/docker-compose.prod.yml logs
  ```

- **Acceder a la aplicación:**  

  Ir a `http://tu-ip-ec2` en un navegador.  

---

### **Comandos Clave**  

```bash
# Copiar archivos a EC2
scp -i tu-clave.pem -r ./* ubuntu@tu-ip-ec2:/opt/myapp/

# Conectarse a la instancia
ssh -i tu-clave.pem ubuntu@tu-ip-ec2

# Ir al directorio del proyecto
cd /opt/myapp

# Instalar dependencias si hace falta
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker ubuntu
newgrp docker

# Copiar nginx.conf dentro del frontend
cp deployment/nginx.conf app/frontend/nginx.conf

# Construir y ejecutar contenedores
docker-compose -f deployment/docker-compose.prod.yml down && docker-compose -f deployment/docker-compose.prod.yml up -d --build

# Aplicar migraciones
docker-compose -f deployment/docker-compose.prod.yml exec backend python manage.py migrate
```

---

Tu aplicación ya debería estar desplegada en `http://tu-ip-ec2`.