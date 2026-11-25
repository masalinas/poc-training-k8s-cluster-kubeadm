# Proposal: Guía de Instalación de Kubernetes en Producción (Manual y con Vagrant)

## Why

Para el desarrollo del primer capítulo de un curso de formación sobre Kubernetes en producción, se requiere un documento técnico exhaustivo, preciso y 100% reproducible por los alumnos. El entorno simula un entorno productivo utilizando un host Ubuntu 20.04 con VirtualBox 7.0 y dos máquinas virtuales con Ubuntu Server 22.04 LTS (1 nodo Master y 1 nodo Worker) configuradas con `kubeadm`, runtime `containerd`, CNI de red y el Dashboard de Kubernetes. 

Para maximizar el valor formativo, la guía se dividirá en dos secciones principales:
1. **Sección 1 (Instalación Manual):** Los alumnos aprenden paso a paso los fundamentos, configuración de red en VirtualBox, módulos de kernel, runtime containerd, inicialización del plano de control, unión del worker y despliegue del Dashboard.
2. **Sección 2 (Automatización con Vagrant):** Los alumnos aprenden a automatizar todo el proceso anterior como código (IaC) mediante un `Vagrantfile` y scripts de provisión desatendida.

El entregable final debe compilarse en un documento PDF profesional denominado `k8s-cluster-kubeadm.pdf`.

## What Changes

- Creación de la **Sección 1 (Manual)** con pasos exactos para la descarga de ISOs, creación manual de VMs en VirtualBox (CPU, RAM, Disco, red dual NAT + Host-Only), desactivación de SWAP, ajustes de kernel (`sysctl`, módulos `overlay`/`br_netfilter`), instalación de `containerd` con `SystemdCgroup = true`, e instalación de `kubeadm`, `kubelet` y `kubectl` desde los repositorios oficiales modernos `pkgs.k8s.io` (v1.31).
- Inicialización manual del plano de control con `kubeadm init`, configuración del CNI Flannel con fijación a la interfaz de red Host-Only, unión del nodo Worker y configuración de `kubectl` tanto en el Master como en la máquina Host física.
- Configuración y despliegue del Dashboard de Kubernetes con cuenta de servicio administrativa y token de autenticación.
- Creación de la **Sección 2 (Automatización con Vagrant)** con un `Vagrantfile` multi-nodo y scripts shell de aprovisionamiento (`provision-common.sh`, `provision-master.sh`, `provision-worker.sh`) para desplegar el cluster completo de forma desatendida con `vagrant up`.
- Maquetación y generación del documento final en PDF titulado `k8s-cluster-kubeadm.pdf`, con tipografía diferenciada para comandos, bloques de código, diagramas y notas de advertencia.

## Capabilities

### New Capabilities
- `cluster-installation`: Especificación técnica y pasos reproducibles para el aprovisionamiento manual de las VMs y el despliegue del cluster con `kubeadm` v1.31, runtime `containerd`, CNI Flannel y Dashboard.
- `vagrant-automation`: Aprovisionamiento automatizado de la infraestructura y configuración del cluster mediante `Vagrantfile` multi-máquina y scripts de aprovisionamiento desatendidos.
- `pdf-generation`: Pipeline y plantillas de diseño para la compilación del contenido técnico completo en el documento final `k8s-cluster-kubeadm.pdf`.

### Modified Capabilities
*Ninguna (proyecto inicial).*

## Impact

- Creación de documentación reproducible y código de automatización (Vagrantfile + scripts) en el repositorio.
- Generación del artefacto PDF compilado `k8s-cluster-kubeadm.pdf` en la raíz del proyecto.
