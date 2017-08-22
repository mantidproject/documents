xcopy /E /Q /I /Y c:\instrument\apps\python\Lib\site-packages\genie_python c:\MantidInstall-unstable\bin\Lib\site-packages\genie_python 
xcopy /E /Q /I /Y c:\instrument\apps\python\Lib\site-packages\ca* c:\MantidInstall-unstable\bin\Lib\site-packages 
xcopy /E /Q /I /Y c:\instrument\apps\python\Lib\site-packages\_ca* c:\MantidInstall-unstable\bin\Lib\site-packages 
xcopy /E /Q /I /Y c:\instrument\apps\python\Lib\site-packages\pywin32* c:\MantidInstall-unstable\bin\Lib\site-packages 
xcopy /E /Q /I /Y \\olympic\babylon5\public\freddie\genie_mantid\win32api.py c:\MantidInstall-unstable\bin\Lib\site-packages 
        
REM set web proxy
set http_proxy=http://wwwcache.rl.ac.uk:8080
set https_proxy=https://wwwcache.rl.ac.uk:8080
set no_proxy=localhost,127.0.0.0/8,127.0.1.1,127.0.1.1*,local.home,130.246.*.*

call %~dp0run_mantid_py -m pip install pyreadline 
