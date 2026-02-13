@echo off
set PYTHON_PATH="C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe"
if exist %PYTHON_PATH% (
    %PYTHON_PATH% main.py
) else (
    python main.py
)
pause
