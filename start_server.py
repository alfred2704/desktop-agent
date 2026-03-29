"""
Desktop Agent Web服务启动脚本
自动检查依赖并启动服务
"""
import subprocess
import sys
import os

def check_python():
    """检查Python版本"""
    version = sys.version_info
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8+")
        return False
    return True

def install_dependencies():
    """安装依赖"""
    dependencies = [
        "flask",
        "flask-socketio",
        "flask-cors"
    ]
    
    print("\n[2/4] 检查依赖...")
    
    for dep in dependencies:
        print(f"  检查 {dep}...", end=" ")
        try:
            __import__(dep.replace("-", "_"))
            print("✅ 已安装")
        except ImportError:
            print("⚠️  需要安装")
            print(f"  正在安装 {dep}...", end=" ")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", dep, "--quiet"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("✅ 安装成功")
            except Exception as e:
                print(f"❌ 安装失败: {e}")
                return False
    
    return True

def start_server():
    """启动服务器"""
    print("\n[3/4] 启动Web服务...")
    
    # 切换到正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("\n" + "="*60)
    print("🌐 访问地址: http://localhost:5000")
    print("📖 API文档: http://localhost:5000/docs")
    print("="*60)
    print("\n按 Ctrl+C 停止服务\n")
    
    # 尝试启动主应用
    try:
        from web.app import app, socketio
        print("✅ 启动完整版Web服务...")
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"⚠️  完整版启动失败: {e}")
        print("✅ 启动简化版Web服务...")
        try:
            import simple_web
        except Exception as e2:
            print(f"❌ 简化版启动也失败: {e2}")
            return False
    
    return True

def main():
    """主函数"""
    print("\n" + "="*60)
    print("Desktop Agent Web服务启动器")
    print("="*60)
    
    # 1. 检查Python
    print("\n[1/4] 检查Python...")
    if not check_python():
        input("\n按Enter键退出...")
        sys.exit(1)
    
    # 2. 安装依赖
    if not install_dependencies():
        input("\n按Enter键退出...")
        sys.exit(1)
    
    # 3. 启动服务
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
