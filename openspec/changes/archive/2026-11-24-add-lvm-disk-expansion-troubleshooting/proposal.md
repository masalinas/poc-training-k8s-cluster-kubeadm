# Proposal: Sección de Resolución de Problemas de Particionamiento LVM y DiskPressure

## Why

Al instalar Ubuntu Server 22.04 con el particionamiento LVM guiado por defecto (Subiquity), el sistema operativo solo asigna aproximadamente el 50% del disco virtual al volumen lógico raíz (`ubuntu-lv`) y reserva el resto en el Volume Group sin asignar. En entornos de laboratorio con discos ajustados (20 GB para worker y 25 GB para master), la descarga de imágenes de contenedores y componentes como el Kubernetes Dashboard hace que el espacio libre caiga rápidamente por debajo del umbral del 10%-15%, activando la condición de `DiskPressure` en el kubelet y provocando el desalojo intempestivo de pods (`ephemeral-storage` eviction). Es necesario documentar este problema, su causa raíz y su procedimiento de resolución en caliente en la guía de instalación para evitar bloqueos durante las prácticas de los alumnos.

## What Changes

- **Nueva subsección en el apartado 6 (Troubleshooting) de la guía (`docs/k8s-installation-steps.md`)**:
  - Explicación del mensaje de error real emitido por el kubelet al desalojar pods por `DiskPressure` y `ephemeral-storage`.
  - Diagnóstico mediante comandos del sistema operativo (`df -h /`, `lsblk`).
  - Causa técnica de la reserva de espacio no asignado en Ubuntu Server LVM.
  - Procedimiento de resolución paso a paso en caliente (`lvextend` y `resize2fs`) aplicable tanto al nodo worker como al nodo master.
  - Procedimiento de limpieza de pods desalojados (`kubectl delete pods --field-selector=status.phase=Failed`).
- **Actualización de la Tabla de Contenidos**:
  - Incorporar la nueva sección dentro del bloque 6 de Resolución de Problemas en `docs/k8s-installation-steps.md`.
- **Sincronización con el compilador de entregables (`scripts/generate_html_pdf.py`)**:
  - Incorporar el contenido en la plantilla HTML con el estilo corporativo de alertas de la guía.
  - Actualizar `OUTLINE_STRUCTURE` para incluir el marcador jerárquico del PDF interactivo.
  - Recompilar `docs/k8s-installation-steps.html` y `k8s-installation-steps.pdf`.

## Capabilities

### New Capabilities
*(Ninguna)*

### Modified Capabilities
- `cluster-installation`: Incorpora el requisito de diagnóstico, resolución y recuperación ante desalojo de pods por `DiskPressure` derivado del particionamiento parcial por defecto de LVM en Ubuntu Server.

## Impact

- **Documentación técnica:** Modificación de `docs/k8s-installation-steps.md`.
- **Herramientas de compilación y entregables:** Modificación de `scripts/generate_html_pdf.py` y regeneración de `docs/k8s-installation-steps.html` y `k8s-installation-steps.pdf`.
- **Scripts de aprovisionamiento:** No se alteran los scripts existentes; se trata de una ampliación documental y metodológica para alumnos del curso.
