# Design: Token Permanente para Kubernetes Dashboard

## Context

En Kubernetes moderno (v1.24+ y v1.31), la API genera tokens temporales firmados por el API Server mediante `kubectl create token`, los cuales expiran por defecto a los 60 minutos. En entornos educativos o de pruebas locales sobre VirtualBox/Vagrant, tener que regenerar y copiar el token periódicamente interrumpe la experiencia de uso.

La API de Kubernetes permite definir declarativamente un `Secret` especial con el tipo `kubernetes.io/service-account-token` y la anotación `kubernetes.io/service-account.name: "admin-user"`. Al aplicar dicho manifiesto, el plano de control genera e incrusta un token JWT permanente en el campo `.data.token` del secreto.

Ver `proposal.md` para la motivación general.

## Goals / Non-Goals

**Goals:**
- Añadir al final de la subsección 4.5 en `docs/k8s-installation-steps.md` el bloque descriptivo para la creación del token permanente.
- Documentar el manifiesto `admin-user-secret.yaml`:
  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: admin-user-secret
    namespace: kubernetes-dashboard
    annotations:
      kubernetes.io/service-account.name: "admin-user"
  type: kubernetes.io/service-account-token
  ```
- Documentar el comando de extracción y decodificación:
  `kubectl get secret admin-user-secret -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d`
- Incluir una advertencia explícita (`[!WARNING]` / `.alert-warning`) indicando que esta práctica no es segura en entornos productivos al carecer de caducidad y rotación automática, pero es admitida por comodidad en el laboratorio local.
- Sincronizar la plantilla HTML y estilos en `scripts/generate_html_pdf.py` y recompilar `k8s-cluster-kubeadm.pdf`.

**Non-Goals:**
- No eliminar el método estándar de generación temporal `kubectl -n kubernetes-dashboard create token admin-user`. El token permanente se presenta como alternativa de laboratorio complementaria.

## Decisions

### 1. Ubicación en el Flujo Documental
- **Decisión:** Situar el contenido al final de la subsección 4.5 (`4.5 Generación del Token de Autenticación Bearer`), inmediatamente antes de pasar al paso 4.6 (`Acceso Seguro mediante Kubectl Proxy`).
- **Razón:** El alumno ya habrá comprendido el mecanismo moderno de tokens temporales de Kubernetes antes de conocer la alternativa persistente para laboratorios.

### 2. Formato de la Advertencia de Seguridad
- **Decisión:** Utilizar un bloque de advertencia (`[!WARNING]` en Markdown y `.alert-warning` en HTML) titulado *"Consideración de Seguridad: Token Permanente vs Producción"*.
- **Razón:** Deja meridianamente claro al alumno que en entornos productivos los tokens deben tener caducidad estricta y auditoría RBAC.

## Risks / Trade-offs

- **[Riesgo: Mala práctica exportada a producción]** → Se mitiga enfatizando tanto en el texto como en el cuadro de advertencia que desde Kubernetes v1.24 los secrets de tokens automáticos fueron retirados precisamente para prevenir credenciales estáticas de larga duración.
