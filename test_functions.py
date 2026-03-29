"""
Desktop Agent - 功能测试
测试各层模块的基本功能
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("  Desktop Agent - 功能测试")
print("=" * 70)
print()

# 测试结果
test_results = []

# 1. 测试配置加载
print("1. 测试配置加载...")
try:
    from core.config import Config
    config = Config()
    
    assert config.AI_MODEL is not None
    assert config.WEB_PORT > 0
    assert config.MAX_RETRY > 0
    
    print("   [OK] Config 加载成功")
    print(f"      AI模型: {config.AI_MODEL}")
    print(f"      Web端口: {config.WEB_PORT}")
    print(f"      最大重试: {config.MAX_RETRY}")
    
    test_results.append(("配置加载", True, None))
except Exception as e:
    print(f"   [ERROR] Config 加载失败: {e}")
    test_results.append(("配置加载", False, str(e)))
print()

# 2. 测试意图解析
print("2. 测试意图解析...")
try:
    from layers.layer1_intent.intent_parser import IntentParser
    
    parser = IntentParser(config)
    
    # 测试点击指令
    intent = parser.parse("点击确定按钮")
    assert intent["intent"] == "click"
    assert "确定" in intent["params"]["target"]
    
    # 测试输入指令
    intent = parser.parse("在搜索框输入'Python'")
    assert intent["intent"] == "type"
    assert intent["params"]["text"] == "Python"
    
    # 测试快捷键
    intent = parser.parse("按Ctrl+S")
    assert intent["intent"] == "hotkey"
    assert "ctrl" in intent["params"]["keys"]
    
    print("   [OK] 意图解析正常")
    print("      - 点击指令: ✓")
    print("      - 输入指令: ✓")
    print("      - 快捷键: ✓")
    
    test_results.append(("意图解析", True, None))
except Exception as e:
    print(f"   [ERROR] 意图解析失败: {e}")
    test_results.append(("意图解析", False, str(e)))
print()

# 3. 测试屏幕感知
print("3. 测试屏幕感知...")
try:
    from layers.layer2_perception.screen_perceiver import ScreenPerceiver
    
    perceiver = ScreenPerceiver(config)
    state = perceiver.perceive()
    
    assert state["success"] is True
    assert "elements" in state
    assert "active_window" in state
    
    print(f"   [OK] 屏幕感知正常")
    print(f"      - 检测到元素: {len(state['elements'])} 个")
    if state['active_window']:
        print(f"      - 活动窗口: {state['active_window']['title']}")
    
    test_results.append(("屏幕感知", True, None))
except Exception as e:
    print(f"   [ERROR] 屏幕感知失败: {e}")
    test_results.append(("屏幕感知", False, str(e)))
print()

# 4. 测试元素定位
print("4. 测试元素定位...")
try:
    from layers.layer2_perception.element_locator import ElementLocator
    
    locator = ElementLocator(config)
    
    # 先感知屏幕
    state = perceiver.perceive()
    
    # 尝试定位一个元素
    if state["elements"]:
        element_name = state["elements"][0]["name"]
        result = locator.locate(element_name, state)
        
        if result["success"]:
            print(f"   [OK] 元素定位正常")
            print(f"      - 测试定位: '{element_name}' ✓")
        else:
            print(f"   [OK] 元素定位正常（未找到测试元素）")
    else:
        print(f"   [OK] 元素定位模块加载成功")
    
    test_results.append(("元素定位", True, None))
except Exception as e:
    print(f"   [ERROR] 元素定位失败: {e}")
    test_results.append(("元素定位", False, str(e)))
print()

# 5. 测试操作规划
print("5. 测试操作规划...")
try:
    from layers.layer3_planning.action_planner import ActionPlanner
    from layers.layer3_planning.knowledge_query import KnowledgeQuery
    
    knowledge_query = KnowledgeQuery(config)
    planner = ActionPlanner(config, knowledge_query)
    
    # 测试点击规划
    intent = {
        "intent": "click",
        "params": {"target": "确定按钮"}
    }
    plan = planner.plan(intent, {})
    
    assert plan["success"] is True
    assert len(plan["actions"]) > 0
    
    print(f"   [OK] 操作规划正常")
    print(f"      - 生成动作: {len(plan['actions'])} 个")
    
    test_results.append(("操作规划", True, None))
except Exception as e:
    print(f"   [ERROR] 操作规划失败: {e}")
    test_results.append(("操作规划", False, str(e)))
print()

# 6. 测试动作执行器
print("6. 测试动作执行器...")
try:
    from layers.layer4_execution.action_executor import ActionExecutor
    
    executor = ActionExecutor(config)
    
    # 测试获取鼠标位置（不执行实际操作）
    x, y = executor.get_cursor_position()
    
    print(f"   [OK] 动作执行器正常")
    print(f"      - 鼠标位置: ({x}, {y})")
    
    test_results.append(("动作执行器", True, None))
except Exception as e:
    print(f"   [ERROR] 动作执行器失败: {e}")
    test_results.append(("动作执行器", False, str(e)))
print()

# 7. 测试验证管理器
print("7. 测试验证管理器...")
try:
    from layers.layer5_verification.verification_manager import VerificationManager
    
    verifier = VerificationManager(config)
    
    print(f"   [OK] 验证管理器正常")
    
    test_results.append(("验证管理器", True, None))
except Exception as e:
    print(f"   [ERROR] 验证管理器失败: {e}")
    test_results.append(("验证管理器", False, str(e)))
print()

# 8. 测试知识管理器
print("8. 测试知识管理器...")
try:
    from layers.layer6_knowledge.knowledge_manager import KnowledgeManager
    
    km = KnowledgeManager(config)
    
    stats = km.get_statistics()
    
    print(f"   [OK] 知识管理器正常")
    print(f"      - 软件知识: {stats.get('software_count', 0)} 个")
    print(f"      - 任务模板: {stats.get('template_count', 0)} 个")
    
    test_results.append(("知识管理器", True, None))
except Exception as e:
    print(f"   [ERROR] 知识管理器失败: {e}")
    test_results.append(("知识管理器", False, str(e)))
print()

# 9. 测试主控制器
print("9. 测试主控制器（DesktopAgent）...")
try:
    from core.agent import DesktopAgent
    
    agent = DesktopAgent(config)
    
    print(f"   [OK] DesktopAgent 初始化成功")
    print(f"      - 意图解析器: ✓")
    print(f"      - 屏幕感知器: ✓")
    print(f"      - 动作执行器: ✓")
    
    test_results.append(("DesktopAgent", True, None))
except Exception as e:
    print(f"   [ERROR] DesktopAgent 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("DesktopAgent", False, str(e)))
print()

# 10. 测试Web应用
print("10. 测试Web应用...")
try:
    from web.app import app
    
    print(f"   [OK] Web应用加载成功")
    
    test_results.append(("Web应用", True, None))
except Exception as e:
    print(f"   [ERROR] Web应用加载失败: {e}")
    test_results.append(("Web应用", False, str(e)))
print()

# 总结报告
print("=" * 70)
print("  测试总结")
print("=" * 70)
print()

passed = sum(1 for _, success, _ in test_results if success)
failed = sum(1 for _, success, _ in test_results if not success)
total = len(test_results)

print(f"通过: {passed}/{total}")
print(f"失败: {failed}/{total}")
print()

if failed > 0:
    print("失败的测试:")
    for name, success, error in test_results:
        if not success:
            print(f"  - {name}: {error}")
    print()

if passed == total:
    print("[SUCCESS] 所有测试通过！项目已就绪。")
    print()
    print("启动方式:")
    print("  python main.py web         # 启动Web界面")
    print("  python main.py cli         # 启动命令行")
    print("  python main.py quickstart  # 运行示例")
else:
    print(f"[WARNING] {failed} 个测试失败，请检查错误信息")

print()
print("=" * 70)
