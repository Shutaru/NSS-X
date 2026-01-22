# NSS X - Deployment Script for NVIDIA Spark Server (PowerShell)
# Target: 192.168.1.208 (spark_001)

param(
    [string]$ServerIP = "192.168.1.208",
    [string]$ServerUser = "spark_001",
    [string]$ServerPassword = "Kotav2022++",
    [string]$RemoteDir = "/home/spark_001/nss-x"
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  NSS X - Deploy to NVIDIA Spark Server" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

Write-Host "Working directory: $ScriptDir" -ForegroundColor Yellow

# Files to transfer
$FilesToCopy = @(
    "Dockerfile",
    "docker-compose.yml",
    "requirements-docker.txt",
    "requirements.txt",
    "README.md"
)

$FoldersToCopy = @(
    "src",
    "scripts",
    "config",
    "01_data",
    "02_analytics"
)

Write-Host ""
Write-Host "Step 1: Creating deployment archive..." -ForegroundColor Green

# Create temp directory for deployment
$TempDir = Join-Path $env:TEMP "nss-x-deploy"
if (Test-Path $TempDir) { Remove-Item $TempDir -Recurse -Force }
New-Item -ItemType Directory -Path $TempDir | Out-Null

# Copy files
foreach ($file in $FilesToCopy) {
    $src = Join-Path $ScriptDir $file
    if (Test-Path $src) {
        Copy-Item $src $TempDir
        Write-Host "  Copied: $file" -ForegroundColor Gray
    }
}

# Copy folders
foreach ($folder in $FoldersToCopy) {
    $src = Join-Path $ScriptDir $folder
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $TempDir $folder) -Recurse
        Write-Host "  Copied: $folder/" -ForegroundColor Gray
    }
}

# Create archive
$ArchivePath = Join-Path $env:TEMP "nss-x-deploy.tar.gz"
if (Test-Path $ArchivePath) { Remove-Item $ArchivePath }

Write-Host ""
Write-Host "Step 2: Creating tarball..." -ForegroundColor Green
Push-Location $TempDir
tar -czf $ArchivePath *
Pop-Location
Write-Host "  Archive created: $ArchivePath" -ForegroundColor Gray

Write-Host ""
Write-Host "Step 3: Transferring to server..." -ForegroundColor Green
Write-Host "  Target: ${ServerUser}@${ServerIP}:${RemoteDir}" -ForegroundColor Gray

# Use SCP to transfer
$scpCommand = "scp -o StrictHostKeyChecking=no `"$ArchivePath`" ${ServerUser}@${ServerIP}:/tmp/nss-x-deploy.tar.gz"
Write-Host "  Running: scp to server..." -ForegroundColor Gray
Invoke-Expression $scpCommand

Write-Host ""
Write-Host "Step 4: Setting up on server..." -ForegroundColor Green

# SSH commands to run on server
$sshCommands = @"
# Create directory
mkdir -p $RemoteDir
cd $RemoteDir

# Extract archive
tar -xzf /tmp/nss-x-deploy.tar.gz
rm /tmp/nss-x-deploy.tar.gz

# Stop existing containers
docker compose down 2>/dev/null || true

# Build and start
echo 'Building Docker image...'
docker compose build

echo 'Starting containers...'
docker compose up -d

# Wait for startup
sleep 15

# Show status
echo ''
echo '=== Container Status ==='
docker compose ps

echo ''
echo '=== Recent Logs ==='
docker compose logs --tail=30
"@

$sshCommand = "ssh -o StrictHostKeyChecking=no ${ServerUser}@${ServerIP} '$sshCommands'"
Write-Host "  Running deployment commands on server..." -ForegroundColor Gray
Invoke-Expression $sshCommand

# Cleanup
Remove-Item $TempDir -Recurse -Force
if (Test-Path $ArchivePath) { Remove-Item $ArchivePath }

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dashboard URLs:" -ForegroundColor Yellow
Write-Host "  Public:  https://nss-x.ngrok.dev" -ForegroundColor White
Write-Host "  Local:   http://${ServerIP}:8501" -ForegroundColor White
Write-Host ""
Write-Host "Management Commands:" -ForegroundColor Yellow
Write-Host "  Logs:    ssh ${ServerUser}@${ServerIP} 'cd ${RemoteDir} && docker compose logs -f'" -ForegroundColor Gray
Write-Host "  Stop:    ssh ${ServerUser}@${ServerIP} 'cd ${RemoteDir} && docker compose down'" -ForegroundColor Gray
Write-Host "  Restart: ssh ${ServerUser}@${ServerIP} 'cd ${RemoteDir} && docker compose restart'" -ForegroundColor Gray
