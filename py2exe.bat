pyinstaller MyServer.py
xcopy setting dist\MyServer\setting /E /I /H /Y
xcopy static dist\MyServer\static /E /I /H /Y
xcopy templates dist\MyServer\templates /E /I /H /Y
xcopy Database dist\MyServer\Database /E /I /H /Y
xcopy data dist\MyServer\data /E /I /H /Y