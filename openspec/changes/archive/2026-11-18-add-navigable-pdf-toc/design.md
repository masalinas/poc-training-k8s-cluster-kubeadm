# Design

## Context

El documento de laboratorio consta de más de 50 páginas y abarca arquitectura, aprovisionamiento de VMs, configuración de red, instalación de containerd, kubeadm, Vagrant IaC, Kubernetes Dashboard y despliegue de Nginx. 

Actualmente, el archivo `scripts/generate_html_pdf.py` define una tabla de contenidos (`<div class="toc">`) maquetada estéticamente, pero compuesta de elementos de texto plano (`<li>`) sin etiquetas de hipervínculo `<a>`, y las cabeceras de sección en el cuerpo del documento carecen de atributos `id`. Aunque Chromium traduce automáticamente los enlaces `<a href="#id">` a anotaciones de enlace interno en el PDF (`GoTo`), la ausencia de enlaces e IDs impide dicha navegación.

Para detalles sobre la motivación y alcance, consultar `proposal.md`.

## Goals / Non-Goals

**Goals:**
- Proporcionar navegación interactiva e instantánea mediante clics desde el Índice General del archivo PDF generado (`k8s-cluster-kubeadm.pdf`) y del HTML (`docs/k8s-installation-steps.html`).
- Asignar atributos `id` normalizados y consistentes a todas las secciones (`h2`), subsecciones (`h3`) y apartados de imágenes (`h4`) en `scripts/generate_html_pdf.py`.
- Integrar hipervínculos `<a>` en todos los ítems (`.toc-item`) y subítems (`.toc-subitem`) del índice apuntando a los anclajes correspondientes.
- Configurar reglas tipográficas CSS para `.toc a` que mantengan la apariencia profesional del manual (sin subrayados toscos ni colores incompatibles con la paleta del curso).
- Alinear el índice de `docs/k8s-installation-steps.md` para que los subapartados también sean navegables en visores de Markdown.

**Non-Goals:**
- No alterar los comandos técnicos, manifiestos YAML, parámetros del cluster ni el contenido explicativo.
- No modificar la disposición de doble imagen por página (`.step-pair`) ni el flujo de paginación existente.

## Decisions

### 1. Esquema de nomenclatura de identificadores (`id`)
- **Decisión**: Utilizar IDs sintéticos, limpios y jerárquicos basados en la numeración de los apartados:
  - Secciones principales: `id="sec-1"`, `id="sec-2"`, `id="sec-3"`, `id="sec-4"`, `id="sec-5"`, `id="sec-6"`.
  - Subsecciones: `id="sec-1-1"`, `id="sec-1-2"`, `id="sec-2-1"`, `id="sec-2-2"`, etc.
  - Subapartados de capturas: `id="sec-2-2-1"`, `id="sec-2-2-2"`, `id="sec-2-2-3"`.
- **Justificación**: Los slugs derivados de títulos con tildes, símbolos o paréntesis (por ejemplo, `#221-creación-de-la-red-solo-anfitrión-(step_00png)`) pueden causar inconsistencias de codificación o fallos en ciertos visores de PDF (como lectores embebidos o visores antiguos). Los IDs alfanuméricos simples garantizan compatibilidad universal del estándar PDF (`/GoTo`).
- **Alternativa descartada**: Slugs dinámicos basados en texto completo.

### 2. Ubicación de los atributos `id`
- **Decisión**: Añadir `id="sec-..."` directamente en la etiqueta de cabecera (`<h2 id="...">`, `<div class="section-banner" id="...">`, `<h3 id="...">`, `<h4 id="...">`).
- **Justificación**: El visor de PDF posiciona el visor exactamente en la coordenada vertical del elemento que contiene el `id`. Ponerlo en la cabecera asegura que el título quede visible en la parte superior tras el salto.

### 3. Estilos tipográficos de `.toc a`
- **Decisión**:
  ```css
  .toc a {
    color: inherit;
    text-decoration: none;
    transition: color 0.15s ease;
  }
  .toc a:hover {
    color: #326ce5;
    text-decoration: underline;
  }
  ```
- **Justificación**: Heredar el color evita que el PDF muestre el clásico azul de hipervínculo web estándar en cada línea, preservando la jerarquía visual de `.toc-item` (azul marino negrita) y `.toc-subitem` (gris pizarra), mientras que en HTML permite interactividad al pasar el cursor.

### 4. Sincronización en Markdown
- **Decisión**: Añadir enlaces relativos a las subsecciones del índice en `docs/k8s-installation-steps.md` utilizando slugs estándar de GitHub Markdown para mantener consistencia multiplataforma.

### 5. Inyección de Marcadores Jerárquicos en el PDF (Document Outlines)
- **Decisión**: Añadir una etapa de post-procesamiento en `scripts/generate_html_pdf.py` utilizando la biblioteca `pypdf`. Tras compilar el PDF con Chrome headless:
  1. Abrir el PDF generado con `pypdf.PdfReader`.
  2. Extraer las páginas destino de cada anclaje a partir de los `named_destinations` que Chromium genera automáticamente para los `id` de las cabeceras (`/sec-1`, `/sec-1-1`, etc.).
  3. Crear un `pypdf.PdfWriter`, clonar el documento y construir el árbol jerárquico de bookmarks (`add_outline_item`) asociando títulos principales y subsecciones a sus respectivas páginas de destino.
  4. Sobrescribir el PDF final con la versión enriquecida con el diccionario `/Outlines`.
- **Justificación**: Chromium headless no genera la estructura de marcadores `/Outlines` de forma nativa a partir de encabezados HTML al imprimir. El post-procesado con `pypdf` es liviano, rápido (< 1 segundo), no altera las imágenes ni el texto vectorizado, y asegura que visores como Chrome PDF Viewer, Evince, Adobe Acrobat y Apple Preview muestren el menú en su panel lateral.

## Risks / Trade-offs

- **[Riesgo]**: Desalineación entre un enlace del TOC y el ID de destino en el documento.
  - **Mitigación**: Revisión sistemática 1 a 1 de cada elemento del TOC frente a su cabecera en el cuerpo de `scripts/generate_html_pdf.py` y comprobación automatizada de enlaces válidos.
- **[Riesgo]**: Enlaces no reconocidos por Chromium al imprimir en PDF.
  - **Mitigación**: Chromium preserva enlaces `<a href="#id">` siempre que el elemento destino exista en el DOM al momento del renderizado. Se verificará con `pdftotext` / inspección del PDF resultante.
