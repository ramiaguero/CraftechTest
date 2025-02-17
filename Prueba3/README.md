# Prueba 3 - CI/CD: Dockerizar un Nginx con index.html Default

## Descripción

Esta solución implementa un proceso de Integración y Despliegue Continuo (CI/CD) para una aplicación web sencilla basada en Nginx. El objetivo es detectar cualquier cambio en el archivo `index.html` (ubicado en la carpeta `Prueba3`), construir una nueva imagen de Docker con la versión actualizada y desplegarla automáticamente utilizando Docker Compose en un entorno de producción.

## Tecnologías Utilizadas

- **Docker:** Para contenerizar la aplicación y empaquetar Nginx junto con el archivo `index.html`.
- **Nginx:** Servidor web que se utiliza para servir el contenido de la aplicación.
- **Docker Compose:** Para gestionar el despliegue y la orquestación del contenedor.
- **GitHub Actions:** Plataforma de CI/CD utilizada para automatizar la construcción y el despliegue de la aplicación.
- **Amazon EC2 con Ubuntu 22.04:** Instancia en la nube donde se despliega la aplicación.
- **Git:** Sistema de control de versiones para gestionar el código fuente.

## Flujo del Pipeline

1. **Detección de cambios:**  
   El pipeline se dispara automáticamente ante cualquier cambio realizado en la carpeta `Prueba3` (especialmente en `index.html`) o en la configuración del workflow (ubicado en `.github/workflows/**`).

2. **Construcción de la imagen:**  
   Cuando se detecta un cambio, GitHub Actions ejecuta el workflow que:
   - Hace un checkout del repositorio.
   - Construye una nueva imagen de Docker basada en el contenido de la carpeta `Prueba3`.
   - Etiqueta la imagen como `latest` y con el hash del commit.

3. **Publicación y Despliegue:**  
   La nueva imagen se sube a Docker Hub y, mediante un runner autohospedado en una instancia EC2 (Ubuntu 22.04), se actualiza el despliegue usando Docker Compose.

## Cómo Probar la Solución

1. **Realizar un Cambio:**  
   - Modifica el contenido del archivo `Prueba3/index.html`.
   - Realiza un commit y push de los cambios al repositorio.

2. **Verificar el Pipeline:**  
   - Ingresa a la pestaña "Actions" en GitHub para observar la ejecución del workflow.
   - El proceso realizará la construcción de la imagen y su despliegue en la instancia EC2.

3. **Acceder a la Aplicación:**  
   - Una vez finalizado el despliegue, abre un navegador y accede a la URL pública de la instancia EC2 (por ejemplo, `http://ec2-75-101-216-18.compute-1.amazonaws.com`).
   - Deberías ver reflejados los cambios realizados en el `index.html`.

## Notas Adicionales

- **Automatización del Despliegue:**  
  La solución demuestra la capacidad para automatizar la parte del proceso de despliegue, integrando las fases de construcción y despliegue en un único pipeline.

- **Configuración del Runner:**  
  Se utiliza un runner autohospedado en una instancia EC2 con Ubuntu 22.04 para ejecutar el proceso de despliegue. La configuración del runner y del servicio systemd asegura que la aplicación se reinicie automáticamente en caso de fallos.

