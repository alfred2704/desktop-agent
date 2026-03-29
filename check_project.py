"""
Desktop Agent - 自检脚本
检查项目完整性和常见问题
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("  Desktop Agent - 自检报告")
print("=" * 70)
print()

issues = []
warnings = []

# 1. 检查Python版本
print("1. 检查Python版本...")
print(f"   Python版本: {sys.version}")
if sys.version_info < (3, 9):
    issues.append("Python版本过低，需要3.9+")
print()

# 2. 检查必需的依赖
print("2. 检查依赖...")
required_packages = {
    "uiautomation": "uiautomation",
    "PIL": "PIL",
    "pyautogui": "pyautogui",
    "flask": "flask",
    "flask_socketio": "flask_socketio",
    "flask_cors": "flask_cors",
    "loguru": "loguru",
    "yaml": "yaml",
    "dotenv": "dotenv",
}

for import_name, package_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"   [OK] {package_name}")
    except ImportError:
        issues.append(f"缺少依赖: {package_name}")
        print(f"   [X] {package_name} (未安装)")
print()

# 3. 检查文件完整性
print("3. 检查核心文件...")
required_files = [
    "core/config.py",
    "core/agent.py",
    "layers/layer1_intent/intent_parser.py",
    "layers/layer1_intent/context_manager.py",
    "layers/layer2_perception/screen_perceiver.py",
    "layers/layer2_perception/element_locator.py",
    "layers/layer3_planning/action_planner.py",
    "layers/layer3_planning/knowledge_query.py",
    "layers/layer4_execution/action_executor.py",
    "layers/layer5_verification/verification_manager.py",
    "layers/layer6_knowledge/knowledge_manager.py",
    "web/app.py",
    "tools/cli.py",
    "main.py",
]

for file_path in required_files:
    if (project_root / file_path).exists():
        print(f"   [OK] {file_path}")
    else:
        issues.append(f"文件不存在: {file_path}")
        print(f"   [X] {file_path}")
print()

# 4. 检查配置文件
print("4. 检查配置...")
env_file = project_root / ".env"
env_example = project_root / ".env.example"

if env_example.exists():
    print(f"   [OK] .env.example")
else:
    issues.append(".env.example 文件不存在")
    print(f"   [X] .env.example")

if env_file.exists():
    print(f"   [OK] .env")
else:
    warnings.append(".env 文件不存在，将使用默认配置")
    print(f"   [!] .env (可选)")
print()

# 5. 检查知识库
print("5. 检查知识库...")
kb_dir = project_root / "knowledge" / "software"
if kb_dir.exists():
    kb_files = list(kb_dir.glob("*.yaml"))
    print(f"   [OK] 软件知识库: {len(kb_files)} 个文件")
    for kb_file in kb_files[:5]:
        print(f"      - {kb_file.name}")
else:
    warnings.append("软件知识库目录不存在")
    print(f"   [X] 软件知识库目录不存在")
print()

# 6. 检查环境变量
print("6. 检查环境变量...")
try:
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    if os.getenv("ZHIPU_API_KEY"):
        print("   [OK] ZHIPU_API_KEY 已配置")
    else:
        warnings.append("ZHIPU_API_KEY 未配置（AI功能将不可用）")
        print("   [!] ZHIPU_API_KEY 未配置")
except:
    pass
print()

# 7. 总结报告
print("=" * 70)
print("  自检总结")
print("=" * 70)
print()

if issues:
    print(f"[ERROR] 发现 {len(issues)} 个问题:")
    for i, issue in enumerate(issues, 1):
        print(f"   {i}. {issue}")
    print()

if warnings:
    print(f"[WARNING] 发现 {len(warnings)} 个警告:")
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")
    print()

if not issues and not warnings:
    print("[OK] 项目检查通过，没有发现问题！")
    print()
    print("[READY] 可以开始使用:")
    print("   python main.py web     # 启动Web界面")
    print("   python main.py cli     # 启动命令行")
    print("   python main.py quickstart  # 运行示例")
elif not issues:
    print("[OK] 项目基本正常，但有一些警告需要注意")
    print()
    print("建议:")
    print("   1. 配置 .env 文件以启用AI功能")
    print("   2. 安装可选依赖（如PaddleOCR）以获得更好体验")
else:
    print("[ERROR] 项目存在严重问题，需要修复后才能使用")
    print()
    print("修复建议:")
    print("   1. 安装缺失的依赖: pip install -r requirements.txt")
    print("   2. 检查文件完整性")
    print("   3. 确保Python版本 >= 3.9")

print()
print("=" * 70)
