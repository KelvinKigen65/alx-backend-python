#!/bin/bash

# setup-ingress.sh - Kubernetes Ingress Setup Script for Django App
# This script installs Nginx Ingress Controller and configures Ingress for Django app

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INGRESS_NAMESPACE="ingress-nginx"
APP_NAMESPACE="default"
INGRESS_NAME="django-messaging-ingress"
SERVICE_NAME="django-messaging-service"

echo -e "${BLUE}=== Kubernetes Ingress Setup for Django App ===${NC}"
echo ""

# Function to print section headers
print_section() {
    echo -e "${YELLOW}=== $1 ===${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_section "Step 1: Checking Prerequisites"
if ! command_exists kubectl; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ kubectl is available${NC}"

# Check if running on minikube
if command_exists minikube && minikube status >/dev/null 2>&1; then
    MINIKUBE_ENV=true
    echo -e "${YELLOW}Detected minikube environment${NC}"
else
    MINIKUBE_ENV=false
    echo "Running on standard Kubernetes cluster"
fi
echo ""

# Step 2: Install Nginx Ingress Controller
print_section "Step 2: Installing Nginx Ingress Controller"

if kubectl get namespace $INGRESS_NAMESPACE >/dev/null 2>&1; then
    echo "Nginx Ingress Controller namespace already exists"
else
    echo "Installing Nginx Ingress Controller..."
    
    if [ "$MINIKUBE_ENV" = true ]; then
        echo "Enabling minikube ingress addon..."
        minikube addons enable ingress
    else
        echo "Installing Nginx Ingress Controller for cloud provider..."
        kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml
    fi
fi

echo "Waiting for Nginx Ingress Controller to be ready..."
kubectl wait --namespace $INGRESS_NAMESPACE \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s

echo -e "${GREEN}✓ Nginx Ingress Controller is ready${NC}"
echo ""

# Step 3: Verify Ingress Controller
print_section "Step 3: Verifying Ingress Controller"
echo "Ingress Controller pods:"
kubectl get pods -n $INGRESS_NAMESPACE

echo ""
echo "Ingress Controller service:"
kubectl get service -n $INGRESS_NAMESPACE
echo ""

# Step 4: Check if service exists, create if needed
print_section "Step 4: Checking Django Service"
if kubectl get service $SERVICE_NAME -n $APP_NAMESPACE >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Service $SERVICE_NAME already exists${NC}"
else
    echo -e "${YELLOW}Service $SERVICE_NAME not found. It will be created with the Ingress configuration.${NC}"
fi
echo ""

# Step 5: Apply Ingress configuration
print_section "Step 5: Applying Ingress Configuration"
if [ ! -f "ingress.yaml" ]; then
    echo -e "${RED}Error: ingress.yaml file not found${NC}"
    echo "Please ensure ingress.yaml is in the current directory"
    exit 1
fi

echo "Applying Ingress configuration..."
kubectl apply -f ingress.yaml

echo -e "${GREEN}✓ Ingress configuration applied${NC}"
echo ""

# Step 6: Verify Ingress resource
print_section "Step 6: Verifying Ingress Resource"
echo "Waiting for Ingress to be ready..."
sleep 10

echo "Ingress resources:"
kubectl get ingress -n $APP_NAMESPACE

echo ""
echo "Detailed Ingress information:"
kubectl describe ingress $INGRESS_NAME -n $APP_NAMESPACE
echo ""

# Step 7: Get access information
print_section "Step 7: Access Information"

if [ "$MINIKUBE_ENV" = true ]; then
    echo -e "${BLUE}Minikube Environment Detected${NC}"
    echo "To access your application:"
    echo "1. Run: minikube tunnel (in a separate terminal)"
    echo "2. Add to /etc/hosts: echo '127.0.0.1 django-messaging.local' | sudo tee -a /etc/hosts"
    echo "3. Access at: http://django-messaging.local"
    echo ""
    echo "Or get the minikube IP:"
    MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "Not available")
    echo "Minikube IP: $MINIKUBE_IP"
    if [ "$MINIKUBE_IP" != "Not available" ]; then
        echo "Add to /etc/hosts: echo '$MINIKUBE_IP django-messaging.local' | sudo tee -a /etc/hosts"
    fi
else
    echo -e "${BLUE}Getting External Access Information${NC}"
    echo "Waiting for external IP assignment..."
    
    # Wait for external IP (timeout after 2 minutes)
    timeout=120
    while [ $timeout -gt 0 ]; do
        EXTERNAL_IP=$(kubectl get service -n $INGRESS_NAMESPACE ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
        if [ -n "$EXTERNAL_IP" ] && [ "$EXTERNAL_IP" != "null" ]; then
            break
        fi
        echo "Waiting for external IP... (${timeout}s remaining)"
        sleep 10
        timeout=$((timeout - 10))
    done
    
    if [ -n "$EXTERNAL_IP" ] && [ "$EXTERNAL_IP" != "null" ]; then
        echo -e "${GREEN}External IP: $EXTERNAL_IP${NC}"
        echo "Access your application at: http://$EXTERNAL_IP"
        echo "API endpoint: http://$EXTERNAL_IP/api/"
        echo "Admin panel: http://$EXTERNAL_IP/admin/"
    else
        echo -e "${YELLOW}External IP not yet assigned. Check later with:${NC}"
        echo "kubectl get service -n $INGRESS_NAMESPACE"
    fi
fi

echo ""

# Step 8: Testing commands
print_section "Step 8: Testing Commands"
echo "Test your application with these commands:"
echo ""
echo "# Check Ingress status:"
echo "kubectl get ingress"
echo ""
echo "# Test with curl (replace <IP> with actual IP):"
echo "curl -H 'Host: django-messaging.local' http://<IP>/"
echo "curl -H 'Host: django-messaging.local' http://<IP>/api/"
echo ""
echo "# View Ingress logs:"
echo "kubectl logs -n $INGRESS_NAMESPACE -l app.kubernetes.io/name=ingress-nginx"
echo ""

# Step 9: Cleanup information
print_section "Cleanup Commands (for future reference)"
echo "To remove the Ingress setup:"
echo "kubectl delete -f ingress.yaml"
echo "kubectl delete namespace $INGRESS_NAMESPACE"
echo ""

echo -e "${GREEN}=== Ingress Setup Complete! ===${NC}"
echo ""
echo "Your Django application should now be accessible through the Ingress controller."
echo "Check the access information abo"