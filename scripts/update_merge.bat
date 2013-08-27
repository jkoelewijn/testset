@echo off

rem Set data directory with GTFS files as text in separate directories
rem containing a gtfs folder
set DATA_DIRECTORY="%~dp0..\tests"

rem Set output directory for tests in GTFS zip format
rem Don't chose a directory inside %DATA_DIRECTORY%
set GTFS_OUTPUT_DIRECTORY="%~dp0tests"

rem Set output file for all tests combined in GTFS zip format
set ALL_TESTS_ZIP="%~dp0alltests.zip"


rem Add 7-zip path to PATH
set SEVEN_ZIP_PATH="C:\Program Files\7-Zip"
if exist %SEVEN_ZIP_PATH% set PATH=%PATH%;%SEVEN_ZIP_PATH%
set SEVEN_ZIP_PATH="C:\Program Files (x86)\7-Zip"
if exist %SEVEN_ZIP_PATH% set PATH=%PATH%;%SEVEN_ZIP_PATH%

rem Create tests in GTFS zip format
mkdir %GTFS_OUTPUT_DIRECTORY%
del /Q %GTFS_OUTPUT_DIRECTORY%\*.*
for /F "delims=" %%f in ('dir %DATA_DIRECTORY% /A:D /B /O:N') do (
    7z a %GTFS_OUTPUT_DIRECTORY%\"%%f.zip" %DATA_DIRECTORY%\"%%f"\gtfs\*.txt
)

rem Combine tests
java -jar "%~dp0..\bin\onebusaway-gtfs-transformer-cli.jar" --overwriteDuplicates %GTFS_OUTPUT_DIRECTORY%\*.zip %ALL_TESTS_ZIP%
