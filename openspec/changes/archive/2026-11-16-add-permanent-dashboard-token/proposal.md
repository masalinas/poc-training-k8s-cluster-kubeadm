# Proposal: Incorporación de Token Permanente para Kubernetes Dashboard

## Why

En Kubernetes moderno (v1.24+ y v1.31), los tokens generados mediante el comando `kubectl create token` son temporales y cuentan con una ventana de caducidad automática de 1 hora por defecto. Esto obliga al alumno a regenerar y copiar un nuevo token cada vez que reanuda sus pruebas en el Dashboard. Incorporar el procedimiento para generar un token no expirable mediante un objeto `Secret` dedicado permite mantener una sesión persistente por comodidad en entornos de prueba locales y laboratorios, documentando a su vez las advertencias de seguridad correspondientes frente a entornos productivos.

## What Changes

- **Manifiesto de Secret para Token Permanente:** Documentación del archivo `admin-user-secret.yaml` en el namespace `kubernetes-dashboard`, con tipo `kubernetes.io/service-account-token` y anotación `kubernetes.io/service-account.name: "admin-user"`.
- **Extracción y Decodificación del Secreto:** Incorporación del comando `kubectl get secret admin-user-secret -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d` para obtener la clave alfanumérica sin límite de expiración.
- **Advertencia de Seguridad:** Integración de una alerta destacando que los tokens permanentes carecen de rotación automática y conllevan riesgos de seguridad en producción, reservando su uso exclusivamente a comodidades de laboratorio y pruebas locales.
- **Actualización de Documentos y PDF:** Integración al cierre de la subsección 4.5 en `docs/k8s-installation-steps.md`, actualización de la plantilla HTML y estilos en `scripts/generate_html_pdf.py` y recompilación de `k8s-cluster-kubeadm.pdf`.

## Capabilities

### New Capabilities
*Ninguna.*

### Modified Capabilities
- `cluster-installation`: Se actualiza el requisito `Despliegue y Acceso al Dashboard de Kubernetes` para incluir el procedimiento declarativo de generación y extracción de tokens permanentes mediante Secret con sus correspondientes advertencias de seguridad.

## Impact

- Modificación de la subsección 4.5 en `docs/k8s-installation-steps.md`.
- Modificación de la subsección 4.5 en `scripts/generate_html_pdf.py`.
- Recompilación del documento PDF `k8s-cluster-kubeadm.pdf` y de `docs/k8s-installation-steps.html`.
