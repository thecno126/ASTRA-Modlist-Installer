@echo off
REM Build script for ASTRA Modlist Installer (Windows)
REM Builds executables using PyInstaller

echo === ASTRA Modlist Installer Build Script ===
echo.

REM Check for virtual environment
if exist "..\venv\Scripts\activate.bat" (
    echo Using virtual environment...
    call ..\venv\Scripts\activate.bat
    set PYTHON_CMD=python
    set PIP_CMD=pip
) else (
    echo No virtual environment found, using system Python...
    set PYTHON_CMD=python
    set PIP_CMD=pip
)

REM Check if PyInstaller is installed
%PYTHON_CMD% -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    %PIP_CMD% install pyinstaller
)

REM Ensure dependencies are installed
echo Checking dependencies...
%PIP_CMD% install -q -r ..\requirements.txt

REM Create dist directory if it doesn't exist
if not exist ..\dist mkdir ..\dist

REM Clean previous builds
echo Cleaning previous builds...
if exist ..\build rmdir /s /q ..\build
if exist ..\dist\Modlist-Installer.exe del /q ..\dist\Modlist-Installer.exe

REM Build Installer
echo.
echo Building Modlist Installer...
pyinstaller --clean -y --distpath ..\dist --workpath ..\build modlist_installer.spec
if %errorlevel% neq 0 (
    echo Build failed!
    exit /b 1
)

echo.
echo === Build completed successfully! ===
echo.
echo Executables created in: ..\dist\
echo   - Modlist-Installer.exe
echo.
echo To test the executable:
echo   ..\dist\Modlist-Installer.exe
echo.
pause
