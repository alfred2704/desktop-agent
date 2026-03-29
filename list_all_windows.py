"""
查看当前所有窗口
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from core.config import Config

config = Config()
perceiver = ScreenPerceiver(config)

print("="*70)
print("  当前所有窗口")
print("="*70)
print()

result = perceiver.perceive_all_windows()

if result["success"]:
    windows = result["windows"]
    print(f"共发现 {len(windows)} 个窗口:")
    print()
    
    for i, window in enumerate(windows, 1):
        print(f"{i}. [{window['title'][:50]}]")
        print(f"   类名: {window['class_name']}")
        print(f"   大小: {window['width']} x {window['height']}")
        print()
else:
    print(f"扫描失败: {result.get('error')}")
