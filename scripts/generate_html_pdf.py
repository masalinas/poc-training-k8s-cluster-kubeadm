#!/usr/bin/env python3
# =============================================================================
# scripts/generate_html_pdf.py
# Genera el documento HTML profesional y compila k8s-installation-steps.pdf
# =============================================================================
import os
import subprocess
import shutil

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(WORKSPACE_DIR, "docs")
HTML_PATH = os.path.join(DOCS_DIR, "k8s-installation-steps.html")
PDF_PATH = os.path.join(WORKSPACE_DIR, "k8s-installation-steps.pdf")

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Guía de Instalación de Kubernetes en Producción</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    @page {
      size: A4 portrait;
      margin: 18mm 14mm 18mm 14mm;
      @bottom-right {
        content: "Página " counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748b;
      }
      @bottom-left {
        content: "Curso Kubernetes - Cap. 1: Instalación de Infraestructura";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748b;
      }
    }

    * {
      box-sizing: border-box;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.55;
      color: #1e293b;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
    }

    /* Portada */
    .cover {
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 90vh;
      padding: 40px 20px;
    }

    .badge-k8s {
      display: inline-block;
      align-self: flex-start;
      background-color: #e0f2fe;
      color: #0369a1;
      font-weight: 700;
      font-size: 9pt;
      padding: 6px 14px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 24px;
    }

    .cover h1 {
      font-size: 28pt;
      font-weight: 800;
      line-height: 1.15;
      color: #0f172a;
      margin: 0 0 16px 0;
    }

    .cover h1 span {
      color: #326ce5; /* K8s Blue */
    }

    .cover .subtitle {
      font-size: 14pt;
      font-weight: 400;
      color: #475569;
      margin-bottom: 40px;
      line-height: 1.4;
    }

    .cover-meta {
      border-top: 2px solid #e2e8f0;
      padding-top: 24px;
      margin-top: 40px;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }

    .meta-item {
      font-size: 9.5pt;
    }

    .meta-label {
      color: #64748b;
      font-weight: 500;
      text-transform: uppercase;
      font-size: 8pt;
      letter-spacing: 0.05em;
    }

    .meta-val {
      color: #0f172a;
      font-weight: 600;
      margin-top: 2px;
    }

    /* Títulos */
    h2 {
      font-size: 16pt;
      font-weight: 700;
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 6px;
      margin-top: 28px;
      margin-bottom: 14px;
      page-break-after: avoid;
    }

    .section-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
      color: #ffffff;
      padding: 16px 20px;
      border-radius: 8px;
      margin-top: 30px;
      margin-bottom: 20px;
      page-break-after: avoid;
    }

    .section-banner h2 {
      color: #ffffff;
      border: none;
      padding: 0;
      margin: 0;
      font-size: 16pt;
    }

    .section-banner p {
      color: #93c5fd;
      margin: 4px 0 0 0;
      font-size: 9pt;
    }

    h3 {
      font-size: 12pt;
      font-weight: 600;
      color: #1e3a8a;
      margin-top: 20px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }

    h4 {
      font-size: 10.5pt;
      font-weight: 600;
      color: #334155;
      margin-top: 14px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }

    p {
      margin-top: 0;
      margin-bottom: 10px;
    }

    ul, ol {
      margin-top: 0;
      margin-bottom: 12px;
      padding-left: 22px;
    }

    li {
      margin-bottom: 4px;
    }

    /* Bloques de Código y Comandos con Ajuste Flexible Sin Barras de Scroll */
    pre {
      background-color: #0f172a;
      color: #f8fafc;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      line-height: 1.45;
      padding: 12px 14px;
      border-radius: 6px;
      border-left: 4px solid #38bdf8;
      margin: 10px 0 14px 0;
      page-break-inside: avoid;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      
      /* Ajuste de línea estricto para impresión sin scrollbar */
      white-space: pre-wrap !important;
      word-wrap: break-word !important;
      word-break: break-all !important;
      overflow-wrap: anywhere !important;
      overflow-x: visible !important;
      overflow-y: visible !important;
      overflow: visible !important;
    }

    code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      background-color: #f1f5f9;
      color: #0f172a;
      padding: 2px 5px;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
      word-break: break-all;
      overflow-wrap: anywhere;
    }

    pre code {
      background-color: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: inherit;
      white-space: pre-wrap !important;
      word-break: break-all !important;
      overflow-wrap: anywhere !important;
    }

    /* Cajas de Alerta */
    .alert {
      padding: 12px 14px;
      border-radius: 6px;
      margin: 14px 0;
      font-size: 9pt;
      page-break-inside: avoid;
      border-left: 4px solid;
    }

    .alert-warning {
      background-color: #fffbeb;
      border-color: #f59e0b;
      color: #92400e;
    }

    .alert-important {
      background-color: #fef2f2;
      border-color: #ef4444;
      color: #991b1b;
    }

    .alert-note {
      background-color: #f0f9ff;
      border-color: #0284c7;
      color: #075985;
    }

    .alert-caution {
      background-color: #fef2f2;
      border-color: #dc2626;
      color: #7f1d1d;
    }

    .alert-title {
      font-weight: 700;
      margin-bottom: 4px;
      text-transform: uppercase;
      font-size: 8pt;
      letter-spacing: 0.05em;
    }

    /* Tablas */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 8.8pt;
      page-break-inside: avoid;
    }

    th, td {
      border: 1px solid #cbd5e1;
      padding: 8px 10px;
      text-align: left;
    }

    /* Figuras e Imágenes */
    .dashboard-figure {
      margin: 16px 0 20px 0;
      text-align: center;
      page-break-inside: avoid;
    }

    .dashboard-figure img {
      max-width: 98%;
      height: auto;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
      display: block;
      margin: 0 auto;
    }

    .figure-caption {
      margin-top: 8px;
      font-size: 8.5pt;
      color: #64748b;
      font-style: italic;
      text-align: center;
    }

    h5 {
      font-size: 9.5pt;
      font-weight: 600;
      color: #1e3a8a;
      margin-top: 6px;
      margin-bottom: 2px;
      page-break-after: avoid;
    }

    .step-pair {
      page-break-inside: avoid;
      margin-bottom: 8px;
    }

    .step-card {
      margin-bottom: 6px;
    }

    .step-card h5 {
      font-size: 9pt;
      font-weight: 600;
      color: #1e3a8a;
      margin-top: 4px;
      margin-bottom: 2px;
    }

    .step-card p {
      font-size: 8.2pt;
      line-height: 1.3;
      margin-top: 0;
      margin-bottom: 4px;
      color: #334155;
    }

    .step-figure {
      margin: 2px 0 4px 0;
      text-align: center;
      page-break-inside: avoid;
    }

    .step-figure img {
      max-width: 98%;
      max-height: 400px;
      height: auto;
      object-fit: contain;
      border: 1px solid #cbd5e1;
      border-radius: 5px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      display: block;
      margin: 0 auto;
    }

    .step-caption {
      margin-top: 2px;
      font-size: 7.5pt;
      color: #64748b;
      font-style: italic;
      text-align: center;
    }

    th {
      background-color: #1e293b;
      color: #ffffff;
      font-weight: 600;
    }

    tr:nth-child(even) {
      background-color: #f8fafc;
    }

    /* Diagramas ASCII */
    .diagram-box {
      background-color: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 10px 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 6.8pt;
      line-height: 1.35;
      color: #0f172a;
      margin: 12px 0;
      page-break-inside: avoid;
      white-space: pre;
      overflow: visible !important;
      overflow-x: visible !important;
    }

    .page-break {
      page-break-before: always;
    }

    .toc {
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 14px 20px;
      margin-bottom: 20px;
      page-break-after: always;
      font-size: 8.5pt;
    }

    .toc h2 {
      margin-top: 0;
      font-size: 13pt;
      margin-bottom: 10px;
      padding-bottom: 4px;
      border-bottom: 2px solid #cbd5e1;
    }

    .toc-list {
      list-style: none;
      padding-left: 0;
      margin: 0;
    }

    .toc-item {
      margin-bottom: 4px;
      font-weight: 600;
      color: #1e3a8a;
    }

    .toc-sublist {
      list-style: none;
      padding-left: 16px;
      margin-top: 2px;
      margin-bottom: 4px;
    }

    .toc-subitem {
      font-weight: 400;
      color: #475569;
      margin-bottom: 1.5px;
      line-height: 1.35;
    }

    .toc a {
      color: inherit;
      text-decoration: none;
      transition: color 0.15s ease;
    }

    .toc a:hover {
      color: #326ce5;
      text-decoration: underline;
    }

    @media print {
      * {
        overflow: visible !important;
        overflow-x: visible !important;
      }
      ::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
      }
    }
  </style>
