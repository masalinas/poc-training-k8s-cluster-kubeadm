# Tasks

## 1. Preparación del Entorno Base de Laboratorio

- [x] 1.1 Documentar la configuración de distribución de teclado y locale en español (`localectl set-x11-keymap es pc105` y `loadkeys es`) en la guía técnica manual y verificar su correcta redacción.
- [x] 1.2 Incorporar el procedimiento paso a paso para la creación previa de la red Host-Only `vboxnet0` en las herramientas de red de VirtualBox y la configuración de las interfaces NAT y Host-Only con modo promiscuo en Permitir todo.
- [x] 1.3 Documentar la desactivación de la gestión de red en `cloud-init` mediante `/etc/cloud/cloud-init.disabled` y la configuración persistente de Netplan en `/etc/netplan/50-cloud-init.yaml` para master (`192.168.56.10`) y worker1 (`192.168.56.11`).

## 2. Dependencias del Sistema y Ejecución de Kubeadm

- [x] 2.1 Actualizar `scripts/common.sh` y la guía manual con la instalación obligatoria de los paquetes `conntrack` y `socat` antes del inicio del cluster, verificando la ausencia de preflight errors.
- [x] 2.2 Integrar en la guía la descarga y modificación limpia del manifiesto `kube-flannel.yml` (fijando `--iface=enp0s8`) y la salida completa y real de terminal de `kubeadm init` en el nodo master.
- [x] 2.3 Documentar los requisitos previos de worker1 y la salida completa y real de terminal de `kubeadm join` verificando la incorporación del nodo.

## 3. Conexión Remota No Destructiva desde el Host

- [x] 3.1 Documentar el procedimiento de extracción de `~/.kube/config` desde el master y su fusión segura en el host anfitrión mediante edición de bloques YAML y mediante el comando `kubectl config view --flatten`.
- [x] 3.2 Documentar la fijación del contexto `kubernetes-admin@kubernetes` y los comandos de verificación remota de salud y nodos (`kubectl cluster-info` y `kubectl get nodes -o wide`).

## 4. Actualización de Fuentes y Compilación del PDF

- [x] 4.1 Reestructurar y redactar los capítulos actualizados en `docs/k8s-installation-steps.md` manteniendo la separación entre la Sección 1 (Manual) y la Sección 2 (Automatizada).
- [x] 4.2 Actualizar el archivo HTML `docs/k8s-installation-steps.html` y el script generador `scripts/generate_html_pdf.py`, garantizando el escape de entidades HTML (`&gt;&gt;`, `&lt;&lt;EOF`, etc.) y estilos CSS anti-desbordamiento sin barras de scroll.
- [x] 4.3 Ejecutar el pipeline de compilación `python3 scripts/generate_html_pdf.py` y validar la correcta generación del archivo entregable `k8s-cluster-kubeadm.pdf` en la raíz del proyecto.

## Workflow follow-up

- Archivar el cambio tras la validación final del PDF y de los scripts por parte del usuario.
