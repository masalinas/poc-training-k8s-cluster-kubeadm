# Tasks

## 1. Plantilla HTML, Identificadores de Anclaje y Estilos del Índice

- [x] 1.1 Añadir en `scripts/generate_html_pdf.py` las reglas CSS para `.toc a` garantizando herencia tipográfica de color, eliminación de subrayado por defecto y realce en hover para visualización web y exportación PDF.
- [x] 1.2 Incorporar atributos `id` jerárquicos y unívocos (`sec-1`, `sec-1-1`, `sec-2`, `sec-2-1`, `sec-2-2`, `sec-2-2-1`... `sec-6`) a todas las cabeceras de sección principal (`h2`), banners divisores, subsecciones (`h3`) y apartados de capturas (`h4`) en `scripts/generate_html_pdf.py`.
- [x] 1.3 Transformar cada entrada (`.toc-item`) y subentrada (`.toc-subitem`) del bloque `<div class="toc">` en un hipervínculo `<a href="#sec-...">` apuntando exactamente a los anclajes asignados.

## 2. Sincronización en la Documentación Markdown

- [x] 2.1 Actualizar la sección de «Tabla de Contenidos» en `docs/k8s-installation-steps.md` incorporando enlaces a las subsecciones para habilitar la navegación interactiva también en visores Markdown y repositorios Git.

## 3. Compilación y Validación de Navegación en PDF y HTML

- [x] 3.1 Ejecutar `python3 scripts/generate_html_pdf.py` para regenerar `docs/k8s-installation-steps.html` y compilar `k8s-cluster-kubeadm.pdf`, verificando salida exitosa con código de retorno 0.
- [x] 3.2 Inspeccionar y validar la presencia de enlaces internos funcionales en el índice del documento PDF compilado y comprobar la ausencia de saltos de página anómalos o desbordamientos visuales.

## 4. Inyección de Marcadores de PDF (Outlines) para el Panel Lateral

- [x] 4.1 Implementar la función de adición de marcadores jerárquicos (Document Outlines) en `scripts/generate_html_pdf.py` utilizando `pypdf` para extraer destinos y construir el árbol de navegación.
- [x] 4.2 Recompilar `k8s-cluster-kubeadm.pdf` y verificar la existencia del diccionario `/Outlines` y la correcta jerarquía y numeración de páginas en el panel lateral.
