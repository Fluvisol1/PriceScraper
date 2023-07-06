@echo off
setlocal EnableDelayedExpansion

REM Get the current directory, split and get the user
set i=1
set "x=%cd%"
set "x!i!=%x:\=" & set /A i+=1 & set "x!i!=%"
set x

set "user=!x3!"

REM Remove the .vbs file from the startup folder
del "C:\Users\%user%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\PriceScraper.lnk"

REM Tell the user that the program has been uninstalled with a message box
msg * "PriceScraper has been uninstalled from your computer."
```