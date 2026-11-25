# Proposal: Incorporación de Guía Visual Paso a Paso para la Creación de VMs en VirtualBox

## Why

El aprovisionamiento manual de máquinas virtuales en VirtualBox para un cluster de Kubernetes suele generar errores en los alumnos debido a configuraciones incorrectas en el tipo de red, particionado LVM, asignación de vCPUs o habilitación de SSH. Incluir capturas de pantalla reales paso a paso con explicaciones didácticas para la creación de la red interna, el nodo master y el nodo worker elimina la ambigüedad y facilita el seguimiento visual del laboratorio.

## What Changes

- **Captura de Creación de Red Sólo-Anfitrión:** Integración de la captura `step_00.png` en la guía técnica ilustrando la creación de la red `vboxnet0` desde la interfaz de VirtualBox.
- **Paso a Paso Visual para VM Master:** Inclusión de las 20 capturas secuenciales (`step_01.png` a `step_20.png`) alojadas en `docs/images/master/`, abarcando desde la definición de nombre y recursos de hardware (2 vCPUs, 3 GB RAM, 25 GB disco) hasta la instalación de Ubuntu Server 22.04.5 y el reinicio final, acompañadas de explicaciones concisas.
- **Paso a Paso Visual para VM Worker:** Inclusión de las 20 capturas secuenciales (`step_01.png` a `step_20.png`) alojadas en `docs/images/worker/`, detallando las especificaciones específicas (2 vCPUs, 2 GB RAM, 20 GB disco), configuración de adaptadores NAT + Host-Only y el asistente de instalación.
- **Reestructuración de la Sección 2.2:** Integración ordenada en la sección *2.2 Creación y Configuración de VMs en VirtualBox 7.0* de `docs/k8s-installation-steps.md` y `docs/k8s-installation-steps.html`.
- **Actualización de Scripts y Compilación:** Actualización del generador de PDF `scripts/generate_html_pdf.py` para soportar las nuevas 41 imágenes con diseño estructurado y recompilación de `k8s-cluster-kubeadm.pdf`.

## Capabilities

### New Capabilities
*Ninguna.*

### Modified Capabilities
- `cluster-installation`: Se enriquece el requisito `Aprovisionamiento y Red de Máquinas Virtuales` para exigir el acompañamiento visual paso a paso de la creación de la red y las máquinas virtuales master y worker en VirtualBox con sus respectivas explicaciones.

## Impact

- Nuevos archivos de imagen organizados en `docs/images/master/`, `docs/images/worker/` y `docs/images/step_00.png`.
- Modificación del documento Markdown `docs/k8s-installation-steps.md` en la subsección 2.2.
- Modificación de la plantilla HTML y estilos en `scripts/generate_html_pdf.py` para formatear adecuadamente las figuras y captions de las 41 imágenes.
- Recompilación del PDF entregable `k8s-cluster-kubeadm.pdf`.
