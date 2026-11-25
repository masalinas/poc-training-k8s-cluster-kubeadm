# Spec Delta: pdf-generation

## Purpose

Define los requisitos de formato, maquetación, estilo visual y generación automatizada para compilar la guía técnica en el archivo PDF k8s-cluster-kubeadm.pdf.

## ADDED Requirements

### Requirement: Compilación de Documento PDF
The system SHALL compile the technical installation guide into a final PDF file named `k8s-cluster-kubeadm.pdf` located at the root of the project.

#### Scenario: Generación exitosa de k8s-cluster-kubeadm.pdf
- **WHEN** se ejecuta el proceso de generación del documento
- **THEN** se crea el archivo k8s-cluster-kubeadm.pdf con formato A4, paginación, índice estructurado y contenido completo de la guía.

### Requirement: Estilos Visuales y Diferenciación Tipográfica
The system SHALL format the PDF document with distinctive typography and visual styles separating explanatory text from commands and configuration files.

#### Scenario: Maquetación y contraste visual de código
- **WHEN** un alumno visualiza el documento PDF
- **THEN** los comandos de terminal y ficheros de configuración se muestran en bloques con fuente monospace, resaltado de sintaxis o fondo diferenciado, y las advertencias críticas utilizan cajas destacadas.
