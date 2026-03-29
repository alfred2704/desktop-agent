"""
Desktop Agent - 快速开始示例
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.agent import DesktopAgent
from core.config import Config
import time


def main():
    """快速开始示例"""
    
    print("=" * 70)
    print("  🎯 Desktop Agent - 快速开始")
    print("=" * 70)
    print()
    
    # 初始化Agent
    print("初始化 Desktop Agent...")
    config = Config()
    agent = DesktopAgent(config)
    print("✓ 初始化完成\n")
    
    # 示例1：感知屏幕
    print("=" * 70)
    print("示例1：感知屏幕")
    print("=" * 70)
    
    screen_state = agent.sense_screen()
    print(f"✓ 检测到 {len(screen_state.get('elements', []))} 个UI元素")
    print(f"✓ 检测到 {len(screen_state.get('texts', []))} 个文字")
    
    window = screen_state.get("active_window")
    if window:
        print(f"✓ 活动窗口: {window.get('title')}")
    
    print()
    
    # 示例2：查找元素
    print("=" * 70)
    print("示例2：查找元素")
    print("=" * 70)
    
    result = agent.find_element("确定")
    if result.get("success"):
        element = result.get("element")
        print(f"✓ 找到确定按钮")
        print(f"  类型: {element.get('type')}")
        print(f"  名称: {element.get('name')}")
        print(f"  位置: {element.get('center')}")
    else:
        print("  未找到确定按钮")
    
    print()
    
    # 示例3：执行指令
    print("=" * 70)
    print("示例3：执行指令")
    print("=" * 70)
    
    instructions = [
        "按Ctrl+S保存",
        "点击确定按钮",
    ]
    
    for instruction in instructions:
        print(f"\n执行: {instruction}")
        print("-" * 70)
        
        # 只演示，不实际执行（注释掉）
        # result = agent.execute(instruction)
        # print(f"结果: {'成功' if result.get('success') else '失败'}")
        # print(f"耗时: {result.get('execution_time', 0):.2f}秒")
        
        print("（演示模式，不实际执行）")
        print()
    
    print("=" * 70)
    print("  快速开始演示完成!")
    print("=" * 70)
    print()
    print("使用方式:")
    print("  1. Web界面: python web/app.py")
    print("  2. 命令行: python tools/cli.py")
    print("  3. Python API: from core.agent import DesktopAgent")
    print()


if __name__ == "__main__":
    main()
