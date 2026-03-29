"""
列出屏幕上的所有UI元素
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from core.config import Config
import time

print("="*70)
print("  屏幕UI元素扫描详情")
print("="*70)
print()

# 初始化
config = Config()
perceiver = ScreenPerceiver(config)

print("正在扫描屏幕...")
print()

# 感知屏幕
start_time = time.time()
screen_state = perceiver.perceive()
elapsed = time.time() - start_time

print(f"扫描完成，耗时: {elapsed:.2f}秒")
print()

# 显示屏幕状态
print("="*70)
print("  屏幕状态")
print("="*70)
print()

if screen_state["active_window"]:
    window = screen_state["active_window"]
    print(f"当前活动窗口:")
    print(f"  标题: {window['title']}")
    print(f"  类名: {window['class_name']}")
    print(f"  句柄: {window['handle']}")
    print(f"  位置: {window['rect']}")
    print()

# 显示所有UI元素
elements = screen_state.get("elements", [])
print("="*70)
print(f"  UI元素列表 (共 {len(elements)} 个)")
print("="*70)
print()

if elements:
    for i, element in enumerate(elements, 1):
        print(f"{i}. [{element.get('type', 'Unknown')}]")
        print(f"   名称: {element.get('name', '(无名称)')}")
        print(f"   类名: {element.get('class_name', '(无)')}")
        print(f"   位置: {element.get('center', '(未知)')}")
        print(f"   矩形: {element.get('rect', '(未知)')}")
        print(f"   启用: {'是' if element.get('enabled', False) else '否'}")
        print(f"   可见: {'是' if element.get('visible', False) else '否'}")
        print(f"   深度: {element.get('depth', 0)}")
        print()
else:
    print("未扫描到任何UI元素")
    print()

# 统计信息
print("="*70)
print("  元素类型统计")
print("="*70)
print()

type_counts = {}
for element in elements:
    elem_type = element.get('type', 'Unknown')
    type_counts[elem_type] = type_counts.get(elem_type, 0) + 1

for elem_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {elem_type}: {count} 个")

print()
print("="*70)

# 保存截图
if screen_state.get("screenshot"):
    screenshot_path = "screen_elements_scan.png"
    screen_state["screenshot"].save(screenshot_path)
    print(f"[截图] 已保存: {screenshot_path}")
    print()
