# Guía de Instalación de Kubernetes en Producción
## Simulación de Entorno Productivo con Ubuntu 22.04, VirtualBox 7.0, Kubeadm y Vagrant

**Autor:** Equipo Docente de Kubernetes  
**Documento Oficial del Curso:** Capítulo 1 - Despliegue de Infraestructura  
**Entregable:** `k8s-cluster-kubeadm.pdf`

---

## Tabla de Contenidos

1. [Arquitectura del Laboratorio](#1-arquitectura-del-laboratorio)
   - [1.1 Diagrama de Topología](#11-diagrama-de-topología)
   - [1.2 Matriz de Hardware e IP](#12-matriz-de-hardware-e-ip)
   - [1.3 Alertas Críticas de Producción](#13-alertas-críticas-de-producción)
2. [Sección 1: Despliegue Manual Paso a Paso con Kubeadm](#2-sección-1-despliegue-manual-paso-a-paso-con-kubeadm)
   - [2.1 Creación de la Red Solo-Anfitrión en VirtualBox (`vboxnet0`)](#21-creación-de-la-red-solo-anfitrión-en-virtualbox-vboxnet0)
   - [2.2 Creación y Configuración de VMs en VirtualBox 7.0](#22-creación-y-configuración-de-vms-en-virtualbox-70)
     * [2.2.1 Creación de la Red Solo-Anfitrión (`step_00.png`)](#221-creación-de-la-red-solo-anfitrión-en-virtualbox-step_00png)
     * [2.2.2 Guía Paso a Paso para la VM Master (`k8s-master`)](#222-asistente-visual-paso-a-paso-para-la-creación-de-la-vm-master-k8s-master)
     * [2.2.3 Guía Paso a Paso para la VM Worker (`k8s-worker1`)](#223-asistente-visual-paso-a-paso-para-la-creación-de-la-vm-worker-k8s-worker1)
   - [2.3 Configuración de Idioma y Teclado Español](#23-configuración-de-idioma-y-teclado-español)
   - [2.4 Persistencia de Red: Bloqueo de Cloud-Init y Netplan Estático](#24-persistencia-de-red-bloqueo-de-cloud-init-y-netplan-estático)
   - [2.5 Preparación Base del Sistema Operativo (SWAP, Kernel y Sysctl)](#25-preparación-base-del-sistema-operativo-swap-kernel-y-sysctl)
   - [2.6 Instalación de Containerd y Dependencias del Sistema (`conntrack`, `socat`)](#26-instalación-de-containerd-y-dependencias-del-sistema-conntrack-socat)
   - [2.7 Instalación de Herramientas Kubernetes (v1.31 en pkgs.k8s.io)](#27-instalación-de-herramientas-kubernetes-v131-en-pkgsk8sio)
   - [2.8 Inicialización del Plano de Control (Master), Flannel CNI y Registros Reales](#28-inicialización-del-plano-de-control-master-flannel-cni-y-registros-reales)
   - [2.9 Unión del Nodo Worker al Cluster con Dependencias y Registros Reales](#29-unión-del-nodo-worker-al-cluster-con-dependencias-y-registros-reales)
   - [2.10 Conexión Remota No Destructiva desde el Host Anfitrión (Merge Kubeconfig)](#210-conexión-remota-no-destructiva-desde-el-host-anfitrión-merge-kubeconfig)
3. [Sección 2: Automatización Completa con Vagrant (IaC)](#3-sección-2-automatización-completa-con-vagrant-iac)
   - [3.1 Introducción a Vagrant para Kubernetes](#31-introducción-a-vagrant-para-kubernetes)
   - [3.2 Estructura del Proyecto de Automatización](#32-estructura-del-proyecto-de-automatización)
   - [3.3 El Archivo `Vagrantfile` Multi-Máquina](#33-el-archivo-vagrantfile-multi-máquina)
   - [3.4 Scripts Shell de Aprovisionamiento Modular](#34-scripts-shell-de-aprovisionamiento-modular)
   - [3.5 Despliegue Desatendido con `vagrant up`](#35-despliegue-desatendido-con-vagrant-up)
   - [3.6 Gestión del Ciclo de Vida del Cluster](#36-gestión-del-ciclo-de-vida-del-cluster)
4. [Sección 3: Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard](#4-sección-3-instalación-acceso-y-verificación-gráfica-del-kubernetes-dashboard)
   - [4.1 Despliegue de los Componentes Oficiales del Dashboard](#41-despliegue-de-los-componentes-oficiales-del-dashboard)
   - [4.2 Verificación del Estado de los Pods del Dashboard](#42-verificación-del-estado-de-los-pods-del-dashboard)
   - [4.3 Creación de Cuenta de Servicio y Privilegios Administrativos (RBAC)](#43-creación-de-cuenta-de-servicio-y-privilegios-administrativos-rbac)
   - [4.4 Comprobación de la Cuenta de Servicio Creada](#44-comprobación-de-la-cuenta-de-servicio-creada)
   - [4.5 Generación del Token de Autenticación Bearer](#45-generación-del-token-de-autenticación-bearer)
   - [4.6 Acceso Seguro mediante Kubectl Proxy](#46-acceso-seguro-mediante-kubectl-proxy)
   - [4.7 Inicio de Sesión y Verificación Visual del Panel](#47-inicio-de-sesión-y-verificación-visual-del-panel)
5. [Sección 4: Ejemplo Práctico de Despliegue en el Cluster (Nginx)](#5-sección-4-ejemplo-práctico-de-despliegue-en-el-cluster-nginx)
   - [5.1 Creación del Deployment de Nginx](#51-creación-del-deployment-de-nginx)
   - [5.2 Inspección Detallada de Recursos del Cluster](#52-inspección-detallada-de-recursos-del-cluster)
   - [5.3 Exposición Externa mediante Servicio NodePort](#53-exposición-externa-mediante-servicio-nodeport)
   - [5.4 Verificación de Conectividad HTTP y Acceso Externo](#54-verificación-de-conectividad-http-y-acceso-externo)
   - [5.5 Acceso Temporal mediante Port-Forward y Limpieza de Recursos](#55-acceso-temporal-mediante-port-forward-y-limpieza-de-recursos)
6. [Resolución de Problemas Frecuentes (Troubleshooting)](#6-resolución-de-problemas-frecuentes-troubleshooting)
   - [6.1 Error 1: Conexión Rechazada al Apiserver](#error-1-the-connection-to-the-server-1002156443-was-refused)
   - [6.2 Error 2: CoreDNS en Estado ContainerCreating o Pending](#error-2-coredns-se-queda-indefinidamente-en-estado-containercreating-o-pending)
   - [6.3 Error 3: Discrepancia en Cgroup Driver de Containerd](#error-3-kubelet-fails-with-cgroup-driver-mismatch)
   - [6.4 Error 4: Worker Node no Conecta al Master:6443](#error-4-worker-node-not-found-or-cannot-connect-to-master6443)
   - [6.5 Error 5: Desalojo de Pods (Evicted) por DiskPressure y Particionamiento LVM](#error-5-desalojo-de-pods-evicted-por-diskpressure-y-particionamiento-lvm-por-defecto)

---

## 1. Arquitectura del Laboratorio

### 1.1 Diagrama de Topología

```text
+-----------------------------------------------------------------------------------+
|  HOST FÍSICO: Ubuntu 20.04 LTS (con VirtualBox 7.0 instalado)                     |
|  IP Red Host-Only: 192.168.56.1                                                   |
|  Gestión: Cliente kubectl instalado en el host apuntando a 192.168.56.10:6443     |
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
|   192.168.56.10                      |   |   192.168.56.11                      |
| Roles: Control Plane                 |   | Roles: Worker Node                   |
|   - kube-apiserver, etcd, scheduler  |   |   - kubelet, kube-proxy              |
|   - controller-manager, kubelet      |   |   - containerd                       |
|   - containerd, Flannel CNI          |   |   - Flannel CNI                      |
|   - Kubernetes Dashboard             |   |                                      |
+--------------------------------------+   +--------------------------------------+
       ^                                                    ^
       +================ Red de Pods (CIDR: 10.244.0.0/16) =+
```

### 1.2 Matriz de Hardware e IP

| Máquina | Rol | vCPU | RAM | Disco | Adaptador 1 (NAT) | Adaptador 2 (Host-Only) |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **k8s-master** | Control Plane | 2 | 3072 MB | 25 GB | DHCP (`10.0.2.15`) | Estática: `192.168.56.10/24` |
| **k8s-worker1** | Worker | 2 | 2048 MB | 20 GB | DHCP (`10.0.2.15`) | Estática: `192.168.56.11/24` |

---

### 1.3 Alertas Críticas de Producción

> [!WARNING]
> **1. Selección de Interfaz en Entornos de Red Dual (VirtualBox):**
> Dado que ambas máquinas virtuales comparten la misma dirección IP en el adaptador NAT (`10.0.2.15`), el plugin de red CNI (Flannel) y el `apiserver` deben configurarse de manera obligatoria para enlazarse a la interfaz del adaptador Host-Only (`enp0s8` / `192.168.56.x`). Si esto se omite, los nodos intentarán comunicarse entre sí usando la IP NAT colisionada y el cluster no alcanzará el estado operativo.

> [!WARNING]
> **2. Espacio de Direccionamiento de Pods (CIDR) sin Solapamiento:**
> La red de pods se establece en `10.244.0.0/16`. No debe utilizarse `192.168.0.0/16` si la red Host-Only es `192.168.56.0/24`, ya que generaría un conflicto de enrutamiento que aislaría el tráfico de red interno.

> [!WARNING]
> **3. Repositorio Oficial Moderno de Kubernetes (`pkgs.k8s.io`):**
> Los antiguos repositorios de Google en `apt.kubernetes.io` y `packages.cloud.google.com` fueron congelados y retirados definitivamente en 2024. Se debe utilizar exclusivamente el repositorio comunitario moderno alojado en `https://pkgs.k8s.io/core:/stable:/v1.31/deb/`.

---

## 2. Sección 1: Despliegue Manual Paso a Paso con Kubeadm

En esta primera sección, los alumnos realizarán la configuración manual completa de cada capa para asimilar en profundidad la arquitectura interna de un cluster de Kubernetes productivo.

---

### 2.1 Creación de la Red Solo-Anfitrión en VirtualBox (`vboxnet0`)

Antes de crear o iniciar las máquinas virtuales, es indispensable aprovisionar la red privada aislada (Host-Only) en VirtualBox que interconectará el nodo de control, el worker y la máquina anfitriona.

#### Procedimiento en VirtualBox:
1. En la ventana principal de VirtualBox, accede al menú superior: **Archivo -> Herramientas -> Administrador de red de host** (o pestaña lateral **Herramientas -> Redes**).
2. Haz clic en el botón **+** (**Crear**) para generar una nueva red sólo-anfitrión. Por defecto se creará con el nombre **`vboxnet0`**.
3. Selecciona `vboxnet0` y configura sus parámetros en la pestaña *Adaptador*:
   * **Dirección IPv4:** `192.168.56.1`
   * **Máscara de red IPv4:** `255.255.255.0` (`/24`)
4. En la pestaña *Servidor DHCP*:
   * Puedes dejar desmarcada la opción *Habilitar servidor* (recomendado), ya que asignaremos direccionamiento estático persistente mediante Netplan en cada máquina virtual.
5. Haz clic en **Aplicar**.

---

### 2.2 Creación y Configuración de VMs en VirtualBox 7.0

Se utilizará la edición para servidores de Ubuntu para maximizar el rendimiento y prescindir de servicios gráficos innecesarios:

* **Distribución:** Ubuntu Server 22.04.5 LTS (Jammy Jellyfish - 64 bits)
* **Enlace de descarga oficial:**
  ```text
  https://releases.ubuntu.com/22.04/ubuntu-22.04.5-live-server-amd64.iso
  ```

Crea dos máquinas virtuales en la interfaz gráfica de VirtualBox con las siguientes especificaciones:

#### Especificaciones para `k8s-master`:
1. **Nombre:** `k8s-master` | **Tipo:** Linux | **Versión:** Ubuntu (64-bit)
2. **Procesador:** Asignar **2 vCPUs** (mínimo estricto requerido por `kubeadm`).
3. **Memoria Base:** Asignar **3072 MB** (3 GB).
4. **Disco Duro:** Crear disco virtual VDI de **25 GB** (reservado dinámicamente).

#### Especificaciones para `k8s-worker1`:
1. **Nombre:** `k8s-worker1` | **Tipo:** Linux | **Versión:** Ubuntu (64-bit)
2. **Procesador:** Asignar **2 vCPUs**.
3. **Memoria Base:** Asignar **2048 MB** (2 GB).
4. **Disco Duro:** Crear disco virtual VDI de **20 GB** (reservado dinámicamente).

#### Configuración de Adaptadores de Red (Aplicar a Ambas VMs):
1. **Adaptador 1:**
   * Marcar: *Habilitar adaptador de red*
   * Conectado a: **NAT** (utilizado para salida a Internet y descarga de paquetes).
2. **Adaptador 2:**
   * Marcar: *Habilitar adaptador de red*
   * Conectado a: **Adaptador sólo-anfitrión (Host-Only)**
   * Nombre: **`vboxnet0`** (la red creada en el paso 2.1 con rango `192.168.56.0/24`)
   * Desplegar *Avanzadas* y establecer **Modo promiscuo:** **Permitir todo** (*Allow All*).

> [!IMPORTANT]
> **Si clonas la máquina master para crear el worker:** En la ventana de clonación, selecciona obligatoriamente la opción **"Generar nuevas direcciones MAC para todos los adaptadores de red"**. De lo contrario, ambas VMs tendrán interfaces de red idénticas y la comunicación fallará.

---

#### 2.2.1 Creación de la Red Solo-Anfitrión en VirtualBox (`step_00.png`)

Antes de crear las máquinas virtuales, es indispensable aprovisionar la red privada aislada que interconectará los nodos. En la consola principal de VirtualBox accedemos al menú lateral **Herramientas -> Redes** y pulsamos en el botón **+** (**Crear**) para generar la red sólo-anfitrión `vboxnet0` con direccionamiento estático `192.168.56.1/24` y el servidor DHCP deshabilitado:

![Creación de la red sólo-anfitrión en VirtualBox](images/step_00.png)
*Figura 2.1: Panel de administración de redes de VirtualBox mostrando la creación de la red sólo-anfitrión vboxnet0.*

---

#### 2.2.2 Asistente Visual Paso a Paso para la Creación de la VM Master (`k8s-master`)

A continuación se ilustran ordenadamente los 20 pasos para la creación de la máquina virtual del plano de control (`k8s-master`) y la instalación guiada de Ubuntu Server 22.04.5 LTS:

##### Paso 1: Nombre, Carpeta de Destino e Imagen ISO
Seleccionamos el nombre descriptivo `k8s-master`, la carpeta de almacenamiento de las VMs y la imagen ISO descargada de Ubuntu Server, marcando la opción de omitir instalación desatendida:
![Paso 1 Master: Nombre y sistema operativo](images/master/step_01.png)
*Figura 2.2: Selección de nombre (k8s-master), tipo Linux (Ubuntu 64-bit) y montaje de la imagen ISO.*

##### Paso 2: Configuración de Instalación Desatendida
Confirmamos los datos del usuario predeterminado o la omisión del instalador desatendido en el asistente:
![Paso 2 Master: Instalación desatendida](images/master/step_02.png)
*Figura 2.3: Ventana de confirmación de instalación del sistema operativo invitado.*

##### Paso 3: Asignación de Recursos de Hardware (RAM y vCPUs)
Asignamos 3072 MB (3 GB) de memoria RAM y 2 vCPUs para garantizar la estabilidad del plano de control exigida por kubeadm:
![Paso 3 Master: Hardware de la máquina virtual](images/master/step_03.png)
*Figura 2.4: Asignación de 3072 MB de RAM y 2 procesadores virtuales vCPUs.*

##### Paso 4: Creación del Disco Duro Virtual VDI
Creamos un disco duro virtual en formato VDI de 25.00 GB con reserva dinámica de espacio:
![Paso 4 Master: Disco duro virtual](images/master/step_04.png)
*Figura 2.5: Creación del disco virtual VDI reservado dinámicamente de 25 GB.*

##### Paso 5: Resumen de Parámetros y Configuración de Red
Revisamos las propiedades de la VM y configuramos las dos interfaces: Adaptador 1 en NAT y Adaptador 2 en `vboxnet0` con modo promiscuo en *Permitir todo*:
![Paso 5 Master: Configuración de red y resumen](images/master/step_05.png)
*Figura 2.6: Ajuste de los adaptadores de red (NAT y vboxnet0 modo promiscuo).*

##### Paso 6: Arranque del Instalador y Selección de Idioma
Iniciamos la máquina virtual e indicamos el idioma predeterminado del instalador de Ubuntu Server:
![Paso 6 Master: Selección de idioma](images/master/step_06.png)
*Figura 2.7: Menú inicial del instalador de Ubuntu Server para la selección de idioma.*

##### Paso 7: Actualización del Asistente Subiquity
Si el asistente detecta una nueva versión del instalador, seleccionamos *Continue without updating* para ceñirnos a la versión estable:
![Paso 7 Master: Actualización del instalador](images/master/step_07.png)
*Figura 2.8: Notificación de actualización del asistente de instalación subiquity.*

##### Paso 8: Configuración de la Distribución del Teclado
Establecemos la disposición del teclado adecuada al teclado físico del usuario:
![Paso 8 Master: Distribución del teclado](images/master/step_08.png)
*Figura 2.9: Configuración de la distribución del teclado en el asistente de instalación.*

##### Paso 9: Selección de la Base de Instalación
Elegimos la opción *Ubuntu Server* estándar, garantizando una instalación minimalista sin entornos de escritorio:
![Paso 9 Master: Base de instalación](images/master/step_09.png)
*Figura 2.10: Selección del paquete base de Ubuntu Server.*

##### Paso 10: Detección de Interfaces de Red
El instalador detecta las dos tarjetas de red (`enp0s3` y `enp0s8`), configurándolas temporalmente por DHCP:
![Paso 10 Master: Interfaces de red detectadas](images/master/step_10.png)
*Figura 2.11: Detección de las interfaces de red primaria (NAT) y secundaria (Host-Only).*

##### Paso 11: Configuración de Proxy HTTP
Al disponer de acceso directo a la red, dejamos en blanco el campo de proxy HTTP:
![Paso 11 Master: Configuración de proxy](images/master/step_11.png)
*Figura 2.12: Pantalla de proxy HTTP dejada en blanco.*

##### Paso 12: Servidor Espejo de Archivos (Ubuntu Archive Mirror)
Confirmamos la URL del repositorio oficial de paquetes de Ubuntu y validamos su respuesta:
![Paso 12 Master: Espejo de paquetes de Ubuntu](images/master/step_12.png)
*Figura 2.13: Validación del mirror oficial de paquetes de Ubuntu.*

##### Paso 13: Esquema de Particionado Guiado (LVM)
Marcamos la opción de utilizar el disco completo (*Use an entire disk*) creando la estructura de volúmenes lógicos LVM:
![Paso 13 Master: Configuración de almacenamiento guiado](images/master/step_13.png)
*Figura 2.14: Selección de uso del disco completo y configuración de grupo LVM.*

##### Paso 14: Confirmación Destructiva de Escritura en Disco
Revisamos las particiones generadas y confirmamos la escritura en el disco virtual pulsando *Continue*:
![Paso 14 Master: Confirmación de particionado](images/master/step_14.png)
*Figura 2.15: Resumen del mapa de particiones y advertencia destructiva de confirmación.*

##### Paso 15: Configuración de Perfil de Usuario y Nombre del Host
Indicamos el nombre de red del servidor (**`k8s-master`**), junto con el usuario y contraseña de administración:
![Paso 15 Master: Configuración de perfil y credenciales](images/master/step_15.png)
*Figura 2.16: Creación de la cuenta de usuario y asignación del hostname k8s-master.*

##### Paso 16: Omisión de Ubuntu Pro
En la ventana de registro y soporte extendido seleccionamos *Skip for now* para omitir el servicio:
![Paso 16 Master: Omisión de Ubuntu Pro](images/master/step_16.png)
*Figura 2.17: Omisión de la suscripción a servicios comerciales de Ubuntu Pro.*

##### Paso 17: Habilitación de OpenSSH Server
Marcamos de forma indispensable la opción **Install OpenSSH server** para habilitar la administración remota segura:
![Paso 17 Master: Instalación de servidor SSH](images/master/step_17.png)
*Figura 2.18: Selección obligatoria del paquete OpenSSH server.*

##### Paso 18: Selección de Featured Server Snaps
Dejamos desmarcados todos los servicios snaps adicionales para mantener un sistema limpio y liviano:
![Paso 18 Master: Snaps de servidor](images/master/step_18.png)
*Figura 2.19: Lista de snaps adicionales desmarcados.*

##### Paso 19: Instalación de Paquetes Base y Seguridad
El instalador transfiere los paquetes del sistema operativo, el núcleo Linux y las actualizaciones de seguridad:
![Paso 19 Master: Proceso de instalación](images/master/step_19.png)
*Figura 2.20: Registro del progreso de instalación de paquetes y configuración del sistema.*

##### Paso 20: Finalización de la Instalación y Reinicio
Pulsamos sobre **Reboot Now**, desmontamos la imagen ISO virtual y confirmamos el arranque limpio de `k8s-master` hasta la consola de login:
![Paso 20 Master: Reinicio e inicio de sesión](images/master/step_20.png)
*Figura 2.21: Finalización del proceso de instalación e inicio de sesión en k8s-master.*

---

#### 2.2.3 Asistente Visual Paso a Paso para la Creación de la VM Worker (`k8s-worker1`)

A continuación se ilustran ordenadamente los 20 pasos para la creación de la máquina virtual del nodo de trabajo (`k8s-worker1`):

##### Paso 1: Nombre, Carpeta e Imagen ISO para el Worker
Definimos el nombre descriptivo `k8s-worker1`, tipo Linux (Ubuntu 64-bit) y la imagen ISO montada marcando omitir instalación desatendida:
![Paso 1 Worker: Nombre y sistema operativo](images/worker/step_01.png)
*Figura 2.22: Creación de la VM k8s-worker1 y selección de la imagen ISO.*

##### Paso 2: Instalación Desatendida
Confirmamos los parámetros de instalación en la pantalla del sistema operativo invitado:
![Paso 2 Worker: Asistente desatendido](images/worker/step_02.png)
*Figura 2.23: Confirmación de parámetros en el asistente de instalación.*

##### Paso 3: Asignación de Recursos de Hardware (RAM y vCPUs)
Asignamos 2048 MB (2 GB) de memoria RAM y 2 vCPUs para la ejecución de cargas de trabajo de pods:
![Paso 3 Worker: Hardware de la máquina virtual](images/worker/step_03.png)
*Figura 2.24: Asignación de 2048 MB de RAM y 2 vCPUs para k8s-worker1.*

##### Paso 4: Creación del Disco Duro Virtual VDI
Creamos un disco duro virtual VDI con asignación dinámica de 20.00 GB de capacidad:
![Paso 4 Worker: Disco duro virtual](images/worker/step_04.png)
*Figura 2.25: Creación del disco virtual VDI de 20 GB para el nodo worker.*

##### Paso 5: Configuración de Adaptadores de Red y Resumen
Ajustamos los adaptadores de red: Adaptador 1 en NAT y Adaptador 2 en `vboxnet0` con modo promiscuo en *Permitir todo*:
![Paso 5 Worker: Configuración de red y resumen](images/worker/step_05.png)
*Figura 2.26: Ajuste de interfaces de red con vboxnet0 y modo promiscuo activado.*

##### Paso 6: Arranque del Instalador y Selección de Idioma
Iniciamos la VM `k8s-worker1` y establecemos el idioma deseado para el proceso:
![Paso 6 Worker: Selección de idioma](images/worker/step_06.png)
*Figura 2.27: Menú de idioma para el nodo k8s-worker1.*

##### Paso 7: Actualización del Instalador
Seleccionamos la opción para continuar con la versión actual del instalador:
![Paso 7 Worker: Actualización del instalador](images/worker/step_07.png)
*Figura 2.28: Confirmación de versión del instalador subiquity.*

##### Paso 8: Distribución del Teclado
Configuramos la disposición adecuada para la entrada de caracteres:
![Paso 8 Worker: Distribución de teclado](images/worker/step_08.png)
*Figura 2.29: Configuración de teclado en el nodo worker.*

##### Paso 9: Base de Instalación de Ubuntu Server
Elegimos la versión estándar de Ubuntu Server sin servicios gráficos adicionales:
![Paso 9 Worker: Selección de paquete base](images/worker/step_09.png)
*Figura 2.30: Selección del paquete estándar sin entorno gráfico.*

##### Paso 10: Interfaces de Red Detectadas
Validamos la correcta identificación de las tarjetas `enp0s3` y `enp0s8`:
![Paso 10 Worker: Interfaces de red](images/worker/step_10.png)
*Figura 2.31: Interfaces de red identificadas en el asistente.*

##### Paso 11: Configuración de Proxy HTTP
Dejamos en blanco la configuración de proxy al contar con salida directa:
![Paso 11 Worker: Proxy HTTP](images/worker/step_11.png)
*Figura 2.32: Configuración de proxy HTTP en blanco.*

##### Paso 12: Repositorio Espejo de Paquetes
Validamos la conexión con el mirror oficial de Ubuntu:
![Paso 12 Worker: Espejo de paquetes](images/worker/step_12.png)
*Figura 2.33: Verificación del mirror oficial de paquetes.*

##### Paso 13: Configuración Guiada del Almacenamiento (LVM)
Seleccionamos el disco entero de 20 GB configurando el grupo de volúmenes LVM:
![Paso 13 Worker: Particionado LVM](images/worker/step_13.png)
*Figura 2.34: Configuración de almacenamiento con particionado LVM.*

##### Paso 14: Confirmación Destructiva de Particionado
Aceptamos la escritura definitiva de los volúmenes en el disco virtual:
![Paso 14 Worker: Confirmación de disco](images/worker/step_14.png)
*Figura 2.35: Confirmación de formateo y creación de volúmenes.*

##### Paso 15: Configuración de Perfil y Nombre del Host
Definimos el nombre de red del servidor (**`k8s-worker1`**) y las credenciales de administración:
![Paso 15 Worker: Configuración de perfil y credenciales](images/worker/step_15.png)
*Figura 2.36: Creación del usuario y asignación del hostname k8s-worker1.*

##### Paso 16: Pantalla de Ubuntu Pro
Seleccionamos *Skip for now* para omitir la activación del soporte extendido:
![Paso 16 Worker: Omisión de Ubuntu Pro](images/worker/step_16.png)
*Figura 2.37: Continuación sin registro en Ubuntu Pro.*

##### Paso 17: Instalación de OpenSSH Server
Marcamos de forma imprescindible la opción **Install OpenSSH server**:
![Paso 17 Worker: Selección de OpenSSH server](images/worker/step_17.png)
*Figura 2.38: Instalación obligatoria del servidor OpenSSH.*

##### Paso 18: Snaps Destacados de Servidor
Mantenemos desmarcados los snaps adicionales para optimizar recursos:
![Paso 18 Worker: Featured Server Snaps](images/worker/step_18.png)
*Figura 2.39: Lista de snaps adicionales desmarcados.*

##### Paso 19: Instalación de Paquetes Base y Dependencias
El instalador descarga y aplica los paquetes del sistema en el nodo worker:
![Paso 19 Worker: Progreso de instalación](images/worker/step_19.png)
*Figura 2.40: Progreso de descarga e instalación del sistema base.*

##### Paso 20: Finalización e Inicio de Sesión
Hacemos clic en **Reboot Now**, retiramos el medio de instalación virtual y confirmamos que `k8s-worker1` arranca hasta el prompt de inicio de sesión:
![Paso 20 Worker: Reinicio e inicio de sesión](images/worker/step_20.png)
*Figura 2.41: Nodo k8s-worker1 operativo y preparado para la configuración de red y unión al cluster.*

---

### 2.3 Configuración de Idioma y Teclado Español

Por defecto, la instalación de Ubuntu Server se inicializa con la distribución de teclado en inglés (US). Esto genera múltiples errores de tipeo al introducir caracteres frecuentes de administración en consola como guiones (`-`), tuberías (`|`), barras (`/`), almohadillas (`#`) o comillas.

Ejecuta en **ambos nodos (`k8s-master` y `k8s-worker1`)** nada más iniciar sesión:

```bash
# 1. Configurar la distribución de teclado a español pc105 de forma persistente
sudo localectl set-x11-keymap es pc105

# 2. Cargar el mapa de teclado en la consola actual de manera inmediata
sudo loadkeys es
```

* `localectl set-x11-keymap es pc105`: Registra la distribución española en `/etc/default/keyboard` para que se aplique en todos los futuros reinicios del sistema.
* `loadkeys es`: Aplica la tabla de teclas inmediatamente en la terminal TTY actual sin necesidad de reiniciar la sesión.

---

### 2.4 Persistencia de Red: Bloqueo de Cloud-Init y Netplan Estático

En Ubuntu Server 22.04 LTS, el servicio de inicialización `cloud-init` gestiona la configuración de red y, por defecto, reescribe los archivos de Netplan al reiniciar el sistema. Si se modifica Netplan sin desactivar la generación de red de `cloud-init`, la dirección IP estática se perderá tras el primer reinicio.

#### Paso 2.4.1: Crear archivo de bloqueo para cloud-init (Ambos Nodos)
Ejecuta en `k8s-master` y `k8s-worker1`:

```bash
sudo touch /etc/cloud/cloud-init.disabled
```

La creación de este archivo deshabilita `cloud-init` por completo en el sistema operativo, evitando que interfiera o reescriba la configuración de red tras reiniciar.

#### Paso 2.4.2: Configurar Netplan con IP Estática
En Ubuntu Server, el archivo de configuración de red predeterminado se ubica en `/etc/netplan/50-cloud-init.yaml`.

Edita el archivo en el nodo **`k8s-master`**:
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Añade la interfaz Host-Only `enp0s8` con la IP `192.168.56.10/24`:
```yaml
network:
  ethernets:
    enp0s3:
      dhcp4: true
      optional: true
    enp0s8:
      dhcp4: false
      addresses:
      - 192.168.56.10/24
      optional: true
  version: 2
```

Edita el archivo en el nodo **`k8s-worker1`**:
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Añade la interfaz Host-Only `enp0s8` con la IP `192.168.56.11/24`:
```yaml
network:
  ethernets:
    enp0s3:
      dhcp4: true
      optional: true
    enp0s8:
      dhcp4: false
      addresses:
      - 192.168.56.11/24
      optional: true
  version: 2
```

#### Paso 2.4.3: Aplicar los cambios de red
En ambos nodos, aplica la configuración:
```bash
sudo netplan apply
```

#### Paso 2.4.4: Verificación con `ip a`
Comprueba que la interfaz `enp0s8` tiene asignada la dirección IP correspondiente.

Salida esperada en **`k8s-master`**:
```text
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:f9:da:df brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
       valid_lft 86121sec preferred_lft 86121sec
    inet6 fe80::a00:27ff:fef9:dadf/64 scope link 
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a2:c7:8f brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.10/24 brd 192.168.56.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fea2:c78f/64 scope link 
       valid_lft forever preferred_lft forever
```

Salida esperada en **`k8s-worker1`**:
```text
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:17:40:ea brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
       valid_lft 86242sec preferred_lft 86242sec
    inet6 fe80::a00:27ff:fe17:40ea/64 scope link 
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:34:ea:f7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.11/24 brd 192.168.56.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe34:eaf7/64 scope link 
       valid_lft forever preferred_lft forever
```

#### Paso 2.4.5: Configuración de Hostname y Resolución Local
En el nodo Master:
```bash
sudo hostnamectl set-hostname k8s-master
```

En el nodo Worker:
```bash
sudo hostnamectl set-hostname k8s-worker1
```

Añadir la resolución estática en `/etc/hosts` de ambas máquinas:
```bash
sudo bash -c 'cat >> /etc/hosts <<EOF
192.168.56.10 k8s-master
192.168.56.11 k8s-worker1
EOF'
```

Prueba la conectividad bidireccional entre nodos:
```bash
ping -c 3 192.168.56.10
ping -c 3 192.168.56.11
```

---

### 2.5 Preparación Base del Sistema Operativo (SWAP, Kernel y Sysctl)

Ejecuta los siguientes pasos en **cada una de las dos máquinas virtuales**.

#### Desactivación Permanente de SWAP
Kubernetes requiere que la memoria SWAP esté completamente inactiva para garantizar la gestión predecible de recursos en `kubelet`:

```bash
# Desactivar en la sesión actual
sudo swapoff -a

# Desactivar de forma permanente al reiniciar
sudo sed -i '/^\/swap\.img/ s/^/#/' /etc/fstab

# Verificación (debe devolver resultado vacío)
swapon --show
```

#### Carga de Módulos de Kernel y Ajustes Sysctl
Habilitar los módulos `overlay` y `br_netfilter` necesarios para el puenteo de red en los contenedores:

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
```

Configurar los parámetros de enrutamiento y filtrado de paquetes:
```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

---

### 2.6 Instalación de Containerd y Dependencias del Sistema (`conntrack`, `socat`)

Desde Kubernetes v1.24, el subsistema `dockershim` fue removido. Instalaremos `containerd` como runtime estándar de contenedores (CRI), junto con dos paquetes fundamentales del sistema operativo:

* **`conntrack`**: Requerido por `kube-proxy` y `kubelet` para gestionar y monitorear las tablas de seguimiento de conexiones de `iptables`/`netfilter`. Sin `conntrack`, la asignación de IPs virtuales de servicio y balanceo de tráfico falla.
* **`socat`**: Utilizado por el API Server de Kubernetes para canalizar flujos de entrada/salida y crear túneles bidireccionales, indispensables para el correcto funcionamiento de comandos como `kubectl exec` y `kubectl port-forward`.

Ejecuta en **ambos nodos (`k8s-master` y `k8s-worker1`)**:

```bash
# 1. Instalar containerd y dependencias de red indispensables
sudo apt-get update
sudo apt-get install -y containerd conntrack socat

# 2. Generar archivo de configuración inicial
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null

# 3. Habilitar el controlador cgroup de systemd (indispensable para kubelet)
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

# 4. Reiniciar y habilitar el servicio containerd
sudo systemctl restart containerd
sudo systemctl enable containerd

# 5. Comprobación de estado activo
sudo systemctl status containerd --no-pager
```

---

### 2.7 Instalación de Herramientas Kubernetes (v1.31 en pkgs.k8s.io)

Ejecuta en **ambos nodos**:

```bash
# 1. Instalar dependencias de transporte seguro
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# 2. Crear directorio de llaveros de confianza
sudo mkdir -p -m 755 /etc/apt/keyrings

# 3. Descargar y almacenar la clave pública oficial de Kubernetes v1.31
K8S_REPO="https://pkgs.k8s.io/core:/stable:/v1.31/deb/"
KEYRING="/etc/apt/keyrings/kubernetes-apt-keyring.gpg"

curl -fsSL "${K8S_REPO}Release.key" \
  | sudo gpg --dearmor -o "${KEYRING}"

# 4. Registrar el repositorio comunitario oficial
echo "deb [signed-by=${KEYRING}] ${K8S_REPO} /" \
  | sudo tee /etc/apt/sources.list.d/kubernetes.list

# 5. Instalar kubelet, kubeadm y kubectl
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

# 6. Bloquear actualizaciones automáticas para preservar estabilidad en versiones menores
sudo apt-mark hold kubelet kubeadm kubectl
```

> [!NOTE] Solución de problemas: Error de validación de claves en `apt update` (Keyring obsoleto o clave no reconocida)
> Si durante la instalación o actualización de paquetes con `apt` el repositorio no es reconocido por Ubuntu o se presentan errores con firmas de claves públicas (por ejemplo, errores de claves no válidas o ausentes en repositorios como HashiCorp preconfigurados en la imagen del sistema, p. ej. `NO_PUBKEY AA16FCBCA621E701`), la solución consiste en añadir la clave correspondiente al keyring (sin recurrir a `apt-key`, que se encuentra obsoleto):
>
> ```bash
> gpg --no-default-keyring --keyring /tmp/hc-old.gpg --keyserver keyserver.ubuntu.com --recv-keys AA16FCBCA621E701
> gpg --no-default-keyring --keyring /tmp/hc-old.gpg --export | sudo tee -a /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
> sudo apt update
> ```

---

### 2.8 Inicialización del Plano de Control (Master), Flannel CNI y Registros Reales

Los pasos de esta subsección se ejecutan en **`k8s-master`**.

#### Paso 2.8.1: Asegurar dependencias de red en el master
Antes de inicializar el cluster, verifica e instala las dependencias de red necesarias (`conntrack` y `socat`):
```bash
sudo apt-get update && sudo apt-get install -y conntrack socat
```

#### Paso 2.8.2: Descarga previa de imágenes de control plane
```bash
sudo kubeadm config images pull
```

#### Paso 2.8.3: Inicialización del cluster con kubeadm
Ejecuta `kubeadm init` indicando la IP de la red Host-Only como dirección de anuncio del API Server:

```bash
sudo kubeadm init \
  --apiserver-advertise-address=192.168.56.10 \
  --pod-network-cidr=10.244.0.0/16 \
  --node-name k8s-master
```

#### Registro Real de Terminal (Benchmark de Inicialización):
A continuación se muestra el registro de ejecución obtenido en el laboratorio, que sirve de referencia para validar el correcto progreso de la instalación:

```text
$ sudo kubeadm init --apiserver-advertise-address=192.168.56.10 --pod-network-cidr=10.244.0.0/16 --node-name k8s-master
I1114 21:49:03.100458   15635 version.go:261] remote version is much newer: v1.37.2; falling back to: stable-1.31
[init] Using Kubernetes version: v1.31.14
[preflight] Running pre-flight checks
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action beforehand using 'kubeadm config images pull'
W1114 21:49:03.258789   15635 checks.go:843] detected that the sandbox image "" of the container runtime is inconsistent with that used by kubeadm.It is recommended to use "registry.k8s.io/pause:3.10" as the CRI sandbox image.
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [k8s-master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.56.10]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.56.10 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.56.10 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "super-admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests"
[kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
[kubelet-check] The kubelet is healthy after 502.603826ms
[api-check] Waiting for a healthy API server. This can take up to 4m0s
[api-check] The API server is healthy after 5.502159471s
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --upload-certs
[mark-control-plane] Marking the node k8s-master as control-plane by adding the labels: [node-role.kubernetes.io/control-plane node.kubernetes.io/exclude-from-external-load-balancers]
[mark-control-plane] Marking the node k8s-master as control-plane by adding the taints [node-role.kubernetes.io/control-plane:NoSchedule]
[bootstrap-token] Using token: 5yjuf0.zo38v6ts77dd8zjc
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.56.10:6443 --token 5yjuf0.zo38v6ts77dd8zjc \
	--discovery-token-ca-cert-hash sha256:3bf340abd39b6c6d30c33c163a9ceccc170567ea6f52f0007b59d3608f2a4e11
```

#### Paso 2.8.4: Configurar credenciales de kubectl para el usuario local
```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

#### Paso 2.8.5: Despliegue del Plugin de Red (Flannel CNI) con fijación de interfaz
Descarga el manifiesto oficial de Flannel:
```bash
FLANNEL_URL="https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml"
curl -sSL "${FLANNEL_URL}" -o kube-flannel.yml
```

En entornos VirtualBox con doble adaptador, Flannel seleccionará erróneamente la interfaz de NAT (`enp0s3`) si no se fuerza la interfaz Host-Only. Debemos añadir el argumento `--iface=enp0s8` en los argumentos del DaemonSet.

Puedes realizar esta sustitución limpiamente con `sed`:
```bash
sed -i 's/- --kube-subnet-mgr/- --kube-subnet-mgr\n        - --iface=enp0s8/' kube-flannel.yml
```

*(Opcional: Si abres el archivo con `nano kube-flannel.yml`, comprueba visualmente que el bloque de argumentos del contenedor `kube-flannel` incluya `--iface=enp0s8`)*:
```yaml
      containers:
      - name: kube-flannel
        image: docker.io/flannel/flannel:...
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        - --iface=enp0s8
```

Aplica el manifiesto modificado:
```bash
kubectl apply -f kube-flannel.yml
```

Verifica el estado del nodo y pods del sistema:
```bash
kubectl get nodes
kubectl get pods -n kube-system
```
*(En menos de un minuto, el nodo `k8s-master` cambiará su estado a `Ready`).*

---

### 2.9 Unión del Nodo Worker al Cluster con Dependencias y Registros Reales

En la máquina virtual **`k8s-worker1`**:

#### Paso 2.9.1: Asegurar dependencias de red en el worker
Antes de ejecutar `kubeadm join`, corrobora que `conntrack` y `socat` están presentes:
```bash
sudo apt-get update && sudo apt-get install -y conntrack socat
```

#### Paso 2.9.2: Ejecución del comando `kubeadm join`
Ejecuta como superusuario el comando devuelto por `kubeadm init` en el Master:

```bash
sudo kubeadm join 192.168.56.10:6443 \
  --token <TU_TOKEN> \
  --discovery-token-ca-cert-hash sha256:<TU_HASH>
```

#### Registro Real de Terminal (Benchmark de Unión):
A continuación se muestra la salida de consola real obtenida en `k8s-worker1`:

```text
$ sudo kubeadm join 192.168.56.10:6443 --token 5yjuf0.zo38v6ts77dd8zjc  --discovery-token-ca-cert-hash sha256:3bf340abd39b6c6d30c33c163a9ceccc170567ea6f52f0007b59d3608f2a4e11
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
[kubelet-check] The kubelet is healthy after 1.001529458s
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

*(Si el token expiró tras 24 horas, puedes regenerar uno nuevo en el master mediante `sudo kubeadm token create --print-join-command`).*

#### Paso 2.9.3: Validación del Cluster Completo desde el Master
Regresa a la terminal de **`k8s-master`** y valida que ambos nodos reporten estado `Ready`:
```bash
kubectl get nodes -o wide
```

Salida esperada:
```text
NAME          STATUS   ROLES           AGE   VERSION    INTERNAL-IP     OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
k8s-master    Ready    control-plane   49m   v1.31.14   192.168.56.10   Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
k8s-worker1   Ready    <none>          21m   v1.31.14   192.168.56.11   Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
```

---

### 2.10 Conexión Remota No Destructiva desde el Host Anfitrión (Merge Kubeconfig)

Permite controlar el cluster directamente desde la máquina host física (Ubuntu 20.04).

> [!CAUTION]
> **No sobrescribas tu archivo `~/.kube/config`:**
> Si ya utilizas Kubernetes en tu equipo (ej. Minikube, Docker Desktop, k3s, EKS, GKE), ejecutar `scp ... ~/.kube/config` borrará tus clusters preexistentes. A continuación se detalla cómo fusionar la nueva configuración de forma segura y no destructiva.

#### Paso 2.10.1: Instalar kubectl en el Host (si no lo tienes instalado)
```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl gpg
sudo mkdir -p -m 755 /etc/apt/keyrings

K8S_REPO="https://pkgs.k8s.io/core:/stable:/v1.31/deb/"
KEYRING="/etc/apt/keyrings/kubernetes-apt-keyring.gpg"

curl -fsSL "${K8S_REPO}Release.key" | sudo gpg --dearmor --yes -o "${KEYRING}"
echo "deb [signed-by=${KEYRING}] ${K8S_REPO} /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update && sudo apt-get install -y kubectl
```

#### Paso 2.10.2: Descargar el archivo kubeconfig del Master a un fichero local
Descarga la configuración del master a un archivo temporal denominado `master-kubeconfig`:
```bash
mkdir -p ~/.kube
scp <usuario>@192.168.56.10:~/.kube/config ./master-kubeconfig
```

#### Paso 2.10.3: Fusión (Merge) de Configuraciones
Dispones de dos alternativas para integrar el cluster sin alterar los existentes:

##### Alternativa A: Fusión Automática con kubectl (Recomendada)
Si ya tienes un `~/.kube/config` existente:
```bash
# 1. Realizar copia de respaldo de seguridad
cp ~/.kube/config ~/.kube/config.bak

# 2. Fusionar ambos archivos en uno nuevo consolidado
KUBECONFIG=~/.kube/config:./master-kubeconfig kubectl config view --flatten > ~/.kube/config.new

# 3. Reemplazar y asegurar permisos
mv ~/.kube/config.new ~/.kube/config
chmod 600 ~/.kube/config
rm -f ./master-kubeconfig
```
*(Si NO tenías un archivo `~/.kube/config` previo en el host, simplemente muévelo: `mv ./master-kubeconfig ~/.kube/config && chmod 600 ~/.kube/config`).*

##### Alternativa B: Fusión Manual de Bloques YAML
Abre `~/.kube/config` y `./master-kubeconfig` con tu editor. Copia y pega dentro de las secciones correspondientes:
1. Bajo `clusters:`, añade la entrada del cluster `kubernetes` con la URL `https://192.168.56.10:6443`.
2. Bajo `users:`, añade el usuario `kubernetes-admin`.
3. Bajo `contexts:`, añade el contexto `kubernetes-admin@kubernetes` que vincula dicho usuario y cluster.

#### Paso 2.10.4: Seleccionar el Contexto y Validar Acceso Remoto
Fija el contexto activo hacia el nuevo cluster:
```bash
kubectl config use-context kubernetes-admin@kubernetes
```

Comprueba la conectividad remota desde la consola de tu host:
```bash
kubectl cluster-info
kubectl get nodes -o wide
```

Salida real benchmark obtenida desde el host anfitrión:
```text
$ kubectl cluster-info
Kubernetes control plane is running at https://192.168.56.10:6443
CoreDNS is running at https://192.168.56.10:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

$ kubectl get nodes -o wide
NAME          STATUS   ROLES           AGE   VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
k8s-master    Ready    control-plane   49m   v1.31.14   192.168.56.10   <none>        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
k8s-worker1   Ready    <none>          21m   v1.31.14   192.168.56.11   <none>        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
```

---

## 3. Sección 2: Automatización Completa con Vagrant (IaC)

Una vez que los alumnos dominan el proceso manual y los componentes internos, esta segunda sección les enseña a codificar todo el laboratorio como infraestructura como código (**Infrastructure as Code - IaC**) mediante Vagrant.

### 3.1 Introducción a Vagrant para Kubernetes

Vagrant permite describir la topología de máquinas virtuales, interfaces de red, asignación de memoria y scripts de ejecución en un único archivo de configuración (`Vagrantfile`). Con un solo comando (`vagrant up`), se descarga la imagen base, se crean las dos VMs en VirtualBox y se aprovisiona el cluster de forma 100% desatendida.

---

### 3.2 Estructura del Proyecto de Automatización

El proyecto de automatización se organiza en la siguiente estructura de carpetas:

```text
poc-training-k8s-cluster-kubeadm/
├── Vagrantfile                    # Definición de infraestructura y máquinas virtuales
├── scripts/
│   ├── common.sh                 # Aprovisionamiento común (SO, kernel, containerd, k8s)
│   ├── master.sh                 # Inicialización de kubeadm, Flannel y exportación de token
│   └── worker.sh                 # Espera activa y ejecución de kubeadm join
└── configs/                       # Directorio compartido para token y kubeconfig
```

---

### 3.3 El Archivo `Vagrantfile` Multi-Máquina

El archivo `Vagrantfile` define de forma declarativa las dos máquinas virtuales con Ubuntu 22.04 LTS (`ubuntu/jammy64`) sobre el proveedor VirtualBox:

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Box base oficial de Ubuntu 22.04 LTS (Jammy Jellyfish)
  config.vm.box = "ubuntu/jammy64"

  # Carpeta compartida para intercambio seguro de tokens y kubeconfig
  config.vm.synced_folder "./configs", "/vagrant_configs", create: true

  # =========================================================================
  # 1. NODO MASTER (Control Plane)
  # =========================================================================
  config.vm.define "k8s-master" do |master|
    master.vm.hostname = "k8s-master"
    master.vm.network "private_network", ip: "192.168.56.10"

    master.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-master"
      vb.cpus = 2
      vb.memory = 3072
      vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    end

    # Aprovisionamiento: Primero configuración común, luego inicialización master
    master.vm.provision "shell", path: "scripts/common.sh"
    master.vm.provision "shell", path: "scripts/master.sh"
  end

  # =========================================================================
  # 2. NODO WORKER
  # =========================================================================
  config.vm.define "k8s-worker1" do |worker|
    worker.vm.hostname = "k8s-worker1"
    worker.vm.network "private_network", ip: "192.168.56.11"

    worker.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-worker1"
      vb.cpus = 2
      vb.memory = 2048
      vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    end

    # Aprovisionamiento: Configuración común y unión automatizada al cluster
    worker.vm.provision "shell", path: "scripts/common.sh"
    worker.vm.provision "shell", path: "scripts/worker.sh"
  end
end
```

---

### 3.4 Scripts Shell de Aprovisionamiento Modular

#### 3.4.1 Script Común (`scripts/common.sh`)
Se ejecuta en cada VM para preparar el sistema operativo, módulos de kernel, containerd y paquetes de Kubernetes:

```bash
#!/bin/bash
set -euo pipefail

echo "==> [COMMON] Configurando resolución de nombres en /etc/hosts..."
cat <<EOF >> /etc/hosts
192.168.56.10 k8s-master
192.168.56.11 k8s-worker1
EOF

echo "==> [COMMON] Desactivando memoria SWAP..."
swapoff -a
sed -i '/^\/swap\.img/ s/^/#/' /etc/fstab

echo "==> [COMMON] Cargando módulos de kernel..."
cat <<EOF > /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
modprobe overlay
modprobe br_netfilter

echo "==> [COMMON] Configurando parámetros sysctl..."
cat <<EOF > /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sysctl --system > /dev/null

echo "==> [COMMON] Instalando y configurando Containerd..."
apt-get update -y > /dev/null
apt-get install -y containerd apt-transport-https ca-certificates curl gpg > /dev/null

mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
systemctl restart containerd
systemctl enable containerd > /dev/null

echo "==> [COMMON] Configurando repositorios de Kubernetes v1.31 (pkgs.k8s.io)..."
K8S_REPO="https://pkgs.k8s.io/core:/stable:/v1.31/deb/"
KEYRING="/etc/apt/keyrings/kubernetes-apt-keyring.gpg"
mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL "${K8S_REPO}Release.key" | gpg --dearmor --yes -o "${KEYRING}"
echo "deb [signed-by=${KEYRING}] ${K8S_REPO} /" > /etc/apt/sources.list.d/kubernetes.list

apt-get update -y > /dev/null
apt-get install -y kubelet kubeadm kubectl > /dev/null
apt-mark hold kubelet kubeadm kubectl
```

#### 3.4.2 Script del Master (`scripts/master.sh`)
Inicializa el cluster, configura Flannel fijando la interfaz `enp0s8`, exporta el kubeconfig y genera el comando de unión en la carpeta compartida:

```bash
#!/bin/bash
set -euo pipefail

MASTER_IP="192.168.56.10"
POD_CIDR="10.244.0.0/16"

echo "==> [MASTER] Inicializando cluster de Kubernetes con kubeadm init..."
kubeadm init \
  --apiserver-advertise-address="${MASTER_IP}" \
  --pod-network-cidr="${POD_CIDR}" \
  --node-name k8s-master > /dev/null

echo "==> [MASTER] Configurando kubeconfig para el usuario vagrant..."
mkdir -p /home/vagrant/.kube
cp -i /etc/kubernetes/admin.conf /home/vagrant/.kube/config
chown vagrant:vagrant /home/vagrant/.kube/config

echo "==> [MASTER] Exportando kubeconfig al directorio compartido..."
cp -i /etc/kubernetes/admin.conf /vagrant_configs/config
chmod 644 /vagrant_configs/config

echo "==> [MASTER] Desplegando Flannel CNI con enlace forzado a la interfaz enp0s8..."
FLANNEL_URL="https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml"
curl -sSL "${FLANNEL_URL}" -o /tmp/kube-flannel.yml
sed -i 's/- --kube-subnet-mgr/- --kube-subnet-mgr\n        - --iface=enp0s8/' /tmp/kube-flannel.yml
kubectl --kubeconfig=/etc/kubernetes/admin.conf apply -f /tmp/kube-flannel.yml > /dev/null

echo "==> [MASTER] Generando comando kubeadm join desatendido..."
kubeadm token create --print-join-command > /vagrant_configs/join.sh
chmod +x /vagrant_configs/join.sh

echo "==> [MASTER] Plano de control listo y operativo."
```

#### 3.4.3 Script del Worker (`scripts/worker.sh`)
Espera de forma activa a que el Master complete la inicialización y genera el token de unión para ejecutar `kubeadm join`:

```bash
#!/bin/bash
set -euo pipefail

echo "==> [WORKER] Esperando a que el nodo Master genere el token de unión..."
while [ ! -f /vagrant_configs/join.sh ]; do
  sleep 3
done

echo "==> [WORKER] Ejecutando comando de unión al cluster..."
bash /vagrant_configs/join.sh > /dev/null

echo "==> [WORKER] Nodo incorporado con éxito al cluster."
```

---

### 3.5 Despliegue Desatendido con `vagrant up`

Para que el alumno levante todo el laboratorio automatizado en su equipo:

1. **Instalar Vagrant y VirtualBox en el Host (Ubuntu 20.04):**
   ```bash
   sudo apt-get update
   sudo apt-get install -y virtualbox vagrant
   ```

2. **Iniciar el cluster:**
   ```bash
   cd poc-training-k8s-cluster-kubeadm
   vagrant up
   ```
   *(Vagrant levantará primero `k8s-master`, aprovisionará el control plane y Flannel, guardará el token en `configs/join.sh`, y luego levantará `k8s-worker1` uniéndolo automáticamente).*

3. **Verificar el estado desde el Host con kubectl:**
   ```bash
   export KUBECONFIG=$(pwd)/configs/config
   kubectl get nodes -o wide
   ```

---

### 3.6 Gestión del Ciclo de Vida del Cluster

Comandos esenciales de Vagrant para los alumnos:

* **Comprobar estado de las VMs:**
  ```bash
  vagrant status
  ```
* **Acceder por SSH a cualquiera de los nodos:**
  ```bash
  vagrant ssh k8s-master
  vagrant ssh k8s-worker1
  ```
* **Detener temporalmente el laboratorio (ahorro de batería/RAM):**
  ```bash
  vagrant halt
  ```
* **Reanudar el laboratorio:**
  ```bash
  vagrant up
  ```
* **Destruir completamente el laboratorio para empezar de cero:**
  ```bash
  vagrant destroy -f
  ```

---

## 4. Sección 3: Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard

Para monitorizar y gestionar visualmente los recursos del cluster sin depender exclusivamente de la línea de comandos, desplegamos la interfaz gráfica oficial: el **Kubernetes Dashboard**. A continuación se detalla el procedimiento completo, incluyendo la verificación de estado de los pods, la creación declarativa de la cuenta administrativa RBAC, la obtención del token Bearer y las capturas visuales de la interfaz.

---

### 4.1 Despliegue de los Componentes Oficiales del Dashboard
Aplica el manifiesto recomendado oficial de Kubernetes (versión v2.7.0), el cual genera el namespace dedicado `kubernetes-dashboard`, las cuentas de servicio, certificados autofirmados, roles RBAC y los deployments de la interfaz y del recolector de métricas:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

**Salida real de terminal:**
```text
namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created
```

---

### 4.2 Verificación del Estado de los Pods del Dashboard
Antes de intentar acceder, comprobamos que tanto el pod principal del Dashboard como el pod auxiliar `dashboard-metrics-scraper` hayan descargado sus imágenes y alcancen el estado `Running`:

```bash
kubectl get pods -n kubernetes-dashboard
```

**Salida real de terminal:**
```text
NAME                                         READY   STATUS    RESTARTS   AGE
dashboard-metrics-scraper-6b96ff7878-2xhlz   1/1     Running   0          31s
kubernetes-dashboard-8696f5f494-hxd9c        1/1     Running   0          31s
```

---

### 4.3 Creación de Cuenta de Servicio y Privilegios Administrativos (RBAC)
Por defecto, el Dashboard se despliega con permisos mínimos restringidos. Para administrar y visualizar todos los namespaces y cargas de trabajo del cluster, creamos un usuario de servicio (`ServiceAccount`) con rol de superusuario (`cluster-admin`).

Crea el archivo `dashboard-adminuser.yaml`:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

Aplica este manifiesto en el cluster:

```bash
kubectl apply -f dashboard-adminuser.yaml
```

**Salida real de terminal:**
```text
serviceaccount/admin-user created
clusterrolebinding.rbac.authorization.k8s.io/admin-user created
```

---

### 4.4 Comprobación de la Cuenta de Servicio Creada
Verificamos que el objeto `ServiceAccount` existe correctamente registrado en el namespace `kubernetes-dashboard`:

```bash
kubectl get serviceaccount admin-user -n kubernetes-dashboard
```

**Salida real de terminal:**
```text
NAME         SECRETS   AGE
admin-user   0         38s
```

---

### 4.5 Generación del Token de Autenticación Bearer
En Kubernetes moderno (v1.24+ y v1.31), los tokens de ServiceAccount ya no se generan indefinidamente en secrets por defecto, sino que se solicitan mediante la API de tokens temporales de `kubectl`:

```bash
kubectl -n kubernetes-dashboard create token admin-user
```

**Salida real de terminal:**
```text
eyJhbGciOiJSUzI1NiIsImtpZCI6IlUyUEhfRVVUckc1M0tfcWstRkFUd1E0ek9aMkluejhkc0FaVmJEOEo4SWcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzk0ODM1NDkyLCJpYXQiOjE3OTQ4MzE4OTIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNzYwODdjOWEtMTQ1ZS00ZWNhLTliMzItMjFlYjM0ZjhiZjIwIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJhZG1pbi11c2VyIiwidWlkIjoiN2ViY2M0YTAtYjk1MC00M2Q0LTg3OTYtMjI3NTNlNmEyODA3In19LCJuYmYiOjE3OTQ4MzE4OTIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlcm5ldGVzLWRhc2hib2FyZDphZG1pbi11c2VyIn0.Geq8LpwDCPqfYDGIfwjnnh8HClQKBLPscWoJ5AgekxMJGLKnXT878KleThDbFtHF5LDxB_DRod8H7yIXpUoimEOXdex0bYGj5jXT-Qt6T734BDh21ppavtrP4CmAJW_feyEcsFzGuXQ4qlmEOheSGRhePKIEahBnI05sqm9B1a90indvH4rx_qxAWrpxsY-QpVyZcjjZXHr9DLcD3FEmpKz8wVFUsw-EaQ7SV3k39gBImBDO9Tk-dJwBiU5VNwYYXuCuGsaX7UxfFor-2fMp3CR-oX1Z1_huGWI7ynYKpRwy-49BnqrMmThjPUMImBL7jBFkURr_erazpiQcj0CziQ
```

> [!NOTE]
> Copia íntegramente la cadena alfanumérica resultante en el portapapeles; será el secreto necesario para identificarte en el panel.

#### Opción Alternativa: Generación de Token Permanente (Sin Expiración)

Por defecto, los tokens generados con `kubectl create token` caducan automáticamente tras 1 hora. Si deseas evitar tener que solicitar y pegar un nuevo token en cada sesión de trabajo, puedes crear un token permanente declarativo asociando un objeto `Secret` al ServiceAccount `admin-user`.

1. Crea el archivo `admin-user-secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: admin-user-secret
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "admin-user"
type: kubernetes.io/service-account-token
```

El tipo `kubernetes.io/service-account-token` le indica al plano de control de Kubernetes que genere de forma automática un token persistente y lo almacene en el secreto.

2. Aplica el manifiesto en el cluster:

```bash
kubectl apply -f admin-user-secret.yaml
```

**Salida en consola:**
```text
secret/admin-user-secret created
```

3. Extrae y decodifica el token permanente en Base64:

```bash
kubectl get secret admin-user-secret -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```

Este comando imprimirá directamente el token JWT no expirable. Puedes guardarlo de forma segura en un gestor de contraseñas local; permanecerá válido indefinidamente para iniciar sesión en el Dashboard mientras no se elimine el secreto `admin-user-secret`.

> [!WARNING]
> **Consideración de Seguridad Crítica:**
> Los tokens permanentes **no son seguros para su uso en entornos de producción**, ya que vulneran el principio de menor privilegio al carecer de caducidad y rotación automática. Si una credencial estática de superadministrador (`cluster-admin`) se filtra, el cluster queda permanentemente comprometido hasta su revocación manual. Sin embargo, para esta prueba local de laboratorio y entornos de aprendizaje, su uso es plenamente válido por comodidad.

---

### 4.6 Acceso Seguro mediante Kubectl Proxy
Para conectarse de forma segura desde el equipo anfitrión físico sin exponer el Dashboard directamente a redes externas no cifradas, iniciamos el túnel local de `kubectl proxy`:

```bash
kubectl proxy
```

**Salida en consola:**
```text
Starting to serve on 127.0.0.1:8001
```

Manteniendo este proceso en ejecución, abre tu navegador web e introduce la siguiente URL exacta:

```text
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

---

### 4.7 Inicio de Sesión y Verificación Visual del Panel

Al acceder a la URL indicada, el Dashboard presenta la pantalla de autenticación. Selecciona la opción **Token**, pega el token generado en el paso 4.5 y pulsa sobre **Sign in**:

![Pantalla de inicio de sesión de Kubernetes Dashboard](images/k8s_dashboard_login.png)
*Figura 3.1: Pantalla de inicio de sesión de Kubernetes Dashboard solicitando autenticación mediante Token.*

Una vez autenticado como `admin-user`, se despliega el panel de control completo. En el selector superior de namespaces seleccionamos `kubernetes-dashboard` para confirmar que los pods, deployments y servicios recién creados se encuentran en estado saludable:

![Vista interna del Kubernetes Dashboard con los recursos del namespace](images/k8s_dashboard.png)
*Figura 3.2: Interfaz web de Kubernetes Dashboard mostrando el estado de los recursos y pods del namespace kubernetes-dashboard.*

---

## 5. Sección 4: Ejemplo Práctico de Despliegue en el Cluster (Nginx)

Una vez que el cluster de Kubernetes se encuentra operativo y verificado (tanto si se ha desplegado manualmente con Kubeadm como si se ha aprovisionado de forma automatizada mediante Vagrant), es fundamental validar el ciclo de vida de una aplicación real: programación de pods en los nodos worker, asignación de IP en el rango CNI de Flannel, exposición mediante un servicio `NodePort` y resolución de tráfico HTTP desde el equipo anfitrión.

---

### 5.1 Creación del Deployment de Nginx

Desplegamos un servidor web Nginx básico en el cluster utilizando un objeto de tipo `Deployment`. Al no especificar namespace, el recurso se creará automáticamente en el namespace `default`:

```bash
kubectl create deployment nginx-test --image=nginx
```

**Salida real del comando:**
```text
deployment.apps/nginx-test created
```

---

### 5.2 Inspección Detallada de Recursos del Cluster

Tras emitir la orden de creación, Kubernetes gestiona automáticamente la jerarquía de objetos: el **Deployment** gestiona un **ReplicaSet**, y este a su vez supervisa la creación y estado de salud de los **Pods**.

#### 1. Verificación del Deployment
Comprobamos el estado del Deployment, observando que la réplica solicitada está lista y disponible:

```bash
kubectl get deployments -o wide
```

**Salida real de terminal:**
```text
NAME         READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
nginx-test   1/1     1            1           11m   nginx        nginx    app=nginx-test
```

#### 2. Verificación del ReplicaSet
El Deployment ha creado un ReplicaSet con el hash correspondiente a la plantilla de Pods:

```bash
kubectl get rs -o wide
```

**Salida real de terminal:**
```text
NAME                    DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES   SELECTOR
nginx-test-5b77bfd686   1         1         1       11m   nginx        nginx    app=nginx-test,pod-template-hash=5b77bfd686
```

#### 3. Verificación del Pod y su Asignación de Red
Comprobamos que el Pod se encuentra en estado `Running`, tiene una IP asignada dentro del rango CIDR de pods de Flannel (`10.244.1.2`) y ha sido programado en el nodo worker (`k8s-worker1`):

```bash
kubectl get pods -o wide
```

**Salida real de terminal:**
```text
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE          NOMINATED NODE   READINESS GATES
nginx-test-5b77bfd686-xsbgg   1/1     Running   0          11m   10.244.1.2   k8s-worker1   <none>           <none>
```

---

### 5.3 Exposición Externa mediante Servicio NodePort

Para acceder al servidor web Nginx desde el equipo anfitrión (o desde fuera del cluster), exponemos el despliegue creando un objeto `Service` de tipo `NodePort`. Este tipo de servicio abre un puerto aleatorio en el rango predeterminado de Kubernetes (`30000-32767`) en **todos** los nodos del cluster (tanto en el control plane `k8s-master` como en el worker `k8s-worker1`):

```bash
kubectl expose deployment nginx-test --port=80 --type=NodePort
```

Listamos los servicios activos en el cluster para identificar el puerto `NodePort` asignado:

```bash
kubectl get services -o wide
```

**Salida real de terminal:**
```text
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE   SELECTOR
kubernetes   ClusterIP   10.96.0.1     <none>        443/TCP        34h   <none>
nginx-test   NodePort    10.98.102.4   <none>        80:30482/TCP   10m   app=nginx-test
```

> [!NOTE]
> En la columna `PORT(S)` observamos el mapeo `80:30482/TCP`. El puerto interno del contenedor es el `80`, mientras que el puerto expuesto en los nodos del cluster es el `30482`. En su entorno de laboratorio este puerto se asignará de manera aleatoria entre el 30000 y el 32767.

---

### 5.4 Verificación de Conectividad HTTP y Acceso Externo

Dado que el servicio `NodePort` publica el puerto en todos los nodos del cluster, podemos consultar cualquiera de las IPs de la red Host-Only (`192.168.56.0/24`) para acceder al servicio.

#### 1. Identificación de las IPs de los Nodos
Listamos los nodos del cluster y sus direcciones IP internas:

```bash
kubectl get nodes -o wide
```

**Salida real de terminal:**
```text
NAME          STATUS   ROLES           AGE   VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
k8s-master    Ready    control-plane   34h   v1.31.14   192.168.56.10   <none>        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
k8s-worker1   Ready    <none>          34h   v1.31.14   192.168.56.11   <none>        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
```

#### 2. Acceso desde el Navegador Web
Desde el navegador del equipo anfitrión físico, podemos acceder a cualquiera de las dos URLs:
* `http://192.168.56.10:30482/` (IP del nodo master)
* `http://192.168.56.11:30482/` (IP del nodo worker)

#### 3. Verificación mediante cURL en Consola
Comprobamos el acceso mediante `curl` apuntando a ambas IPs:

```bash
curl http://192.168.56.10:30482/
```

**Salida de respuesta:**
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy,
API gateway, load balancer, content cache, or other features.</p>

<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Comprobación contra el worker:
```bash
curl http://192.168.56.11:30482/
```

**Salida de respuesta:**
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy,
API gateway, load balancer, content cache, or other features.</p>

<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

> [!TIP]
> Aunque el contenedor de Nginx está ejecutándose físicamente en el nodo worker (`k8s-worker1` en `10.244.1.2`), la petición dirigida a la IP del master (`192.168.56.10:30482`) responde con éxito. Esto es posible gracias a `kube-proxy` y al plugin de red CNI Flannel, que enrutan el tráfico entre nodos a través de reglas iptables e interfaces de túnel VXLAN de manera transparente.

---

### 5.5 Acceso Temporal mediante Port-Forward y Limpieza de Recursos

Además de exponer un servicio mediante `NodePort`, Kubernetes permite redirigir tráfico de forma temporal para pruebas y depuración inmediata utilizando el comando `kubectl port-forward`. Este comando abre un túnel directo desde un puerto local hacia el Pod o Deployment sin necesidad de un objeto Service:

```bash
kubectl port-forward deployment/nginx-test 8080:80 --address 0.0.0.0
```

**Salida real del comando:**
```text
Forwarding from 0.0.0.0:8080 -> 80
```

Con este túnel activo, podemos comprobar el servicio accediendo a `http://localhost:8080` o a la IP del nodo en el puerto `8080`.

#### Limpieza de Recursos de Prueba
Una vez concluidas las pruebas de validación, procedemos a eliminar tanto el Deployment como el Service creados para dejar el cluster en su estado original:

```bash
kubectl delete deployment,svc nginx-test
```

---

## 6. Resolución de Problemas Frecuentes (Troubleshooting)

### Error 1: "The connection to the server 10.0.2.15:6443 was refused"
* **Causa:** No se configuró `--apiserver-advertise-address=192.168.56.10` al ejecutar `kubeadm init`, y el apiserver intentó anunciarse con la IP NAT compartida.
* **Solución:** Reiniciar la configuración con `sudo kubeadm reset -f` y volver a inicializar especificando explícitamente `--apiserver-advertise-address=192.168.56.10`.

### Error 2: "CoreDNS se queda indefinidamente en estado ContainerCreating o Pending"
* **Causa:** El plugin de red (CNI) no ha sido instalado o se ha vinculado a la tarjeta errónea.
* **Solución:** Aplicar el CNI Flannel con el parámetro `--iface=enp0s8`. Comprobar con `kubectl get pods -n kube-system -l k8s-app=flannel`.

### Error 3: "kubelet fails with cgroup driver mismatch"
* **Causa:** `containerd` se instaló sin configurar `SystemdCgroup = true` en `/etc/containerd/config.toml`.
* **Solución:** Modificar la directiva a `SystemdCgroup = true` y reiniciar el servicio con `sudo systemctl restart containerd && sudo systemctl restart kubelet`.

### Error 4: "Worker node not found or cannot connect to master:6443"
* **Causa:** Cortafuegos activo en el master bloqueando el puerto 6443 o IP de Host-Only no alcanzable.
* **Solución:** En el master, verificar `sudo ufw status` (debe estar inactivo o permitir el puerto 6443: `sudo ufw allow 6443/tcp`) y hacer ping a `192.168.56.10` desde el worker.

### Error 5: Desalojo de Pods (Evicted) por DiskPressure y Particionamiento LVM por Defecto

* **Síntomas y Alerta en el Kubelet:**
  En el Kubernetes Dashboard o ejecutando `kubectl get pods -A` se observan pods en estado `Failed` o `Evicted` (frecuentemente los pods de `kubernetes-dashboard`). Al consultar los eventos del pod o del nodo (`kubectl describe node k8s-worker1` o `journalctl -u kubelet`), se evidencia un mensaje similar al siguiente:
  ```text
  The node was low on resource: ephemeral-storage. Threshold quantity: 1569603441, available: 1356228Ki.
  Container kubernetes-dashboard was using 1084Ki, request is 0, has larger consumption of ephemeral-storage.
  ```
  **Desglose técnico del mensaje:**
  * **ephemeral-storage:** Es el almacenamiento en disco local del nodo utilizado para las capas de escritura de contenedores, logs de pods y volúmenes `emptyDir`.
  * **Threshold quantity (~1.46 GiB):** Umbral mínimo de espacio libre que exige el `kubelet` (por defecto suele ser el 10%-15% del sistema de archivos raíz montado en `/`). Al caer por debajo de este límite, se activa la condición de presión de disco (`DiskPressure`).
  * **available (~1.29 GiB):** Espacio libre real remanente en el nodo. Ante el déficit de espacio, el kubelet comienza a desalojar pods para evitar el colapso del sistema operativo.
  * **Container request is 0:** El contenedor desalojado no es necesariamente el culpable de agotar el disco. Sin embargo, al no disponer de una reserva mínima (`requests.ephemeral-storage` igual a 0), cualquier consumo supera su cuota y el planificador lo selecciona como primer candidato para desalojo.

* **Causa Raíz:**
  Al instalar Ubuntu Server 22.04 LTS seleccionando el particionado guiado por defecto con LVM (*"Set up this disk as an LVM group"* en el instalador Subiquity), el instalador no asigna el 100% del disco al volumen lógico raíz (`ubuntu-lv`). Por diseño de ingeniería, solo entrega aproximadamente la mitad (o un mínimo de 10 GB) dentro del Volume Group (`ubuntu-vg`), reservando el resto como espacio libre no asignado para posibles instantáneas (*snapshots*) o particiones separadas:
  * En la VM worker (disco de 20 GB): la partición `sda3` dispone de 18.2 GB, pero `ubuntu-lv` solo tiene 10.0 GB (quedando ~8.2 GB en reserva sin asignar).
  * En la VM master (disco de 25 GB): la partición `sda3` dispone de 23 GB, pero `ubuntu-lv` solo tiene 11.5 GB (quedando 11.5 GB en reserva sin asignar).
  `kubeadm` no modifica ni particiona discos. Al descargarse las imágenes de los contenedores base, Flannel y Kubernetes Dashboard, el espacio libre desciende bajo el umbral del 10% y salta la protección de `ephemeral-storage`.

* **Diagnóstico en los Nodos:**
  Acceder vía SSH a la máquina virtual afectada (por ejemplo, el nodo worker):
  ```bash
  ssh k8sworker1@192.168.56.11
  ```
  Verificar la capacidad del sistema de archivos raíz (`/`):
  ```bash
  df -h /
  ```
  Salida representativa:
  ```text
  Filesystem                         Size  Used Avail Use% Mounted on
  /dev/mapper/ubuntu--vg-ubuntu--lv  9.7G  7.2G  1.5G  83% /
  ```
  Comprobar la jerarquía de bloques y el espacio no asignado en el disco con `lsblk`:
  ```bash
  lsblk
  ```
  Salida representativa:
  ```text
  NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
  sda                         8:0    0   20G  0 disk 
  ├─sda1                      8:1    0    1M  0 part 
  ├─sda2                      8:2    0  1.8G  0 part /boot
  └─sda3                      8:3    0 18.2G  0 part 
    └─ubuntu--vg-ubuntu--lv 253:0    0 10.0G  0 lvm  /
  ```

* **Solución en Caliente (Aplicar en Worker y Master):**
  1. Extender el volumen lógico LVM para ocupar el 100% del espacio libre disponible en el Volume Group:
     ```bash
     sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
     ```
  2. Redimensionar en caliente el sistema de archivos ext4 (en línea, sin reiniciar ni desmontar):
     ```bash
     sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
     ```
  3. Confirmar que el sistema de archivos raíz dispone ahora de la totalidad del disco asignado:
     ```bash
     df -h /
     ```
     *(En `k8s-worker1` el tamaño pasará de 9.7 GB a ~18.2 GB utilizables; en `k8s-master` pasará de 11.5 GB a ~23.0 GB utilizables).*

* **Limpieza de Pods Desalojados:**
  Una vez ampliado el espacio, limpiar los pods que quedaron en estado `Failed` o `Evicted` para que el controlador despliegue nuevas réplicas sanas:
  ```bash
  kubectl delete pods -n kubernetes-dashboard --field-selector=status.phase=Failed
  ```
  *(Opcional: purgar todos los pods en estado fallido del cluster)*:
  ```bash
  kubectl delete pods --all-namespaces --field-selector=status.phase=Failed
  ```
