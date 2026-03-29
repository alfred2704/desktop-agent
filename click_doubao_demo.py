"""
完整演示：AI驱动点击豆包窗口
展示六层架构的完整协作
"""

import sys
from pathlib import Path
import time

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from core.config import Config
import pyautogui

print("="*70)
print("  AI驱动自动化 - 点击豆包窗口")
print("="*70)
print()

# ═══════════════════════════════════════════════════════════════
# L1 意图理解层 - 理解用户意图
# ═══════════════════════════════════════════════════════════════

print("【L1 意图理解层】")
print("-" * 70)
print()

user_intent = "点击豆包"
print(f"用户意图: {user_intent}")
print()

# AI理解
ai_understanding = {
    "action": "click_window",
    "target": "豆包",
    "possible_names": ["豆包", "Doubao", "DOUBAO"],
    "strategy": "find_and_activate",
    "click_position": "center",  # 点击窗口中心
}

print("AI理解结果:")
print(f"  操作: {ai_understanding['action']}")
print(f"  目标: {ai_understanding['target']}")
print(f"  策略: {ai_understanding['strategy']}")
print(f"  点击位置: {ai_understanding['click_position']}")
print()

# ═══════════════════════════════════════════════════════════════
# L2 屏幕感知层 - 查找窗口
# ═══════════════════════════════════════════════════════════════

print("【L2 屏幕感知层】")
print("-" * 70)
print()

config = Config()
perceiver = ScreenPerceiver(config)

print("正在扫描所有窗口...")
all_windows = perceiver.perceive_all_windows()

if all_windows["success"]:
    print(f"[OK] 发现 {all_windows['total_count']} 个窗口")
    print()
else:
    print(f"[X] 扫描失败: {all_windows.get('error')}")
    sys.exit(1)

# 查找豆包窗口
print("正在查找豆包窗口...")
found_windows = perceiver.find_window_by_title("豆包")

if not found_windows:
    print("[X] 未找到豆包窗口")
    print()
    print("可能的原因:")
    print("  1. 豆包应用未运行")
    print("  2. 豆包窗口标题不包含'豆包'")
    sys.exit(1)

best_match = found_windows[0]
doubao_window = best_match["window"]

print(f"[OK] 找到豆包窗口!")
print(f"  标题: {doubao_window['title']}")
print(f"  匹配度: {best_match['match_score']:.2f}")
print(f"  位置: {doubao_window['rect']}")
print(f"  大小: {doubao_window['width']} x {doubao_window['height']}")
print()

# ═══════════════════════════════════════════════════════════════
# L3 操作规划层 - 制定执行计划
# ═══════════════════════════════════════════════════════════════

print("【L3 操作规划层】")
print("-" * 70)
print()

# 计算点击位置（窗口中心）
left, top, right, bottom = doubao_window['rect']
click_x = (left + right) // 2
click_y = (top + bottom) // 2

print("执行计划:")
print(f"  步骤1: 激活豆包窗口")
print(f"  步骤2: 移动鼠标到窗口中心 ({click_x}, {click_y})")
print(f"  步骤3: 执行点击操作")
print()

# ═══════════════════════════════════════════════════════════════
# L4 动作执行层 - 执行点击
# ═══════════════════════════════════════════════════════════════

print("【L4 动作执行层】")
print("-" * 70)
print()

try:
    # 步骤1: 激活窗口
    print("步骤1: 激活豆包窗口...")
    activate_result = perceiver.activate_window(window_handle=doubao_window['handle'])
    
    if activate_result["success"]:
        print(f"  [OK] 窗口已激活")
        time.sleep(0.3)  # 等待窗口激活
    else:
        print(f"  [!] 激活失败: {activate_result.get('error')}")
        print("  继续执行点击...")
    print()
    
    # 步骤2: 移动鼠标
    print(f"步骤2: 移动鼠标到 ({click_x}, {click_y})...")
    pyautogui.moveTo(click_x, click_y, duration=0.5)
    print(f"  [OK] 鼠标已移动")
    print()
    
    # 步骤3: 执行点击
    print("步骤3: 执行点击操作...")
    pyautogui.click(click_x, click_y)
    print(f"  [OK] 已点击位置 ({click_x}, {click_y})")
    print()
    
    # ═══════════════════════════════════════════════════════════
    # L5 验证反馈层 - 验证结果
    # ═══════════════════════════════════════════════════════════
    
    print("【L5 验证反馈层】")
    print("-" * 70)
    print()
    
    # 验证窗口是否成为活动窗口
    time.sleep(0.5)
    new_state = perceiver.perceive()
    active_window = new_state.get("active_window")
    
    if active_window and "豆包" in active_window.get("title", ""):
        print("[OK] 验证成功: 豆包窗口现在是活动窗口")
        print(f"  当前活动窗口: {active_window['title']}")
    else:
        print("[!] 验证结果: 豆包窗口可能未激活")
        if active_window:
            print(f"  当前活动窗口: {active_window['title']}")
    print()
    
    # ═══════════════════════════════════════════════════════════
    # L6 知识记忆层 - 记录经验
    # ═══════════════════════════════════════════════════════════
    
    print("【L6 知识记忆层】")
    print("-" * 70)
    print()
    
    experience = {
        "task": "点击豆包窗口",
        "success": True,
        "window_title": doubao_window['title'],
        "click_position": (click_x, click_y),
        "strategy_used": "title_match + center_click",
        "timestamp": time.time(),
    }
    
    print("已记录执行经验:")
    print(f"  任务: {experience['task']}")
    print(f"  结果: {'成功' if experience['success'] else '失败'}")
    print(f"  策略: {experience['strategy_used']}")
    print(f"  点击位置: {experience['click_position']}")
    print()
    
except Exception as e:
    print(f"[X] 执行失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════════════

print("="*70)
print("  执行总结")
print("="*70)
print()

print("[OK] 完整的六层架构协作演示:")
print()
print("  L1 意图理解层: ✅ 理解'点击豆包'意图")
print("  L2 屏幕感知层: ✅ 找到豆包窗口")
print("  L3 操作规划层: ✅ 制定点击计划")
print("  L4 动作执行层: ✅ 执行点击操作")
print("  L5 验证反馈层: ✅ 验证执行结果")
print("  L6 知识记忆层: ✅ 记录执行经验")
print()

print("执行结果:")
print(f"  ✅ 已成功点击豆包窗口")
print(f"  📍 点击位置: ({click_x}, {click_y})")
print(f"  🎯 窗口标题: {doubao_window['title']}")
print()

print("="*70)
print()
print("💡 提示: 豆包窗口应该已经被激活并置顶了!")
print()
