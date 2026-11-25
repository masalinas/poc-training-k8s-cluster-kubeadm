# Proposal: Enriquecimiento e Ilustración Gráfica de la Instalación de Kubernetes Dashboard

## Why

La sección de Kubernetes Dashboard en la guía técnica del cluster requiere actualizarse con los procedimientos reales completos recogidos en `/home/miguel/temp/07_README_INSTALL_DASHBOARD.md`. Es necesario documentar no solo el despliegue de componentes, sino las comprobaciones intermedias de salud de los pods y de la cuenta de servicio administrativa, así como incorporar evidencia gráfica real de la pantalla de inicio de sesión y del panel de control navegando por los recursos del namespace recién creado.

## What Changes

- **Procedimiento Detallado de Despliegue del Dashboard como Sección Propia:** Reorganización de la documentación en `docs/k8s-installation-steps.md` extrayendo el contenido de la subsección 2.11 y configurando una sección dedicada previa al ejemplo de Nginx:
  - Creación de la Sección 3: *Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard* (capítulo 4 de la guía) con los pasos detallados de `/home/miguel/temp/07_README_INSTALL_DASHBOARD.md`.
  - Reubicación del ejemplo de Nginx como Sección 4 (*Ejemplo Práctico de Despliegue en el Cluster (Nginx)*, capítulo 5 de la guía).
  - Renumeración del capítulo de Resolución de Problemas (Troubleshooting) al capítulo 6.
  - Despliegue del manifiesto oficial v2.7.0 con salida real detallada de creación de todos los recursos (namespace, cuentas de servicio, secretos, roles y deployments).
  - Verificación del estado de los pods (`dashboard-metrics-scraper` y `kubernetes-dashboard` en estado `Running`).
  - Creación del manifiesto declarativo `dashboard-adminuser.yaml` (`ServiceAccount` y `ClusterRoleBinding` con permisos `cluster-admin`).
  - Verificación de la cuenta de servicio administrativa con `kubectl get serviceaccount`.
  - Generación del token de autenticación Bearer con registro real de salida.
  - Ejecución de `kubectl proxy` en el equipo anfitrión y acceso por URL exacta.
- **Incorporación de Recursos Gráficos:**
  - Creación del directorio de activos `docs/images/` y copia de las imágenes:
    - `k8s_dashboard_login.png`: Captura de pantalla de la interfaz de inicio de sesión por token del Dashboard.
    - `k8s_dashboard.png`: Captura de pantalla del interior del Dashboard mostrando la carga de trabajo y recursos del namespace `kubernetes-dashboard`.
  - Inserción de ambas imágenes en el flujo didáctico del documento Markdown.
- **Actualización de Entregables:** Sincronización del generador `scripts/generate_html_pdf.py` para soportar las imágenes y regeneración de `docs/k8s-installation-steps.html` y del PDF compilado `k8s-cluster-kubeadm.pdf`.

## Capabilities

### New Capabilities
*Ninguna.*

### Modified Capabilities
- `cluster-installation`: Modifica el requisito `Despliegue y Acceso al Dashboard de Kubernetes` para exigir la verificación del estado de los pods del Dashboard, la creación declarativa y comprobación del ServiceAccount administrativo, y la confirmación visual del acceso mediante capturas de la pantalla de autenticación y de la vista interna de recursos.

## Impact

- Documentación: enriquecimiento de la sección correspondiente en `docs/k8s-installation-steps.md`.
- Activos del proyecto: nuevo directorio `docs/images/` conteniendo `k8s_dashboard_login.png` y `k8s_dashboard.png`.
- Scripts de publicación: adaptación de `scripts/generate_html_pdf.py` para renderizar las imágenes en HTML y PDF.
- Entregable final: recompilación de `k8s-cluster-kubeadm.pdf`.
