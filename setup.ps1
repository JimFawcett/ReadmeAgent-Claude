# README Agent Setup Script for Windows 11
# Run this script to set up the README generator

Write-Host "README Generator Agent - Setup" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow

$pythonCmd = $null
$pythonCommands = @("python", "python3", "py")

foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = $cmd
            Write-Host "✓ Found: $version" -ForegroundColor Green
            break
        }
    }
    catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "`nPlease install Python 3.7+ from:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/`n" -ForegroundColor Cyan
    exit 1
}

# Install dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$requirementsFile = Join-Path $scriptDir "requirements.txt"

if (Test-Path $requirementsFile) {
    & $pythonCmd -m pip install -r $requirementsFile
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "✗ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Check for GitHub token
Write-Host "`nChecking GitHub token configuration..." -ForegroundColor Yellow

$githubToken = $env:GITHUB_TOKEN

if ($githubToken) {
    Write-Host "✓ GITHUB_TOKEN environment variable is set" -ForegroundColor Green
}
else {
    Write-Host "⚠ GITHUB_TOKEN not set (optional but recommended)" -ForegroundColor Yellow
    Write-Host "`nTo avoid GitHub API rate limits, set your token:" -ForegroundColor Cyan
    Write-Host "  1. Create token at: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "  2. Set environment variable:" -ForegroundColor White
    Write-Host "     `$env:GITHUB_TOKEN = 'your_token_here'" -ForegroundColor Gray
    Write-Host "  3. Or add to PowerShell profile for persistence:`n" -ForegroundColor White
    Write-Host "     Add this line to: $PROFILE" -ForegroundColor Gray
    Write-Host "     `$env:GITHUB_TOKEN = 'your_token_here'`n" -ForegroundColor Gray
}

# Test the agent
Write-Host "`nTesting README agent..." -ForegroundColor Yellow

$testScript = Join-Path $scriptDir "readme_agent.py"

if (Test-Path $testScript) {
    & $pythonCmd $testScript --help > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Agent is working correctly" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Agent test failed" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "Usage Examples:" -ForegroundColor Yellow
Write-Host "  # Using PowerShell wrapper:" -ForegroundColor White
Write-Host "  .\generate-readme.ps1 octocat/Hello-World`n" -ForegroundColor Gray

Write-Host "  # Using Python directly:" -ForegroundColor White
Write-Host "  python readme_agent.py microsoft/vscode`n" -ForegroundColor Gray

Write-Host "  # Create custom template:" -ForegroundColor White
Write-Host "  python readme_agent.py --create-template`n" -ForegroundColor Gray

Write-Host "  # With custom output location:" -ForegroundColor White
Write-Host "  .\generate-readme.ps1 torvalds/linux -Output C:\Projects\linux_README.md`n" -ForegroundColor Gray

Write-Host "For more options, run:" -ForegroundColor White
Write-Host "  python readme_agent.py --help`n" -ForegroundColor Gray