</head>
<body>

  <!-- PORTADA -->
  <div class="cover">
    <div class="badge-k8s">Kubernetes Training Series • Capítulo 1</div>
    <h1>Guía de Instalación de <span>Kubernetes en Producción</span></h1>
    <div class="subtitle">
      Simulación de Entorno Productivo con Ubuntu Server 22.04 LTS, VirtualBox 7.0, Kubeadm v1.31 y Automatización con Vagrant
    </div>

    <div class="cover-meta">
      <div class="meta-item">
        <div class="meta-label">Sistema Operativo Host</div>
        <div class="meta-val">Ubuntu 20.04 LTS / VirtualBox 7.0</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Sistema Operativo Nodos</div>
        <div class="meta-val">Ubuntu Server 22.04.5 LTS</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Topología de Cluster</div>
        <div class="meta-val">1 Master (Control Plane) + 1 Worker</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Versión de Kubernetes</div>
        <div class="meta-val">v1.31 (Repositorio pkgs.k8s.io)</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Runtime y CNI</div>
        <div class="meta-val">Containerd (systemd cgroups) + Flannel CNI</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Modalidades Cubiertas</div>
        <div class="meta-val">Sección 1 (Manual) y Sección 2 (IaC con Vagrant)</div>
      </div>
    </div>
  </div>

  <!-- TABLA DE CONTENIDOS -->
  <div class="toc">
    <h2>Índice General</h2>
    <ul class="toc-list">
      <li class="toc-item"><a href="#sec-1">1. Arquitectura del Laboratorio</a>
        <ul class="toc-sublist">
          <li class="toc-subitem"><a href="#sec-1-1">1.1 Diagrama de Topología de Red y Componentes</a></li>
          <li class="toc-subitem"><a href="#sec-1-2">1.2 Matriz de Hardware e IP</a></li>
          <li class="toc-subitem"><a href="#sec-1-3">1.3 Alertas Críticas de Producción (Trampas habituales)</a></li>
        </ul>
      </li>
      <li class="toc-item"><a href="#sec-2">2. Sección 1: Despliegue Manual Paso a Paso con Kubeadm</a>
        <ul class="toc-sublist">
          <li class="toc-subitem"><a href="#sec-2-1">2.1 Creación de la Red Solo-Anfitrión en VirtualBox (vboxnet0)</a></li>
          <li class="toc-subitem"><a href="#sec-2-2">2.2 Creación y Configuración de VMs en VirtualBox 7.0</a>
            <ul class="toc-sublist">
              <li class="toc-subitem"><a href="#sec-2-2-1">2.2.1 Creación de la Red Solo-Anfitrión (step_00.png)</a></li>
              <li class="toc-subitem"><a href="#sec-2-2-2">2.2.2 Guía Paso a Paso para la VM Master (k8s-master)</a></li>
              <li class="toc-subitem"><a href="#sec-2-2-3">2.2.3 Guía Paso a Paso para la VM Worker (k8s-worker1)</a></li>
            </ul>
          </li>
          <li class="toc-subitem"><a href="#sec-2-3">2.3 Configuración de Idioma y Teclado Español</a></li>
          <li class="toc-subitem"><a href="#sec-2-4">2.4 Persistencia de Red: Bloqueo de Cloud-Init y Netplan Estático</a></li>
          <li class="toc-subitem"><a href="#sec-2-5">2.5 Preparación Base del Sistema Operativo (SWAP, Kernel y Sysctl)</a></li>
          <li class="toc-subitem"><a href="#sec-2-6">2.6 Instalación de Containerd y Dependencias del Sistema (conntrack, socat)</a></li>
          <li class="toc-subitem"><a href="#sec-2-7">2.7 Instalación de Herramientas Kubernetes v1.31 (pkgs.k8s.io)</a></li>
          <li class="toc-subitem"><a href="#sec-2-8">2.8 Inicialización del Plano de Control (Master), Flannel CNI y Registros Reales</a></li>
          <li class="toc-subitem"><a href="#sec-2-9">2.9 Unión del Nodo Worker al Cluster con Dependencias y Registros Reales</a></li>
          <li class="toc-subitem"><a href="#sec-2-10">2.10 Conexión Remota No Destructiva desde el Host Anfitrión (Merge Kubeconfig)</a></li>
        </ul>
      </li>
      <li class="toc-item"><a href="#sec-3">3. Sección 2: Automatización Completa con Vagrant (IaC)</a>
        <ul class="toc-sublist">
          <li class="toc-subitem"><a href="#sec-3-1">3.1 Arquitectura de Automatización con Vagrant</a></li>
          <li class="toc-subitem"><a href="#sec-3-2">3.2 Estructura del Proyecto de Infraestructura</a></li>
          <li class="toc-subitem"><a href="#sec-3-3">3.3 Archivo Vagrantfile Multi-Máquina</a></li>
          <li class="toc-subitem"><a href="#sec-3-4">3.4 Scripts de Aprovisionamiento Modular (common, master, worker)</a></li>
          <li class="toc-subitem"><a href="#sec-3-5">3.5 Despliegue Desatendido con un solo comando (vagrant up)</a></li>
          <li class="toc-subitem"><a href="#sec-3-6">3.6 Ciclo de Vida del Laboratorio (status, halt, ssh, destroy)</a></li>
        </ul>
      </li>
      <li class="toc-item"><a href="#sec-4">4. Sección 3: Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard</a>
        <ul class="toc-sublist">
          <li class="toc-subitem"><a href="#sec-4-1">4.1 Despliegue de los Componentes Oficiales del Dashboard</a></li>
          <li class="toc-subitem"><a href="#sec-4-2">4.2 Verificación del Estado de los Pods del Dashboard</a></li>
          <li class="toc-subitem"><a href="#sec-4-3">4.3 Creación de Cuenta de Servicio y Privilegios Administrativos (RBAC)</a></li>
          <li class="toc-subitem"><a href="#sec-4-4">4.4 Comprobación de la Cuenta de Servicio Creada</a></li>
          <li class="toc-subitem"><a href="#sec-4-5">4.5 Generación del Token de Autenticación Bearer</a></li>
          <li class="toc-subitem"><a href="#sec-4-6">4.6 Acceso Seguro mediante Kubectl Proxy</a></li>
          <li class="toc-subitem"><a href="#sec-4-7">4.7 Inicio de Sesión y Verificación Visual del Panel</a></li>
        </ul>
      </li>
      <li class="toc-item"><a href="#sec-5">5. Sección 4: Ejemplo Práctico de Despliegue en el Cluster (Nginx)</a>
        <ul class="toc-sublist">
          <li class="toc-subitem"><a href="#sec-5-1">5.1 Creación del Deployment de Nginx</a></li>
          <li class="toc-subitem"><a href="#sec-5-2">5.2 Inspección Detallada de Recursos del Cluster</a></li>
          <li class="toc-subitem"><a href="#sec-5-3">5.3 Exposición Externa mediante Servicio NodePort</a></li>
          <li class="toc-subitem"><a href="#sec-5-4">5.4 Verificación de Conectividad HTTP y Acceso Externo</a></li>
          <li class="toc-subitem"><a href="#sec-5-5">5.5 Acceso Temporal mediante Port-Forward y Limpieza de Recursos</a></li>
        </ul>
      </li>
      <li class="toc-item"><a href="#sec-6">6. Resolución de Problemas Frecuentes (Troubleshooting)</a>
        <ul class="toc-sublist">
          <li class="toc-subitem"><a href="#sec-6-5">6.5 Desalojo de Pods (Evicted) por DiskPressure y Particionamiento LVM</a></li>
        </ul>
      </li>
    </ul>
  </div>

  <!-- 1. ARQUITECTURA -->
  <h2 id="sec-1">1. Arquitectura del Laboratorio</h2>
  <p>
    Para simular con fidelidad un entorno de producción sobre una máquina anfitriona Ubuntu 20.04 sin saturar los recursos físicos, se implementa una arquitectura virtualizada aislada compuesta por un nodo <strong>Master (Plano de Control)</strong> y un nodo <strong>Worker</strong>.
  </p>

  <h3 id="sec-1-1">1.1 Diagrama de Topología de Red y Componentes</h3>
  <div class="diagram-box">+-----------------------------------------------------------------------------------+
|  HOST FÍSICO: Ubuntu 20.04 LTS (con VirtualBox 7.0 instalado)                     |
|  IP Red Host-Only: 192.168.56.1                                                   |
|  Gestión: Cliente kubectl instalado en el host apuntando a 192.168.56.10:6443     |
+-----------------------------------------------------------------------------------+
       |                                                    |
       | Red Host-Only (vboxnet0: 192.168.56.0/24)          | Red NAT (Salida a Internet)
       v                                                    v
