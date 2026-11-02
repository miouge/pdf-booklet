@echo off
setlocal

rem Forward to the MiKTeX binary with a stable command name.
set "MIKTEX_BIN=%~dp0..\miktex-private\install\miktex\bin\x64"

set "PATH=%MIKTEX_BIN%;%PATH%"
"%MIKTEX_BIN%\kpsewhich.exe" %*
