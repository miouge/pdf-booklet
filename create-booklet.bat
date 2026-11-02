@echo off

REM Run from the script directory.
cd /d "%~dp0"

REM Expose local helper commands to pdfbook2.
set "PATH=%~dp0.tools\bin;%PATH%"

REM Activate virtual environment.
call .venv\Scripts\activate.bat

::     GENERAL
::
::         --paper=STR, -p STR
::                 Format of the output paper dimensions as latex keyword (e.g.
::                 a4paper, letterpaper, legalpaper, ...)
::         --short-edge, -s
::                 Format the booklet for short-edge double-sided printing
::         --no-crop, -n
::                 Prevent the cropping to the content area
::
::     MARGINS
::
::         --outer-margin=INT, -o INT
::                 Defines the outer margin in the booklet (default: 40)
::         --inner-margin=INT, -i INT
::                 Defines the inner margin between the pages in the booklet
::                 (default: 150)
::         --top-margin=INT, -t INT
::                 Defines the top margin in the booklet (default: 30)
::         --bottom-margin=INT, -b INT
::                 Defines the bottom margin in the booklet (default: 30)
::
::     ADVANCED
::
::         --signature=INT
::                 Define the signature for the booklet handed to pdfjam, needs to
::                 be multiple of 4 (default: 4)
::         --signature*=INT
::                 Same as --signature
::         --resolution=INT
::                 Resolution used by ghostscript in bp (default: 72)

:: Check if parameter is provided
if "%~1"=="" (
    echo Erreur: Veuillez fournir le chemin du fichier PDF
    echo Usage: create-booklet.bat "chemin\vers\fichier.pdf"
    exit /b 1
)

:: Get input file path and extract directory and filename
set "INPUT_FILE=%~1"
set "INPUT_DIR=%~dp1"
set "INPUT_NAME=%~n1"
set "INPUT_EXT=%~x1"

:: Check if file exists
if not exist "%INPUT_FILE%" (
    echo Erreur: Le fichier "%INPUT_FILE%" n'existe pas
    exit /b 1
)

:: Remove previous output because pdfbook2 cannot overwrite it.
if exist "%INPUT_DIR%%INPUT_NAME%-book%INPUT_EXT%" (
    del /Q "%INPUT_DIR%%INPUT_NAME%-book%INPUT_EXT%"
)

:: Execute pdfbook2 command
call .\.tools\bin\pdfbook2.cmd "%INPUT_FILE%" --no-crop --outer-margin=0  --inner-margin=0  --top-margin=0 --bottom-margin=0
if errorlevel 1 exit /b %ERRORLEVEL%

:: Verify the output beside the source PDF.
if exist "%INPUT_DIR%%INPUT_NAME%-book%INPUT_EXT%" (
    echo Fichier cree: %INPUT_DIR%%INPUT_NAME%-book%INPUT_EXT%
) else (
    echo Attention: Le fichier de sortie n'a pas ete trouve
    exit /b 1
)
