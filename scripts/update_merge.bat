@ECHO OFF

REM Set data directory with GTFS files as text in separate directories
SET DATA_DIRECTORY="%~dp0..\data\gtfs"

REM Set output directory for tests in GTFS zip format
REM Don't chose a directory inside %DATA_DIRECTORY%
SET GTFS_OUTPUT_DIRECTORY="%~dp0tests"

REM Set output file for all tests combined in GTFS zip format
SET ALL_TESTS_ZIP="%~dp0alltests.zip"


REM Add 7-zip path to PATH
SET SEVEN_ZIP_PATH="C:\Program Files\7-Zip"
IF EXIST %SEVEN_ZIP_PATH% SET PATH=%PATH%;%SEVEN_ZIP_PATH%
SET SEVEN_ZIP_PATH="C:\Program Files (x86)\7-Zip"
IF EXIST %SEVEN_ZIP_PATH% SET PATH=%PATH%;%SEVEN_ZIP_PATH%

REM Create tests in GTFS zip format
MKDIR %GTFS_OUTPUT_DIRECTORY%
DEL /Q %GTFS_OUTPUT_DIRECTORY%\*.*
FOR /F "delims=" %%f in ('dir %DATA_DIRECTORY% /A:D /B /O:N') DO (
    7z a %GTFS_OUTPUT_DIRECTORY%\"%%f.zip" %DATA_DIRECTORY%\"%%f"\*.txt
)

REM Combine tests
java -jar "%~dp0..\bin\onebusaway-gtfs-transformer-cli.jar" --overwriteDuplicates %GTFS_OUTPUT_DIRECTORY%\*.zip %ALL_TESTS_ZIP%
