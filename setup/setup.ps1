# Windows setup: right-click > Run with PowerShell, or: powershell -ExecutionPolicy Bypass -File setup\setup.ps1
$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent)
$py = $null
foreach ($c in @("py -3", "python", "python3")) {
  try { $v = Invoke-Expression "$c --version" 2>$null; if ($v -match "Python 3\.(1[0-9]|[2-9][0-9])") { $py = $c; break } } catch {}
}
if (-not $py) {
  Write-Host "Python 3.10+ not found - installing with winget..."
  winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
  Write-Host "Open a NEW terminal and run this script again."; exit 1
}
Write-Host "Using $py"
Invoke-Expression "$py engine/doctor.py --install"
Invoke-Expression "$py engine/doctor.py"
