# Design: Integración Visual de Creación de VMs en VirtualBox

## Context

Actualmente, la sección 2.2 de la guía técnica detalla los requerimientos de hardware y red para las máquinas virtuales `k8s-master` y `k8s-worker1` únicamente mediante texto y tablas descriptivas. El usuario ha aportado 41 capturas de pantalla reales que documentan de principio a fin la creación de la red sólo-anfitrión (`step_00.png`), la creación y particionado de la VM master (20 capturas en `/home/miguel/temp/kubeadm/master/`) y de la VM worker (20 capturas en `/home/miguel/temp/kubeadm/worker/`).

Ver `proposal.md` para la motivación y objetivos generales.

## Goals / Non-Goals

**Goals:**
- Almacenar las 41 imágenes dentro del repositorio bajo `docs/images/` (`step_00.png`, `docs/images/master/step_01.png` a `step_20.png`, y `docs/images/worker/step_01.png` a `step_20.png`).
- Reestructurar la sección 2.2 de `docs/k8s-installation-steps.md` incorporando:
  1. La imagen `step_00.png` con la explicación para crear la red privada `vboxnet0`.
  2. Los 20 pasos visuales de la VM `k8s-master` con sus explicaciones contextuales.
  3. Los 20 pasos visuales de la VM `k8s-worker1` con sus explicaciones contextuales.
- Actualizar `scripts/generate_html_pdf.py` con clases CSS dedicadas (`.step-figure`, `.step-caption`) con control de salto de página (`page-break-inside: avoid`) para evitar cortes a mitad de imagen.
- Compilar y validar el documento final `k8s-cluster-kubeadm.pdf`.

**Non-Goals:**
- No se modifican los pasos de configuración del sistema operativo ni de kubeadm (subsecciones 2.3 a 2.10).
- No se alteran los scripts de Vagrant (Sección 2) ni el ejemplo de despliegue de Nginx (Sección 4).

## Decisions

### 1. Estructura de Directorios para Imágenes
- **Decisión:** Alojar `step_00.png` en `docs/images/` y crear subdirectorios específicos `docs/images/master/` y `docs/images/worker/`.
- **Razón:** Mantiene una separación limpia entre los activos generales y los pasos específicos de cada nodo, evitando colisiones de nombres (`step_01.png` existe para ambos nodos).
- **Alternativa descartada:** Renombrar todas las imágenes a un único prefijo plano (`master_step_01.png`). Se prefiere mantener la estructura modular original.

### 2. Organización de Subsecciones en 2.2
- **Decisión:** Subdividir la sección 2.2 en tres apartados secuenciales:
  - `2.2.1 Creación de la Red Solo-Anfitrión en VirtualBox (step_00.png)`
  - `2.2.2 Asistente Visual Paso a Paso para la VM Master (k8s-master)` (Pasos 1 al 20)
  - `2.2.3 Asistente Visual Paso a Paso para la VM Worker (k8s-worker1)` (Pasos 1 al 20)
- **Razón:** Respeta escrupulosamente el orden pedagógico solicitado por el usuario (red -> master -> worker).

### 3. Maquetación y Control de Paginación en PDF
- **Decisión:** Usar etiquetas semánticas `<figure class="step-figure"><img ...><figcaption class="step-caption">...</figcaption></figure>` con estilos:
  ```css
  .step-figure {
    page-break-inside: avoid;
    text-align: center;
    margin: 18px 0;
  }
  .step-figure img {
    max-width: 92%;
    height: auto;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  }
  .step-caption {
    font-size: 8.5pt;
    color: #4b5563;
    font-style: italic;
    margin-top: 6px;
  }
  ```
- **Razón:** Evita que Chromium corte imágenes horizontalmente entre páginas y garantiza una lectura limpia y agradable.

## Risks / Trade-offs

- **[Riesgo: Incremento del tamaño del archivo PDF]** → 41 imágenes de entre 10 KB y 180 KB aumentarán el PDF en aproximadamente 3-5 MB. Dado que la distribución es digital y el peso resultante rondará los 6-8 MB, es un equilibrio idóneo entre calidad gráfica y ligereza.
- **[Riesgo: Salto de página huérfano entre caption e imagen]** → Se mitiga fijando `page-break-inside: avoid` sobre el elemento contenedor `<figure>`.
