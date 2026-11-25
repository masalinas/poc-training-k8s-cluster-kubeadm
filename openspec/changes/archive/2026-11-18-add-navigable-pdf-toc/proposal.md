# Proposal

## Why

Actualmente, el documento `k8s-cluster-kubeadm.pdf` (de más de 50 páginas) cuenta con una sección de «Índice General», pero sus elementos son texto plano estático sin hipervínculos internos. Tampoco las cabeceras de sección del HTML disponen de identificadores unívocos (`id`). Como resultado, los alumnos y lectores no pueden navegar directamente haciendo clic en los apartados del índice, lo que dificulta la consulta rápida y la experiencia de lectura en un manual técnico extenso.

Hacer el índice completamente navegable tanto en el HTML como en el PDF compilado resuelve este problema, permitiendo saltar con un solo clic a cualquier sección o subsección relevante.

## What Changes

- **Asignación de identificadores de anclaje (`id`) unívocos**: Dotar a cada sección principal (`h2`), subsección (`h3`) y subapartado (`h4`) relevante en `scripts/generate_html_pdf.py` de un atributo `id` semántico y estandarizado (por ejemplo, `id="sec-1"`, `id="sec-2-2"`, etc.).
- **Hipervínculos interactivos en el Índice General**: Envolver cada ítem (`.toc-item`) y subítem (`.toc-subitem`) del `<div class="toc">` en etiquetas `<a>` con referencias a dichos anclajes (`href="#sec-..."`).
- **Estilos de navegación en PDF y HTML**: Añadir reglas CSS para `.toc a` para garantizar una lectura limpia, tipografía profesional integrada (sin subrayados toscos por defecto, manteniendo colores acordes a la guía) y comportamiento consistente en pantalla e impresión PDF.
- **Generación de Marcadores de Documento (PDF Outlines) para el Panel Lateral**: Incorporar un paso posterior a la compilación en `scripts/generate_html_pdf.py` mediante la librería `pypdf` para inyectar el árbol jerárquico de navegación (`/Outlines`) en el archivo PDF, de modo que cualquier visor de PDF muestre el índice en su panel lateral.
- **Sincronización en la documentación Markdown**: Actualizar los enlaces de subsección en el índice de `docs/k8s-installation-steps.md` para que los lectores en repositorios Git y visores Markdown también disfruten de navegación directa a las subsecciones.
- **Recompilación del entregable PDF**: Ejecutar el script generador para producir `k8s-cluster-kubeadm.pdf` con todos los hipervínculos PDF internos activos y marcadores de esquema en el panel lateral.

## Capabilities

### New Capabilities
*(Ninguna)*

### Modified Capabilities
- `pdf-generation`: Se actualizan los requisitos de compilación de la guía en PDF para exigir que, además del índice interno maquetado, el documento contenga marcadores PDF nativos (outlines/bookmarks) jerárquicos visibles y navegables desde el panel lateral de cualquier visor de documentos.

## Impact

- **Archivos afectados**:
  - `scripts/generate_html_pdf.py`: Añade IDs a las secciones/subsecciones, hipervínculos en el TOC y estilos CSS asociados.
  - `docs/k8s-installation-steps.html`: Regenerado con el índice interactivo.
  - `k8s-cluster-kubeadm.pdf`: Recompilado con anotaciones de enlace interno clicables en visores PDF.
  - `docs/k8s-installation-steps.md`: Actualización de enlaces en la tabla de contenidos para alineación de experiencia de lectura.
- **Rendimiento y compatibilidad**: Sin impacto negativo en tamaño de archivo ni dependencias adicionales; el motor de renderizado de Chromium convierte automáticamente los hipervínculos relativos internos `<a href="#id">` en acciones GoTo directas del formato PDF estándar.
