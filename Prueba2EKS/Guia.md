A continuación se presenta la guía mejorada y minimalista para la configuración paso a paso de un clúster EKS usando Helm, con las mejores prácticas. Esta guía asume que el clúster se crea y elimina con frecuencia, por lo que es necesario reconfigurarlo cada vez.

---

# Guía para Configuración en EKS

## Justificación
Cada vez que se crea (o se elimina) un clúster EKS, se deben volver a aplicar las configuraciones y políticas necesarias para que los workers funcionen correctamente, el almacenamiento persistente (mediante el controlador EBS CSI) esté habilitado y la aplicación se despliegue mediante Helm.

---

## Paso 1: Crear el Clúster de EKS

Ejecutar el siguiente comando para crear un clúster EKS en la región us-east-1 con Kubernetes 1.31 (este setup está probado en 1.31; la 1.32 ya está disponible, pero se utiliza 1.31 para este ejemplo):

```sh
eksctl create cluster \
  --name craftech-cluster \
  --region us-east-1 \
  --version 1.31 \
  --nodegroup-name craftech-nodegroup \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 3 \
  --managed
```

> Asegúrese de ejecutar el comando en una sola línea o usar correctamente la barra invertida (`\`) para evitar errores como “command not found: --nodegroup-name”.

El comando creará el clúster y un nodegroup gestionado. Al finalizar, se guardará el kubeconfig y se podrá verificar la disponibilidad de los nodos con:

```sh
kubectl get nodes -o wide
```

---

## Paso 2: Adjuntar las Políticas IAM Requeridas a los Workers

Para que los nodos puedan interactuar con EKS, extraer imágenes y, sobre todo, provisionar volúmenes EBS, se deben adjuntar las siguientes políticas al rol asignado al nodegroup. Use los siguientes comandos:

```sh
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
  --role-name $(aws iam list-roles --query "Roles[?contains(RoleName, 'eksctl-craftech-nodegroup')].RoleName" --output text)

aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
  --role-name $(aws iam list-roles --query "Roles[?contains(RoleName, 'eksctl-craftech-nodegroup')].RoleName" --output text)

aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
  --role-name $(aws iam list-roles --query "Roles[?contains(RoleName, 'eksctl-craftech-nodegroup')].RoleName" --output text)
```

Verifique que las políticas estén adjuntas con:

```sh
aws iam list-attached-role-policies --role-name <NOMBRE_DEL_ROLE>
```

Reemplace `<NOMBRE_DEL_ROLE>` por el nombre obtenido (por ejemplo, `eksctl-craftech-cluster-nodegroup--NodeInstanceRole-XXXX`).

---

## Paso 3: Instalar y Configurar el Controlador EBS CSI

Para habilitar el almacenamiento persistente, se debe instalar el addon del controlador EBS CSI.

Si OIDC está habilitado en el clúster (recomendado), ejecute:

```sh
eksctl utils associate-iam-oidc-provider --cluster craftech-cluster --approve
```

Luego, instale el addon:

```sh
eksctl create addon --name aws-ebs-csi-driver --cluster craftech-cluster --service-account-role-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/AmazonEBSCSIDriverRole
```

Si OIDC no está habilitado, el comando mostrará un aviso. En ese caso, asegúrese de que el rol de los nodos tenga la política necesaria (lo cual se realizó en el Paso 2) y, de ser necesario, configure manualmente las asociaciones de identidad.

---

## Paso 4: Desplegar la Aplicación Usando Helm

El Helm chart del repositorio despliega tanto el backend como el frontend. El chart se encuentra en el directorio `app-chart`.

### Actualizar valores de Helm antes del despliegue

Abra el archivo `./app-chart/values.yaml` y verifique las siguientes secciones:

- **Imagenes:**

  ```yaml
  image:
    backend: "ramiroaguero/craftechtest:backend-1.17.6"
    frontend: "ramiroaguero/craftechtest:frontend-1.17.4"
    pullPolicy: Always
  ```

- **Servicio (puerto):**

  ```yaml
  service:
    type: LoadBalancer
    backendPort: 8000
    frontendPort: 3000
  ```

> Nota: No es necesario actualizar las IPs del Load Balancer en el values.yaml. El ELB se crea y se actualiza automáticamente. Los archivos como ConfigMap o .env (si los hay) se deben actualizar en el clúster mediante `kubectl edit` si es necesario.

### Instalar/Actualizar el Chart

Ejecute el siguiente comando en el directorio raíz del chart:

```sh
helm upgrade --install craftech-app ./app-chart -f ./app-chart/values.yaml -n default
```

Esto desplegará los componentes (backend y frontend) en el namespace `default`.

---

## Paso 5: Obtener las URLs de los ELB

Después del despliegue, obtenga las direcciones externas de los servicios:

```sh
kubectl get svc backend-service frontend-service -n default
```

El resultado mostrará algo similar a:

```
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)
backend-service    LoadBalancer   10.100.174.130   aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com    8000:30348/TCP
frontend-service   LoadBalancer   10.100.124.195   a1ea82fa5c25a46e4a572f1871350ccb-1392024633.us-east-1.elb.amazonaws.com   3000:31944/TCP
```

Utilice estas URLs para acceder a la aplicación.

---

## Paso 6: Actualizar Configuraciones (si es necesario)

Si el clúster se recrea y cambian las direcciones ELB, actualice:

### ConfigMap del Backend

```sh
kubectl edit configmap django-env -n default
```

Actualice `DJANGO_ALLOWED_HOSTS` para incluir la nueva URL del ELB, por ejemplo:

```yaml
DJANGO_ALLOWED_HOSTS: "localhost,127.0.0.1,[::1],backend-service,backend-service.default.svc.cluster.local,aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com"
```

Luego reinicie el backend:

```sh
kubectl rollout restart deployment django-backend -n default
```

### ConfigMap o .env del Frontend

Si la aplicación React usa un ConfigMap para sus variables, actualice el backend URL:

```sh
kubectl edit configmap frontend-env -n default
```

Establezca:

```yaml
REACT_APP_BACKEND_URL: "http://aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com:8000"
```

Luego reinicie el frontend:

```sh
kubectl rollout restart deployment react-frontend -n default
```

---

## Paso 7: Ajustes de Seguridad (si es necesario)

Si existen problemas de comunicación entre servicios:

1. Identifique el Security Group asociado al ELB en la consola de EC2.
2. Asegúrese de que se permita el tráfico entrante en el puerto 8000 (para el backend) desde el rango adecuado (generalmente 0.0.0.0/0 o los IPs internos del clúster).

Ejemplo para autorizar tráfico:

```sh
aws ec2 authorize-security-group-ingress \
  --group-id <ID_DEL_SECURITY_GROUP> \
  --protocol tcp --port 8000 --cidr 0.0.0.0/0
```

Reemplace `<ID_DEL_SECURITY_GROUP>` según corresponda.

---

## Paso 8: Reiniciar y Probar

Si surge algún problema o cambio de configuración, reinicie los despliegues:

```sh
kubectl rollout restart deployment django-backend -n default
kubectl rollout restart deployment react-frontend -n default
```

Verifique los logs si aparecen errores:

```sh
kubectl logs -l app=backend -n default --tail=50
kubectl logs -l app=frontend -n default --tail=50
```

---

## Conclusión

Cada vez que se recrea el clúster EKS:
- Se debe crear el clúster con eksctl usando el comando del Paso 1.
- Se adjuntan las políticas IAM en el Paso 2.
- Se instala el addon de EBS CSI en el Paso 3.
- Se despliega la aplicación con Helm en el Paso 4.
- Se obtienen y actualizan las URLs de los ELB en los Pasos 5 y 6.
- Se revisan y ajustan los Security Groups en el Paso 7.
- Se reinician los despliegues y se realizan pruebas en el Paso 8.

Esta guía integra las mejores prácticas y mantiene el proceso lo más simple y reproducible posible. Si necesitas más aclaraciones o ajustes, por favor indícalo.