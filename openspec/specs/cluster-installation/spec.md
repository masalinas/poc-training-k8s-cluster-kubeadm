# cluster-installation Specification

## Purpose

Define los requisitos funcionales, configuraciones de entorno y pasos de verificación para desplegar un cluster de Kubernetes de dos nodos utilizando kubeadm, containerd y Ubuntu Server 22.04 sobre VirtualBox.

## Requirements

### Requirement: Aprovisionamiento y Red de Máquinas Virtuales
The system SHALL document the minimum hardware requirements and dual network topology (NAT and Host-Only) for both the master and worker virtual machines, providing step-by-step visual guidance with screenshots and explanatory captions for VirtualBox network setup and node provisioning.

#### Scenario: Configuración de hardware y red de nodos
- **WHEN** el alumno provisiona las VMs en VirtualBox 7.0
- **THEN** la VM k8s-master dispone de al menos 2 vCPUs y 3 GB RAM, la VM k8s-worker1 dispone de al menos 2 vCPUs y 2 GB RAM, y ambas poseen un adaptador NAT y un adaptador Host-Only con direccionamiento estático en 192.168.56.0/24 sin solapamiento de MACs.

#### Scenario: Guía visual para la creación de red virtual sólo-anfitrión
- **WHEN** el alumno consulta el procedimiento de configuración de red en la sección 2.2
- **THEN** la documentación incluye la captura `step_00.png` ilustrando la creación de la red `vboxnet0` en la interfaz de VirtualBox junto con su explicación detallada.

#### Scenario: Guía visual paso a paso para la creación de VM master
- **WHEN** el alumno crea y configura la máquina virtual `k8s-master`
- **THEN** la sección 2.2 presenta ordenadamente las 20 capturas secuenciales (`step_01.png` a `step_20.png`) alojadas en `docs/images/master/` detallando hardware, adaptadores de red y cada pantalla del instalador de Ubuntu Server con notas explicativas al pie.

#### Scenario: Guía visual paso a paso para la creación de VM worker
- **WHEN** el alumno crea y configura la máquina virtual `k8s-worker1`
- **THEN** la sección 2.2 presenta ordenadamente las 20 capturas secuenciales (`step_01.png` a `step_20.png`) alojadas en `docs/images/worker/` detallando hardware, adaptadores de red y cada pantalla del instalador de Ubuntu Server con notas explicativas al pie.

### Requirement: Preparación del Sistema Operativo y Dependencias Base
The system SHALL specify permanent swap disabling, network kernel module loading, and sysctl parameter configuration on all cluster nodes.

#### Scenario: Verificación de configuración del host
- **WHEN** se ejecutan las comprobaciones previas en cualquier nodo
- **THEN** el comando `swapon --show` devuelve vacío, los módulos `overlay` y `br_netfilter` están cargados, y `net.ipv4.ip_forward` es igual a 1.

### Requirement: Configuración de Runtime Containerd y Repositorios Kubernetes
The system SHALL detail containerd installation with SystemdCgroup support and installation of kubeadm, kubelet, and kubectl from the pkgs.k8s.io repository.

#### Scenario: Validación de containerd y kubeadm
- **WHEN** se verifica el estado de containerd y kubeadm
- **THEN** containerd se ejecuta con `SystemdCgroup = true` y los paquetes kubelet, kubeadm y kubectl corresponden a la versión 1.31 fijados con apt-mark hold.

### Requirement: Inicialización del Plano de Control y Despliegue de CNI
The system SHALL detail cluster initialization with kubeadm init binding to the Host-Only IP, setting pod CIDR, and applying Flannel CNI configured for that interface.

#### Scenario: Cluster master listo
- **WHEN** se completa kubeadm init y se aplica el manifiesto CNI Flannel
- **THEN** el nodo k8s-master alcanza el estado Ready y el comando `kubectl get nodes` reporta el nodo como maestro operativo.

