# Tasks

## 1. Preparación y Organización de Activos Gráficos

- [x] 1.1 Copiar `/home/miguel/temp/kubeadm/step_00.png` a `docs/images/step_00.png` y verificar su presencia e integridad.
- [x] 1.2 Crear el directorio `docs/images/master/` y copiar las 20 imágenes desde `/home/miguel/temp/kubeadm/master/`, verificando la existencia de los 20 archivos (`step_01.png` a `step_20.png`).
- [x] 1.3 Crear el directorio `docs/images/worker/` y copiar las 20 imágenes desde `/home/miguel/temp/kubeadm/worker/`, verificando la existencia de los 20 archivos (`step_01.png` a `step_20.png`).

## 2. Actualización de la Documentación Markdown

- [x] 2.1 Reestructurar la sección 2.2 de `docs/k8s-installation-steps.md` para incorporar en primer término la imagen `step_00.png` con la explicación detallada de la creación de la red `vboxnet0` en VirtualBox.
- [x] 2.2 Incorporar en la sección 2.2 de `docs/k8s-installation-steps.md` la secuencia completa de 20 imágenes de la VM `k8s-master` con notas explicativas al pie de cada paso del asistente e instalador.
- [x] 2.3 Incorporar en la sección 2.2 de `docs/k8s-installation-steps.md` la secuencia completa de 20 imágenes de la VM `k8s-worker1` con notas explicativas al pie de cada paso del asistente e instalador.

## 3. Actualización de Plantilla HTML y Compilación PDF

- [x] 3.1 Actualizar `scripts/generate_html_pdf.py` con estilos CSS `.step-figure` y `.step-caption` que eviten saltos de página indebidos (`page-break-inside: avoid`) e integrar el bloque HTML de las 41 imágenes en la subsección 2.2.
- [x] 3.2 Ejecutar `python3 scripts/generate_html_pdf.py` para regenerar `docs/k8s-installation-steps.html` y compilar `k8s-cluster-kubeadm.pdf`, verificando que el script finalice con código de salida 0.

## 4. Verificación de Calidad

- [x] 4.1 Validar que las 41 figuras e imágenes se rendericen con nitidez en el documento PDF y que no existan enlaces rotos ni solapamientos visuales.
