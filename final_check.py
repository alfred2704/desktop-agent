"""
Desktop Agent - 最终验证测试
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("  Desktop Agent - 最终验证")
print("=" * 70)
print()

all_ok = True

# 1. 验证核心模块
print("1. 验证核心模块...")
try:
    from core.config import Config
    from core.agent import DesktopAgent
    
    config = Config()
    agent = DesktopAgent(config)
    
    print("   [OK] 核心模块正常")
except Exception as e:
    print(f"   [ERROR] {e}")
    all_ok = False
print()

# 2. 验证六层架构
print("2. 验证六层架构...")
layers = {
    "Layer1 - Intent": "layers.layer1_intent.intent_parser.IntentParser",
    "Layer2 - Perception": "layers.layer2_perception.screen_perceiver.ScreenPerceiver",
    "Layer3 - Planning": "layers.layer3_planning.action_planner.ActionPlanner",
    "Layer4 - Execution": "layers.layer4_execution.action_executor.ActionExecutor",
    "Layer5 - Verification": "layers.layer5_verification.verification_manager.VerificationManager",
    "Layer6 - Knowledge": "layers.layer6_knowledge.knowledge_manager.KnowledgeManager",
}

for layer_name, module_path in layers.items():
    try:
        parts = module_path.split(".")
        module = ".".join(parts[:-1])
        cls_name = parts[-1]
        
        mod = __import__(module, fromlist=[cls_name])
        cls = getattr(mod, cls_name)
        
        print(f"   [OK] {layer_name}")
    except Exception as e:
        print(f"   [ERROR] {layer_name}: {e}")
        all_ok = False
print()

# 3. 验证Web界面
print("3. 验证Web界面...")
try:
    from web.app import app
    print("   [OK] Web应用")
    
    # 检查路由
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    print(f"      - 路由数量: {len(routes)}")
    
except Exception as e:
    print(f"   [ERROR] {e}")
    all_ok = False
print()

# 4. 验证知识库
print("4. 验证知识库...")
try:
    kb_dir = project_root / "knowledge" / "software"
    kb_files = list(kb_dir.glob("*.yaml"))
    
    print(f"   [OK] 知识库: {len(kb_files)} 个软件")
    for kb_file in kb_files:
        print(f"      - {kb_file.stem}")
    
except Exception as e:
    print(f"   [ERROR] {e}")
    all_ok = False
print()

# 5. 简单功能测试
print("5. 简单功能测试...")
try:
    # 测试意图解析
    intent = agent.intent_parser.parse("点击确定按钮")
    assert intent["intent"] == "click"
    
    # 测试屏幕感知
    state = agent.screen_perceiver.perceive()
    assert state["success"] is True
    
    print(f"   [OK] 功能测试通过")
    print(f"      - 意图解析: OK")
    print(f"      - 屏幕感知: OK (检测到 {len(state['elements'])} 个元素)")
    
except Exception as e:
    print(f"   [ERROR] {e}")
    all_ok = False
print()

# 最终报告
print("=" * 70)
print("  验证结果")
print("=" * 70)
print()

if all_ok:
    print("[SUCCESS] 所有验证通过！")
    print()
    print("项目已就绪，可以开始使用：")
    print()
    print("  启动Web界面:")
    print("    python main.py web")
    print()
    print("  启动命令行:")
    print("    python main.py cli")
    print()
    print("  运行示例:")
    print("    python main.py quickstart")
    print()
    print("  访问Web界面:")
    print("    http://localhost:5000")
    print()
else:
    print("[ERROR] 存在问题，请检查上述错误信息")

print()
print("=" * 70)
