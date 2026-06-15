@echo off
:: Navigate to your project folder
cd /d "C:\Users\Oome\Documents\GitHub\umamusume-auto-train"

:: Run the python script
:: The window will stay open until the bot calls os._exit(0)
python main.py

:: Exit the terminal once python stops
exit