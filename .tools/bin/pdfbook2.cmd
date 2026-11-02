@echo off
setlocal

rem Run the repository script with the local virtual environment when available.
for %%I in ("%~dp0..\..") do set "PROJECT_ROOT=%%~fI"
set "VENV_PYTHON=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "SCRIPT_PATH=%PROJECT_ROOT%\pdfbook2\pdfbook2"

rem Expose companion commands resolved by the Python script.
set "PATH=%PROJECT_ROOT%\.tools\bin;%PATH%"

if exist "%VENV_PYTHON%" (
    "%VENV_PYTHON%" "%SCRIPT_PATH%" %*
) else (
    python "%SCRIPT_PATH%" %*
)
