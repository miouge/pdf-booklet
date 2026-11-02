@echo off
setlocal

rem Ensure MiKTeX tools are available for the script.
set "MIKTEX_BIN=%~dp0..\miktex-private\install\miktex\bin\x64"
if not defined PDFJAM_SCRIPT set "PDFJAM_SCRIPT=%APPDATA%\MiKTeX\2.9\scripts\pdfjam\pdfjam"
set "SH_EXE=C:\Program Files\Git\usr\bin\sh.exe"
set "GIT_USR_BIN=C:\Program Files\Git\usr\bin"

set "PATH=%GIT_USR_BIN%;%MIKTEX_BIN%;%PATH%"
"%SH_EXE%" "%PDFJAM_SCRIPT%" %*
