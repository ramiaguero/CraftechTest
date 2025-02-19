## Justificación del uso de Docker Compose para ejecución local

**demo**

https://youtu.be/YrIcRuisj2Y

- **Facilidad de configuración**: Permite definir todos los servicios (frontend, backend y base de datos) en un solo archivo y levantarlos con un solo comando. (dentro del readme explicando como ejecutar dejare un script para un deployment mas sencillo)
- **Gestión de múltiples servicios**: Automatiza la conexión entre los servicios sin necesidad de configuración manual.
- **Persistencia de datos**: Usa volúmenes de Docker para que la base de datos mantenga su información entre reinicios del contenedor. (por default esta activado flush, por ende los datos no seran persistentes)


