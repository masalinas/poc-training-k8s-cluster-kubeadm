# Design: Enriquecimiento e Ilustración de la Instalación de Kubernetes Dashboard

## Context

La guía `docs/k8s-installation-steps.md` cuenta actualmente con una descripción básica del Kubernetes Dashboard en el apartado 2.11. El usuario ha suministrado la guía detallada `/home/miguel/temp/07_README_INSTALL_DASHBOARD.md` con comandos de verificación y salidas de consola reales, junto a dos capturas gráficas (`/home/miguel/temp/k8s_dashboard_login.png` y `/home/miguel/temp/k8s_dashboard.png`).

## Goals / Non-Goals

**Goals:**
- Actualizar el apartado 2.11 de `docs/k8s-installation-steps.md` estructurando el procedimiento completo:
  - Despliegue de manifiesto v2.7.0 con salida real detallada.
  - Verificación intermedia de pods (`dashboard-metrics-scraper` y `kubernetes-dashboard`).
  - Creación declarativa del manifiesto `dashboard-adminuser.yaml` (`ServiceAccount` y `ClusterRoleBinding` cluster-admin).
  - Verificación de la cuenta `admin-user`.
  - Generación del token Bearer con salida real.
  - Ejecución de `kubectl proxy` y acceso a la URL del proxy.
  - Autenticación y navegación ilustrada con las dos imágenes del Dashboard.
- Crear el directorio `docs/images/` y alojar de forma permanente `k8s_dashboard_login.png` y `k8s_dashboard.png`.
- Adaptar `scripts/generate_html_pdf.py` para renderizar adecuadamente las imágenes y compilar `k8s-cluster-kubeadm.pdf`.

**Non-Goals:**
- Configurar balanceadores de carga tipo LoadBalancer o Ingress con TLS público para el Dashboard (se preserva el mecanismo oficial de acceso vía `kubectl proxy`).
- Modificar scripts de automatización de Vagrant (`scripts/master.sh`).

## Decisions

### Decisión 1: Organización de recursos estáticos (imágenes)
- **Elección:** Crear `docs/images/` y copiar allí `k8s_dashboard_login.png` y `k8s_dashboard.png`.
- **Razón:** Mantiene la documentación autocontenida en el repositorio y accesible tanto para visualizadores Markdown en GitHub/GitLab como para navegadores y generadores HTML.

### Decisión 2: Estructura de secciones en la guía técnica
- **Elección:** Extraer el Dashboard de la subsección 2.11 (donde el despliegue manual termina en 2.10 con la fusión de kubeconfig) y promoverlo a sección independiente:
  - `## 4. Sección 3: Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard` (subapartados 4.1 a 4.7).
  - `## 5. Sección 4: Ejemplo Práctico de Despliegue en el Cluster (Nginx)` (subapartados 5.1 a 5.5).
  - `## 6. Resolución de Problemas Frecuentes (Troubleshooting)`.
- **Razón:** Satisface la petición explícita del usuario de conceder al Dashboard una sección propia previa al ejemplo práctico de Nginx, desacoplándolo del proceso manual de inicialización base y presentándolo como un componente de gestión de nivel superior aplicable tanto al despliegue manual como al automatizado con Vagrant.

### Decisión 3: Maquetación de imágenes para exportación PDF
- **Elección:** En `scripts/generate_html_pdf.py` incluir estilos CSS específicos para figuras:
  - `.dashboard-figure`: contenedor con centrado, borde suave, sombra y `page-break-inside: avoid`.
  - `.figure-caption`: texto explicativo en tipografía secundaria.
  - Uso de rutas absolutas `file://` en la compilación headless de Chrome para garantizar la carga instantánea de imágenes locales sin bloqueos de origen cruzado.

## Risks / Trade-offs

- **[Paginación y corte de imágenes en el PDF]** → Se aplicará `page-break-inside: avoid` en las figuras para evitar que las capturas de pantalla se dividan entre dos páginas consecutivas.
