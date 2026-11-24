# Design: Documentación del Diagnóstico y Resolución de Particionamiento LVM y DiskPressure

## Context

Ver `proposal.md` para la motivación general del cambio. La guía técnica de instalación de Kubernetes se mantiene de forma dual en el repositorio:
1. Archivo fuente en Markdown: `docs/k8s-installation-steps.md`.
2. Archivo script generador de HTML/PDF: `scripts/generate_html_pdf.py`, que contiene la plantilla HTML y la estructura de navegación `OUTLINE_STRUCTURE` utilizada para compilar `docs/k8s-installation-steps.html` y `k8s-installation-steps.pdf`.

El apartado 6 de la guía contiene actualmente cuatro casos típicos de error (Error 1 a Error 4). La incorporación del problema de LVM requiere coherencia estilística, técnica y tipográfica con el resto del manual.

## Goals / Non-Goals

**Goals:**
- Añadir formalmente el "Error 5: Desalojo de Pods (Evicted) por DiskPressure y Particionamiento LVM por Defecto" en el apartado 6 de `docs/k8s-installation-steps.md`.
- Explicar detalladamente:
  1. Síntomas y mensajes de alerta del kubelet (`ephemeral-storage`).
  2. Diagnóstico del sistema mediante `df -h /` y `lsblk`.
  3. Causa técnica en el instalador Subiquity de Ubuntu Server (reserva del 50% en el Volume Group).
  4. Pasos exactos de resolución en caliente con `lvextend -l +100%FREE` y `resize2fs` tanto para el nodo worker (`k8s-worker1`) como para el master (`k8s-master`).
  5. Limpieza de pods en estado Failed/Evicted con `kubectl delete pods --field-selector=status.phase=Failed`.
- Actualizar el índice general en la Tabla de Contenidos de `docs/k8s-installation-steps.md`.
- Sincronizar el script `scripts/generate_html_pdf.py` incorporando el HTML estilizado y el identificador en `OUTLINE_STRUCTURE`.
- Compilar los entregables finales (`docs/k8s-installation-steps.html` y `k8s-installation-steps.pdf`).

**Non-Goals:**
- No modificar los scripts de aprovisionamiento desatendido con Vagrant (`scripts/*.sh`), ya que las cajas base en la nube/Vagrant no emplean el instalador interactivo Subiquity ni bloquean el 50% de disco libre.
- No alterar la configuración por defecto de los umbrales de desalojo del kubelet (eviction thresholds); se mantiene el comportamiento estándar de Kubernetes de producción.

## Decisions

### Decisión 1: Estructura del Error 5 en la Guía
Se adoptará una estructura didáctica homogénea con el resto de la guía pero con mayor profundidad técnica:
- **Causa:** Explicación precisa de la coexistencia de Subiquity (reserva de VG en LVM) y Kubernetes (`ephemeral-storage` DiskPressure).
- **Diagnóstico paso a paso:** Comandos `ssh`, `df -h /` y `lsblk` con salidas de terminal reales.
- **Resolución en caliente:** Comandos `lvextend` y `resize2fs` sin reinicio de la máquina.
- **Limpieza de Pods:** Explicación del flag `--field-selector=status.phase=Failed`.

*Alternativas consideradas:*
- Incluir un script bash automático: Se descarta para priorizar el valor formativo de que el alumno entienda el esquema de volúmenes lógicos y ejecute los comandos conscientemente.

### Decisión 2: Sincronización en `scripts/generate_html_pdf.py`
Se insertará un bloque `<div class="alert alert-important">` o sección `<h3>` estilizada dentro del contenedor `<h2 id="sec-6">` del script, y se agregará la entrada correspondiente en la lista jerárquica `OUTLINE_STRUCTURE` para que los lectores PDF mantengan los marcadores interactivos.

## Risks / Trade-offs

- **[Riesgo] Discrepancia en los nombres de volúmenes LVM en entornos personalizados.**
  → *Mitigación:* Se especificará explícitamente en el texto cómo identificar la ruta del dispositivo mediante `df -h /` antes de ejecutar `lvextend`, señalando la ruta predeterminada `/dev/mapper/ubuntu--vg-ubuntu--lv`.
- **[Riesgo] Dependencias de generación de PDF en el entorno local.**
  → *Mitigación:* Se validará la ejecución de `python3 scripts/generate_html_pdf.py` comprobando que las librerías `weasyprint` y `pypdf` estén operativas o reporten resultados limpios.
