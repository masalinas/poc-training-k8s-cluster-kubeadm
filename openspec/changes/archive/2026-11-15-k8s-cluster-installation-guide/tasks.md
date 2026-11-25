# Tasks: Guía de Instalación de Kubernetes en Producción (Manual y con Vagrant)

## 1. Sección 1: Elaboración de la Guía de Despliegue Manual

- [x] 1.1 Redactar la guía completa de instalación manual paso a paso: descarga de ISO de Ubuntu Server 22.04 LTS, creación y dimensionamiento de VMs en VirtualBox 7.0, configuración de red Dual (NAT + Host-Only), desactivación permanente de SWAP, parámetros sysctl y módulos de red, configuración de containerd con SystemdCgroup, instalación de kubeadm/kubelet/kubectl v1.31 desde `pkgs.k8s.io`, inicialización del cluster, CNI Flannel con `--iface=enp0s8`, unión del nodo worker, configuración remota de kubectl y despliegue del Dashboard con autenticación por token.
- [x] 1.2 Revisar y validar que todos los comandos y configuraciones de la sección manual utilicen estilos visuales y bloques diferenciados del texto conceptual con sus respectivas notas de alerta.

## 2. Sección 2: Desarrollo y Documentación de la Automatización con Vagrant

- [x] 2.1 Crear el `Vagrantfile` multi-nodo definiendo las especificaciones de `k8s-master` (2 vCPUs, 3 GB RAM, IP 192.168.56.10) y `k8s-worker1` (2 vCPUs, 2 GB RAM, IP 192.168.56.11) con el proveedor VirtualBox y la box `ubuntu/jammy64`.
- [x] 2.2 Crear los scripts de aprovisionamiento shell (`scripts/common.sh`, `scripts/master.sh`, `scripts/worker.sh`) implementando la instalación desatendida, generación del comando join en carpeta compartida `/vagrant` y verificación de espera activa en el worker.
- [x] 2.3 Redactar la sección explicativa de Vagrant detallando la estructura del Vagrantfile, los comandos de ciclo de vida (`vagrant up`, `vagrant status`, `vagrant ssh`, `vagrant destroy`) y cómo conectarse con kubectl desde el host tras la automatización.

## 3. Maquetación y Generación del Documento PDF

- [x] 3.1 Diseñar la plantilla de presentación HTML/CSS con soporte para impresión A4 conteniendo ambas secciones (Manual y Vagrant), índice estructurado, diagramas de arquitectura en bloques destacados y estilos contrastados para comandos monospace.
- [x] 3.2 Compilar y generar el documento final `k8s-cluster-kubeadm.pdf` en la raíz del espacio de trabajo utilizando Google Chrome Headless (`--headless --print-to-pdf`).
- [x] 3.3 Verificar la existencia, integridad y paginación del archivo `k8s-cluster-kubeadm.pdf` resultante comprobando que contiene las dos secciones completas.