+--------------------------------------+   +--------------------------------------+
| VM: k8s-master                       |   | VM: k8s-worker1                      |
| Sistema: Ubuntu Server 22.04 LTS     |   | Sistema: Ubuntu Server 22.04 LTS     |
| CPU: 2 vCPUs | RAM: 3072 MB (3 GB)   |   | CPU: 2 vCPUs | RAM: 2048 MB (2 GB)   |
| Disco: 25 GB                         |   | Disco: 20 GB                         |
| Adaptador 1 (NAT): 10.0.2.15         |   | Adaptador 1 (NAT): 10.0.2.15         |
| Adaptador 2 (Host-Only):             |   | Adaptador 2 (Host-Only):             |
|   192.168.56.10                      |   |   192.168.56.11                      |
| Roles: Control Plane                 |   | Roles: Worker Node                   |
|   - kube-apiserver, etcd, scheduler  |   |   - kubelet, kube-proxy              |
|   - controller-manager, kubelet      |   |   - containerd                       |
|   - containerd, Flannel CNI          |   |   - Flannel CNI                      |
|   - Kubernetes Dashboard             |   |                                      |
+--------------------------------------+   +--------------------------------------+
       ^                                                    ^
       +================ Red de Pods (CIDR: 10.244.0.0/16) =+</div>

  <h3 id="sec-1-2">1.2 Matriz de Hardware e IP</h3>
  <table>
    <thead>
      <tr>
        <th>Máquina</th>
        <th>Rol</th>
        <th>vCPUs</th>
        <th>RAM</th>
        <th>Disco</th>
        <th>Adaptador 1 (NAT)</th>
        <th>Adaptador 2 (Host-Only)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>k8s-master</strong></td>
        <td>Control Plane</td>
        <td>2 vCPUs (mínimo)</td>
        <td>3072 MB (3 GB)</td>
        <td>25 GB</td>
        <td>DHCP (10.0.2.15)</td>
        <td>Estática: <code>192.168.56.10/24</code></td>
      </tr>
      <tr>
        <td><strong>k8s-worker1</strong></td>
        <td>Worker Node</td>
        <td>2 vCPUs</td>
        <td>2048 MB (2 GB)</td>
        <td>20 GB</td>
        <td>DHCP (10.0.2.15)</td>
        <td>Estática: <code>192.168.56.11/24</code></td>
      </tr>
    </tbody>
  </table>

  <h3 id="sec-1-3">1.3 Alertas Críticas de Producción (Trampas Habituales)</h3>
  <div class="alert alert-warning">
    <div class="alert-title">Advertencia 1: Detección de Interfaz en Red Dual (NAT + Host-Only)</div>
    En VirtualBox con red dual, ambas máquinas tienen la misma IP en NAT (<code>10.0.2.15</code>). Tanto <code>kubeadm init</code> como el CNI Flannel deben forzarse a enlazarse a la interfaz Host-Only (<code>enp0s8</code> / <code>192.168.56.x</code>). De lo contrario, los nodos intentarán comunicarse por la IP colisionada y el cluster no funcionará.
  </div>

  <div class="alert alert-warning">
    <div class="alert-title">Advertencia 2: Conflicto de Rangos IP de Pods (CIDR)</div>
    La red de pods se establece en <code>10.244.0.0/16</code>. Si se utiliza el rango por defecto de Calico (<code>192.168.0.0/16</code>) sobre una red Host-Only <code>192.168.56.0/24</code>, colisionan y se produce un fallo de enrutamiento grave.
  </div>

  <div class="alert alert-important">
    <div class="alert-title">Importante: Repositorio Oficial Moderno (pkgs.k8s.io)</div>
    Los antiguos repositorios <code>apt.kubernetes.io</code> de Google están deprecados y retirados. Toda instalación debe apuntar a la clave y repositorio comunitario oficial en <code>https://pkgs.k8s.io/core:/stable:/v1.31/deb/</code>.
  </div>

  <!-- SECCIÓN 1: MANUAL -->
  <div class="page-break"></div>
  <div class="section-banner">
    <h2 id="sec-2">2. Sección 1: Despliegue Manual Paso a Paso con Kubeadm</h2>
    <p>Objetivo pedagógico: Comprender en profundidad cada capa del sistema, kernel, runtime de contenedores y red interna.</p>
  </div>

  <h3 id="sec-2-1">2.1 Creación de la Red Solo-Anfitrión en VirtualBox (vboxnet0)</h3>
  <p>
    Antes de crear o iniciar las máquinas virtuales, es indispensable aprovisionar la red privada aislada (Host-Only) en VirtualBox que interconectará el nodo de control, el worker y la máquina anfitriona.
  </p>
  <ol>
    <li>En la ventana principal de VirtualBox, accede al menú: <strong>Archivo -&gt; Herramientas -&gt; Administrador de red de host</strong> (o la pestaña lateral <strong>Herramientas -&gt; Redes</strong>).</li>
    <li>Haz clic en el botón <strong>+</strong> (<strong>Crear</strong>) para generar una nueva red sólo-anfitrión. Por defecto se creará con el nombre <code>vboxnet0</code>.</li>
    <li>Selecciona <code>vboxnet0</code> y configura sus parámetros en la pestaña <em>Adaptador</em>:
      <ul>
        <li><strong>Dirección IPv4:</strong> <code>192.168.56.1</code></li>
        <li><strong>Máscara de red IPv4:</strong> <code>255.255.255.0</code> (<code>/24</code>)</li>
      </ul>
    </li>
    <li>En la pestaña <em>Servidor DHCP</em>: Desmarca la casilla <em>Habilitar servidor</em> (recomendado), ya que asignaremos direccionamiento estático persistente mediante Netplan en cada máquina virtual.</li>
    <li>Haz clic en <strong>Aplicar</strong>.</li>
  </ol>

  <h3 id="sec-2-2">2.2 Creación y Configuración de VMs en VirtualBox 7.0</h3>
  <p>Descarga la imagen oficial para servidores de Ubuntu 22.04 LTS (Jammy Jellyfish):</p>
  <ul>
    <li><strong>URL de descarga:</strong> <code>https://releases.ubuntu.com/22.04/ubuntu-22.04.5-live-server-amd64.iso</code></li>
  </ul>
  <p>Crea dos máquinas virtuales en la interfaz gráfica de VirtualBox respetando estrictamente los siguientes parámetros:</p>
  <ul>
    <li><strong>k8s-master:</strong> 2 vCPUs, 3072 MB RAM, 25 GB de disco dinámico VDI.</li>
    <li><strong>k8s-worker1:</strong> 2 vCPUs, 2048 MB RAM, 20 GB de disco dinámico VDI.</li>
    <li><strong>Configuración de red en ambas VMs:</strong>
      <ul>
        <li><strong>Adaptador 1:</strong> Conectado a <strong>NAT</strong> (salida a internet para descargar paquetes).</li>
        <li><strong>Adaptador 2:</strong> Conectado a <strong>Adaptador sólo-anfitrión (Host-Only)</strong> (nombre: <code>vboxnet0</code>, modo promiscuo: <em>Permitir todo</em>).</li>
      </ul>
    </li>
  </ul>
  <div class="alert alert-important">
    <div class="alert-title">Atención al clonar máquinas</div>
    Si instalas el Master y lo clonas para crear el Worker, marca obligatoriamente: <strong>"Generar nuevas direcciones MAC para todos los adaptadores de red"</strong>. Si tienen la misma MAC, la red fallará.
  </div>

  <h4 id="sec-2-2-1">2.2.1 Creación de la Red Solo-Anfitrión en VirtualBox</h4>
  <p>
    Antes de crear las máquinas virtuales, es indispensable aprovisionar la red privada aislada que interconectará los nodos. En la consola principal de VirtualBox accedemos al menú lateral <strong>Herramientas -&gt; Redes</strong> y pulsamos en el botón <strong>+</strong> (<strong>Crear</strong>) para generar la red sólo-anfitrión <code>vboxnet0</code> con direccionamiento estático <code>192.168.56.1/24</code> y el servidor DHCP deshabilitado:
  </p>
  <figure class="step-figure">
    <img src="images/step_00.png" alt="Creación de red sólo-anfitrión en VirtualBox">
    <figcaption class="step-caption">Figura 2.1: Panel de administración de redes de VirtualBox mostrando la creación de la red sólo-anfitrión vboxnet0.</figcaption>
  </figure>

  <div class="page-break"></div>
  <h4 id="sec-2-2-2">2.2.2 Asistente Visual Paso a Paso para la Creación de la VM Master (k8s-master)</h4>
  <p>
    A continuación se ilustran ordenadamente los 20 pasos para la creación de la máquina virtual del plano de control (<code>k8s-master</code>) y la instalación guiada de Ubuntu Server 22.04.5 LTS:
  </p>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 1: Nombre, Carpeta de Destino e Imagen ISO</h5>
  <p>Seleccionamos el nombre descriptivo <code>k8s-master</code>, la carpeta de almacenamiento de las VMs y la imagen ISO descargada de Ubuntu Server, marcando la opción de omitir instalación desatendida:</p>
  <figure class="step-figure">
    <img src="images/master/step_01.png" alt="Paso 1 Master: Nombre y sistema operativo">
    <figcaption class="step-caption">Figura 2.2: Selección de nombre (k8s-master), tipo Linux (Ubuntu 64-bit) y montaje de la imagen ISO.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 2: Configuración de Instalación Desatendida</h5>
  <p>Confirmamos los datos del usuario predeterminado o la omisión del instalador desatendido en el asistente:</p>
  <figure class="step-figure">
    <img src="images/master/step_02.png" alt="Paso 2 Master: Instalación desatendida">
    <figcaption class="step-caption">Figura 2.3: Ventana de confirmación de instalación del sistema operativo invitado.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 3: Asignación de Recursos de Hardware (RAM y vCPUs)</h5>
  <p>Asignamos 3072 MB (3 GB) de memoria RAM y 2 vCPUs para garantizar la estabilidad del plano de control exigida por kubeadm:</p>
  <figure class="step-figure">
    <img src="images/master/step_03.png" alt="Paso 3 Master: Hardware de la máquina virtual">
    <figcaption class="step-caption">Figura 2.4: Asignación de 3072 MB de RAM y 2 procesadores virtuales vCPUs.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 4: Creación del Disco Duro Virtual VDI</h5>
  <p>Creamos un disco duro virtual en formato VDI de 25.00 GB con reserva dinámica de espacio:</p>
  <figure class="step-figure">
    <img src="images/master/step_04.png" alt="Paso 4 Master: Disco duro virtual">
    <figcaption class="step-caption">Figura 2.5: Creación del disco virtual VDI reservado dinámicamente de 25 GB.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 5: Resumen de Parámetros y Configuración de Red</h5>
  <p>Revisamos las propiedades de la VM y configuramos las dos interfaces: Adaptador 1 en NAT y Adaptador 2 en <code>vboxnet0</code> con modo promiscuo en <em>Permitir todo</em>:</p>
  <figure class="step-figure">
    <img src="images/master/step_05.png" alt="Paso 5 Master: Configuración de red y resumen">
    <figcaption class="step-caption">Figura 2.6: Ajuste de los adaptadores de red (NAT y vboxnet0 modo promiscuo).</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 6: Arranque del Instalador y Selección de Idioma</h5>
  <p>Iniciamos la máquina virtual e indicamos el idioma predeterminado del instalador de Ubuntu Server:</p>
  <figure class="step-figure">
    <img src="images/master/step_06.png" alt="Paso 6 Master: Selección de idioma">
    <figcaption class="step-caption">Figura 2.7: Menú inicial del instalador de Ubuntu Server para la selección de idioma.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 7: Actualización del Asistente Subiquity</h5>
  <p>Si el asistente detecta una nueva versión del instalador, seleccionamos <em>Continue without updating</em> para ceñirnos a la versión estable:</p>
  <figure class="step-figure">
    <img src="images/master/step_07.png" alt="Paso 7 Master: Actualización del instalador">
    <figcaption class="step-caption">Figura 2.8: Notificación de actualización del asistente de instalación subiquity.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 8: Configuración de la Distribución del Teclado</h5>
  <p>Establecemos la disposición del teclado adecuada al teclado físico del usuario:</p>
  <figure class="step-figure">
    <img src="images/master/step_08.png" alt="Paso 8 Master: Distribución del teclado">
    <figcaption class="step-caption">Figura 2.9: Configuración de la distribución del teclado en el asistente de instalación.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 9: Selección de la Base de Instalación</h5>
  <p>Elegimos la opción <em>Ubuntu Server</em> estándar, garantizando una instalación minimalista sin entornos de escritorio:</p>
  <figure class="step-figure">
    <img src="images/master/step_09.png" alt="Paso 9 Master: Base de instalación">
    <figcaption class="step-caption">Figura 2.10: Selección del paquete base de Ubuntu Server.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 10: Detección de Interfaces de Red</h5>
  <p>El instalador detecta las dos tarjetas de red (<code>enp0s3</code> y <code>enp0s8</code>), configurándolas temporalmente por DHCP:</p>
  <figure class="step-figure">
    <img src="images/master/step_10.png" alt="Paso 10 Master: Interfaces de red detectadas">
    <figcaption class="step-caption">Figura 2.11: Detección de las interfaces de red primaria (NAT) y secundaria (Host-Only).</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 11: Configuración de Proxy HTTP</h5>
  <p>Al disponer de acceso directo a la red, dejamos en blanco el campo de proxy HTTP:</p>
  <figure class="step-figure">
    <img src="images/master/step_11.png" alt="Paso 11 Master: Configuración de proxy">
    <figcaption class="step-caption">Figura 2.12: Pantalla de proxy HTTP dejada en blanco.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 12: Servidor Espejo de Archivos (Ubuntu Archive Mirror)</h5>
  <p>Confirmamos la URL del repositorio oficial de paquetes de Ubuntu y validamos su respuesta:</p>
  <figure class="step-figure">
    <img src="images/master/step_12.png" alt="Paso 12 Master: Espejo de paquetes de Ubuntu">
    <figcaption class="step-caption">Figura 2.13: Validación del mirror oficial de paquetes de Ubuntu.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 13: Esquema de Particionado Guiado (LVM)</h5>
  <p>Marcamos la opción de utilizar el disco completo (<em>Use an entire disk</em>) creando la estructura de volúmenes lógicos LVM:</p>
  <figure class="step-figure">
    <img src="images/master/step_13.png" alt="Paso 13 Master: Configuración de almacenamiento guiado">
    <figcaption class="step-caption">Figura 2.14: Selección de uso del disco completo y configuración de grupo LVM.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 14: Confirmación Destructiva de Escritura en Disco</h5>
  <p>Revisamos las particiones generadas y confirmamos la escritura en el disco virtual pulsando <em>Continue</em>:</p>
  <figure class="step-figure">
    <img src="images/master/step_14.png" alt="Paso 14 Master: Confirmación de particionado">
    <figcaption class="step-caption">Figura 2.15: Resumen del mapa de particiones y advertencia destructiva de confirmación.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 15: Configuración de Perfil de Usuario y Nombre del Host</h5>
  <p>Indicamos el nombre de red del servidor (<strong><code>k8s-master</code></strong>), junto con el usuario y contraseña de administración:</p>
  <figure class="step-figure">
    <img src="images/master/step_15.png" alt="Paso 15 Master: Configuración de perfil y credenciales">
    <figcaption class="step-caption">Figura 2.16: Creación de la cuenta de usuario y asignación del hostname k8s-master.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 16: Omisión de Ubuntu Pro</h5>
  <p>En la ventana de registro y soporte extendido seleccionamos <em>Skip for now</em> para omitir el servicio:</p>
  <figure class="step-figure">
    <img src="images/master/step_16.png" alt="Paso 16 Master: Omisión de Ubuntu Pro">
    <figcaption class="step-caption">Figura 2.17: Omisión de la suscripción a servicios comerciales de Ubuntu Pro.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 17: Habilitación de OpenSSH Server</h5>
  <p>Marcamos de forma indispensable la opción <strong>Install OpenSSH server</strong> para habilitar la administración remota segura:</p>
  <figure class="step-figure">
    <img src="images/master/step_17.png" alt="Paso 17 Master: Instalación de servidor SSH">
    <figcaption class="step-caption">Figura 2.18: Selección obligatoria del paquete OpenSSH server.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 18: Selección de Featured Server Snaps</h5>
  <p>Dejamos desmarcados todos los servicios snaps adicionales para mantener un sistema limpio y liviano:</p>
  <figure class="step-figure">
    <img src="images/master/step_18.png" alt="Paso 18 Master: Snaps de servidor">
    <figcaption class="step-caption">Figura 2.19: Lista de snaps adicionales desmarcados.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 19: Instalación de Paquetes Base y Seguridad</h5>
  <p>El instalador transfiere los paquetes del sistema operativo, el núcleo Linux y las actualizaciones de seguridad:</p>
  <figure class="step-figure">
    <img src="images/master/step_19.png" alt="Paso 19 Master: Proceso de instalación">
    <figcaption class="step-caption">Figura 2.20: Registro del progreso de instalación de paquetes y configuración del sistema.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 20: Finalización de la Instalación y Reinicio</h5>
  <p>Pulsamos sobre <strong>Reboot Now</strong>, desmontamos la imagen ISO virtual y confirmamos el arranque limpio de <code>k8s-master</code> hasta la consola de login:</p>
  <figure class="step-figure">
    <img src="images/master/step_20.png" alt="Paso 20 Master: Reinicio e inicio de sesión">
    <figcaption class="step-caption">Figura 2.21: Finalización del proceso de instalación e inicio de sesión en k8s-master.</figcaption>
  </figure>
    </div>
  </div>

  <div class="page-break"></div>
  <h4 id="sec-2-2-3">2.2.3 Asistente Visual Paso a Paso para la Creación de la VM Worker (k8s-worker1)</h4>
  <p>
    A continuación se ilustran ordenadamente los 20 pasos para la creación de la máquina virtual del nodo de trabajo (<code>k8s-worker1</code>):
  </p>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 1: Nombre, Carpeta e Imagen ISO para el Worker</h5>
  <p>Definimos el nombre descriptivo <code>k8s-worker1</code>, tipo Linux (Ubuntu 64-bit) y la imagen ISO montada marcando omitir instalación desatendida:</p>
  <figure class="step-figure">
    <img src="images/worker/step_01.png" alt="Paso 1 Worker: Nombre y sistema operativo">
    <figcaption class="step-caption">Figura 2.22: Creación de la VM k8s-worker1 y selección de la imagen ISO.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 2: Instalación Desatendida</h5>
  <p>Confirmamos los parámetros de instalación en la pantalla del sistema operativo invitado:</p>
  <figure class="step-figure">
    <img src="images/worker/step_02.png" alt="Paso 2 Worker: Asistente desatendido">
    <figcaption class="step-caption">Figura 2.23: Confirmación de parámetros en el asistente de instalación.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 3: Asignación de Recursos de Hardware (RAM y vCPUs)</h5>
  <p>Asignamos 2048 MB (2 GB) de memoria RAM y 2 vCPUs para la ejecución de cargas de trabajo de pods:</p>
  <figure class="step-figure">
    <img src="images/worker/step_03.png" alt="Paso 3 Worker: Hardware de la máquina virtual">
    <figcaption class="step-caption">Figura 2.24: Asignación de 2048 MB de RAM y 2 vCPUs para k8s-worker1.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 4: Creación del Disco Duro Virtual VDI</h5>
  <p>Creamos un disco duro virtual VDI con asignación dinámica de 20.00 GB de capacidad:</p>
  <figure class="step-figure">
    <img src="images/worker/step_04.png" alt="Paso 4 Worker: Disco duro virtual">
    <figcaption class="step-caption">Figura 2.25: Creación del disco virtual VDI de 20 GB para el nodo worker.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 5: Configuración de Adaptadores de Red y Resumen</h5>
  <p>Ajustamos los adaptadores de red: Adaptador 1 en NAT y Adaptador 2 en <code>vboxnet0</code> con modo promiscuo en <em>Permitir todo</em>:</p>
  <figure class="step-figure">
    <img src="images/worker/step_05.png" alt="Paso 5 Worker: Configuración de red y resumen">
    <figcaption class="step-caption">Figura 2.26: Ajuste de interfaces de red con vboxnet0 y modo promiscuo activado.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 6: Arranque del Instalador y Selección de Idioma</h5>
  <p>Iniciamos la VM <code>k8s-worker1</code> y establecemos el idioma deseado para el proceso:</p>
  <figure class="step-figure">
    <img src="images/worker/step_06.png" alt="Paso 6 Worker: Selección de idioma">
    <figcaption class="step-caption">Figura 2.27: Menú de idioma para el nodo k8s-worker1.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 7: Actualización del Instalador</h5>
  <p>Seleccionamos la opción para continuar con la versión actual del instalador:</p>
  <figure class="step-figure">
    <img src="images/worker/step_07.png" alt="Paso 7 Worker: Actualización del instalador">
    <figcaption class="step-caption">Figura 2.28: Confirmación de versión del instalador subiquity.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 8: Distribución del Teclado</h5>
  <p>Configuramos la disposición adecuada para la entrada de caracteres:</p>
  <figure class="step-figure">
    <img src="images/worker/step_08.png" alt="Paso 8 Worker: Distribución de teclado">
    <figcaption class="step-caption">Figura 2.29: Configuración de teclado en el nodo worker.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 9: Base de Instalación de Ubuntu Server</h5>
  <p>Elegimos la versión estándar de Ubuntu Server sin servicios gráficos adicionales:</p>
  <figure class="step-figure">
    <img src="images/worker/step_09.png" alt="Paso 9 Worker: Selección de paquete base">
    <figcaption class="step-caption">Figura 2.30: Selección del paquete estándar sin entorno gráfico.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 10: Interfaces de Red Detectadas</h5>
  <p>Validamos la correcta identificación de las tarjetas <code>enp0s3</code> y <code>enp0s8</code>:</p>
  <figure class="step-figure">
    <img src="images/worker/step_10.png" alt="Paso 10 Worker: Interfaces de red">
    <figcaption class="step-caption">Figura 2.31: Interfaces de red identificadas en el asistente.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 11: Configuración de Proxy HTTP</h5>
  <p>Dejamos en blanco la configuración de proxy al contar con salida directa:</p>
  <figure class="step-figure">
    <img src="images/worker/step_11.png" alt="Paso 11 Worker: Proxy HTTP">
    <figcaption class="step-caption">Figura 2.32: Configuración de proxy HTTP en blanco.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 12: Repositorio Espejo de Paquetes</h5>
  <p>Validamos la conexión con el mirror oficial de Ubuntu:</p>
  <figure class="step-figure">
    <img src="images/worker/step_12.png" alt="Paso 12 Worker: Espejo de paquetes">
    <figcaption class="step-caption">Figura 2.33: Verificación del mirror oficial de paquetes.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 13: Configuración Guiada del Almacenamiento (LVM)</h5>
  <p>Seleccionamos el disco entero de 20 GB configurando el grupo de volúmenes LVM:</p>
  <figure class="step-figure">
    <img src="images/worker/step_13.png" alt="Paso 13 Worker: Particionado LVM">
    <figcaption class="step-caption">Figura 2.34: Configuración de almacenamiento con particionado LVM.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 14: Confirmación Destructiva de Particionado</h5>
  <p>Aceptamos la escritura definitiva de los volúmenes en el disco virtual:</p>
  <figure class="step-figure">
    <img src="images/worker/step_14.png" alt="Paso 14 Worker: Confirmación de disco">
    <figcaption class="step-caption">Figura 2.35: Confirmación de formateo y creación de volúmenes.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 15: Configuración de Perfil y Nombre del Host</h5>
  <p>Definimos el nombre de red del servidor (<strong><code>k8s-worker1</code></strong>) y las credenciales de administración:</p>
  <figure class="step-figure">
    <img src="images/worker/step_15.png" alt="Paso 15 Worker: Configuración de perfil y credenciales">
    <figcaption class="step-caption">Figura 2.36: Creación del usuario y asignación del hostname k8s-worker1.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 16: Pantalla de Ubuntu Pro</h5>
  <p>Seleccionamos <em>Skip for now</em> para omitir la activación del soporte extendido:</p>
  <figure class="step-figure">
    <img src="images/worker/step_16.png" alt="Paso 16 Worker: Omisión de Ubuntu Pro">
    <figcaption class="step-caption">Figura 2.37: Continuación sin registro en Ubuntu Pro.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 17: Instalación de OpenSSH Server</h5>
  <p>Marcamos de forma imprescindible la opción <strong>Install OpenSSH server</strong>:</p>
  <figure class="step-figure">
    <img src="images/worker/step_17.png" alt="Paso 17 Worker: Selección de OpenSSH server">
    <figcaption class="step-caption">Figura 2.38: Instalación obligatoria del servidor OpenSSH.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 18: Snaps Destacados de Servidor</h5>
  <p>Mantenemos desmarcados los snaps adicionales para optimizar recursos:</p>
  <figure class="step-figure">
    <img src="images/worker/step_18.png" alt="Paso 18 Worker: Featured Server Snaps">
    <figcaption class="step-caption">Figura 2.39: Lista de snaps adicionales desmarcados.</figcaption>
  </figure>
    </div>
  </div>

  <div class="step-pair">
    <div class="step-card">
      <h5>Paso 19: Instalación de Paquetes Base y Dependencias</h5>
  <p>El instalador descarga y aplica los paquetes del sistema en el nodo worker:</p>
  <figure class="step-figure">
    <img src="images/worker/step_19.png" alt="Paso 19 Worker: Progreso de instalación">
    <figcaption class="step-caption">Figura 2.40: Progreso de descarga e instalación del sistema base.</figcaption>
  </figure>
    </div>
    <div class="step-card">
      <h5>Paso 20: Finalización e Inicio de Sesión</h5>
  <p>Hacemos clic en <strong>Reboot Now</strong>, retiramos el medio de instalación virtual y confirmamos que <code>k8s-worker1</code> arranca hasta el prompt de inicio de sesión:</p>
  <figure class="step-figure">
    <img src="images/worker/step_20.png" alt="Paso 20 Worker: Reinicio e inicio de sesión">
    <figcaption class="step-caption">Figura 2.41: Nodo k8s-worker1 operativo y preparado para la configuración de red y unión al cluster.</figcaption>
  </figure>
    </div>
  </div>

  <div class="page-break"></div>
  <h3 id="sec-2-3">2.3 Configuración de Idioma y Teclado Español</h3>
  <p>
    Por defecto, Ubuntu Server se instala con la distribución de teclado en inglés (US). Esto genera errores de tipeo al introducir caracteres frecuentes de administración en consola como guiones (<code>-</code>), tuberías (<code>|</code>), barras (<code>/</code>), almohadillas (<code>#</code>) o comillas.
  </p>
  <p>Ejecuta en <strong>ambos nodos (k8s-master y k8s-worker1)</strong> nada más iniciar sesión:</p>
  <pre><code># 1. Configurar la distribución de teclado a español pc105 de forma persistente
sudo localectl set-x11-keymap es pc105

# 2. Cargar el mapa de teclado en la consola actual de manera inmediata
sudo loadkeys es</code></pre>
  <p>
    <code>localectl</code> persiste la configuración en <code>/etc/default/keyboard</code> para todos los futuros arranques, mientras que <code>loadkeys es</code> aplica la tabla de teclas de inmediato en la sesión TTY actual.
  </p>

  <h3 id="sec-2-4">2.4 Persistencia de Red: Bloqueo de Cloud-Init y Netplan Estático</h3>
  <p>
    En Ubuntu Server 22.04 LTS, el servicio <code>cloud-init</code> gestiona la configuración de red y reescribe los archivos de Netplan al reiniciar el sistema. Si se modifica Netplan sin desactivar la generación de red de <code>cloud-init</code>, la dirección IP estática se perderá tras reiniciar la máquina virtual.
  </p>

  <h4>2.4.1 Crear archivo de bloqueo para cloud-init (Ambos Nodos)</h4>
  <p>Ejecuta en <code>k8s-master</code> y <code>k8s-worker1</code>:</p>
  <pre><code>sudo touch /etc/cloud/cloud-init.disabled</code></pre>

  <h4>2.4.2 Configurar Netplan con IP Estática</h4>
  <p>Edita el archivo <code>/etc/netplan/50-cloud-init.yaml</code> en el nodo <strong>k8s-master</strong>:</p>
  <pre><code>network:
  ethernets:
    enp0s3:
      dhcp4: true
      optional: true
    enp0s8:
      dhcp4: false
      addresses:
      - 192.168.56.10/24
      optional: true
  version: 2</code></pre>

  <p>Edita el archivo <code>/etc/netplan/50-cloud-init.yaml</code> en el nodo <strong>k8s-worker1</strong>:</p>
  <pre><code>network:
  ethernets:
    enp0s3:
      dhcp4: true
      optional: true
    enp0s8:
      dhcp4: false
      addresses:
      - 192.168.56.11/24
      optional: true
  version: 2</code></pre>

  <h4>2.4.3 Aplicar los cambios de red</h4>
  <pre><code>sudo netplan apply</code></pre>

  <h4>2.4.4 Verificación de Direccionamiento IP con <code>ip a</code></h4>
  <p>Salida benchmark real en <strong>k8s-master</strong>:</p>
  <pre><code>$ ip a
1: lo: &lt;LOOPBACK,UP,LOWER_UP&gt; mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:f9:da:df brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
       valid_lft 86121sec preferred_lft 86121sec
    inet6 fe80::a00:27ff:fef9:dadf/64 scope link 
       valid_lft forever preferred_lft forever
3: enp0s8: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a2:c7:8f brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.10/24 brd 192.168.56.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fea2:c78f/64 scope link 
       valid_lft forever preferred_lft forever</code></pre>

  <p>Salida benchmark real en <strong>k8s-worker1</strong>:</p>
  <pre><code>$ ip a
1: lo: &lt;LOOPBACK,UP,LOWER_UP&gt; mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:17:40:ea brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
       valid_lft 86242sec preferred_lft 86242sec
    inet6 fe80::a00:27ff:fe17:40ea/64 scope link 
       valid_lft forever preferred_lft forever
3: enp0s8: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:34:ea:f7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.11/24 brd 192.168.56.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe34:eaf7/64 scope link 
       valid_lft forever preferred_lft forever</code></pre>

  <h4>2.4.5 Nombres de host y resolución local</h4>
  <p>En el Master:</p>
  <pre><code>sudo hostnamectl set-hostname k8s-master</code></pre>

  <p>En el Worker:</p>
  <pre><code>sudo hostnamectl set-hostname k8s-worker1</code></pre>

  <p>En ambos nodos, registrar en <code>/etc/hosts</code>:</p>
  <pre><code>sudo bash -c 'cat &gt;&gt; /etc/hosts &lt;&lt;EOF
192.168.56.10 k8s-master
192.168.56.11 k8s-worker1
EOF'</code></pre>
  <pre><code>ping -c 3 192.168.56.10
ping -c 3 192.168.56.11</code></pre>

  <h3 id="sec-2-5">2.5 Preparación Base del Sistema Operativo (SWAP, Kernel y Sysctl)</h3>
  <p>Ejecuta los siguientes pasos en <strong>ambas máquinas virtuales</strong>:</p>

  <h4>2.5.1 Desactivación Permanente de SWAP</h4>
  <pre><code>sudo swapoff -a
sudo sed -i '/^\/swap\.img/ s/^/#/' /etc/fstab
swapon --show  # Debe devolver salida vacía</code></pre>

  <h4>2.5.2 Módulos de Kernel y Sysctl</h4>
  <pre><code>cat &lt;&lt;EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

cat &lt;&lt;EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system</code></pre>

  <h3 id="sec-2-6">2.6 Instalación de Containerd y Dependencias del Sistema (conntrack, socat)</h3>
  <p>
    Desde Kubernetes v1.24, el subsistema <code>dockershim</code> fue removido. Instalaremos <code>containerd</code> como runtime estándar de contenedores (CRI), junto con dos paquetes fundamentales del sistema operativo:
  </p>
  <ul>
    <li><strong><code>conntrack</code>:</strong> Requerido por <code>kube-proxy</code> y <code>kubelet</code> para gestionar y monitorear las tablas de seguimiento de conexiones de <code>iptables</code>/<code>netfilter</code>. Sin <code>conntrack</code>, la asignación de IPs virtuales de servicio y balanceo de tráfico falla.</li>
    <li><strong><code>socat</code>:</strong> Utilizado por el API Server de Kubernetes para canalizar flujos de entrada/salida y crear túneles bidireccionales, indispensables para el correcto funcionamiento de comandos como <code>kubectl exec</code> y <code>kubectl port-forward</code>.</li>
  </ul>

  <p>Ejecuta en <strong>ambos nodos (k8s-master y k8s-worker1)</strong>:</p>
  <pre><code>sudo apt-get update
sudo apt-get install -y containerd conntrack socat

sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml &gt; /dev/null

# Habilitar SystemdCgroup (Obligatorio para evitar discrepancias con kubelet)
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable containerd
sudo systemctl status containerd --no-pager</code></pre>

  <h3 id="sec-2-7">2.7 Instalación de Herramientas Kubernetes v1.31 (pkgs.k8s.io)</h3>
  <p>Ejecuta en <strong>ambos nodos</strong>:</p>
  <pre><code># 1. Instalar dependencias de transporte seguro
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# 2. Crear directorio de llaveros de confianza
sudo mkdir -p -m 755 /etc/apt/keyrings

# 3. Descargar y almacenar la clave pública oficial de Kubernetes v1.31
K8S_REPO="https://pkgs.k8s.io/core:/stable:/v1.31/deb/"
KEYRING="/etc/apt/keyrings/kubernetes-apt-keyring.gpg"

curl -fsSL "${K8S_REPO}Release.key" \
  | sudo gpg --dearmor -o "${KEYRING}"

# 4. Registrar el repositorio comunitario oficial
echo "deb [signed-by=${KEYRING}] ${K8S_REPO} /" \
  | sudo tee /etc/apt/sources.list.d/kubernetes.list

# 5. Instalar kubelet, kubeadm y kubectl
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

# 6. Bloquear actualizaciones automáticas para preservar estabilidad
sudo apt-mark hold kubelet kubeadm kubectl</code></pre>

  <div class="alert alert-note">
    <div class="alert-title">Solución de Problemas: Error de validación de claves en apt update</div>
    <p>Si durante la instalación o actualización de paquetes con <code>apt</code> el repositorio no es reconocido por Ubuntu o se presentan errores con firmas de claves públicas (por ejemplo, errores de claves no válidas o ausentes en repositorios como HashiCorp preexistentes en la máquina virtual, p. ej. <code>NO_PUBKEY AA16FCBCA621E701</code>), la solución consiste en añadir la clave al keyring (sin utilizar <code>apt-key</code>, que se encuentra obsoleto):</p>
    <pre><code>gpg --no-default-keyring --keyring /tmp/hc-old.gpg --keyserver keyserver.ubuntu.com --recv-keys AA16FCBCA621E701
gpg --no-default-keyring --keyring /tmp/hc-old.gpg --export | sudo tee -a /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
sudo apt update</code></pre>
  </div>

  <div class="page-break"></div>
  <h3 id="sec-2-8">2.8 Inicialización del Plano de Control (Master), Flannel CNI y Registros Reales</h3>
  <p>Los pasos de esta subsección se ejecutan en <strong>k8s-master</strong>.</p>
  
  <h4>2.8.1 Asegurar dependencias de red en el master</h4>
  <p>Antes de inicializar el cluster, verifica e instala las dependencias de red necesarias (<code>conntrack</code> y <code>socat</code>):</p>
  <pre><code>sudo apt-get update && sudo apt-get install -y conntrack socat</code></pre>

  <h4>2.8.2 Pre-descarga de imágenes e inicialización</h4>
  <pre><code>sudo kubeadm config images pull

sudo kubeadm init \
  --apiserver-advertise-address=192.168.56.10 \
  --pod-network-cidr=10.244.0.0/16 \
  --node-name k8s-master</code></pre>

  <h4>Registro Real de Terminal (Benchmark de Inicialización):</h4>
  <p>A continuación se muestra el registro de ejecución obtenido en el laboratorio, que sirve de referencia para validar el correcto progreso de la instalación:</p>
  <pre><code>$ sudo kubeadm init --apiserver-advertise-address=192.168.56.10 --pod-network-cidr=10.244.0.0/16 --node-name k8s-master
I1114 21:49:03.100458   15635 version.go:261] remote version is much newer: v1.37.2; falling back to: stable-1.31
[init] Using Kubernetes version: v1.31.14
[preflight] Running pre-flight checks
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action beforehand using 'kubeadm config images pull'
W1114 21:49:03.258789   15635 checks.go:843] detected that the sandbox image "" of the container runtime is inconsistent with that used by kubeadm.It is recommended to use "registry.k8s.io/pause:3.10" as the CRI sandbox image.
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [k8s-master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.56.10]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.56.10 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.56.10 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "super-admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests"
[kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
[kubelet-check] The kubelet is healthy after 502.603826ms
[api-check] Waiting for a healthy API server. This can take up to 4m0s
[api-check] The API server is healthy after 5.502159471s
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --upload-certs
[mark-control-plane] Marking the node k8s-master as control-plane by adding the labels: [node-role.kubernetes.io/control-plane node.kubernetes.io/exclude-from-external-load-balancers]
[mark-control-plane] Marking the node k8s-master as control-plane by adding the taints [node-role.kubernetes.io/control-plane:NoSchedule]
[bootstrap-token] Using token: 5yjuf0.zo38v6ts77dd8zjc
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.56.10:6443 --token 5yjuf0.zo38v6ts77dd8zjc \
	--discovery-token-ca-cert-hash sha256:3bf340abd39b6c6d30c33c163a9ceccc170567ea6f52f0007b59d3608f2a4e11</code></pre>

  <h4>2.8.3 Configurar credenciales de kubectl local</h4>
  <pre><code>mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config</code></pre>

  <h4>2.8.4 Desplegar CNI Flannel con fijación de interfaz</h4>
  <p>Descarga el manifiesto oficial de Flannel:</p>
  <pre><code>FLANNEL_URL="https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml"
curl -sSL "${FLANNEL_URL}" -o kube-flannel.yml</code></pre>

  <p>Añade el argumento <code>--iface=enp0s8</code> para que Flannel se comunique por la red Host-Only. Puedes aplicarlo automáticamente con <code>sed</code>:</p>
  <pre><code>sed -i 's/- --kube-subnet-mgr/- --kube-subnet-mgr\n        - --iface=enp0s8/' kube-flannel.yml</code></pre>

  <p>O editar manualmente con <code>nano kube-flannel.yml</code> para que la sección <code>args</code> quede así:</p>
  <pre><code>      containers:
      - name: kube-flannel
        image: docker.io/flannel/flannel:...
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        - --iface=enp0s8</code></pre>

  <p>Aplica el manifiesto modificado:</p>
  <pre><code>kubectl apply -f kube-flannel.yml

kubectl get nodes
kubectl get pods -n kube-system</code></pre>

  <h3 id="sec-2-9">2.9 Unión del Nodo Worker al Cluster con Dependencias y Registros Reales</h3>
  <p>En la máquina virtual <strong>k8s-worker1</strong>:</p>

  <h4>2.9.1 Asegurar dependencias de red en el worker</h4>
  <pre><code>sudo apt-get update &amp;&amp; sudo apt-get install -y conntrack socat</code></pre>

  <h4>2.9.2 Ejecución del comando kubeadm join</h4>
  <pre><code>sudo kubeadm join 192.168.56.10:6443 \
  --token &lt;TU_TOKEN&gt; \
  --discovery-token-ca-cert-hash sha256:&lt;TU_HASH&gt;</code></pre>

  <h4>Registro Real de Terminal (Benchmark de Unión):</h4>
  <p>A continuación se muestra la salida de consola real obtenida en <code>k8s-worker1</code>:</p>
  <pre><code>$ sudo kubeadm join 192.168.56.10:6443 --token 5yjuf0.zo38v6ts77dd8zjc  --discovery-token-ca-cert-hash sha256:3bf340abd39b6c6d30c33c163a9ceccc170567ea6f52f0007b59d3608f2a4e11
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
[kubelet-check] The kubelet is healthy after 1.001529458s
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.</code></pre>

  <h4>2.9.3 Validación del Cluster Completo desde el Master</h4>
  <p>Regresa a la terminal de <strong>k8s-master</strong> y valida que ambos nodos reporten estado <code>Ready</code>:</p>
  <pre><code>kubectl get nodes -o wide</code></pre>
  <pre><code>$ kubectl get nodes -o wide
NAME          STATUS   ROLES           AGE   VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
k8s-master    Ready    control-plane   49m   v1.31.14   192.168.56.10   &lt;none&gt;        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
k8s-worker1   Ready    &lt;none&gt;          21m   v1.31.14   192.168.56.11   &lt;none&gt;        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1</code></pre>

  <h3 id="sec-2-10">2.10 Conexión Remota No Destructiva desde el Host Anfitrión (Merge Kubeconfig)</h3>
  <div class="alert alert-caution">
    <div class="alert-title">Precaución: No sobrescribas tu archivo ~/.kube/config</div>
    Si ya utilizas Kubernetes en tu equipo host (ej. Minikube, Docker Desktop, k3s, EKS, GKE), ejecutar <code>scp ... ~/.kube/config</code> destruirá tus contextos y configuraciones preexistentes. A continuación se detalla cómo fusionar la nueva configuración de forma segura y no destructiva.
  </div>

  <h4>2.10.1 Instalar herramientas base en el terminal del Host (Ubuntu 20.04)</h4>
  <pre><code>sudo apt-get update &amp;&amp; sudo apt-get install -y \
  apt-transport-https ca-certificates curl gpg

sudo mkdir -p -m 755 /etc/apt/keyrings

K8S_REPO="https://pkgs.k8s.io/core:/stable:/v1.31/deb/"
KEYRING="/etc/apt/keyrings/kubernetes-apt-keyring.gpg"

curl -fsSL "${K8S_REPO}Release.key" \
  | sudo gpg --dearmor -o "${KEYRING}"

echo "deb [signed-by=${KEYRING}] ${K8S_REPO} /" \
  | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update &amp;&amp; sudo apt-get install -y kubectl</code></pre>

  <h4>2.10.2 Descargar el archivo kubeconfig del Master a un fichero local</h4>
  <pre><code>mkdir -p ~/.kube
scp &lt;usuario&gt;@192.168.56.10:~/.kube/config ./master-kubeconfig</code></pre>

  <h4>2.10.3 Fusión (Merge) de Configuraciones</h4>
  <p><strong>Alternativa A: Fusión Automática con kubectl (Recomendada)</strong></p>
  <pre><code># 1. Copia de respaldo
cp ~/.kube/config ~/.kube/config.bak

# 2. Fusión consolidada sin perder clusters anteriores
KUBECONFIG=~/.kube/config:./master-kubeconfig kubectl config view --flatten &gt; ~/.kube/config.new

# 3. Aplicar nuevo archivo y asegurar permisos
mv ~/.kube/config.new ~/.kube/config
chmod 600 ~/.kube/config
rm -f ./master-kubeconfig</code></pre>

  <p><strong>Alternativa B: Fusión Manual de Bloques YAML</strong></p>
  <p>Abre <code>~/.kube/config</code> y <code>./master-kubeconfig</code> en un editor y copia de forma ordenada:</p>
  <ul>
    <li>Bajo <code>clusters:</code> añade la definición del cluster <code>kubernetes</code> (servidor: <code>https://192.168.56.10:6443</code>).</li>
    <li>Bajo <code>users:</code> añade el usuario <code>kubernetes-admin</code>.</li>
    <li>Bajo <code>contexts:</code> añade el contexto <code>kubernetes-admin@kubernetes</code> que relaciona usuario y cluster.</li>
  </ul>

  <h4>2.10.4 Fijar Contexto Activo y Validar Conexión</h4>
  <pre><code>kubectl config use-context kubernetes-admin@kubernetes</code></pre>
  
  <p>Comprobación remota y salida real benchmark obtenida desde el host anfitrión:</p>
  <pre><code>$ kubectl cluster-info
Kubernetes control plane is running at https://192.168.56.10:6443
CoreDNS is running at https://192.168.56.10:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

$ kubectl get nodes -o wide
NAME          STATUS   ROLES           AGE   VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
k8s-master    Ready    control-plane   49m   v1.31.14   192.168.56.10   &lt;none&gt;        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
k8s-worker1   Ready    &lt;none&gt;          21m   v1.31.14   192.168.56.11   &lt;none&gt;        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1</code></pre>

  <!-- SECCIÓN 2: VAGRANT -->
  <div class="page-break"></div>
  <div class="section-banner">
    <h2 id="sec-3">3. Sección 2: Automatización Completa con Vagrant (IaC)</h2>
    <p>Objetivo pedagógico: Aprovisionar todo el laboratorio productivo de forma desatendida mediante Infrastructure as Code.</p>
  </div>

  <h3 id="sec-3-1">3.1 Arquitectura de Automatización con Vagrant</h3>
  <p>
    Vagrant permite definir y aprovisionar entornos de máquinas virtuales de manera reproducible. Gracias al <code>Vagrantfile</code> y a los scripts de provisión shell modulares, todo el proceso manual visto en la Sección 1 se ejecuta automáticamente en orden:
  </p>
  <ol>
    <li>Descarga automática de la box <code>ubuntu/jammy64</code>.</li>
    <li>Creación y encendido de <code>k8s-master</code>, asignando 2 vCPUs, 3 GB RAM e IP <code>192.168.56.10</code>.</li>
    <li>Ejecución de <code>scripts/common.sh</code> y <code>scripts/master.sh</code>, desplegando containerd, conntrack, socat, kubeadm v1.31, Flannel CNI y Dashboard.</li>
    <li>Exportación del token de unión y del archivo <code>kubeconfig</code> a la carpeta compartida <code>./configs/</code>.</li>
    <li>Creación y encendido de <code>k8s-worker1</code>, asignando 2 vCPUs, 2 GB RAM e IP <code>192.168.56.11</code>.</li>
    <li>Ejecución de <code>scripts/common.sh</code> y <code>scripts/worker.sh</code>, incorporando el worker al cluster sin intervención humana.</li>
  </ol>

  <h3 id="sec-3-2">3.2 Estructura del Proyecto de Infraestructura</h3>
  <pre><code>poc-training-k8s-cluster-kubeadm/
├── Vagrantfile                   # Declaración de VMs, red y provisioners
├── scripts/
│   ├── common.sh                # Preparación SO, dependencias de red, containerd y kubeadm
│   ├── master.sh                # kubeadm init, Flannel, Dashboard y exportación
│   └── worker.sh                # Espera activa y ejecución de kubeadm join
└── configs/                      # Carpeta compartida (kubeconfig y tokens)</code></pre>

  <h3 id="sec-3-3">3.3 Archivo Vagrantfile Multi-Máquina</h3>
  <pre><code>Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.synced_folder "./configs", "/vagrant_configs", create: true
  config.vm.box_check_update = false

  # Master Node (Control Plane)
  config.vm.define "k8s-master" do |master|
    master.vm.hostname = "k8s-master"
    master.vm.network "private_network", ip: "192.168.56.10"
    master.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-master"
      vb.cpus = 2
      vb.memory = 3072
      vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    end
    master.vm.provision "shell", path: "scripts/common.sh"
    master.vm.provision "shell", path: "scripts/master.sh"
  end

  # Worker Node
  config.vm.define "k8s-worker1" do |worker|
    worker.vm.hostname = "k8s-worker1"
    worker.vm.network "private_network", ip: "192.168.56.11"
    worker.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-worker1"
      vb.cpus = 2
      vb.memory = 2048
      vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    end
    worker.vm.provision "shell", path: "scripts/common.sh"
    worker.vm.provision "shell", path: "scripts/worker.sh"
  end
end</code></pre>

  <div class="page-break"></div>
  <h3 id="sec-3-4">3.4 Scripts de Aprovisionamiento Modular</h3>

  <h4>3.4.1 Script Común: <code>scripts/common.sh</code></h4>
  <pre><code>#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

# 1. Hosts y resolución
cat &lt;&lt;EOF &gt;&gt; /etc/hosts
192.168.56.10 k8s-master
192.168.56.11 k8s-worker1
EOF

# 2. Swap off permanente
swapoff -a
sed -i '/^\/swap\.img/ s/^/#/' /etc/fstab

# 3. Carga de módulos de kernel
cat &lt;&lt;EOF &gt; /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
modprobe overlay &amp;&amp; modprobe br_netfilter

# 4. Parámetros Sysctl
cat &lt;&lt;EOF &gt; /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sysctl --system &gt; /dev/null

# 5. Containerd y dependencias de red indispensables
apt-get update -y &gt; /dev/null
apt-get install -y containerd apt-transport-https ca-certificates curl gpg conntrack socat &gt; /dev/null
mkdir -p /etc/containerd
containerd config default &gt; /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
systemctl restart containerd &amp;&amp; systemctl enable containerd &gt; /dev/null

# 6. Kubernetes v1.31 (pkgs.k8s.io)
K8S_REPO="https://pkgs.k8s.io/core:/stable:/v1.31/deb/"
KEYRING="/etc/apt/keyrings/kubernetes-apt-keyring.gpg"
mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL "${K8S_REPO}Release.key" | gpg --dearmor --yes -o "${KEYRING}"
echo "deb [signed-by=${KEYRING}] ${K8S_REPO} /" \
  &gt; /etc/apt/sources.list.d/kubernetes.list

apt-get update -y &gt; /dev/null
apt-get install -y kubelet kubeadm kubectl &gt; /dev/null
apt-mark hold kubelet kubeadm kubectl &gt; /dev/null</code></pre>

  <h4>3.4.2 Script del Master: <code>scripts/master.sh</code></h4>
  <pre><code>#!/bin/bash
set -euo pipefail
MASTER_IP="192.168.56.10"
POD_CIDR="10.244.0.0/16"

kubeadm config images pull &gt; /dev/null
kubeadm init \
  --apiserver-advertise-address="${MASTER_IP}" \
  --pod-network-cidr="${POD_CIDR}" \
  --node-name k8s-master &gt; /dev/null

mkdir -p /home/vagrant/.kube /root/.kube /vagrant_configs
cp -i /etc/kubernetes/admin.conf /home/vagrant/.kube/config
cp -i /etc/kubernetes/admin.conf /vagrant_configs/config
chown -R vagrant:vagrant /home/vagrant/.kube
chmod 644 /vagrant_configs/config

# Flannel CNI
FLANNEL_URL="https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml"
curl -sSL "${FLANNEL_URL}" -o /tmp/kube-flannel.yml
sed -i 's/- --kube-subnet-mgr/- --kube-subnet-mgr\n        - --iface=enp0s8/' /tmp/kube-flannel.yml
kubectl --kubeconfig=/etc/kubernetes/admin.conf apply -f /tmp/kube-flannel.yml &gt; /dev/null

# Generar join command para el worker
kubeadm token create --print-join-command &gt; /vagrant_configs/join.sh
chmod +x /vagrant_configs/join.sh</code></pre>

  <h4>3.4.3 Script del Worker: <code>scripts/worker.sh</code></h4>
  <pre><code>#!/bin/bash
set -euo pipefail

# Espera activa hasta que el master termine de inicializar
while [ ! -f /vagrant_configs/join.sh ]; do
  sleep 3
done

bash /vagrant_configs/join.sh &gt; /dev/null</code></pre>

  <h3 id="sec-3-5">3.5 Despliegue Desatendido con un solo comando</h3>
  <pre><code># 1. En el Host Ubuntu 20.04:
sudo apt-get update &amp;&amp; sudo apt-get install -y virtualbox vagrant

# 2. Levantar todo el cluster:
vagrant up

# 3. Administrar el cluster desde el host inmediatamente:
export KUBECONFIG=$(pwd)/configs/config
kubectl get nodes -o wide</code></pre>

  <h3 id="sec-3-6">3.6 Gestión del Ciclo de Vida del Cluster</h3>
  <table>
    <thead>
      <tr>
        <th>Operación</th>
        <th>Comando</th>
        <th>Descripción</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Consultar estado</strong></td>
        <td><code>vagrant status</code></td>
        <td>Muestra el estado de ejecución de ambas VMs.</td>
      </tr>
      <tr>
        <td><strong>Conexión SSH</strong></td>
        <td><code>vagrant ssh k8s-master</code></td>
        <td>Abre sesión de terminal en el nodo seleccionado.</td>
      </tr>
      <tr>
        <td><strong>Detener laboratorio</strong></td>
        <td><code>vagrant halt</code></td>
        <td>Apaga las VMs guardando el estado en disco (ahorro de batería).</td>
      </tr>
      <tr>
        <td><strong>Reanudar laboratorio</strong></td>
        <td><code>vagrant up</code></td>
        <td>Enciende nuevamente el cluster sin reinstalar.</td>
      </tr>
      <tr>
        <td><strong>Destruir laboratorio</strong></td>
        <td><code>vagrant destroy -f</code></td>
        <td>Elimina por completo las VMs de VirtualBox para empezar de cero.</td>
      </tr>
    </tbody>
  </table>

  <!-- SECCIÓN 3: KUBERNETES DASHBOARD -->
  <div class="page-break"></div>
  <div class="section-banner">
    <h2 id="sec-4">4. Sección 3: Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard</h2>
    <p>Objetivo pedagógico: Desplegar y acceder a la interfaz gráfica oficial del cluster, validando permisos RBAC y monitorización visual.</p>
  </div>

  <p>
    Para monitorizar y gestionar visualmente los recursos del cluster sin depender exclusivamente de la línea de comandos, desplegamos la interfaz gráfica oficial: el <strong>Kubernetes Dashboard</strong>. A continuación se detalla el procedimiento completo, incluyendo la verificación de estado de los pods, la creación declarativa de la cuenta administrativa RBAC, la obtención del token Bearer y las capturas visuales de la interfaz.
  </p>

  <h3 id="sec-4-1">4.1 Despliegue de los Componentes Oficiales del Dashboard</h3>
  <p>
    Aplica el manifiesto recomendado oficial de Kubernetes (versión v2.7.0), el cual genera el namespace dedicado <code>kubernetes-dashboard</code>, las cuentas de servicio, certificados autofirmados, roles RBAC y los deployments de la interfaz y del recolector de métricas:
  </p>
  <pre><code>kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created</code></pre>

  <h3 id="sec-4-2">4.2 Verificación del Estado de los Pods del Dashboard</h3>
  <p>
    Antes de intentar acceder, comprobamos que tanto el pod principal del Dashboard como el pod auxiliar <code>dashboard-metrics-scraper</code> hayan descargado sus imágenes y alcancen el estado <code>Running</code>:
  </p>
  <pre><code>kubectl get pods -n kubernetes-dashboard</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>NAME                                         READY   STATUS    RESTARTS   AGE
dashboard-metrics-scraper-6b96ff7878-2xhlz   1/1     Running   0          31s
kubernetes-dashboard-8696f5f494-hxd9c        1/1     Running   0          31s</code></pre>

  <h3 id="sec-4-3">4.3 Creación de Cuenta de Servicio y Privilegios Administrativos (RBAC)</h3>
  <p>
    Por defecto, el Dashboard se despliega con permisos mínimos restringidos. Para administrar y visualizar todos los namespaces y cargas de trabajo del cluster, creamos un usuario de servicio (<code>ServiceAccount</code>) con rol de superusuario (<code>cluster-admin</code>).
  </p>
  <p>Crea el archivo <code>dashboard-adminuser.yaml</code>:</p>
  <pre><code>apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard</code></pre>

  <p>Aplica este manifiesto en el cluster:</p>
  <pre><code>kubectl apply -f dashboard-adminuser.yaml</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>serviceaccount/admin-user created
clusterrolebinding.rbac.authorization.k8s.io/admin-user created</code></pre>

  <h3 id="sec-4-4">4.4 Comprobación de la Cuenta de Servicio Creada</h3>
  <p>Verificamos que el objeto <code>ServiceAccount</code> existe correctamente registrado en el namespace <code>kubernetes-dashboard</code>:</p>
  <pre><code>kubectl get serviceaccount admin-user -n kubernetes-dashboard</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>NAME         SECRETS   AGE
admin-user   0         38s</code></pre>

  <h3 id="sec-4-5">4.5 Generación del Token de Autenticación Bearer</h3>
  <p>
    En Kubernetes moderno (v1.24+ y v1.31), los tokens de ServiceAccount ya no se generan indefinidamente en secrets por defecto, sino que se solicitan mediante la API de tokens temporales de <code>kubectl</code>:
  </p>
  <pre><code>kubectl -n kubernetes-dashboard create token admin-user</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>eyJhbGciOiJSUzI1NiIsImtpZCI6IlUyUEhfRVVUckc1M0tfcWstRkFUd1E0ek9aMkluejhkc0FaVmJEOEo4SWcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzk0ODM1NDkyLCJpYXQiOjE3OTQ4MzE4OTIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNzYwODdjOWEtMTQ1ZS00ZWNhLTliMzItMjFlYjM0ZjhiZjIwIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJhZG1pbi11c2VyIiwidWlkIjoiN2ViY2M0YTAtYjk1MC00M2Q0LTg3OTYtMjI3NTNlNmEyODA3In19LCJuYmYiOjE3OTQ4MzE4OTIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlcm5ldGVzLWRhc2hib2FyZDphZG1pbi11c2VyIn0.Geq8LpwDCPqfYDGIfwjnnh8HClQKBLPscWoJ5AgekxMJGLKnXT878KleThDbFtHF5LDxB_DRod8H7yIXpUoimEOXdex0bYGj5jXT-Qt6T734BDh21ppavtrP4CmAJW_feyEcsFzGuXQ4qlmEOheSGRhePKIEahBnI05sqm9B1a90indvH4rx_qxAWrpxsY-QVyZcjjZXHr9DLcD3FEmpKz8wVFUsw-EaQ7SV3k39gBImBDO9Tk-dJwBiU5VNwYYXuCuGsaX7UxfFor-2fMp3CR-oX1Z1_huGWI7ynYKpRwy-49BnqrMmThjPUMImBL7jBFkURr_erazpiQcj0CziQ</code></pre>

  <div class="alert alert-note">
    <div class="alert-title">Nota sobre el Token Bearer</div>
    Copia íntegramente la cadena alfanumérica resultante en el portapapeles; será el secreto necesario para identificarte en el panel.
  </div>

  <h4>Opción Alternativa: Generación de Token Permanente (Sin Expiración)</h4>
  <p>
    Por defecto, los tokens generados con <code>kubectl create token</code> caducan automáticamente tras 1 hora. Si deseas evitar tener que solicitar y pegar un nuevo token en cada sesión de trabajo, puedes crear un token permanente declarativo asociando un objeto <code>Secret</code> al ServiceAccount <code>admin-user</code>.
  </p>

  <p>1. Crea el archivo <code>admin-user-secret.yaml</code>:</p>
  <pre><code>apiVersion: v1
kind: Secret
metadata:
  name: admin-user-secret
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "admin-user"
type: kubernetes.io/service-account-token</code></pre>
  <p>
    El tipo <code>kubernetes.io/service-account-token</code> le indica al plano de control de Kubernetes que genere de forma automática un token persistente y lo almacene en el secreto.
  </p>

  <p>2. Aplica el manifiesto en el cluster:</p>
  <pre><code>kubectl apply -f admin-user-secret.yaml</code></pre>
  <p><strong>Salida en consola:</strong></p>
  <pre><code>secret/admin-user-secret created</code></pre>

  <p>3. Extrae y decodifica el token permanente en Base64:</p>
  <pre><code>kubectl get secret admin-user-secret -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d</code></pre>
  <p>
    Este comando imprimirá directamente el token JWT no expirable. Puedes guardarlo de forma segura en un gestor de contraseñas local; permanecerá válido indefinidamente para iniciar sesión en el Dashboard mientras no se elimine el secreto <code>admin-user-secret</code>.
  </p>

  <div class="alert alert-warning">
    <div class="alert-title">Consideración de Seguridad Crítica: Token Permanente vs Producción</div>
    Los tokens permanentes <strong>no son seguros para su uso en entornos de producción</strong>, ya que vulneran el principio de menor privilegio al carecer de caducidad y rotación automática. Si una credencial estática de superadministrador (<code>cluster-admin</code>) se filtra, el cluster queda permanentemente comprometido hasta su revocación manual. Sin embargo, para esta prueba local de laboratorio y entornos de aprendizaje, su uso es plenamente válido por comodidad.
  </div>

  <h3 id="sec-4-6">4.6 Acceso Seguro mediante Kubectl Proxy</h3>
  <p>
    Para conectarse de forma segura desde el equipo anfitrión físico sin exponer el Dashboard directamente a redes externas no cifradas, iniciamos el túnel local de <code>kubectl proxy</code>:
  </p>
  <pre><code>kubectl proxy</code></pre>
  <p><strong>Salida en consola:</strong></p>
  <pre><code>Starting to serve on 127.0.0.1:8001</code></pre>
  <p>
    Manteniendo este proceso en ejecución, abre tu navegador web e introduce la siguiente URL exacta:
  </p>
  <pre><code>http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/</code></pre>

  <h3 id="sec-4-7">4.7 Inicio de Sesión y Verificación Visual del Panel</h3>
  <p>
    Al acceder a la URL indicada, el Dashboard presenta la pantalla de autenticación. Selecciona la opción <strong>Token</strong>, pega el token generado en el paso 4.5 y pulsa sobre <strong>Sign in</strong>:
  </p>
  <figure class="dashboard-figure">
    <img src="images/k8s_dashboard_login.png" alt="Pantalla de inicio de sesión de Kubernetes Dashboard">
    <figcaption class="figure-caption">Figura 3.1: Pantalla de inicio de sesión de Kubernetes Dashboard solicitando autenticación mediante Token.</figcaption>
  </figure>

  <p>
    Una vez autenticado como <code>admin-user</code>, se despliega el panel de control completo. En el selector superior de namespaces seleccionamos <code>kubernetes-dashboard</code> para confirmar que los pods, deployments y servicios recién creados se encuentran en estado saludable:
  </p>
  <figure class="dashboard-figure">
    <img src="images/k8s_dashboard.png" alt="Vista interna del Kubernetes Dashboard con los recursos del namespace">
    <figcaption class="figure-caption">Figura 3.2: Interfaz web de Kubernetes Dashboard mostrando el estado de los recursos y pods del namespace kubernetes-dashboard.</figcaption>
  </figure>

  <!-- SECCIÓN 4: EJEMPLO DE DESPLIEGUE -->
  <div class="page-break"></div>
  <div class="section-banner">
    <h2 id="sec-5">5. Sección 4: Ejemplo Práctico de Despliegue en el Cluster (Nginx)</h2>
    <p>Objetivo pedagógico: Validar la operatividad del cluster desplegando una carga de trabajo, exponiéndola vía NodePort y verificando tráfico HTTP.</p>
  </div>

  <h3 id="sec-5-1">5.1 Creación del Deployment de Nginx</h3>
  <p>
    Desplegamos un servidor web Nginx básico en el cluster utilizando un objeto de tipo <code>Deployment</code> en el namespace <code>default</code>:
  </p>
  <pre><code>kubectl create deployment nginx-test --image=nginx</code></pre>
  <p><strong>Salida real del comando:</strong></p>
  <pre><code>deployment.apps/nginx-test created</code></pre>

  <h3 id="sec-5-2">5.2 Inspección Detallada de Recursos del Cluster</h3>
  <p>
    Tras emitir la orden de creación, Kubernetes gestiona automáticamente la jerarquía de objetos: el Deployment gestiona un ReplicaSet, y este a su vez supervisa la creación y estado de salud de los Pods.
  </p>

  <h4>1. Verificación del Deployment</h4>
  <p>Comprobamos el estado del Deployment, observando que la réplica solicitada está lista y disponible:</p>
  <pre><code>kubectl get deployments -o wide</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>NAME         READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
nginx-test   1/1     1            1           11m   nginx        nginx    app=nginx-test</code></pre>

  <h4>2. Verificación del ReplicaSet</h4>
  <p>El Deployment ha creado un ReplicaSet con el hash correspondiente a la plantilla de Pods:</p>
  <pre><code>kubectl get rs -o wide</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>NAME                    DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES   SELECTOR
nginx-test-5b77bfd686   1         1         1       11m   nginx        nginx    app=nginx-test,pod-template-hash=5b77bfd686</code></pre>

  <h4>3. Verificación del Pod y su Asignación de Red</h4>
  <p>Comprobamos que el Pod se encuentra en estado <code>Running</code>, tiene una IP asignada dentro del rango CIDR de Flannel (<code>10.244.1.2</code>) y ha sido programado en el nodo worker (<code>k8s-worker1</code>):</p>
  <pre><code>kubectl get pods -o wide</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE          NOMINATED NODE   READINESS GATES
nginx-test-5b77bfd686-xsbgg   1/1     Running   0          11m   10.244.1.2   k8s-worker1   &lt;none&gt;           &lt;none&gt;</code></pre>

  <h3 id="sec-5-3">5.3 Exposición Externa mediante Servicio NodePort</h3>
  <p>
    Para acceder al servidor web Nginx desde el equipo anfitrión (o desde fuera del cluster), exponemos el despliegue creando un objeto <code>Service</code> de tipo <code>NodePort</code>. Este tipo de servicio abre un puerto aleatorio en el rango predeterminado de Kubernetes (<code>30000-32767</code>) en <strong>todos</strong> los nodos del cluster (tanto en <code>k8s-master</code> como en <code>k8s-worker1</code>):
  </p>
  <pre><code>kubectl expose deployment nginx-test --port=80 --type=NodePort</code></pre>

  <p>Listamos los servicios activos en el cluster para identificar el puerto <code>NodePort</code> asignado:</p>
  <pre><code>kubectl get services -o wide</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE   SELECTOR
kubernetes   ClusterIP   10.96.0.1     &lt;none&gt;        443/TCP        34h   &lt;none&gt;
nginx-test   NodePort    10.98.102.4   &lt;none&gt;        80:30482/TCP   10m   app=nginx-test</code></pre>

  <div class="alert alert-note">
    <div class="alert-title">Mapeo de Puertos NodePort</div>
    En la columna <code>PORT(S)</code> observamos el mapeo <code>80:30482/TCP</code>. El puerto interno del contenedor es el <code>80</code>, mientras que el puerto expuesto en los nodos del cluster es el <code>30482</code>. En su entorno de laboratorio este puerto se asignará de manera aleatoria entre el 30000 y el 32767.
  </div>

  <h3 id="sec-5-4">5.4 Verificación de Conectividad HTTP y Acceso Externo</h3>
  <p>
    Dado que el servicio <code>NodePort</code> publica el puerto en todos los nodos del cluster, podemos consultar cualquiera de las IPs de la red Host-Only (<code>192.168.56.0/24</code>) para acceder al servicio.
  </p>

  <h4>1. Identificación de las IPs de los Nodos</h4>
  <p>Listamos los nodos del cluster y sus direcciones IP internas:</p>
  <pre><code>kubectl get nodes -o wide</code></pre>
  <p><strong>Salida real de terminal:</strong></p>
  <pre><code>NAME          STATUS   ROLES           AGE   VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
k8s-master    Ready    control-plane   34h   v1.31.14   192.168.56.10   &lt;none&gt;        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1
k8s-worker1   Ready    &lt;none&gt;          34h   v1.31.14   192.168.56.11   &lt;none&gt;        Ubuntu 22.04.5 LTS   5.15.0-203-generic   containerd://2.2.1</code></pre>

  <h4>2. Acceso desde el Navegador Web</h4>
  <p>Desde el navegador del equipo anfitrión físico, podemos acceder a cualquiera de las dos URLs:</p>
  <ul>
    <li><code>http://192.168.56.10:30482/</code> (IP del nodo master)</li>
    <li><code>http://192.168.56.11:30482/</code> (IP del nodo worker)</li>
  </ul>

  <h4>3. Verificación mediante cURL en Consola</h4>
  <p>Comprobamos el acceso mediante <code>curl</code> apuntando a la IP del master:</p>
  <pre><code>curl http://192.168.56.10:30482/</code></pre>
  <p><strong>Salida de respuesta:</strong></p>
  <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;Welcome to nginx!&lt;/title&gt;
&lt;style&gt;
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
&lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;h1&gt;Welcome to nginx!&lt;/h1&gt;
&lt;p&gt;If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy,
API gateway, load balancer, content cache, or other features.&lt;/p&gt;

&lt;p&gt;For online documentation and support please refer to
&lt;a href="https://nginx.org/"&gt;nginx.org&lt;/a&gt;.&lt;br/&gt;
To engage with the community please visit
&lt;a href="https://community.nginx.org/"&gt;community.nginx.org&lt;/a&gt;.&lt;br/&gt;
For enterprise grade support, professional services, additional
security features and capabilities please refer to
&lt;a href="https://f5.com/nginx"&gt;f5.com/nginx&lt;/a&gt;.&lt;/p&gt;

&lt;p&gt;&lt;em&gt;Thank you for using nginx.&lt;/em&gt;&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

  <p>Comprobamos el acceso apuntando a la IP del worker:</p>
  <pre><code>curl http://192.168.56.11:30482/</code></pre>
  <p><strong>Salida de respuesta:</strong></p>
  <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;Welcome to nginx!&lt;/title&gt;
&lt;style&gt;
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
&lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;h1&gt;Welcome to nginx!&lt;/h1&gt;
&lt;p&gt;If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy,
API gateway, load balancer, content cache, or other features.&lt;/p&gt;

&lt;p&gt;For online documentation and support please refer to
&lt;a href="https://nginx.org/"&gt;nginx.org&lt;/a&gt;.&lt;br/&gt;
To engage with the community please visit
&lt;a href="https://community.nginx.org/"&gt;community.nginx.org&lt;/a&gt;.&lt;br/&gt;
For enterprise grade support, professional services, additional
security features and capabilities please refer to
&lt;a href="https://f5.com/nginx"&gt;f5.com/nginx&lt;/a&gt;.&lt;/p&gt;

&lt;p&gt;&lt;em&gt;Thank you for using nginx.&lt;/em&gt;&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

  <div class="alert alert-tip">
    <div class="alert-title">Enrutamiento Multinodo Transparente</div>
    Aunque el pod de Nginx está ejecutándose en el worker (<code>k8s-worker1</code>), la petición a la IP del master responde correctamente gracias a <code>kube-proxy</code> y Flannel CNI, que gestionan el balanceo y enrutamiento interno entre nodos automáticamente.
  </div>

  <h3 id="sec-5-5">5.5 Acceso Temporal mediante Port-Forward y Limpieza de Recursos</h3>
  <p>
    Además de exponer un servicio mediante <code>NodePort</code>, Kubernetes permite redirigir tráfico de forma temporal para pruebas y depuración inmediata utilizando el comando <code>kubectl port-forward</code>. Este comando abre un túnel directo desde un puerto local hacia el Pod o Deployment sin necesidad de un objeto Service:
  </p>
  <pre><code>kubectl port-forward deployment/nginx-test 8080:80 --address 0.0.0.0</code></pre>
  <p><strong>Salida real del comando:</strong></p>
  <pre><code>Forwarding from 0.0.0.0:8080 -&gt; 80</code></pre>
  <p>Con este túnel activo, podemos comprobar el servicio accediendo a <code>http://localhost:8080</code> o a la IP del nodo en el puerto <code>8080</code>.</p>

  <h4>Limpieza de Recursos de Prueba</h4>
  <p>Una vez concluidas las pruebas de validación, procedemos a eliminar tanto el Deployment como el Service creados para dejar el cluster en su estado original:</p>
  <pre><code>kubectl delete deployment,svc nginx-test</code></pre>

  <!-- TROUBLESHOOTING -->
  <div class="page-break"></div>
  <h2 id="sec-6">6. Resolución de Problemas Frecuentes (Troubleshooting)</h2>

  <div class="alert alert-important">
    <div class="alert-title">Fallo 1: "The connection to the server 10.0.2.15:6443 was refused"</div>
    <strong>Causa:</strong> No se especificó <code>--apiserver-advertise-address=192.168.56.10</code> en <code>kubeadm init</code> y el plano de control intentó anunciarse por la IP NAT.<br>
    <strong>Solución:</strong> Ejecutar <code>sudo kubeadm reset -f</code> en el master y volver a inicializar añadiendo explícitamente el parámetro de dirección.
  </div>

  <div class="alert alert-warning">
    <div class="alert-title">Fallo 2: "CoreDNS en estado Pending o CrashLoopBackOff"</div>
    <strong>Causa:</strong> El CNI no se ha instalado o Flannel eligió la interfaz incorrecta.<br>
    <strong>Solución:</strong> Verificar que Flannel tiene inyectado <code>- --iface=enp0s8</code>. Comprobar los logs de los pods de Flannel con <code>kubectl logs -n kube-system -l k8s-app=flannel</code>.
  </div>

  <div class="alert alert-warning">
    <div class="alert-title">Fallo 3: "kubelet fails with cgroup driver mismatch"</div>
    <strong>Causa:</strong> Containerd no tiene activado <code>SystemdCgroup = true</code> en <code>/etc/containerd/config.toml</code>.<br>
    <strong>Solución:</strong> Modificar el archivo de configuración de containerd y reiniciar con <code>sudo systemctl restart containerd &amp;&amp; sudo systemctl restart kubelet</code>.
  </div>

  <div class="alert alert-note">
    <div class="alert-title">Fallo 4: "El worker no puede conectarse al puerto 6443 del master"</div>
    <strong>Causa:</strong> El cortafuegos local (UFW) de Ubuntu Server está bloqueando el tráfico en la red privada.<br>
    <strong>Solución:</strong> En el master ejecutar <code>sudo ufw allow 6443/tcp</code> o deshabilitarlo para el laboratorio con <code>sudo ufw disable</code>.
  </div>

  <div class="alert alert-important" id="sec-6-5">
    <div class="alert-title">Fallo 5: Desalojo de Pods (Evicted) por "DiskPressure" y Particionamiento LVM por Defecto</div>
    <p>
      <strong>Síntomas:</strong> Pods en estado <code>Failed</code> o <code>Evicted</code> (frecuentemente los del Kubernetes Dashboard). En los eventos del pod o logs del kubelet se registra:
    </p>
    <pre><code>The node was low on resource: ephemeral-storage. Threshold quantity: 1569603441, available: 1356228Ki.
Container kubernetes-dashboard was using 1084Ki, request is 0, has larger consumption of ephemeral-storage.</code></pre>
    <p>
      <strong>Causa Raíz:</strong> Al instalar Ubuntu Server 22.04 LTS con LVM guiado por defecto, el instalador Subiquity no asigna el 100% del disco al volumen raíz (<code>ubuntu-lv</code>). Reserva ~50% del espacio en el Volume Group sin asignar (~8.2 GB libres en worker de 20 GB; ~11.5 GB libres en master de 25 GB). Al descargar imágenes de contenedores, el disco cae bajo el umbral mínimo del 10%-15% y el kubelet activa <em>DiskPressure</em> desalojando pods.
    </p>
    <p>
      <strong>Diagnóstico:</strong> Comprobar con <code>df -h /</code> (muestra solo ~9.7 GB en worker / ~11.5 GB en master) y con <code>lsblk</code> (muestra la partición <code>sda3</code> con el tamaño total pero <code>ubuntu--vg-ubuntu--lv</code> con solo la mitad asignada).
    </p>
    <p>
      <strong>Solución en Caliente (Worker y Master):</strong>
    </p>
    <pre><code># 1. Extender el volumen lógico al 100% del espacio libre restante en el VG
sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv

# 2. Redimensionar en caliente el sistema de archivos ext4 en línea
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv

# 3. Purgar los pods desalojados para que el Deployment regenere réplicas limpias
kubectl delete pods -n kubernetes-dashboard --field-selector=status.phase=Failed</code></pre>
  </div>

</body>
</html>
"""

OUTLINE_STRUCTURE = [
    {"title": "Portada", "page": 0},
    {"title": "Índice General", "page": 1},
    {
        "title": "1. Arquitectura del Laboratorio",
        "id": "sec-1",
        "children": [
            {"title": "1.1 Diagrama de Topología de Red y Componentes", "id": "sec-1-1"},
            {"title": "1.2 Matriz de Hardware e IP", "id": "sec-1-2"},
            {"title": "1.3 Alertas Críticas de Producción (Trampas habituales)", "id": "sec-1-3"},
        ]
    },
    {
        "title": "2. Sección 1: Despliegue Manual Paso a Paso con Kubeadm",
        "id": "sec-2",
        "children": [
            {"title": "2.1 Creación de la Red Solo-Anfitrión en VirtualBox (vboxnet0)", "id": "sec-2-1"},
            {
                "title": "2.2 Creación y Configuración de VMs en VirtualBox 7.0",
                "id": "sec-2-2",
                "children": [
                    {"title": "2.2.1 Creación de la Red Solo-Anfitrión (step_00.png)", "id": "sec-2-2-1"},
                    {"title": "2.2.2 Guía Paso a Paso para la VM Master (k8s-master)", "id": "sec-2-2-2"},
                    {"title": "2.2.3 Guía Paso a Paso para la VM Worker (k8s-worker1)", "id": "sec-2-2-3"},
                ]
            },
            {"title": "2.3 Configuración de Idioma y Teclado Español", "id": "sec-2-3"},
            {"title": "2.4 Persistencia de Red: Bloqueo de Cloud-Init y Netplan Estático", "id": "sec-2-4"},
            {"title": "2.5 Preparación Base del Sistema Operativo (SWAP, Kernel y Sysctl)", "id": "sec-2-5"},
            {"title": "2.6 Instalación de Containerd y Dependencias del Sistema (conntrack, socat)", "id": "sec-2-6"},
            {"title": "2.7 Instalación de Herramientas Kubernetes v1.31 (pkgs.k8s.io)", "id": "sec-2-7"},
            {"title": "2.8 Inicialización del Plano de Control (Master), Flannel CNI y Registros Reales", "id": "sec-2-8"},
            {"title": "2.9 Unión del Nodo Worker al Cluster con Dependencias y Registros Reales", "id": "sec-2-9"},
            {"title": "2.10 Conexión Remota No Destructiva desde el Host Anfitrión (Merge Kubeconfig)", "id": "sec-2-10"},
        ]
    },
    {
        "title": "3. Sección 2: Automatización Completa con Vagrant (IaC)",
        "id": "sec-3",
        "children": [
            {"title": "3.1 Arquitectura de Automatización con Vagrant", "id": "sec-3-1"},
            {"title": "3.2 Estructura del Proyecto de Infraestructura", "id": "sec-3-2"},
            {"title": "3.3 Archivo Vagrantfile Multi-Máquina", "id": "sec-3-3"},
            {"title": "3.4 Scripts de Aprovisionamiento Modular (common, master, worker)", "id": "sec-3-4"},
            {"title": "3.5 Despliegue Desatendido con un solo comando (vagrant up)", "id": "sec-3-5"},
            {"title": "3.6 Ciclo de Vida del Laboratorio (status, halt, ssh, destroy)", "id": "sec-3-6"},
        ]
    },
    {
        "title": "4. Sección 3: Instalación, Acceso y Verificación Gráfica del Kubernetes Dashboard",
        "id": "sec-4",
        "children": [
            {"title": "4.1 Despliegue de los Componentes Oficiales del Dashboard", "id": "sec-4-1"},
            {"title": "4.2 Verificación del Estado de los Pods del Dashboard", "id": "sec-4-2"},
            {"title": "4.3 Creación de Cuenta de Servicio y Privilegios Administrativos (RBAC)", "id": "sec-4-3"},
            {"title": "4.4 Comprobación de la Cuenta de Servicio Creada", "id": "sec-4-4"},
            {"title": "4.5 Generación del Token de Autenticación Bearer", "id": "sec-4-5"},
            {"title": "4.6 Acceso Seguro mediante Kubectl Proxy", "id": "sec-4-6"},
            {"title": "4.7 Inicio de Sesión y Verificación Visual del Panel", "id": "sec-4-7"},
        ]
    },
    {
        "title": "5. Sección 4: Ejemplo Práctico de Despliegue en el Cluster (Nginx)",
        "id": "sec-5",
        "children": [
            {"title": "5.1 Creación del Deployment de Nginx", "id": "sec-5-1"},
            {"title": "5.2 Inspección Detallada de Recursos del Cluster", "id": "sec-5-2"},
            {"title": "5.3 Exposición Externa mediante Servicio NodePort", "id": "sec-5-3"},
            {"title": "5.4 Verificación de Conectividad HTTP y Acceso Externo", "id": "sec-5-4"},
            {"title": "5.5 Acceso Temporal mediante Port-Forward y Limpieza de Recursos", "id": "sec-5-5"},
        ]
    },
    {
        "title": "6. Resolución de Problemas Frecuentes (Troubleshooting)",
        "id": "sec-6",
        "children": [
            {"title": "6.5 Desalojo de Pods por DiskPressure y Particionamiento LVM", "id": "sec-6-5"}
        ]
    }
]

def add_pdf_bookmarks(pdf_path):
    """Inyecta el árbol de marcadores (Document Outlines) en el PDF usando pypdf."""
    try:
        import pypdf
    except ImportError:
        print("Aviso: 'pypdf' no está disponible. Omitiendo inyección de marcadores del panel lateral.")
        return

    print("Inyectando marcadores jerárquicos (Document Outlines) en el panel lateral del PDF...")
    reader = pypdf.PdfReader(pdf_path)
    writer = pypdf.PdfWriter()
    writer.append(reader)

    def get_page(target_id):
        for key in (target_id, "/" + target_id):
            if key in reader.named_destinations:
                return reader.get_destination_page_number(reader.named_destinations[key])
        return None

    def add_items(items, parent=None):
        for item in items:
            p_num = item.get("page")
            if p_num is None and "id" in item:
                p_num = get_page(item["id"])
            if p_num is not None:
                node = writer.add_outline_item(item["title"], p_num, parent=parent)
                if "children" in item:
                    add_items(item["children"], parent=node)

    add_items(OUTLINE_STRUCTURE)

    temp_path = pdf_path + ".tmp"
    with open(temp_path, "wb") as f:
        writer.write(f)
    os.replace(temp_path, pdf_path)


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"HTML generado en: {HTML_PATH}")

    chrome_candidates = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    chrome_bin = None
    for cand in chrome_candidates:
        if os.path.exists(cand):
            chrome_bin = cand
            break
        found = shutil.which(cand)
        if found:
            chrome_bin = found
            break

    if not chrome_bin:
        chrome_bin = "google-chrome"
    cmd = [
        chrome_bin,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--enable-local-file-accesses",
        "--user-data-dir=/tmp/chrome-user-data",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH}",
        f"file://{HTML_PATH}"
    ]
    print(f"Compilando PDF con Chrome headless a: {PDF_PATH}...")
    if os.path.exists(PDF_PATH):
        os.remove(PDF_PATH)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and os.path.exists(PDF_PATH):
        add_pdf_bookmarks(PDF_PATH)
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"¡Éxito! Archivo PDF generado con marcadores del panel lateral: {PDF_PATH} ({size_kb:.1f} KB)")
    else:
        print("Error generando PDF:")
        print(res.stderr)
        exit(1)

if __name__ == "__main__":
    main()
