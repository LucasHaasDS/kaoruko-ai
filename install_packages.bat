@echo off
cd /d "%~dp0"

echo Installing Kaoruko AI Python packages...
if exist ".venv\Scripts\python.exe" (
    echo Using project venv: .venv
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
) else (
    echo No .venv found, using system python
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
)

echo.
echo Done.
echo Tkinter is part of Python, not pip. If "import tkinter" fails,
echo reinstall Python and tick "tcl/tk and IDLE".
echo You still need the Ollama app installed separately, plus a model
echo such as: ollama pull llama3.2
pause
