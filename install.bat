@echo off
setlocal EnableDelayedExpansion

REM Get the current directory
set "current_dir=%cd%"

REM Replace the forward slashes with backslashes
set "current_dir=%current_dir:\=/%"

REM Get the current directory, split and get the user
set i=1
set "x=%cd%"
set "x!i!=%x:\=" & set /A i+=1 & set "x!i!=%"
set x

set "user=!x3!"

REM Now run the .exe on startup
REM Create a .vbs file that will run the .exe on startup
REM We need to pass the current directory as an argument to the .exe
echo Set oShell = CreateObject("WScript.Shell") > PriceScraper.vbs
echo sLinkFile = "C:\Users\%user%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\PriceScraper.lnk" >> PriceScraper.vbs
echo Set oLink = oShell.CreateShortcut(sLinkFile) >> PriceScraper.vbs
echo oLink.TargetPath = "%current_dir%/PriceScraper.exe" >> PriceScraper.vbs
echo oLink.Arguments = """%current_dir%""" >> PriceScraper.vbs
echo oLink.Save >> PriceScraper.vbs

REM Run the .vbs file
cscript PriceScraper.vbs

REM Remove the .vbs file
del PriceScraper.vbs

REM Tell the user that the program has been installed with a message box and tell them that it will run on startup
msg * "PriceScraper has been installed on your computer. It will run on startup."
```