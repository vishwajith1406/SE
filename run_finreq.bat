@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -3.12 -m venv .venv
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8000
goto done
:failed
echo FinReq could not start. Check that Python 3.12 is installed and try again.
pause
:done
endlocal
