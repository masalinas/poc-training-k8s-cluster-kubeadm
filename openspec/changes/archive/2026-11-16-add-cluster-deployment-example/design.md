# Design: Integración del Ejemplo de Despliegue en el Cluster

## Context

La guía técnica `docs/k8s-installation-steps.md` contiene la documentación completa del laboratorio de Kubernetes:
- Capítulo 1: Arquitectura del Laboratorio.
- Capítulo 2: Sección 1: Despliegue Manual Paso a Paso con Kubeadm.
- Capítulo 3: Sección 2: Automatización Completa con Vagrant (IaC).
- Capítulo 4: Resolución de Problemas Frecuentes (Troubleshooting).

El usuario solicita incorporar un ejemplo práctico de despliegue definido en `/home/miguel/temp/SAMPLE.md` en la sección 4 del documento. El documento se compila además a HTML y PDF mediante el script `scripts/generate_html_pdf.py`.

## Goals / Non-Goals

**Goals:**
- Estructurar e incorporar el ejemplo de `/home/miguel/temp/SAMPLE.md` como la nueva Sección 4 del documento: `## 4. Sección 3: Ejemplo Práctico de Despliegue en el Cluster (Nginx)`.
- Reordenar la sección de "Resolución de Problemas Frecuentes (Troubleshooting)" como Sección 5 (`## 5. Resolución de Problemas Frecuentes (Troubleshooting)`).
- Actualizar la Tabla de Contenidos al inicio de la guía reflejando la nueva sección y sus subapartados.
- Adaptar las explicaciones breves e inglés informal de `SAMPLE.md` a la prosa técnica pedagógica en español que caracteriza el resto de la guía, manteniendo los comandos y salidas reales de consola íntegros.
- Actualizar `scripts/generate_html_pdf.py` para sincronizar `docs/k8s-installation-steps.html` y compilar el entregable final `k8s-cluster-kubeadm.pdf`.

**Non-Goals:**
- Modificar scripts de infraestructura (`scripts/master.sh`, `scripts/worker.sh`, `scripts/common.sh`) o el `Vagrantfile`.
- Configurar controladores Ingress, almacenamiento persistente (PV/PVC) ni certificados SSL en este ejemplo (se mantiene el alcance en un despliegue básico + NodePort según `SAMPLE.md`).

## Decisions

### Decisión 1: Estructura y numeración de secciones
- **Elección:** Titular la sección como `## 4. Sección 3: Ejemplo Práctico de Despliegue en el Cluster (Nginx)` y reubicar Troubleshooting como `## 5. Resolución de Problemas Frecuentes (Troubleshooting)`.
- **Alternativa considerada:** Añadir el ejemplo como subapartado dentro de la Sección 2. Se descartó porque el despliegue es agnóstico del método de creación del cluster (sirve tanto para el cluster creado manualmente como para el creado con Vagrant) y el usuario solicitó explícitamente ubicarlo en la sección 4.
- **Subsecciones planificadas:**
  - `4.1 Creación del Deployment de Nginx`: `kubectl create deployment nginx-test --image=nginx`
  - `4.2 Inspección de Recursos en el Cluster`: `kubectl get deployments,rs,pods -o wide`
  - `4.3 Exposición Externa mediante Servicio NodePort`: `kubectl expose deployment nginx-test --port=80 --type=NodePort` y `kubectl get services -o wide`
  - `4.4 Verificación de Conectividad HTTP desde el Anfitrión`: consulta a través de IPs Host-Only (`192.168.56.10:<NodePort>` y `192.168.56.11:<NodePort>`) mediante navegador y `curl`.
  - `4.5 Exposición Temporal con Port-Forward y Limpieza de Recursos`: uso alternativo de `kubectl port-forward deployment/nginx-test 8080:80 --address 0.0.0.0` para pruebas directas y borrado con `kubectl delete deployment,svc nginx-test`.

### Decisión 2: Enriquecimiento pedagógico manteniendo fidelidad a SAMPLE.md
- **Elección:** Conservar las salidas exactas de consola documentadas en `SAMPLE.md` (nombres de pods, hash del replicaset, puerto 30482, respuesta HTML de Nginx), pero añadir contexto didáctico:
  - Explicación de cómo funciona el selector de etiquetas `app=nginx-test`.
  - Explicación del funcionamiento de `NodePort` y el rango predeterminado de Kubernetes (`30000-32767`).
  - Aclaración de que la petición responde en cualquier nodo del cluster (master o worker) gracias al enrutamiento de red de `kube-proxy`.

### Decisión 3: Flujo de actualización de artefactos
- **Elección:** Actualizar primero `docs/k8s-installation-steps.md`, trasladar los cambios al generador `scripts/generate_html_pdf.py` y compilar `k8s-cluster-kubeadm.pdf` con validación de existencia y tamaño.

## Risks / Trade-offs

- **[Variación del puerto NodePort en ejecuciones reales del alumno]** → Se incluirá una advertencia indicando que el puerto `30482` es el asignado aleatoriamente en el ejemplo, pero en su ejecución el puerto puede variar dentro del rango 30000-32767.
- **[Ruptura del formato visual en la generación del PDF]** → Se mantendrán los estilos CSS de `.code-block`, `.terminal-output` y cajas de alerta compatibles con la herramienta de maquetación en `scripts/generate_html_pdf.py`.
