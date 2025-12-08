# README Generator Agent - PowerShell Wrapper
# For Windows 11 developers

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Repository,
    
    [Parameter(Mandatory=$false)]
    [string]$Output = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Template = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Token = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateTemplate
)

# Script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if Python is available
$pythonCmd = $null
$pythonCommands = @("python", "python3", "py")

foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = $cmd
            Write-Host "Using Python: $version" -ForegroundColor Green
            break
        }
    }
    catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Host "Error: Python not found. Please install Python 3.7+ from python.org" -ForegroundColor Red
    exit 1
}

# Check if requests module is installed
$checkRequests = & $pythonCmd -c "import requests" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing required Python package 'requests'..." -ForegroundColor Yellow
    & $pythonCmd -m pip install requests
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install requests. Try: pip install requests" -ForegroundColor Red
        exit 1
    }
}

# Build arguments
$args = @($Repository)

if ($Output) {
    $args += @("-o", $Output)
}

if ($Template) {
    $args += @("-t", $Template)
}

if ($Token) {
    $args += @("--token", $Token)
}

if ($CreateTemplate) {
    $args = @("--create-template")
}

# Run the Python script
$pythonScript = Join-Path $ScriptDir "readme_agent.py"

if (-not (Test-Path $pythonScript)) {
    Write-Host "Error: readme_agent.py not found in $ScriptDir" -ForegroundColor Red
    exit 1
}

Write-Host "`nRunning README Generator Agent...`n" -ForegroundColor Cyan

& $pythonCmd $pythonScript @args

exit $LASTEXITCODE
