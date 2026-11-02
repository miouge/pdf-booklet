@echo off
setlocal

rem Use the pdflatex format through the MiKTeX PDFTeX binary.
set "MIKTEX_BIN=%~dp0..\miktex-private\install\miktex\bin\x64"

set "PATH=%MIKTEX_BIN%;%PATH%"
"%MIKTEX_BIN%\pdflatex.exe" %*
