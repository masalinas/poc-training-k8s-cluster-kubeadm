# Design: Arquitectura y Pipeline del Manual de Instalación K8s (Manual y Vagrant)

## Context

Para la creación del primer capítulo del curso sobre Kubernetes en producción (ver `proposal.md` - Why), se debe formalizar la arquitectura de infraestructura virtualizada, la configuración técnica de red, la automatización con Vagrant y el pipeline de compilación del documento final en formato PDF (`k8s-cluster-kubeadm.pdf`). El documento se estructurará en dos secciones: Sección 1 (Manual) y Sección 2 (Automatizada con Vagrant).

## Goals / Non-Goals

**Goals:**
- Establecer una arquitectura de laboratorio virtualizada en VirtualBox 7.0 que sea 100% reproducible y aislada de los cambios de red física (Wi-Fi, cambios de IP en host).
- Documentar los comandos precisos y diferenciados tipográficamente para la Sección 1: preparación manual de los nodos, instalación de componentes modernos de Kubernetes (v1.31) y despliegue del Dashboard.
- Diseñar la Sección 2 con un `Vagrantfile` multi-nodo y scripts shell de aprovisionamiento desatendidos (`provision-common.sh`, `provision-master.sh`, `provision-worker.sh`) para desplegar el laboratorio completo mediante un único comando `vagrant up`.
- Definir el método de maquetación y generación del PDF `k8s-cluster-kubeadm.pdf` integrando ambas secciones de forma clara y profesional.

**Non-Goals:**
- Despliegue de Alta Disponibilidad (HA) multi-master (etcd externo / HAProxy), priorizando la viabilidad de recursos en los equipos de los alumnos.
- Utilización de herramientas de orquestación complejas como Ansible o Terraform para esta entrega, priorizando Shell scripting transparente dentro de Vagrant para facilitar la lectura del código por parte de los alumnos.

## Decisions

### Decisión 1: Topología de Red en VirtualBox (Doble Adaptador: NAT + Host-Only)
- **Elección:** 
  - Adaptador 1: NAT (permite salida a internet para `apt`, repositorios e imágenes de contenedor).
  - Adaptador 2: Host-Only (`vboxnet0`, `192.168.56.0/24`) con IPs fijas (`192.168.56.10` para Master, `192.168.56.11` para Worker).
- **Razón:** La red Puente (Bridged) suele fallar en entornos de alumnos cuando se conectan por Wi-Fi o cuando el router asigna IPs dinámicas variables. La red Host-Only proporciona estabilidad absoluta e IPs fijas entre el Host Ubuntu 20.04 y las VMs.
- **Alternativas consideradas:** Red NAT con reenvío de puertos (más compleja de configurar por alumnos), Modo Puente (inestable en Wi-Fi).

### Decisión 2: Repositorios Oficiales Comunitarios (`pkgs.k8s.io`) y Kubernetes v1.31
- **Elección:** Utilizar `https://pkgs.k8s.io/core:/stable:/v1.31/deb/`.
- **Razón:** El repositorio legacy de Google (`apt.kubernetes.io`) fue congelado y retirado en 2024. `v1.31` es la versión estable de referencia actual compatible con Ubuntu 22.04 LTS.
- **Alternativas consideradas:** Versiones anteriores (v1.28 o v1.29) que ya se acercan al fin de soporte.

### Decisión 3: Runtime de Contenedores (`containerd` con `SystemdCgroup = true`)
- **Elección:** `containerd` estándar con `SystemdCgroup = true` explícito en `/etc/containerd/config.toml`.
- **Razón:** Estándar de la industria tras la eliminación de dockershim en Kubernetes v1.24. La alineación del driver cgroup con systemd es obligatoria para evitar que kubelet falle al iniciar.
- **Alternativas consideradas:** CRI-O (menos común en distribuciones Debian/Ubuntu estándar para principiantes), Docker Engine con cri-dockerd (añade complejidad innecesaria).

### Decisión 4: Plugin de Red (CNI) Flannel con detección explícita de interfaz
- **Elección:** Flannel con Pod CIDR `10.244.0.0/16` e inyección de `--iface=enp0s8`.
- **Razón:** Con dos tarjetas de red en VirtualBox, los plugins de red suelen vincularse por error al adaptador NAT (`10.0.2.15`). Forzar la interfaz `enp0s8` garantiza que el tráfico entre pods viaje por la red Host-Only. Además, evita la colisión de CIDR que provocaría Calico si usara su rango por defecto (`192.168.0.0/16`) sobre la red Host-Only (`192.168.56.0/24`).
- **Alternativas consideradas:** Calico (requiere editar Tigera Operator / Custom Resources para cambiar CIDR e interfaz).

### Decisión 5: Automatización con Vagrant (Sección 2)
- **Elección:** `Vagrantfile` multi-máquina con box `ubuntu/jammy64`, asignación de IPs privadas (`192.168.56.10` y `192.168.56.11`), y aprovisionamiento modular mediante scripts shell en directorio `scripts/`:
  - `scripts/common.sh`: Instalación de dependencias base, desactivación de SWAP, sysctl, containerd y paquetes Kubernetes.
  - `scripts/master.sh`: `kubeadm init`, CNI Flannel, exportación del comando de unión a `/vagrant/.join-cmd.sh`, y copia de `admin.conf` a la carpeta compartida.
  - `scripts/worker.sh`: Espera a la generación de `/vagrant/.join-cmd.sh` y ejecución del join.
- **Razón:** Vagrant define el orden secuencial de arranque (master primero, worker después), permitiendo que la sincronización del token ocurra a través de la carpeta montada `/vagrant` sin necesidad de servidores externos.
- **Alternativas consideradas:** Terraform (más orientado a nubes públicas), Ansible solo (requiere que las VMs ya existan).

### Decisión 6: Generación y Maquetación del PDF (`k8s-cluster-kubeadm.pdf`)
- **Elección:** Maquetación del documento en HTML5/CSS3 profesional con soporte `@page`, fuentes del sistema, cajas de notas visuales, bloques de comandos coloreados y exportación a PDF mediante motor Chromium / Chrome Headless (`--headless --print-to-pdf`).
- **Razón:** Produce un acabado gráfico editorial sin requerir la instalación pesada de LaTeX, garantizando que el diseño y la separación visual de comandos y texto sea exacta tanto para la Sección 1 como para la Sección 2.
- **Alternativas consideradas:** Pandoc con LaTeX (requiere cientos de megabytes en paquetes TeX), LibreOffice CLI (conversión menos controlada a nivel de estilos CSS).

## Risks / Trade-offs

- **[Risk] Conflicto de MACs al clonar VMs en VirtualBox** → *Mitigation*: Incluir advertencia explícita en la Sección 1 manual para marcar la opción "Generar nuevas direcciones MAC". En Vagrant esto se gestiona automáticamente.
- **[Risk] Reactivación de SWAP tras reinicio de la VM** → *Mitigation*: Desactivar con `swapoff -a` y comentar permanentemente la línea de swap en `/etc/fstab` (tanto en manual como en scripts de Vagrant).
- **[Risk] CNI Flannel seleccionando la interfaz NAT** → *Mitigation*: Modificar explícitamente el archivo de despliegue `kube-flannel.yml` con el parámetro `--iface=enp0s8`.
- **[Risk] Sincronización temporal en Vagrant (worker arranca antes de que el master termine `kubeadm init`)** → *Mitigation*: Incluir en `scripts/worker.sh` un bucle de espera activa comprobando la existencia de `/vagrant/.join-cmd.sh`.
