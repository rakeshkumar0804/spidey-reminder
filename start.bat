@echo off
cd /d "%~dp0"
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "%~dp0companion.py"
) else (
    py "%~dp0companion.py"
)
