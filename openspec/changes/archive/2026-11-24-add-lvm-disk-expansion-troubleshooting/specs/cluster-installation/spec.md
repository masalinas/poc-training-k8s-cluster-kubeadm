# Spec Delta: cluster-installation

## ADDED Requirements

### Requirement: Diagnóstico y Resolución de Presión de Disco LVM
The system SHALL document troubleshooting procedures for pod eviction caused by DiskPressure and insufficient ephemeral-storage due to Ubuntu Server's default LVM allocation, providing diagnostic commands and on-line volume expansion steps for both control plane and worker nodes.

#### Scenario: Diagnóstico de desalojo de Pods por DiskPressure
- **WHEN** un alumno experimenta pods en estado Failed o Evicted debido al umbral de ephemeral-storage
- **THEN** la guía detalla el análisis del mensaje de error del kubelet y proporciona los comandos `df -h /` y `lsblk` para confirmar la disparidad entre el tamaño del disco físico y el Logical Volume raíz montado en `/`.

#### Scenario: Expansión en caliente de volumen LVM y sistema de archivos
- **WHEN** el alumno ejecuta la ampliación de espacio en el nodo worker o master
- **THEN** la guía documenta la ejecución de `sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv` seguido de `sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv` y valida que el sistema de archivos raíz refleje el total del espacio asignado al disco virtual.

#### Scenario: Limpieza de pods fallidos por desalojo
- **WHEN** el alumno subsana el problema de espacio y requiere depurar el estado del cluster
- **THEN** la guía especifica el comando `kubectl delete pods --field-selector=status.phase=Failed` en el namespace afectado para restablecer los pods limpios y operativos.
