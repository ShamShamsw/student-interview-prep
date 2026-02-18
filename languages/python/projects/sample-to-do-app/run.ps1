param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AppArgs
)

$appPath = Join-Path $PSScriptRoot "final/app.py"

$py312 = "C:/Users/jhase/AppData/Local/Microsoft/WindowsApps/python3.12.exe"

if (Test-Path $py312) {
    & $py312 $appPath @AppArgs
    exit $LASTEXITCODE
}

if (Get-Command python3.12 -ErrorAction SilentlyContinue) {
    python3.12 $appPath @AppArgs
    exit $LASTEXITCODE
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    python $appPath @AppArgs
    exit $LASTEXITCODE
}

Write-Error "Python runtime not found. Install Python 3.12+ and try again."
exit 1
