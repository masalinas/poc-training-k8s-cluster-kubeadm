# Tasks

## 1. Preparación de Activos Gráficos

- [x] 1.1 Crear el directorio `docs/images/` y copiar los archivos `/home/miguel/temp/k8s_dashboard_login.png` y `/home/miguel/temp/k8s_dashboard.png`, verificando que ambos archivos queden alojados en el repositorio.

## 2. Actualización del Documento Markdown

- [x] 2.1 Reestructurar `docs/k8s-installation-steps.md` extrayendo el contenido de Dashboard de la subsección 2.11 y configurándolo como la nueva Sección 3 (`## 4. Sección 3: Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard`), renumerando Nginx a Sección 4 (`## 5. Sección 4: Ejemplo Práctico de Despliegue en el Cluster (Nginx)`) y Troubleshooting al capítulo 6, actualizando la Tabla de Contenidos.

## 3. Actualización de Estilos y Generación HTML/PDF

- [x] 3.1 Actualizar `scripts/generate_html_pdf.py` para reflejar la Sección 3 de Dashboard con su banner y figuras, renumerar la Sección 4 de Nginx y la Sección 6 de Troubleshooting.
- [x] 3.2 Ejecutar `python3 scripts/generate_html_pdf.py` para regenerar `docs/k8s-installation-steps.html` y compilar `k8s-cluster-kubeadm.pdf`, verificando que el script finalice con código de salida 0 y el PDF se genere correctamente.

## 4. Verificación de Calidad

- [x] 4.1 Comprobar que todos los comandos, salidas reales y manifiestos de `/home/miguel/temp/07_README_INSTALL_DASHBOARD.md` están reflejados fielmente en la documentación técnica.
- [x] 4.2 Validar que el documento PDF compilado renderice las dos imágenes con resolución nítida y sin desbordamiento ni saltos de página inadecuados.
