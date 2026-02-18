@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "APP_PATH=%SCRIPT_DIR%final\app.py"
set "PY312=C:\Users\jhase\AppData\Local\Microsoft\WindowsApps\python3.12.exe"

if exist "%PY312%" (
  "%PY312%" "%APP_PATH%" %*
  exit /b %errorlevel%
)

where python3.12 >nul 2>nul
if %errorlevel%==0 (
  python3.12 "%APP_PATH%" %*
  exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%APP_PATH%" %*
  exit /b %errorlevel%
)

echo Python runtime not found. Install Python 3.12+ and try again.
exit /b 1
