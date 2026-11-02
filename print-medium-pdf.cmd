@echo off
REM Activate virtual environment and launch print-medium-pdf.py

cd /d "%~dp0"

REM Expose local helper commands to the GUI and child scripts.
set "PATH=%~dp0.tools\bin;%PATH%"

call .venv\Scripts\activate.bat

python "%~dp0print-medium-pdf.py"

::pause
