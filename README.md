# decentralized-model-api
---
```markdown
# Decentralized Model API

This repository contains the code for the Decentralized Model API project. This document provides instructions on how to set up and run the project.

## Prerequisites

You will need to have the following software installed on your system:

- Docker Desktop for Windows
- kubectl (Kubernetes command-line utility)
- kind (Kubernetes IN Docker)

If you do not have these installed, you can use the Chocolatey package manager to install them. Run the following commands in an elevated PowerShell:

```bash
choco install docker-desktop
choco install kubernetes-cli
choco install kind
```

## Setup

Follow these steps to set up and run the project:

1. **Create a cluster**. Run the command `kind create cluster`.

2. **Get ingress**. Run the following commands:

   ```bash
   helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
   helm repo update
   helm install my-release ingress-nginx/ingress-nginx
   ```

3. **Deploy the application**. Run the following commands:

   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f model-server-ingress.yaml
   ```

   Please note that you may need to wait for a while (around 30 minutes) for everything to download.

5. **Open `index.html`**.

6. **Test the application**. Paste an image URL into the textbox in the opened webpage and submit it.

You're done!

## Verification

To verify that the Kubernetes setup is ready, run the command `kubectl get pods`.
