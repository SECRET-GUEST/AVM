@echo off
set "CONDA_ROOT_PREFIX=%~dp0installer_files\conda"
set "INSTALL_ENV_DIR=%~dp0installer_files\env"

CALL "%CONDA_ROOT_PREFIX%\Scripts\activate.bat" "%INSTALL_ENV_DIR%"
"%INSTALL_ENV_DIR%\python.exe" "%~dp0\avm.py"
