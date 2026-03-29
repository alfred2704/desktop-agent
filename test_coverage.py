"""
Desktop Agent - 覆盖率测试
测试95%覆盖率目标
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.enhanced_intent_parser import EnhancedIntentParser
from core.config import Config

print("=" * 70)
print("  Desktop Agent - 覆盖率测试")
print("=" * 70)
print()

# 初始化
config = Config()
parser = EnhancedIntentParser(config)

# 测试用例
test_cases = [
    # ═══════════════════════════════════════════════════════════════
    # 基础操作（应该全部通过规则匹配）
    # ═══════════════════════════════════════════════════════════════
    ("点击确定按钮", "click", {"target": "确定按钮"}, "rules"),
    ("单击文件", "click", {"target": "文件"}, "rules"),
    ("按保存按钮", "click", {"target": "保存按钮"}, "rules"),
    ("双击桌面", "double_click", {"target": "桌面"}, "rules"),
    ("右键菜单", "right_click", {"target": "菜单"}, "rules"),
    ("右击文件", "right_click", {"target": "文件"}, "rules"),
    
    ("在搜索框输入'Python'", "type", {"element": "搜索框", "text": "Python"}, "rules"),
    ("在用户名填写\"admin\"", "type", {"element": "用户名", "text": "admin"}, "rules"),
    ("输入'Hello World'", "type", {"text": "Hello World"}, "rules"),
    
    ("按Ctrl+S", "hotkey", {"keys": ["ctrl", "s"]}, "rules"),
    ("按下Ctrl+C", "hotkey", {"keys": ["ctrl", "c"]}, "rules"),
    ("按复制", "hotkey", {"keys": ["ctrl", "c"]}, "rules"),
    ("按保存", "hotkey", {"keys": ["ctrl", "s"]}, "rules"),
    
    ("点击文件菜单下的保存", "menu", {"menu_path": ["文件", "保存"]}, "rules"),
    ("打开编辑菜单的查找", "menu", {"menu_path": ["编辑", "查找"]}, "rules"),
    
    ("向上滚动", "scroll", {"direction": "up"}, "rules"),
    ("向下滚动3次", "scroll", {"direction": "down"}, "rules"),
    ("上翻页", "scroll", {"direction": "up"}, "rules"),
    
    ("等待确定按钮", "wait", {"target": "确定按钮"}, "rules"),
    ("等3秒", "wait", {"duration": 3}, "rules"),
    
    ("查找确定按钮", "find", {"target": "确定按钮"}, "rules"),
    ("搜索文件", "find", {"target": "文件"}, "rules"),
    
    # ═══════════════════════════════════════════════════════════════
    # 扩展操作（应该通过规则匹配）
    # ═══════════════════════════════════════════════════════════════
    ("如果确定按钮存在就点击", "if_exists", {"condition": "确定按钮", "action": "点击"}, "rules"),
    ("重复点击确定3次", "loop_times", {"action": "点击确定", "times": 3}, "rules"),
    ("点击第2个按钮", "click_index", {"index": 2, "target": "按钮"}, "rules"),
    ("点击第一个文件", "click_first", {"target": "文件"}, "rules"),
    ("点击最后一条消息", "click_last", {"target": "消息"}, "rules"),
    ("点击所有按钮", "click_all", {"target": "按钮"}, "rules"),
    ("拖动文件到文件夹", "drag", {"source": "文件", "target": "文件夹"}, "rules"),
    ("清空搜索框并输入'Python'", "clear_type", {"element": "搜索框", "text": "Python"}, "rules"),
    
    # ═══════════════════════════════════════════════════════════════
    # 复杂操作（需要AI或确认）
    # ═══════════════════════════════════════════════════════════════
    ("把刚才复制的内容粘贴到这里", None, None, "ai"),
    ("如果价格小于100就购买", None, None, "ai"),
    ("找到最贵的商品", None, None, "ai"),
    ("点击那个红色的按钮", None, None, "ai"),
]

# 运行测试
print("开始测试...")
print()

passed = 0
failed = 0
results = []

for instruction, expected_intent, expected_params, expected_method in test_cases:
    result = parser.parse(instruction)
    
    success = result.get("intent") == expected_intent if expected_intent else True
    method_match = result.get("method") == expected_method
    
    if success and method_match:
        passed += 1
        status = "[OK]"
    else:
        failed += 1
        status = "[FAIL]"
    
    results.append({
        "instruction": instruction,
        "expected": expected_intent,
        "actual": result.get("intent"),
        "expected_method": expected_method,
        "actual_method": result.get("method"),
        "success": success and method_match,
    })
    
    print(f"{status} {instruction}")
    if not success:
        print(f"     Expected: {expected_intent} ({expected_method})")
        print(f"     Got: {result.get('intent')} ({result.get('method')})")

print()
print("=" * 70)
print("  测试结果")
print("=" * 70)
print()

total = len(test_cases)
coverage = (passed / total * 100) if total > 0 else 0

print(f"总计: {total}")
print(f"通过: {passed}")
print(f"失败: {failed}")
print(f"覆盖率: {coverage:.1f}%")
print()

if coverage >= 95:
    print("[SUCCESS] 已达到95%覆盖率目标！")
elif coverage >= 80:
    print("[GOOD] 接近目标，需要继续优化")
else:
    print("[WARNING] 覆盖率不足，需要改进")

print()
print("=" * 70)

# 显示失败详情
if failed > 0:
    print("失败详情:")
    print("-" * 70)
    for r in results:
        if not r["success"]:
            print(f"指令: {r['instruction']}")
            print(f"  期望: {r['expected']} ({r['expected_method']})")
            print(f"  实际: {r['actual']} ({r['actual_method']})")
            print()
