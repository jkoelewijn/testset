@echo off

rem This script copies the GTFS-RT tripUpdates.pb files to the bin directory that are needed
rem by gtfs-rt-server.jar

rem Set data directory with GTFS-RT files as tripUpdates.pb files in separate directories
set DATA_DIRECTORY="%~dp0..\tests"

rem Set output directory. This should be the directory containing gtfs-rt-server.jar
set BIN_DIRECTORY="%~dp0..\bin"


rem Copy and rename GTFS-RT tripUpdates.pb files
del /Q %BIN_DIRECTORY%\"tripUpdates_*.pb" 2> nul
for /F "delims=" %%f in ('dir %DATA_DIRECTORY% /A:D /B /O:N') do (
    copy /B /V /Y %DATA_DIRECTORY%\"%%f"\gtfs\tripUpdates.pb %BIN_DIRECTORY%\"tripUpdates_%%f.pb" > nul
)

echo The tripUpdates.pb files have been copied to
echo   "%~dp0..\bin".
echo The GTFS-RT server can now be started using the following commands:
echo.
echo cd "%~dp0..\bin"
echo java -jar gtfs-rt-server.jar
echo.
echo It will serve the *.pb files in the directory every 10 seconds to
echo connected clients via WebSockets.
echo Its url is ws://localhost:8088/tripUpdates.
echo.
pause
