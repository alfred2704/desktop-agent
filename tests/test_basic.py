"""
Desktop Agent - 单元测试
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from layers.layer1_intent.intent_parser import IntentParser
from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from layers.layer2_perception.element_locator import ElementLocator
from layers.layer3_planning.action_planner import ActionPlanner


def test_config():
    """测试配置"""
    print("测试配置...")
    
    config = Config()
    
    assert config.AI_MODEL is not None
    assert config.WEB_PORT == 5000
    assert config.MAX_RETRY > 0
    
    print("✓ 配置测试通过")
    return True


def test_intent_parser():
    """测试意图解析"""
    print("\n测试意图解析...")
    
    config = Config()
    parser = IntentParser(config)
    
    # 测试点击
    intent = parser.parse("点击确定按钮")
    assert intent["intent"] == "click"
    assert intent["params"]["target"] == "确定按钮"
    
    # 测试输入
    intent = parser.parse("在搜索框输入'Python'")
    assert intent["intent"] == "type"
    assert intent["params"]["text"] == "Python"
    
    # 测试快捷键
    intent = parser.parse("按Ctrl+S")
    assert intent["intent"] == "hotkey"
    assert "ctrl" in intent["params"]["keys"]
    
    print("✓ 意图解析测试通过")
    return True


def test_screen_perceiver():
    """测试屏幕感知"""
    print("\n测试屏幕感知...")
    
    config = Config()
    perceiver = ScreenPerceiver(config)
    
    # 测试感知屏幕
    state = perceiver.perceive()
    
    assert state["success"] is not None
    assert "elements" in state
    assert "active_window" in state
    
    print(f"✓ 检测到 {len(state['elements'])} 个元素")
    print("✓ 屏幕感知测试通过")
    
    return True


def test_element_locator():
    """测试元素定位"""
    print("\n测试元素定位...")
    
    config = Config()
    locator = ElementLocator(config)
    perceiver = ScreenPerceiver(config)
    
    # 感知屏幕
    state = perceiver.perceive()
    
    # 测试精确匹配
    if state["elements"]:
        element = state["elements"][0]
        result = locator.locate(element["name"], state)
        
        if result["success"]:
            print(f"✓ 找到元素: {element['name']}")
    
    print("✓ 元素定位测试通过")
    return True


def test_action_planner():
    """测试动作规划"""
    print("\n测试动作规划...")
    
    config = Config()
    from layers.layer3_planning.knowledge_query import KnowledgeQuery
    
    knowledge_query = KnowledgeQuery(config)
    planner = ActionPlanner(config, knowledge_query)
    
    # 测试点击规划
    intent = {
        "intent": "click",
        "params": {
            "target": "确定按钮",
            "aliases": ["确定", "确认"]
        }
    }
    
    plan = planner.plan(intent, {})
    
    assert plan["success"] is True
    assert len(plan["actions"]) > 0
    
    print(f"✓ 生成 {len(plan['actions'])} 个动作")
    print("✓ 动作规划测试通过")
    
    return True


def main():
    """运行所有测试"""
    print("=" * 70)
    print("  Desktop Agent - 单元测试")
    print("=" * 70)
    
    tests = [
        test_config,
        test_intent_parser,
        test_screen_perceiver,
        test_element_locator,
        test_action_planner,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result, None))
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            results.append((test.__name__, False, str(e)))
    
    # 总结
    print("\n" + "=" * 70)
    print("  测试结果总结")
    print("=" * 70)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    for name, result, error in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
        if error:
            print(f"  错误: {error}")
    
    print(f"\n通过: {passed}/{total}")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
