# PoC Training: Despliegue de Clúster Kubernetes con Kubeadm en Bare-Metal / VirtualBox

<div align="center">

![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.31-326CE5?logo=kubernetes&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420?logo=ubuntu&logoColor=white)
![VirtualBox](https://img.shields.io/badge/VirtualBox-7.0-183A61?logo=virtualbox&logoColor=white)
![Vagrant](https://img.shields.io/badge/Vagrant-2.x-1563FF?logo=vagrant&logoColor=white)
![CNI](https://img.shields.io/badge/CNI-Flannel_v0.25-009688)
![Course](https://img.shields.io/badge/Curso-Capítulo_1-blue)
![Deliverable](https://img.shields.io/badge/PDF-k8s--installation--steps.pdf-red?logo=adobeacrobatreader)

**Laboratorio Práctico y Guía Oficial:** Despliegue desde cero de un clúster Kubernetes v1.31 multi-nodo sobre Ubuntu 22.04 LTS y VirtualBox 7.0. Acondicionamiento de bajo nivel del sistema operativo, runtime Containerd con cgroups v2 (`SystemdCgroup = true`), red Flannel CNI con enlace forzado a interfaz privada (`enp0s8`), orquestación desatendida mediante Vagrant (IaC), panel gráfico Kubernetes Dashboard v2.7.0 con RBAC, y resolución exhaustiva de fallos reales de producción.

</div>

---

## 🎯 Objetivo Pedagógico

El propósito fundamental de este laboratorio es **desmitificar la arquitectura interna y el aprovisionamiento de Kubernetes en infraestructura propia (Bare-Metal / On-Premise)**.

En entornos gestionados en la nube pública (como Google Kubernetes Engine - GKE, AWS EKS o Azure AKS), los proveedores ocultan por completo los componentes del plano de control (`etcd`, `kube-apiserver`, `kube-controller-manager`, `kube-scheduler`), abstraen la configuración de red CNI y aprovisionan el runtime de contenedores de forma transparente. Aunque este enfoque acelera el desarrollo, crea una notable brecha de conocimiento en ingeniería DevOps y SRE a la hora de depurar incidentes de red, entender los requisitos de cgroups del kernel de Linux o diagnosticar fallos de quórum y certificados TLS.

A través de este proyecto aprenderás:
1. **Topología de Red Dual y Prevención de Colisiones IP:** Cómo gestionar máquinas virtuales con adaptador NAT (acceso a Internet) y adaptador Host-Only / Solo-Anfitrión privado (`192.168.56.0/24`), evitando que el apiserver o el CNI se enlacen por error a la IP colisionada por defecto de VirtualBox (`10.0.2.15`).
2. **Acondicionamiento del Sistema Operativo y del Kernel Linux:** Desactivación estricta de memoria SWAP, carga de módulos de red (`overlay`, `br_netfilter`) y ajuste de parámetros `sysctl` (`net.bridge.bridge-nf-call-iptables`, `net.ipv4.ip_forward`) indispensables para el filtrado de paquetes y el tráfico entre Pods.
3. **Container Runtime Interface (CRI) de Alto Rendimiento:** Instalación y configuración de `containerd` unificado bajo cgroups v2 (`SystemdCgroup = true`), evitando discrepancias críticas de gestión de recursos con `kubelet`.
4. **Adopción del Repositorio Comunitario Moderno:** Migración desde los antiguos repositorios deprecados de Google (`apt.kubernetes.io`) hacia el repositorio oficial moderno comunitario alojado en `pkgs.k8s.io` con llaves GPG blindadas.
5. **Inicialización y Bootstrap del Plano de Control:** Ejecución determinista de `kubeadm init`, parametrización de rangos CIDR sin solapamiento (`10.244.0.0/16`), despliegue de Flannel CNI fijado a la interfaz de red interna (`--iface=enp0s8`) y generación segura de tokens de incorporación.
6. **Incorporación Segura de Nodos Worker:** Procedimiento de unión (`kubeadm join`) con verificación de huella criptográfica SHA-256 del certificado raíz de la CA del clúster.
7. **Conexión Remota No Destructiva desde el Host:** Fusión (*merge*) de credenciales en `~/.kube/config` preservando otros contextos y clústeres preexistentes en la estación de trabajo del ingeniero.
8. **Infraestructura como Código (IaC) con Vagrant:** Automatización integral desatendida mediante scripts modulares (`common.sh`, `master.sh`, `worker.sh`) capaces de levantar el clúster completo y operativo con un único comando: `vagrant up`.
9. **Observabilidad Gráfica y Gestión de Permisos:** Despliegue de Kubernetes Dashboard v2.7.0, provisión de ServiceAccount administrativa con ClusterRoleBinding y acceso seguro a través de `kubectl proxy`.
10. **Validación Práctica de Cargas de Trabajo:** Despliegue de un servicio Nginx con balanceo NodePort y verificación de conectividad HTTP extremo a extremo.

---

## ⚖️ Comparativa Conceptual: Cloud Gestionado vs Kubeadm Bare-Metal

| Dimensión Arquitectónica | Kubernetes Gestionado (GKE / EKS / AKS) | Kubeadm en Bare-Metal / VMs (Este Repositorio) |
| :--- | :--- | :--- |
| **Control Plane (Plano de Control)** | Oculto y gestionado como servicio por el proveedor (SaaS/IaaS) | **100% visible, auditable e instalado nodo a nodo** (`k8s-master`) |
| **Acceso a etcd y Certificados** | Inaccesible; el proveedor gestiona el cifrado y la rotación | **Acceso total a `/etc/kubernetes/pki`** y al almacenamiento Raft de `etcd` |
| **Capa de Red (CNI)** | Plugins propietarios de red VPC (VPC-native, AWS VPC CNI, Azure CNI) | **Flannel CNI** con encapsulación VXLAN y enlace manual a interfaz física/virtual |
| **Container Runtime (CRI)** | Gestionado y fijado en la imagen base de los nodos de trabajo | **Containerd** configurado manualmente con driver systemd para cgroups v2 |
| **Gestión de Cgroup y Kernel** | Abstraído; no requiere interacción a nivel de kernel por el usuario | **Ajuste explícito de módulos `br_netfilter`, `overlay` y `sysctl.conf`** |
| **Almacenamiento Dinámico** | Controladores CSI de almacenamiento en bloque instalados de serie | Requiere aprovisionador dinámico (p. ej., `local-path-provisioner`) o PVs estáticos |
| **Valor Pedagógico y Diagnóstico** | Orientado a consumo y despliegue de aplicaciones | **Dominio profundo de la infraestructura y capacidad de resolución de fallos críticos** |

---

## 🏗️ Topología y Arquitectura del Clúster

El laboratorio recrea una arquitectura de dos nodos sobre VirtualBox 7.0 interconectados por una red interna de alto aislamiento, controlada desde la máquina anfitriona:

```text
+-----------------------------------------------------------------------------------+
|  HOST FÍSICO / ESTACIÓN DE TRABAJO (Ubuntu / Linux con VirtualBox 7.0 instalado)  |
|  IP Red Host-Only: 192.168.56.1                                                   |
|  Gestión: Cliente kubectl instalado en el host apuntando a 192.168.56.10:6443     |
|  Acceso Gráfico: Navegador web -> http://localhost:8001 (vía kubectl proxy)       |
+-----------------------------------------------------------------------------------+
       |                                                    |
       | Red Host-Only (vboxnet0: 192.168.56.0/24)          | Red NAT (Salida a Internet)
       v                                                    v
+--------------------------------------+   +--------------------------------------+
| VM: k8s-master                       |   | VM: k8s-worker1                      |
| Sistema: Ubuntu Server 22.04 LTS     |   | Sistema: Ubuntu Server 22.04 LTS     |
| CPU: 2 vCPUs | RAM: 3072 MB (3 GB)   |   | CPU: 2 vCPUs | RAM: 2048 MB (2 GB)   |
| Disco: 25 GB                         |   | Disco: 20 GB                         |
| Adaptador 1 (NAT): 10.0.2.15         |   | Adaptador 1 (NAT): 10.0.2.15         |
| Adaptador 2 (Host-Only):             |   | Adaptador 2 (Host-Only):             |
|   192.168.56.10 (enp0s8)             |   |   192.168.56.11 (enp0s8)             |
|                                      |   |                                      |
| Roles y Componentes:                 |   | Roles y Componentes:                 |
|   - kube-apiserver (:6443)           |   |   - kubelet                          |
|   - etcd (:2379, :2380)              |   |   - kube-proxy                       |
|   - kube-controller-manager          |   |   - containerd runtime               |
|   - kube-scheduler                   |   |   - Flannel CNI daemonset            |
|   - kubelet & containerd             |   |   - Cargas de usuario (Pods Nginx)   |
|   - Flannel CNI (Subnet 10.244.0.0)  |   |   - Flannel CNI (Subnet 10.244.1.0)  |
|   - Kubernetes Dashboard v2.7.0      |   |                                      |
+--------------------------------------+   +--------------------------------------+
       ^                                                    ^
       +================ Red de Pods (CIDR: 10.244.0.0/16) =+
```

### Matriz de Hardware e Interfaces de Red

| Nodo | Rol | vCPUs | Memoria RAM | Disco | Adaptador 1 (NAT) | Adaptador 2 (Host-Only) | Rango de Pods Asignado |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **`k8s-master`** | Control Plane | 2 | 3072 MB | 25 GB | DHCP (`10.0.2.15`) | Estática: `192.168.56.10/24` | `10.244.0.0/24` |
| **`k8s-worker1`** | Worker Node | 2 | 2048 MB | 20 GB | DHCP (`10.0.2.15`) | Estática: `192.168.56.11/24` | `10.244.1.0/24` |

---

### ⚠️ Alertas Críticas de Arquitectura en Producción

> [!WARNING]
> **1. Selección de Interfaz en Entornos de Red Dual (VirtualBox):**
> Al usar VirtualBox, todas las máquinas virtuales reciben la misma dirección IP por defecto en el adaptador NAT (`10.0.2.15`). Por esta razón, el comando `kubeadm init` debe invocar explícitamente `--apiserver-advertise-address=192.168.56.10` y el daemonset de Flannel debe configurarse obligatoriamente con el argumento `--iface=enp0s8`. Si se omite, los nodos intentarán encaminar el tráfico de pods a través de la IP colisionada y el clúster quedará inoperativo.

> [!WARNING]
> **2. Espacio de Direccionamiento de Pods (CIDR) sin Solapamiento:**
> La red de pods del clúster está configurada como `10.244.0.0/16`. Jamás debe configurarse un CIDR como `192.168.0.0/16` en Flannel cuando la red física o la red Host-Only es `192.168.56.0/24`, ya que generaría un conflicto de enrutamiento en la tabla del kernel que aislaría los pods del apiserver.

> [!WARNING]
> **3. Repositorio Oficial Moderno de Kubernetes (`pkgs.k8s.io`):**
> Los antiguos repositorios de Google en `apt.kubernetes.io` y `packages.cloud.google.com` fueron congelados y dados de baja permanentemente. Se debe utilizar exclusivamente el repositorio comunitario moderno alojado en `https://pkgs.k8s.io/core:/stable:/v1.31/deb/`.

---

## 📁 Estructura del Repositorio

```text
poc-training-k8s-cluster-kubeadm/
├── Vagrantfile                       # Definición IaC de las VMs (k8s-master y k8s-worker1 en VirtualBox)
├── scripts/
│   ├── common.sh                     # Acondicionamiento base del SO, kernel, containerd y paquetes K8s v1.31
│   ├── master.sh                     # Inicialización del Control Plane, Flannel CNI, Dashboard y tokens
│   ├── worker.sh                     # Sincronización y ejecución de la unión (join) del worker al clúster
│   └── generate_html_pdf.py          # Pipeline desatendido de compilación de documentación A4 a PDF
├── docs/
│   ├── k8s-installation-steps.md     # Guía técnica exhaustiva paso a paso (manual, IaC y troubleshooting)
│   ├── k8s-installation-steps.html   # Documento editorial maquetado con estilos CSS para impresión A4
│   └── images/                       # Diagramas, capturas de VirtualBox, Dashboard y evidencias visuales
│       ├── master/                   # Capturas de configuración paso a paso de la VM Master
│       ├── worker/                   # Capturas de configuración paso a paso de la VM Worker
│       ├── k8s_dashboard.png         # Captura de verificación del panel gráfico operativo
│       ├── k8s_dashboard_login.png   # Captura del formulario de autenticación Bearer Token
│       └── step_00.png               # Configuración de la red Host-Only vboxnet0 en VirtualBox
├── openspec/                         # Especificaciones y trazabilidad de cambios del proyecto
│   ├── specs/                        # Capacidades normativas activas del laboratorio
│   └── changes/                      # Historial de cambios y validaciones arquitectónicas
├── k8s-cluster-kubeadm.pdf           # Entregable oficial compilado en PDF de alta fidelidad editorial
└── README.md                         # Presentación ejecutiva y técnica del repositorio
```

---

## 🚀 Vía 1: Despliegue Rápido Automatizado con Vagrant (IaC)

Esta es la vía recomendada para desplegar el laboratorio en cuestión de minutos de manera completamente reproducible y desatendida.

### Requisitos Previos en la Máquina Anfitriona
* **Sistema Operativo:** Linux (Ubuntu 20.04/22.04 recomendado), macOS o Windows con WSL2.
* **Hipervisor:** Oracle VirtualBox 7.0+ instalado.
* **Vagrant:** Versión 2.3+ instalada (`vagrant --version`).
* **Recursos de Hardware Disponibles:** Mínimo 8 GB de RAM física y 4 núcleos de CPU libres.

### 1. Despliegue Desatendido del Clúster
Clona el repositorio y ejecuta el aprovisionamiento automatizado:

```bash
vagrant up
```

Durante el proceso, Vagrant realizará en secuencia:
1. Creación de la red Host-Only privada `192.168.56.0/24` en VirtualBox.
2. Descarga e instanciación de la imagen oficial `ubuntu/jammy64` (Ubuntu 22.04 LTS).
3. Ejecución de [`scripts/common.sh`](file:///home/miguel/git/poc-training-k8s-cluster-kubeadm/scripts/common.sh) en ambos nodos (desactivación de swap, módulos de kernel, containerd con systemd y paquetes de Kubernetes v1.31).
4. Ejecución de [`scripts/master.sh`](file:///home/miguel/git/poc-training-k8s-cluster-kubeadm/scripts/master.sh) en `k8s-master` (`kubeadm init`, Flannel enlazado a `enp0s8`, despliegue del Dashboard v2.7.0, token RBAC y script de unión).
5. Ejecución de [`scripts/worker.sh`](file:///home/miguel/git/poc-training-k8s-cluster-kubeadm/scripts/worker.sh) en `k8s-worker1` (espera sincronizada y ejecución de `join.sh`).

### 2. Verificación del Estado del Clúster
Accede al nodo Master mediante SSH y comprueba el estado de los nodos:

```bash
vagrant ssh k8s-master
kubectl get nodes -o wide
```

**Salida esperada:**
```text
NAME          STATUS   ROLES           AGE     VERSION   INTERNAL-IP     OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
k8s-master    Ready    control-plane   3m20s   v1.31.2   192.168.56.10   Ubuntu 22.04.5 LTS   5.15.0-125-generic  containerd://1.7.23
k8s-worker1   Ready    <none>          1m45s   v1.31.2   192.168.56.11   Ubuntu 22.04.5 LTS   5.15.0-125-generic  containerd://1.7.23
```

Comprueba los pods de sistema en todos los namespaces:
```bash
kubectl get pods -A
```

**Salida esperada:**
```text
NAMESPACE              NAME                                         READY   STATUS    RESTARTS   AGE
kube-system            coredns-7c65d6cfc9-5k8r2                     1/1     Running   0          3m
kube-system            coredns-7c65d6cfc9-w87tl                     1/1     Running   0          3m
kube-system            etcd-k8s-master                              1/1     Running   0          3m
kube-system            kube-apiserver-k8s-master                    1/1     Running   0          3m
kube-system            kube-controller-manager-k8s-master           1/1     Running   0          3m
kube-system            kube-flannel-ds-g74nm                        1/1     Running   0          2m
kube-system            kube-flannel-ds-tbq5v                        1/1     Running   0          1m
kube-system            kube-proxy-8x4km                             1/1     Running   0          3m
kube-system            kube-proxy-m92lx                             1/1     Running   0          1m
kube-system            kube-scheduler-k8s-master                    1/1     Running   0          3m
kubernetes-dashboard   dashboard-metrics-scraper-7bfdf779ff-q5klt   1/1     Running   0          2m
kubernetes-dashboard   kubernetes-dashboard-545d8b76-4j8xz          1/1     Running   0          2m
```

### 3. Conexión Remota No Destructiva desde el Host Anfitrión
Vagrant exporta automáticamente el archivo `kubeconfig` a la carpeta local `./configs/config`. Para gestionar el clúster cómodamente desde la terminal de tu máquina anfitriona sin pisar configuraciones de otros clústeres (como Minikube, Kind o clústeres corporativos):

```bash
# 1. Combinar temporalmente la variable KUBECONFIG
export KUBECONFIG=~/.kube/config:$(pwd)/configs/config

# 2. Volcar la configuración combinada en un archivo limpio
kubectl config view --flatten > /tmp/kubeconfig_merged.yaml
mv /tmp/kubeconfig_merged.yaml ~/.kube/config
chmod 600 ~/.kube/config
unset KUBECONFIG

# 3. Cambiar de contexto al nuevo clúster
kubectl config use-context kubernetes-admin@kubernetes
kubectl get nodes
```

### 4. Gestión del Ciclo de Vida con Vagrant
* **Pausar máquinas virtuales:** `vagrant suspend`
* **Reanudar máquinas virtuales:** `vagrant resume`
* **Apagar el clúster ordenadamente:** `vagrant halt`
* **Destruir el laboratorio por completo:** `vagrant destroy -f && rm -rf configs/`

---

## 🛠️ Vía 2: Despliegue Manual Paso a Paso con Kubeadm

Para comprender en detalle cada comando ejecutado en los scripts automatizados, a continuación se desglosan las fases esenciales del despliegue manual.

### 1. Configuración de la Red Solo-Anfitrión en VirtualBox
1. Abrir VirtualBox -> **Herramientas** -> **Redes**.
2. Crear red `vboxnet0` con IPv4 `192.168.56.1` y máscara `255.255.255.0`.
3. **Desactivar el servidor DHCP** de `vboxnet0` para garantizar que las IPs se asignen de forma estática y determinista por Netplan.

### 2. Configuración de Netplan en cada Nodo
En ambas máquinas virtuales, desactivar el control de red de Cloud-Init y editar `/etc/netplan/00-installer-config.yaml`:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: false
      addresses:
        - 192.168.56.10/24   # Usar .11/24 en k8s-worker1
```
Aplicar cambios: `sudo netplan apply`.

### 3. Acondicionamiento Base del Sistema Operativo
Ejecutar en **ambos nodos** (`k8s-master` y `k8s-worker1`):

```bash
# 1. Resolución de nombres local
sudo tee -a /etc/hosts <<EOF
192.168.56.10 k8s-master
192.168.56.11 k8s-worker1
EOF

# 2. Desactivar memoria SWAP de forma inmediata y permanente
sudo swapoff -a
sudo sed -i '/swap/s/^/#/' /etc/fstab

# 3. Cargar módulos de kernel requeridos
sudo tee /etc/modules-load.d/k8s.conf <<EOF
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter

# 4. Parámetros sysctl de red
sudo tee /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system
```

### 4. Instalación de Containerd con SystemdCgroup
Ejecutar en **ambos nodos**:

```bash
sudo apt-get update
sudo apt-get install -y containerd conntrack socat

sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd
```

### 5. Instalación de Kubernetes v1.31 desde `pkgs.k8s.io`
Ejecutar en **ambos nodos**:

```bash
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

### 6. Inicialización del Plano de Control (Solo en `k8s-master`)
```bash
sudo kubeadm init \
  --apiserver-advertise-address=192.168.56.10 \
  --pod-network-cidr=10.244.0.0/16 \
  --node-name k8s-master

# Configurar kubeconfig para el usuario actual
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### 7. Despliegue de Flannel CNI fijado a `enp0s8` (Solo en `k8s-master`)
```bash
curl -sSL https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml -o /tmp/kube-flannel.yml
sed -i 's/- --kube-subnet-mgr/- --kube-subnet-mgr\n        - --iface=enp0s8/' /tmp/kube-flannel.yml
kubectl apply -f /tmp/kube-flannel.yml
```

### 8. Incorporación del Worker (Solo en `k8s-worker1`)
En el nodo Master, genera el comando de unión:
```bash
kubeadm token create --print-join-command
```

Ejecuta el comando resultante en `k8s-worker1` con `sudo`:
```bash
sudo kubeadm join 192.168.56.10:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

---

## 🖥️ Kubernetes Dashboard y Validación de Cargas

El repositorio incluye el despliegue automático del panel oficial de control gráfico de Kubernetes.

### Acceso Administrativo al Dashboard
1. **Obtener el token Bearer:**
   Si usaste Vagrant, el token se encuentra en `./configs/dashboard-token.txt`.
   Si realizaste la instalación manual, genera un token con:
   ```bash
   kubectl -n kubernetes-dashboard create token admin-user
   ```

2. **Abrir el túnel seguro mediante `kubectl proxy`:**
   En tu máquina anfitriona (con `kubectl` configurado):
   ```bash
   kubectl proxy
   ```

3. **Acceder a la interfaz web:**
   Abre tu navegador en la URL oficial de proxy:
   ```text
   http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
   ```
   Selecciona la opción **Token**, pega el token generado y accede a la vista global de salud del clúster, pods, nodos y eventos en tiempo real.

---

### Despliegue de Prueba: Nginx con Servicio NodePort

Para certificar que la comunicación inter-nodo, el enrutamiento de red de Flannel y la traducción de direcciones de `kube-proxy` funcionan correctamente, desplegamos una carga de trabajo real:

```bash
# 1. Crear deployment de Nginx con 2 réplicas
kubectl create deployment nginx-demo --image=nginx:alpine --replicas=2

# 2. Exponer el deployment a través de un servicio NodePort en el puerto 30080
kubectl create service nodeport nginx-demo --tcp=80:80 --node-port=30080

# 3. Comprobar distribución de pods en los nodos
kubectl get pods -o wide -l app=nginx-demo
```

**Verificación de Conectividad HTTP Externa:**
Desde tu máquina anfitriona (o desde cualquier nodo del clúster), realiza peticiones HTTP a la IP del Worker o del Master en el puerto 30080:

```bash
curl -I http://192.168.56.11:30080
```

**Salida esperada:**
```text
HTTP/1.1 200 OK
Server: nginx/1.27.x
Content-Type: text/html
Connection: keep-alive
```

---

## 💥 Diagnóstico y Resolución de Problemas Frecuentes (Troubleshooting)

A continuación se documentan los 5 incidentes reales más frecuentes al desplegar Kubernetes con Kubeadm en entornos virtuales, su causa raíz y la solución definitiva:

```
+---------------------------------------------------------------------------------------------------+
|                           MATRIZ DE TROUBLESHOOTING EN KUBEADM BARE-METAL                         |
+------------------------------+-------------------------------------+------------------------------+
| Síntoma / Error              | Causa Raíz                          | Solución Definitiva          |
+------------------------------+-------------------------------------+------------------------------+
| Error 1: Conexión rechazada  | kubeadm init escuchando en la IP    | Pasar explícitamente:        |
| al apiserver en 10.0.2.15    | NAT por omisión de advertise-address| --apiserver-advertise-address|
+------------------------------+-------------------------------------+------------------------------+
| Error 2: CoreDNS atascado en | Falta de CNI o Flannel intentando   | Parchear DaemonSet con:      |
| Pending o ContainerCreating  | usar enp0s3 (NAT) en vez de enp0s8  | - --iface=enp0s8             |
+------------------------------+-------------------------------------+------------------------------+
| Error 3: Kubelet falla con   | Containerd usando cgroupfs en lugar | Configurar en config.toml:   |
| cgroup driver mismatch       | del cgroup driver unificado systemd | SystemdCgroup = true         |
+------------------------------+-------------------------------------+------------------------------+
| Error 4: Worker no conecta   | Sin resolución DNS local de nombre  | Mapear /etc/hosts y activar  |
| con k8s-master:6443          | o modo promiscuo apagado en vbox    | --nicpromisc2 allow-all      |
+------------------------------+-------------------------------------+------------------------------+
| Error 5: Desalojo de Pods    | Instalación por defecto de Ubuntu   | Ejecutar:                    |
| (Evicted) por DiskPressure   | asigna solo 10GB al volumen LVM     | lvextend -l +100%FREE ...    |
+------------------------------+-------------------------------------+------------------------------+
```

### 1. Error 1: `The connection to the server 10.0.2.15:6443 was refused`
* **Síntoma:** Tras ejecutar `kubeadm init`, cualquier comando `kubectl` falla con error de conexión rechazada hacia `10.0.2.15:6443`.
* **Causa Raíz:** Al contar con múltiples adaptadores, `kubeadm` tomó como ruta por defecto la interfaz NAT de VirtualBox (`enp0s3`).
* **Solución Definitiva:** Inicializar siempre con el parámetro explícito `--apiserver-advertise-address=192.168.56.10`.

### 2. Error 2: `CoreDNS se queda indefinidamente en estado ContainerCreating o Pending`
* **Síntoma:** Los dos pods de CoreDNS no alcanzan el estado `Running` tras varios minutos de inicializar el Master.
* **Causa Raíz:** Kubernetes no programa pods de red hasta que no existe un CNI operativo instalado. Si Flannel se instaló sin especificar la interfaz, intentará enlazarse a la interfaz NAT colisionada `enp0s3`.
* **Solución Definitiva:** Aplicar el manifiesto de Flannel modificando sus argumentos para incluir `- --iface=enp0s8`.

### 3. Error 3: `kubelet fails with cgroup driver mismatch`
* **Síntoma:** El servicio `kubelet` se detiene y falla al arrancar (`code=exited, status=1/FAILURE`).
* **Causa Raíz:** `kubelet` en Kubernetes v1.31 utiliza `systemd` como cgroup driver por defecto. Si Containerd genera la configuración predeterminada sin modificar, utiliza `cgroupfs` (`SystemdCgroup = false`).
* **Solución Definitiva:** Asegurarse de sustituir `SystemdCgroup = false` por `SystemdCgroup = true` en `/etc/containerd/config.toml` y reiniciar containerd (`sudo systemctl restart containerd`).

### 4. Error 4: `Worker node cannot connect to master:6443`
* **Síntoma:** Al ejecutar `kubeadm join`, el comando se bloquea en `[check-etcd] Checking that the etcd cluster is healthy` o devuelve `context deadline exceeded`.
* **Causa Raíz:** El nodo worker no puede resolver el hostname `k8s-master` o los paquetes de red Host-Only están siendo bloqueados por no tener activado el modo promiscuo en el adaptador de red de VirtualBox.
* **Solución Definitiva:** Añadir las entradas de IP/hostname en `/etc/hosts` de cada máquina y configurar `modifyvm :id --nicpromisc2 allow-all` en el archivo [`Vagrantfile`](file:///home/miguel/git/poc-training-k8s-cluster-kubeadm/Vagrantfile).

### 5. Error 5: Desalojo de Pods (`Evicted`) por `DiskPressure`
* **Síntoma:** Los pods entran en estado `Evicted` poco después de arrancar con eventos de advertencia de `The node was low on resource: ephemeral-storage`.
* **Causa Raíz:** El instalador de Ubuntu Server con LVM configura por defecto solo la mitad del disco virtual (10 GB de un disco de 25 GB), superando el umbral de desalojo por presión de disco del 85% de `kubelet`.
* **Solución Definitiva:** Expandir el volumen lógico para aprovechar el 100% del disco físico disponible:
  ```bash
  sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
  sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
  ```

---

## 📄 Compilación de la Guía PDF y Documentación Editorial

El entregable oficial de este laboratorio, [`k8s-cluster-kubeadm.pdf`](file:///home/miguel/git/poc-training-k8s-cluster-kubeadm/k8s-cluster-kubeadm.pdf), se encuentra precompilado en la raíz del repositorio.

Este documento técnico de alta fidelidad editorial (con maquetación A4, tipografía Inter y JetBrains Mono, numeración de páginas, reglas `@page` y árbol navegable de marcadores PDF) puede regenerarse automáticamente mediante el pipeline de Python incluido en el proyecto:

```bash
# Ejecutar el compilador automatizado de Markdown a PDF
python3 scripts/generate_html_pdf.py
```

* **Pipeline Interno:**
  1. Parsea el archivo fuente [`docs/k8s-installation-steps.md`](file:///home/miguel/git/poc-training-k8s-cluster-kubeadm/docs/k8s-installation-steps.md) a HTML estructurado.
  2. Inyecta la hoja de estilos CSS optimizada para impresión y resolución de imágenes en [`docs/k8s-installation-steps.html`](file:///home/miguel/git/poc-training-k8s-cluster-kubeadm/docs/k8s-installation-steps.html).
  3. Renderiza e imprime en formato PDF mediante Google Chrome / Chromium en modo headless.
  4. Analiza la jerarquía de encabezados (`H1`, `H2`, `H3`) mediante `pypdf` para incrustar el árbol completo de marcadores de navegación en el panel lateral del visor PDF.

---

<div align="center">

**Curso de Kubernetes · Capítulo 1: Despliegue de Infraestructura Productiva**  
*Diseñado con rigor pedagógico y excelencia técnica para entornos de formación en Arquitectura Cloud Native.*

</div>
