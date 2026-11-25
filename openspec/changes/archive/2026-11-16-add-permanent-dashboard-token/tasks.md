# Tasks

## 1. Actualización de la Documentación Markdown

- [x] 1.1 Incorporar al final de la sección 4.5 en `docs/k8s-installation-steps.md` el manifiesto `admin-user-secret.yaml`, el comando de aplicación `kubectl apply` y la extracción del token permanente decodificado en Base64.
- [x] 1.2 Añadir en la sección 4.5 de `docs/k8s-installation-steps.md` el bloque de advertencia (`[!WARNING]`) sobre las consideraciones de seguridad del token permanente frente a entornos productivos y su conveniencia para el laboratorio local.

## 2. Actualización de Plantilla HTML y Compilación PDF

- [x] 2.1 Actualizar la subsección 4.5 en `scripts/generate_html_pdf.py` con el manifiesto `admin-user-secret.yaml`, comandos formateados y el bloque `.alert-warning`.
- [x] 2.2 Ejecutar `python3 scripts/generate_html_pdf.py` para regenerar `docs/k8s-installation-steps.html` y compilar `k8s-cluster-kubeadm.pdf`, verificando que el script finalice con código de salida 0.

## 3. Verificación de Calidad

- [x] 3.1 Comprobar mediante extracción y validación de texto que el contenido del token permanente y su alerta de seguridad están correctamente renderizados en el documento PDF.
