# ============================================================
# Windows PowerShell script to run FLO v2 ROS Docker
# ============================================================
# Prerequisites:
# 1. Install Docker Desktop for Windows
# 2. Install VcXsrv (Windows X Server) from: https://sourceforge.net/projects/vcxsrv/
# 3. Start VcXsrv with: "Multiple windows", "Start no client", and DISABLE "Native opengl" + CHECK "Disable access control"
# ============================================================

Write-Host "=== FLO v2 Docker Setup for Windows ===" -ForegroundColor Cyan

# Stop and remove old container if exists
Write-Host "`nRemoving old container..." -ForegroundColor Yellow
docker rm -f flo_v2_container 2>$null

# Build Docker image
Write-Host "`nBuilding Docker image (this may take 10-20 minutes on first run)..." -ForegroundColor Yellow
docker build -t flo_v2_image .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nDocker image built successfully!" -ForegroundColor Green

# Get host IP for X11 (in case host.docker.internal doesn't work)
$hostIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*WSL*" -or $_.InterfaceAlias -like "*Ethernet*" -or $_.InterfaceAlias -like "*Wi-Fi*"} | Select-Object -First 1).IPAddress

Write-Host "`n=== Starting Container ===" -ForegroundColor Cyan
Write-Host "Display will be forwarded to: host.docker.internal:0" -ForegroundColor Yellow
Write-Host "Make sure VcXsrv is running!" -ForegroundColor Yellow
Write-Host "`nPress any key to continue..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Run container
docker run -it --rm `
  --name flo_v2_container `
  -e DISPLAY=host.docker.internal:0 `
  -e QT_X11_NO_MITSHM=1 `
  -e LIBGL_ALWAYS_INDIRECT=1 `
  -p 11311:11311 `
  -p 1883:1883 `
  -p 8080:8080 `
  --network bridge `
  flo_v2_image

Write-Host "`nContainer exited." -ForegroundColor Yellow

