#!/usr/bin/env python3
"""
启动Web界面
"""
import os
import sys

# 切换到正确的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*60)
print("Desktop Agent - Web界面启动")
print("="*60)
print()

# 检查依赖
print("检查依赖...")
try:
    import flask
    print(f"✅ Flask {flask.__version__}")
except ImportError:
    print("❌ Flask未安装")
    print("运行: pip install flask")
    sys.exit(1)

try:
    import flask_socketio
    print(f"✅ Flask-SocketIO {flask_socketio.__version__}")
except ImportError:
    print("❌ Flask-SocketIO未安装")
    print("运行: pip install flask-socketio")
    sys.exit(1)

try:
    import flask_cors
    print(f"✅ Flask-CORS installed")
except ImportError:
    print("❌ Flask-CORS未安装")
    print("运行: pip install flask-cors")
    sys.exit(1)

print()
print("="*60)
print("启动Web服务...")
print("访问地址: http://localhost:5000")
print("按 Ctrl+C 停止服务")
print("="*60)
print()

# 启动应用
from web.app import app, socketio

try:
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
except KeyboardInterrupt:
    print("\n\n👋 服务已停止")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
