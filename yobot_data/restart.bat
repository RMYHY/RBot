
                    ping 127.0.0.1 -n 2 >nul
                    taskkill /pid 2176 /f >nul
                    ping 127.0.0.1 -n 3 >nul
                    powershell Start-Process -FilePath 'C:\Users\Administrator\qqbot\yobot\yobot.exe'
                    