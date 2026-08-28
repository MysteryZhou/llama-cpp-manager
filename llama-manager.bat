@echo off
rem =====================================================
rem  llama.cpp Model Manager - one-click launcher
rem  Double-click to open the dashboard in your browser.
rem =====================================================
setlocal
cd /d "%~dp0"

rem --- already running? just open browser ---
netstat -ano | findstr ":17890" | findstr "LISTENING" >nul 2>nul
if %errorlevel%==0 goto open

rem --- locate python ---
set "PY=python"
where python >nul 2>nul || set "PY=py -3"

rem --- start backend (hidden window) ---
start "llama-manager" /min "%PY%" server.py

rem --- wait for port then open browser ---
set /a n=0
:waitloop
netstat -ano | findstr ":17890" | findstr "LISTENING" >nul 2>nul
if not %errorlevel%==0 (
  set /a n+=1
  if %n% lss 20 ( timeout /t 1 /nobreak >nul & goto waitloop )
)

:open
start "" "http://127.0.0.1:17890"
endlocal
exit /b
