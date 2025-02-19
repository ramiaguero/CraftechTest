# **Justificación del Uso de EKS**

Decidí usar Amazon EKS para desplegar la aplicación, no tanto por su funcionalidad actual, sino por lo que representa en términos de arquitectura. Aunque la app en sí no es tan compleja ahora mismo, si en el futuro crece con más microservicios, como un chat u otros módulos, lo más eficiente sería tener cada uno separado en Kubernetes, con su propio Deployment y Service, comunicándose a través de NodePorts y con un Ingress manejando el tráfico externo.

## **Por qué EKS y no ECS o algo más simple**
Podría haber usado AWS Copilot con ECS, que es compatible con Docker Compose, y la verdad es que para una app sencilla como esta podría haber sido suficiente. Pero pensando en escalabilidad, gestión de múltiples servicios y actualizaciones más controladas, Kubernetes con Helm me da más flexibilidad.

- Con Helm, tengo una estructura organizada y fácil de desplegar.
- Si quisiera agregar más servicios en el futuro, solo sumo un nuevo deployment sin romper nada.
- Podría escalar individualmente cada componente según la demanda.
- Mayor seguridad: usando roles con permisos mínimos y certificados en un Ingress.

## **Lo que hice en este despliegue**
No lo llevé al extremo de un stack Kubernetes full enterprise, porque la app en sí no lo requiere. Pero sí estructuré el despliegue de forma que se pueda escalar sin hacer cambios bruscos.

- Separé backend y frontend en sus propios deployments y services.
- Base de datos gestionada aparte para evitar fallos al reiniciar el clúster.
- Configuré un LoadBalancer por servicio en lugar de usar un Ingress, para simplificar.
- Automaticé la instalación con Helm, para que sea más fácil levantar todo con un solo comando.

## **Cómo lo mejoraría en el futuro**
Si el proyecto crece, la idea sería:
- Usar **Ingress** en vez de LoadBalancers separados, para manejar mejor el tráfico externo.
- Agregar **ArgoCD** para actualizaciones automáticas sin downtime.
- Manejar **bases de datos con replicas y backups** mejor organizados.

Por ahora, este stack en **EKS con Helm** da la flexibilidad justa sin hacer el despliegue más complejo de lo necesario.