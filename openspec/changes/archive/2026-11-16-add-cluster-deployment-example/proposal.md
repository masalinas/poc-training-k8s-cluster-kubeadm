# Proposal: Inclusión de Ejemplo Práctico de Despliegue en el Cluster (Nginx)

## Why

Tras completar la instalación del cluster de Kubernetes (tanto de forma manual como automatizada con Vagrant), los alumnos necesitan un ejemplo práctico guiado que valide el funcionamiento de la infraestructura desplegada (programación de pods, red CNI Flannel y exposición externa mediante NodePort). La incorporación de este ejemplo en una nueva Sección 4 del documento y guía técnica proporciona un flujo de verificación end-to-end con comandos y salidas reales verificadas.

## What Changes

- **Integración del Ejemplo de Despliegue en la Sección 4:** Incorporación de un nuevo capítulo en `docs/k8s-installation-steps.md` estructurado en la Sección 4 (desplazando Troubleshooting a la Sección 5), que incluye:
  - Despliegue de servicio Nginx (`kubectl create deployment nginx-test --image=nginx`).
  - Inspección exhaustiva de recursos creados en el namespace por defecto (`deployments`, `replicasets` y `pods` con `-o wide`).
  - Exposición del despliegue a través de un servicio `NodePort` en el puerto 80 (`kubectl expose deployment ... --type=NodePort`).
  - Consulta del servicio (`kubectl get services -o wide`) e identificación del puerto asignado en el rango 30000-32767.
  - Verificación del acceso desde el anfitrión o navegador usando las IPs de los nodos (`192.168.56.10` y `192.168.56.11`) mediante peticiones HTTP (curl y navegador web) y validación de la página de bienvenida de Nginx.
- **Actualización del Índice y Estructura:** Actualización de la Tabla de Contenidos de `docs/k8s-installation-steps.md` y reordenación de la sección de Resolución de Problemas (Troubleshooting) a la Sección 5.
- **Sincronización de Formatos de Publicación:** Actualización de `scripts/generate_html_pdf.py` para reflejar la nueva sección y regeneración de `docs/k8s-installation-steps.html` y del PDF compilado `k8s-cluster-kubeadm.pdf`.

## Capabilities

### New Capabilities
- `cluster-sample-deployment`: Requisitos funcionales y de verificación para el despliegue de una carga de trabajo de prueba (Nginx), inspección de recursos nativos de Kubernetes, exposición mediante servicio NodePort y validación de conectividad HTTP externa a través de las IPs de los nodos del cluster.

### Modified Capabilities
*Ninguna.*

## Impact

- Documentación técnica: modificación de `docs/k8s-installation-steps.md`.
- Scripts de generación de entregables: actualización de `scripts/generate_html_pdf.py`.
- Entregables generados: actualización de `docs/k8s-installation-steps.html` y recompilación de `k8s-cluster-kubeadm.pdf`.
