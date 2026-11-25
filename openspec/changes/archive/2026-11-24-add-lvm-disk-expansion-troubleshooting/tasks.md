# Tasks

## 1. Actualización de la Guía de Instalación (Markdown)

- [x] 1.1 Redactar la subsección "Error 5: Desalojo de Pods (Evicted) por DiskPressure y Particionamiento LVM por Defecto" en la sección 6 de `docs/k8s-installation-steps.md` incluyendo síntomas (`ephemeral-storage`), diagnóstico con `df -h /` y `lsblk`, causa técnica de Ubuntu Server LVM, comandos de expansión en caliente (`lvextend`, `resize2fs`) para worker y master, y limpieza de pods con `kubectl delete pods --field-selector=status.phase=Failed`.
- [x] 1.2 Actualizar la Tabla de Contenidos de `docs/k8s-installation-steps.md` incorporando el enlace a la nueva subsección de Error 5 y comprobar que la jerarquía de encabezados se mantenga coherente.

## 2. Sincronización del Generador y Compilación de Entregables (HTML / PDF)

- [x] 2.1 Actualizar el archivo `scripts/generate_html_pdf.py` agregando la plantilla HTML del Error 5 en la sección 6 e incorporando el elemento correspondiente en el array `OUTLINE_STRUCTURE` para los marcadores interactivos del PDF.
- [x] 2.2 Ejecutar `python3 scripts/generate_html_pdf.py` y verificar que se compilen exitosamente `docs/k8s-installation-steps.html` y `k8s-cluster-kubeadm.pdf`.

## 3. Validación y Control de Calidad

- [x] 3.1 Comprobar visualmente que el documento Markdown y el archivo PDF compilado incluyan la nueva sección sin errores tipográficos, con formato de código correcto y con la terminología técnica adecuada.
