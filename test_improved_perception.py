"""
测试改进后的屏幕感知层 - 全窗口扫描
"""

import sys
from pathlib import Path
import json

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from core.config import Config
import time

print("="*70)
print("  改进后的屏幕感知层测试")
print("="*70)
print()

# 初始化
config = Config()
perceiver = ScreenPerceiver(config)

# 测试1: 扫描所有窗口
print("[测试1】扫描所有窗口")
print("-" * 70)
print()

start_time = time.time()
all_windows_result = perceiver.perceive_all_windows()
elapsed = time.time() - start_time

print(f"扫描完成，耗时: {elapsed:.2f}秒")
print()

if all_windows_result["success"]:
    print(f"[OK] 共找到 {all_windows_result['total_count']} 个可见窗口")
    print()
    
    # 显示活动窗口
    active_window = all_windows_result.get("active_window")
    if active_window:
        print(f"活动窗口: {active_window['title']}")
        print()
    
    # 显示所有窗口列表（前10个）
    windows = all_windows_result.get("windows", [])
    print("窗口列表（前10个）:")
    print()
    
    for i, window in enumerate(windows[:10], 1):
        print(f"{i}. [{window['title'][:40]}]")
        print(f"   类名: {window['class_name']}")
        print(f"   大小: {window['width']} x {window['height']}")
        print(f"   句柄: {window['handle']}")
        print()
    
    if len(windows) > 10:
        print(f"... 还有 {len(windows) - 10} 个窗口")
        print()
else:
    print(f"[X] 扫描失败: {all_windows_result.get('error')}")
    print()

# 测试2: 通过标题查找窗口
print("="*70)
print("[测试2】查找包含\"豆包\"的窗口")
print("-" * 70)
print()

found_windows = perceiver.find_window_by_title("豆包")

if found_windows:
    print(f"[OK] 找到 {len(found_windows)} 个匹配的窗口:")
    print()
    
    for i, result in enumerate(found_windows, 1):
        window = result["window"]
        print(f"{i}. [{window['title']}]")
        print(f"   匹配度: {result['match_score']:.2f}")
        print(f"   位置: {window['rect']}")
        print(f"   大小: {window['width']} x {window['height']}")
        print()
else:
    print("[X] 未找到包含\"豆包\"的窗口")
    print()

# 测试3: 获取指定窗口的UI元素
print("="*70)
print("[测试3】获取豆包窗口的UI元素")
print("-" * 70)
print()

if found_windows:
    # 获取匹配度最高的窗口
    best_window = found_windows[0]
    window_handle = best_window["window"]["handle"]
    
    print(f"正在获取窗口UI元素: {best_window['title']}")
    print()
    
    start_time = time.time()
    window_elements_result = perceiver.get_window_elements(window_handle=window_handle)
    elapsed = time.time() - start_time
    
    print(f"获取完成，耗时: {elapsed:.2f}秒")
    print()
    
    if window_elements_result["success"]:
        elements = window_elements_result.get("elements", [])
        print(f"[OK] 共找到 {len(elements)} 个UI元素")
        print()
        
        # 显示前15个元素
        print("元素列表（前15个）:")
        print()
        
        for i, element in enumerate(elements[:15], 1):
            print(f"{i}. [{element['type']}]")
            print(f"   名称: {element['name']}")
            print(f"   位置: {element['center']}")
            print(f"   矩形: {element['rect']}")
            print(f"   状态: {'启用' if element['enabled'] else '禁用'}")
            print(f"   可见: {'是' if element['visible'] else '否'}")
            print()
        
        if len(elements) > 15:
            print(f"... 还有 {len(elements) - 15} 个元素")
            print()
        
        # 统计元素类型
        type_counts = {}
        for element in elements:
            elem_type = element['type']
            type_counts[elem_type] = type_counts.get(elem_type, 0) + 1
        
        print("元素类型统计:")
        print()
        for elem_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {elem_type}: {count} 个")
        print()
    else:
        print(f"[X] 获取失败: {window_elements_result.get('error')}")
        print()
else:
    print("[!] 无法测试UI元素获取（未找到豆包窗口）")
    print()

# 测试4: 激活窗口
print("="*70)
print("[测试4】激活豆包窗口")
print("-" * 70)
print()

if found_windows:
    best_window = found_windows[0]
    window_handle = best_window["window"]["handle"]
    
    print(f"正在激活窗口: {best_window['title']}")
    print()
    
    activate_result = perceiver.activate_window(window_handle=window_handle)
    
    if activate_result["success"]:
        window = activate_result.get("window")
        print(f"[OK] 窗口已激活")
        print(f"  标题: {window['title']}")
        print(f"  类名: {window['class_name']}")
        print(f"  句柄: {window['handle']}")
        print()
    else:
        print(f"[X] 激活失败: {activate_result.get('error')}")
        print()
else:
    print("[!] 无法测试窗口激活（未找到豆包窗口）")
    print()

# 总结
print("="*70)
print("  测试总结")
print("="*70)
print()

print("改进的功能:")
print("  1. perceive_all_windows() - 扫描所有可见窗口")
print("  2. find_window_by_title() - 通过标题关键词查找窗口")
print("  3. get_window_elements() - 获取指定窗口的UI元素")
print("  4. activate_window() - 激活指定窗口")
print()

print("改进的优势:")
print("  - [OK] 不再局限于活动窗口")
print("  - [OK] 可以发现后台窗口")
print("  - [OK] 支持多窗口场景")
print("  - [OK] 可以主动激活特定窗口")
print("  - [OK] 可以获取任意窗口的UI元素")
print()

print("="*70)