### Requirement: Incorporación del Nodo Worker y Configuración de Kubectl Remoto
The system SHALL detail worker node join procedure with cluster tokens and export of kubeconfig credentials for remote management from the physical host.

#### Scenario: Cluster completo y gestión remota
- **WHEN** el worker ejecuta kubeadm join y el host copia el archivo kubeconfig
- **THEN** `kubectl get nodes` ejecutado desde el host Ubuntu 20.04 muestra ambos nodos k8s-master y k8s-worker1 en estado Ready.

### Requirement: Despliegue y Acceso al Dashboard de Kubernetes
The system SHALL guide Kubernetes Dashboard deployment, pod health verification, administrative service account creation with cluster-admin binding, token generation (both time-limited and permanent via Secret with security warnings), secure proxy access, and visual verification with interface screenshots.

#### Scenario: Despliegue y verificación de componentes del Dashboard
- **WHEN** el alumno aplica el manifiesto oficial del Dashboard con `kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml`
- **THEN** la guía detalla la creación de todos los recursos y verifica mediante `kubectl get pods -n kubernetes-dashboard` que los pods `kubernetes-dashboard` y `dashboard-metrics-scraper` están en estado Running.

#### Scenario: Creación y verificación de cuenta administrativa RBAC
- **WHEN** el alumno crea y aplica el manifiesto `dashboard-adminuser.yaml` vinculando la cuenta `admin-user` al rol `cluster-admin`
- **THEN** la guía confirma la creación del ServiceAccount y ClusterRoleBinding, y valida su existencia mediante `kubectl get serviceaccount admin-user -n kubernetes-dashboard`.

#### Scenario: Acceso web al Dashboard
- **WHEN** el alumno genera el token de autenticación con `kubectl -n kubernetes-dashboard create token admin-user`, ejecuta `kubectl proxy` y navega a la URL del proxy
- **THEN** la guía documenta el acceso por token, ilustra la pantalla de autenticación con `k8s_dashboard_login.png` y muestra la interfaz gráfica interna con los recursos del namespace mediante `k8s_dashboard.png`.

#### Scenario: Generación de token permanente no expirable mediante Secret
- **WHEN** el alumno crea el manifiesto `admin-user-secret.yaml` de tipo `kubernetes.io/service-account-token` vinculado a `admin-user`, lo aplica y extrae el token decodificado en Base64
- **THEN** la guía documenta la obtención de un token persistente sin expiración para pruebas locales y laboratorios, e incorpora una advertencia de seguridad explícita desaconsejando esta práctica en entornos productivos.

### Requirement: Diagnóstico y Resolución de Presión de Disco LVM
The system SHALL document troubleshooting procedures for pod eviction caused by DiskPressure and insufficient ephemeral-storage due to Ubuntu Server's default LVM allocation, providing diagnostic commands and on-line volume expansion steps for both control plane and worker nodes.

#### Scenario: Diagnóstico de desalojo de Pods por DiskPressure
- **WHEN** un alumno experimenta pods en estado Failed o Evicted debido al umbral de ephemeral-storage
- **THEN** la guía detalla el análisis del mensaje de error del kubelet y proporciona los comandos `df -h /` y `lsblk` para confirmar la disparidad entre el tamaño del disco físico y el Logical Volume raíz montado en `/`.

#### Scenario: Expansión en caliente de volumen LVM y sistema de archivos
- **WHEN** el alumno ejecuta la ampliación de espacio en el nodo worker o master
- **THEN** la guía documenta la ejecución de `sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv` seguido de `sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv` y valida que el sistema de archivos raíz refleje el total del espacio asignado al disco virtual.

#### Scenario: Limpieza de pods fallidos por desalojo
- **WHEN** el alumno subsana el problema de espacio y requiere depurar el estado del cluster
- **THEN** la guía especifica el comando `kubectl delete pods --field-selector=status.phase=Failed` en el namespace afectado para restablecer los pods limpios y operativos.
