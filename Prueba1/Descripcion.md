# Descripción de la Arquitectura

La infraestructura de la aplicación web está diseñada para cumplir con los requisitos de cargas variables y alta disponibilidad (HA), implementada completamente en AWS para asegurar escalabilidad, seguridad y resiliencia.

## Cargas Variables y Alta Disponibilidad

Para soportar cargas variables, utilizamos un **Application Load Balancer (ALB)** distribuido en múltiples **Availability Zones**, permitiendo la distribución eficiente del tráfico entrante hacia las instancias **EC2** en un **Auto Scaling Group**. Este enfoque garantiza que la infraestructura pueda escalar automáticamente en función de la demanda, aumentando el número de instancias EC2 durante los picos de tráfico y reduciendo el número cuando la demanda disminuye. (Posibilidad de agregar **CloudWatch** para métricas y ajustes de escalado por **thresholds**).

## Frontend

El frontend está basado en **JavaScript** y se aloja detrás de una distribución de **Amazon CloudFront**, que actúa como un **CDN** para mejorar el rendimiento de la entrega de contenido estático a nivel global. El tráfico se resuelve mediante **Amazon Route 53**, que apunta a **CloudFront** para el frontend y al **ALB** para el backend. El **ALB** está configurado para recibir solo tráfico **HTTPS**, asegurado con un certificado **TLS** gestionado por **AWS Certificate Manager (ACM)**. (Asumiendo que el cliente tiene su dominio, también se puede crear el certificado en **ACM** o gestionar uno existente de otra autoridad).

## Backend

El backend está compuesto por instancias **EC2** en **subnets privadas**, garantizando que no estén directamente expuestas a Internet. Estas instancias están configuradas para consumir dos microservicios externos a través de un **NAT Gateway** ubicado en una **subnet pública**, lo que les permite realizar solicitudes salientes hacia Internet mientras mantienen su seguridad al no recibir tráfico entrante desde el exterior.(Aqui estoy asumiendo que la aprte de codigo y endpoints propios del back no es parte del scope)

## Bases de Datos

En cuanto a la base de datos, se utiliza **Amazon RDS** en una configuración **Multi-AZ** para garantizar alta disponibilidad y redundancia de los datos. La base de datos relacional está accesible únicamente desde las instancias backend a través de un **Security Group**. Además, se emplea **Amazon DynamoDB**, una base de datos **NoSQL**, accesible desde las instancias **EC2** mediante un **VPC Endpoint**, lo que permite una conexión privada y segura a **DynamoDB** sin tener que salir a Internet.

## Alta Disponibilidad

El diseño de la infraestructura cumple con los requisitos de **alta disponibilidad (HA)** mediante la distribución de los recursos en múltiples **Availability Zones**, asegurando que, en caso de falla de una zona, los recursos en otras zonas puedan seguir funcionando sin interrupciones. El **Auto Scaling Group**, el **ALB**, y las configuraciones de **RDS Multi-AZ** y **DynamoDB VPC Endpoint** permiten que la aplicación se adapte dinámicamente a los cambios en la carga de trabajo y garantice una experiencia continua y sin interrupciones para el usuario final.
