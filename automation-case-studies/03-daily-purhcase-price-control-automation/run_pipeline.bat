@echo off

cd /d "%~dp0"

if not exist "logs" mkdir "logs"

set PYTHONUTF8=1

echo. >> "logs\run_pipeline.log"
echo %date% %time% - Proces zahajen >> "logs\run_pipeline.log"

"%~dp0..\..\.venv\Scripts\python.exe" "%~dp0src\pricing_control.py" >> "logs\run_pipeline.log" 2>&1

set EXIT_CODE=%ERRORLEVEL%

echo %date% %time% - Navratovy kod: %EXIT_CODE% >> "logs\run_pipeline.log"

exit /b %EXIT_CODE%