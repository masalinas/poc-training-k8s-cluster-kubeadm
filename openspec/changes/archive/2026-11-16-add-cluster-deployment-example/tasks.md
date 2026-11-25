# Tasks

## 1. Actualización del Documento Markdown

- [x] 1.1 Actualizar la Tabla de Contenidos en `docs/k8s-installation-steps.md` incorporando la Sección 4 y sus subapartados, y renumerando Troubleshooting a Sección 5, verificando la coherencia de los anclajes de navegación.
- [x] 1.2 Redactar e incorporar la Sección 4 (`## 4. Sección 3: Ejemplo Práctico de Despliegue en el Cluster (Nginx)`) en `docs/k8s-installation-steps.md` a partir del contenido de `/home/miguel/temp/SAMPLE.md`, estructurando los pasos de creación de deployment, inspección de recursos (`deployments`, `rs`, `pods`), exposición `NodePort` y verificación HTTP con `curl` y navegador, incluyendo salidas reales de terminal.
- [x] 1.3 Renumerar la sección de Resolución de Problemas a Sección 5 (`## 5. Resolución de Problemas Frecuentes (Troubleshooting)`) en `docs/k8s-installation-steps.md`, verificando la numeración uniforme de cabeceras.
- [x] 1.4 Incorporar el subapartado 4.5 en `docs/k8s-installation-steps.md` (y su enlace en el índice) con la opción de exposición temporal mediante `kubectl port-forward` y la eliminación de recursos de prueba (`kubectl delete deployment,svc nginx-test`).

## 2. Actualización del Generador HTML y Compilación PDF

- [x] 2.1 Actualizar `scripts/generate_html_pdf.py` para integrar la nueva Sección 4 en la plantilla HTML y renumerar la Sección 5 de Troubleshooting, aplicando las clases de estilo tipográfico para bloques de comandos y terminales.
- [x] 2.2 Ejecutar `python3 scripts/generate_html_pdf.py` para regenerar `docs/k8s-installation-steps.html` y compilar el documento final `k8s-cluster-kubeadm.pdf`, verificando que el script finalice con código de retorno 0 y el PDF exista en la raíz del proyecto.
- [x] 2.3 Actualizar `scripts/generate_html_pdf.py` para integrar la subsección 4.5 de `port-forward` y borrado de recursos, y recompilar el entregable `k8s-cluster-kubeadm.pdf`.

## 3. Verificación de Calidad y Consistencia

- [x] 3.1 Contrastar que todos los comandos, parámetros e información técnica de `/home/miguel/temp/SAMPLE.md` están fielmente reflejados en la documentación técnica generada.
- [x] 3.2 Validar que el PDF resultante contiene el índice actualizado y las páginas maquetadas correctamente sin desbordamiento de bloques de texto o código.
