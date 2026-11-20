@echo off
REM ==========================================================
REM Batch Script สำหรับ Deploy จากเครื่อง Windows ไปยัง k8s-control
REM การใช้งาน: ดับเบิลคลิก หรือรัน deploy.bat ใน PowerShell/CMD
REM ==========================================================

set CONTROL_USER=yut
set CONTROL_IP=192.168.1.10

for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"

echo ==========================================================
echo  [1/2] Uploading project 68130239 to %CONTROL_USER%@%CONTROL_IP% ...
echo ==========================================================
ssh %CONTROL_USER%@%CONTROL_IP% "rm -rf ~/68130239/68130239"
scp -r "%PROJECT_DIR%" %CONTROL_USER%@%CONTROL_IP%:~/

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] SCP upload failed. Check SSH connectivity to %CONTROL_IP%.
    pause
    exit /b 1
)

echo ==========================================================
echo  [2/2] Running deploy.sh on k8s-control ...
echo ==========================================================
ssh %CONTROL_USER%@%CONTROL_IP% "sed -i 's/\r$//' ~/68130239/scripts/*.sh && chmod +x ~/68130239/scripts/*.sh && bash ~/68130239/scripts/deploy.sh"

echo.
echo ==========================================================
echo  Done! Press Ctrl+F5 in your browser to clear cache.
echo ==========================================================
pause
