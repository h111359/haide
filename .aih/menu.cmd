@echo off
where py >nul 2>nul
if errorlevel 1 goto fallback
py -3 -B "%~dp0engine\cli.py" menu %*
exit /b %errorlevel%
:fallback
where python >nul 2>nul
if errorlevel 1 goto missing
python -B "%~dp0engine\cli.py" menu %*
exit /b %errorlevel%
:missing
echo AIH requires Python 3.11 or newer. Install Python, then run py -3 -B .aih\engine\cli.py menu. 1>&2
exit /b 1
