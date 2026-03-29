@echo off
chcp 65001 >nul
echo ========================================
echo Desktop Agent Web服务启动
echo ========================================
echo.

REM 检查Python
echo [1/4] 检查Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python已安装

REM 检查pip
echo.
echo [2/4] 检查pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip不可用
    pause
    exit /b 1
)
echo ✅ pip可用

REM 安装依赖
echo.
echo [3/4] 安装依赖...
echo   安装 flask...
python -m pip install flask --quiet
echo   安装 flask-socketio...
python -m pip install flask-socketio --quiet
echo   安装 flask-cors...
python -m pip install flask-cors --quiet
echo ✅ 依赖安装完成

REM 启动服务
echo.
echo [4/4] 启动Web服务...
echo.
echo ========================================
echo 🌐 访问地址: http://localhost:5000
echo 📖 API文档: http://localhost:5000/docs
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

cd desktop-agent

REM 尝试启动主应用
python web\app.py
if errorlevel 1 (
    echo.
    echo ❌ 主应用启动失败
    echo 尝试使用简单模式...
    python simple_web.py
)

pause
