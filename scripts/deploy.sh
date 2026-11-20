#!/usr/bin/env bash
# ==========================================================
# Automated Deploy Script for Student ID: 68130239
# Run on k8s-control: bash scripts/deploy.sh
# ==========================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
NS="id-239"

echo "=========================================================="
echo " [1/5] Checking NGINX Ingress Controller..."
echo "=========================================================="
if ! kubectl get namespace ingress-nginx >/dev/null 2>&1; then
  echo "Installing NGINX Ingress Controller (Bare-metal)..."
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.3/deploy/static/provider/baremetal/deploy.yaml
  echo "Waiting for ingress-nginx-controller to be ready..."
  kubectl wait --namespace ingress-nginx \
    --for=condition=ready pod \
    --selector=app.kubernetes.io/component=controller \
    --timeout=180s
else
  echo "NGINX Ingress Controller already installed."
fi

# กำหนด NodePort ของ Ingress Controller เป็น 31080 เพื่อไม่ให้ชนกับ Lab เดิม (30080)
kubectl patch svc ingress-nginx-controller -n ingress-nginx \
  --type='json' \
  -p='[{"op":"replace","path":"/spec/ports/0/nodePort","value":31080}]' >/dev/null 2>&1 || true

echo "=========================================================="
echo " [2/5] Creating Namespace & Persistent Storage..."
echo "=========================================================="
kubectl apply -f "$PROJECT_DIR/k8s/00-namespace.yaml"
kubectl apply -f "$PROJECT_DIR/k8s/01-storage.yaml"

echo "=========================================================="
echo " [3/5] Packaging Application Code into ConfigMaps..."
echo "=========================================================="
kubectl create configmap app-about-files \
  --from-file="$PROJECT_DIR/apps/app-about/" \
  -n "$NS" --dry-run=client -o yaml | kubectl apply -f -

kubectl create configmap app-research-code \
  --from-file="$PROJECT_DIR/apps/app-research/server.py" \
  -n "$NS" --dry-run=client -o yaml | kubectl apply -f -

kubectl create configmap app-api-code \
  --from-file="$PROJECT_DIR/apps/app-api/server.py" \
  -n "$NS" --dry-run=client -o yaml | kubectl apply -f -

echo "=========================================================="
echo " [4/5] Deploying Deployments, Services & Ingress..."
echo "=========================================================="
kubectl apply -f "$PROJECT_DIR/k8s/02-app-about.yaml"
kubectl apply -f "$PROJECT_DIR/k8s/03-app-research.yaml"
kubectl apply -f "$PROJECT_DIR/k8s/04-app-api.yaml"
kubectl apply -f "$PROJECT_DIR/k8s/05-ingress.yaml"

echo "=========================================================="
echo " [5/5] Restarting & Waiting for Pods to become Ready..."
echo "=========================================================="
kubectl rollout restart deployment/app-about deployment/app-research deployment/app-api -n "$NS"
kubectl rollout status deployment/app-about -n "$NS" --timeout=120s
kubectl rollout status deployment/app-research -n "$NS" --timeout=120s
kubectl rollout status deployment/app-api -n "$NS" --timeout=120s

echo ""
echo "Deployment Complete! Current resources in namespace '$NS':"
kubectl get pv,pvc,pods,svc,ingress -n "$NS" -o wide
