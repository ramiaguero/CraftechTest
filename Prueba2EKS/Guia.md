# **Guíapara Configuración en EKS**

## **referirse primero a la justificacion de stack donde hay un ejemplo y la explicacion del caso**

## **Crear el Clúster de EKS**
Cada vez que creamos y eliminamos el clúster de EKS, hace falta configurarlo de nuevo. Los siguientes comandos despliegan un nuevo clúster de EKS y adjuntarán las políticas IAM necesarias.

### **1️ Crear el Clúster de EKS**
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
Esto crea un clúster de EKS con un nodegroup.
**esta la 1.32 ya disponible, pero este setup esta testeado en 1.31**

---

## **Paso 2: Adjuntar las Políticas IAM Requeridas**
Para que los workers funcionen correctamente:
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
Esto garantiza que los workers puedan interactuar con EKS.

---

## **Paso 3: Instalar y Configurar el Controlador EBS CSI**
Esto permite que Kubernetes cree Volúmenes Persistentes (PVs):
```sh
eksctl create addon --name aws-ebs-csi-driver --cluster craftech-cluster --service-account-role-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/AmazonEBSCSIDriverRole
```
Ahora el almacenamiento persistente está habilitado.

---

## **Paso 4: Desplegar la Aplicación Usando Helm**
El Helm chart que hice despliega tanto el backend como el frontend.

### **Actualizar valores de Helm antes del despliegue**
Antes de desplegar la app, actualizá:
```sh
nano ./app-chart/values.yaml
```
**Actualizar las IPs del Load Balancer** (**cambian cuando recreás el clúster**):
```yaml
backend:
  service:
    hostname: "aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com"

frontend:
  service:
    hostname: "a1ea82fa5c25a46e4a572f1871350ccb-1392024633.us-east-1.elb.amazonaws.com"
```
Estas IPs cambian cuando el clúster es recreado, así que hay que actualizarlas.

### **Instalar/Actualizar el Chart de Helm**
Ejecutar:
```sh
helm upgrade --install craftech-app ./app-chart -f ./app-chart/values.yaml -n default
```
Esto despliega el backend y frontend.

---

## **Paso 5: Encontrar las URLs del ELB**
Después del despliegue, obtené los Load Balancers externos:
```sh
kubectl get svc backend-service frontend-service -n default
```
Ejemplo de output:
```
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)
backend-service    LoadBalancer   10.100.174.130   aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com    8000:30348/TCP
frontend-service   LoadBalancer   10.100.124.195   a1ea82fa5c25a46e4a572f1871350ccb-1392024633.us-east-1.elb.amazonaws.com   3000:31944/TCP
```
Usá estas nuevas IPs de ELB en los archivos que siguen.

---

## **Paso 6: Dónde Actualizar las IPs del ELB**
Cada vez que el clúster es recreado, hay que actualizar estos archivos:

### **ConfigMap del Backend**
```sh
kubectl edit configmap django-env -n default
```
**Actualizar `DJANGO_ALLOWED_HOSTS`**:
```yaml
DJANGO_ALLOWED_HOSTS: "localhost,127.0.0.1,[::1],backend-service,backend-service.default.svc.cluster.local,aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com"
```
Guardá y reiniciá el backend:
```sh
kubectl rollout restart deployment django-backend -n default
```
Esto garantiza que Django acepte requests desde el nuevo ELB.

### **`.env` del Frontend**
Actualizar las variables de entorno en React:
```sh
kubectl edit configmap frontend-env -n default
```
**Actualizar `REACT_APP_BACKEND_URL`**:
```yaml
REACT_APP_BACKEND_URL: "http://aaffc0a22feb44a18be60ad86a9d24b1-935174219.us-east-1.elb.amazonaws.com:8000"
```
Guardá y reiniciá el frontend:
```sh
kubectl rollout restart deployment react-frontend -n default
```
Ahora React llamará correctamente al backend.

---

## **Paso 7: Ajustes de Seguridad en Security Groups**
Si el frontend no puede comunicarse con el backend, revisar los Security Groups.

### **1️Encontrar el Security Group del Backend ELB**
```sh
aws ec2 describe-security-groups --query "SecurityGroups[].[GroupId,GroupName]" --output table
```
Buscá el **ID** del grupo de seguridad del backend (`k8s-elb-aaffc0a22feb...`).

### **Permitir Comunicación del Frontend al Backend**
```sh
aws ec2 authorize-security-group-ingress \
  --group-id sg-025f63019f321c679 \
  --protocol tcp --port 8000 --cidr 0.0.0.0/0
```
Esto permite que **el frontend se comunique con el backend**.

---

## **Paso 8: Reiniciar y Probar**
Si algo no funciona, reiniciar todos los despliegues:
```sh
kubectl rollout restart deployment django-backend -n default
kubectl rollout restart deployment react-frontend -n default
```
Esto refresca toda la configuración.

---

## **Paso 9: Debugging**
Si el frontend no carga:
```sh
kubectl logs -l app=frontend -n default --tail=50
```
Si el backend no responde:
```sh
kubectl logs -l app=backend -n default --tail=50
```
Si React todavía usa una URL vieja del backend:
```sh
kubectl exec -it $(kubectl get pods -l app=frontend -n default -o jsonpath="{.items[0].metadata.name}") -- printenv | grep REACT_APP_BACKEND_URL
```
Si el backend no está corriendo:
```sh
kubectl exec -it $(kubectl get pods -l app=backend -n default -o jsonpath="{.items[0].metadata.name}") -- nc -zv localhost 8000
```
Corregir **cualquier configuración incorrecta** y reiniciar el despliegue.

---

## **Conclusión**
Cada vez que eliminás y recreás el clúster:
- **Actualizá**: `values.yaml`, `django-env`, `frontend-env`
- **Reiniciá** los despliegues con:
  ```sh
  kubectl rollout restart deployment django-backend -n default
  kubectl rollout restart deployment react-frontend -n default
  ```
- **Verificá los logs** si hay errores.