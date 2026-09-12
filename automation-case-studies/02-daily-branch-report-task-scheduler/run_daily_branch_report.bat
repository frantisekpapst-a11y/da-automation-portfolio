@echo off

cd /d "C:\Users\frant\Documents\data-analytics-workspace\da-automation-portfolio"

"C:\Users\frant\Documents\data-analytics-workspace\da-automation-portfolio\.venv\Scripts\python.exe" "C:\Users\frant\Documents\data-analytics-workspace\da-automation-portfolio\automation-case-studies\02-daily-branch-report-task-scheduler\src\daily_branch_report.py"

exit /b %ERRORLEVEL%