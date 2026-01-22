#!/bin/bash
# NSS X - Deployment Script for NVIDIA Spark Server
# Target: 192.168.1.208 (spark_001)

set -e

# Configuration
SERVER_IP="192.168.1.208"
SERVER_USER="spark_001"
PROJECT_NAME="nss-x"
REMOTE_DIR="/home/spark_001/nss-x"

echo "=========================================="
echo "  NSS X - Deploy to NVIDIA Spark Server"
echo "=========================================="

# Check if sshpass is available (for non-interactive password)
if ! command -v sshpass &> /dev/null; then
    echo "Note: sshpass not found. You'll be prompted for password."
    SSH_CMD="ssh"
    SCP_CMD="scp"
else
    echo "Using sshpass for automated login"
    SSH_CMD="sshpass -p 'Kotav2022++' ssh"
    SCP_CMD="sshpass -p 'Kotav2022++' scp"
fi

SSH_OPTS="-o StrictHostKeyChecking=no"

echo ""
echo "Step 1: Creating remote directory..."
ssh $SSH_OPTS ${SERVER_USER}@${SERVER_IP} "mkdir -p ${REMOTE_DIR}"

echo ""
echo "Step 2: Syncing project files..."
# Use rsync if available, otherwise scp
if command -v rsync &> /dev/null; then
    rsync -avz --progress \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='*.pyc' \
        --exclude='.pytest_cache' \
        --exclude='node_modules' \
        ./ ${SERVER_USER}@${SERVER_IP}:${REMOTE_DIR}/
else
    # Create tarball excluding unnecessary files
    tar --exclude='.venv' --exclude='__pycache__' --exclude='.git' \
        --exclude='*.pyc' --exclude='.pytest_cache' \
        -czf /tmp/nss-x.tar.gz .
    scp $SSH_OPTS /tmp/nss-x.tar.gz ${SERVER_USER}@${SERVER_IP}:${REMOTE_DIR}/
    ssh $SSH_OPTS ${SERVER_USER}@${SERVER_IP} "cd ${REMOTE_DIR} && tar -xzf nss-x.tar.gz && rm nss-x.tar.gz"
fi

echo ""
echo "Step 3: Building and starting Docker containers..."
ssh $SSH_OPTS ${SERVER_USER}@${SERVER_IP} << 'ENDSSH'
cd /home/spark_001/nss-x

# Stop existing containers
docker compose down 2>/dev/null || true

# Build and start
docker compose build --no-cache
docker compose up -d

# Show status
echo ""
echo "Container Status:"
docker compose ps

echo ""
echo "Waiting for services to start..."
sleep 10

# Check health
docker compose logs --tail=20
ENDSSH

echo ""
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
echo ""
echo "Dashboard URL: https://nss-x.ngrok.dev"
echo "Local URL: http://${SERVER_IP}:8501"
echo ""
echo "To check logs: ssh ${SERVER_USER}@${SERVER_IP} 'cd ${REMOTE_DIR} && docker compose logs -f'"
echo "To stop: ssh ${SERVER_USER}@${SERVER_IP} 'cd ${REMOTE_DIR} && docker compose down'"
