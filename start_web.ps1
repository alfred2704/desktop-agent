# Desktop Agent Web启动脚本 (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Desktop Agent Web服务启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python
Write-Host "[1/4] 检查Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未安装或不在PATH中" -ForegroundColor Red
    Write-Host "请先安装Python 3.8+" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

# 检查pip
Write-Host ""
Write-Host "[2/4] 检查pip..." -ForegroundColor Yellow
try {
    python -m pip --version | Out-Null
    Write-Host "✅ pip可用" -ForegroundColor Green
} catch {
    Write-Host "❌ pip不可用" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

# 安装依赖
Write-Host ""
Write-Host "[3/4] 安装依赖..." -ForegroundColor Yellow
$dependencies = @("flask", "flask-socketio", "flask-cors")
foreach ($dep in $dependencies) {
    Write-Host "  安装 $dep..." -NoNewline
    python -m pip install $dep --quiet 2>&1 | Out-Null
    if ($?) {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ⚠️" -ForegroundColor Yellow
    }
}

# 启动服务
Write-Host ""
Write-Host "[4/4] 启动Web服务..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🌐 访问地址: http://localhost:5000" -ForegroundColor Green
Write-Host "📖 API文档: http://localhost:5000/docs" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 切换到desktop-agent目录
Set-Location desktop-agent

# 启动Flask应用
try {
    python web\app.py
} catch {
    Write-Host ""
    Write-Host "❌ 启动失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "尝试使用简单模式启动..." -ForegroundColor Yellow
    python simple_web.py
}

Read-Host "`n按Enter键退出"
