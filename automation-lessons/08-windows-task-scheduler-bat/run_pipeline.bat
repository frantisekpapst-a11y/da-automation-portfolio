@echo off
cd /d "%~dp0..\.."

".venv\Scripts\python.exe" "automation-lessons\06-logging-monitoring\src\validate_github_issues.py"

exit /b %ERRORLEVEL%