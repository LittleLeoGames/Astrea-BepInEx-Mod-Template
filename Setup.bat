@ECHO OFF
REM Change working directory to script's directory
cd /d "%~dp0SetupFiles"

REM Step 1: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo Python is not installed. Exiting.
        pause
        exit /b 1
    )
) 


REM Step 2: Find Python executable location using "where" command
for /f %%i in ('where python.exe') do (
    set "PYTHON=%%i"
)

REM Step 3: Check if PYTHON variable is set
if "%PYTHON%"=="" (
    echo Python executable not found. Exiting.
    pause
    exit /b 1
) else (
    echo PYTHON variable set to: %PYTHON%
)


@echo -------------------------------------
@echo Executing GetMainAstreaDLLs.py
@echo -------------------------------------

"%PYTHON%" GetMainAstreaDLLs.py %* 2>&1
if errorlevel 1 (
    py GetMainAstreaDLLs.py %* 2>&1
    if errorlevel 1 (
        echo could not execute GetMainAstreaDLLs.py, will be skipped.
        pause
    )
) 

@echo -------------------------------------
@echo Executing RenameAstreaModProject.py
@echo -------------------------------------

"%PYTHON%" RenameAstreaModProject.py %* 2>&1
if errorlevel 1 (
    py RenameAstreaModProject.py %* 2>&1
    if errorlevel 1 (
        echo could not execute RenameAstreaModProject.py, will be skipped.
        pause
    )
) 

pause
