# Proposal: Enriquecimiento de la Guía Manual de Instalación de Kubernetes

## Why

Durante las pruebas reales de despliegue del cluster de Kubernetes sobre Ubuntu 22.04 y VirtualBox 7.0, se identificaron puntos críticos que causan fallos o bloqueos habituales en los alumnos: la distribución de teclado en inglés por defecto en Ubuntu Server, la necesidad de crear manualmente la red `vboxnet0` antes de crear las VMs, el riesgo de que `cloud-init` sobrescriba la configuración de Netplan, la falta de dependencias obligatorias del sistema (`conntrack` y `socat`) para kubelet/kubeadm, y la sobreescritura accidental del archivo `~/.kube/config` en el host cuando el alumno ya dispone de otros clusters. Es necesario enriquecer la guía técnica y el PDF para incorporar estos pasos probados y sus salidas reales de terminal.

## What Changes

- **Configuración de Idioma y Teclado:** Incorporación del paso inicial de configuración de distribución de teclado español (`localectl set-x11-keymap es pc105` y `loadkeys es`) tras iniciar sesión en las VMs de Ubuntu Server.
- **Creación Previa de Red en VirtualBox:** Detalle del procedimiento en la interfaz de VirtualBox (*Herramientas -> Redes*) para crear la red Host-Only `vboxnet0` antes de aprovisionar las VMs y fijar el modo promiscuo en *Permitir todo*.
- **Persistencia de Red y Desactivación de Cloud-Init:** Creación del archivo de bloqueo `/etc/cloud/cloud-init.disabled` y edición de `/etc/netplan/50-cloud-init.yaml` con verificación mediante `ip a`.
- **Dependencias de Red Obligatorias:** Instalación de `conntrack` y `socat` antes de ejecutar `kubeadm init` y `kubeadm join` en master y worker, documentando las razones técnicas e integrando los registros de salida reales obtenidos en consola.
- **Fusión Segura de Kubectl en el Host:** Sustitución de la sobreescritura destructiva de `~/.kube/config` por una metodología de integración y fusión (merge manual y CLI `kubectl config view --flatten`), preservando clusters existentes y fijando el contexto activo.
- **Actualización de Artefactos de Entrega:** Regeneración de `docs/k8s-installation-steps.md`, `docs/k8s-installation-steps.html`, scripts de automatización y el PDF compilado `k8s-cluster-kubeadm.pdf`.

## Capabilities

### New Capabilities
- `manual-lab-setup`: Requisitos y procedimientos verificables para la preparación del entorno de laboratorio: teclado español en consola, creación de `vboxnet0` en VirtualBox y persistencia de red con Netplan y bloqueo de `cloud-init`.
- `cluster-dependencies-and-access`: Requisitos de dependencias del sistema (`conntrack`, `socat`), registro de salidas de terminal verificadas de kubeadm y procedimiento no destructivo de fusión de `kubeconfig` en el host físico.

### Modified Capabilities
*Ninguna.*

## Impact

- Actualización de los capítulos de la Sección 1 en `docs/k8s-installation-steps.md` y `docs/k8s-installation-steps.html`.
- Incorporación de dependencias `conntrack` y `socat` en `scripts/common.sh`.
- Recompilación del entregable final `k8s-cluster-kubeadm.pdf`.
