"""
查找屏幕上的"豆包"
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from layers.layer2_perception.element_locator import ElementLocator
from core.config import Config
import time

print("="*70)
print("  屏幕感知测试 - 查找\"豆包\"")
print("="*70)
print()

# 初始化
config = Config()
perceiver = ScreenPerceiver(config)
locator = ElementLocator(config)

print("正在感知屏幕...")
print()

# 感知屏幕
start_time = time.time()
screen_state = perceiver.perceive()
elapsed = time.time() - start_time

print(f"感知完成，耗时: {elapsed:.2f}秒")
print()

# 显示屏幕状态
print("【屏幕状态】")
if screen_state["active_window"]:
    print(f"  当前窗口: {screen_state['active_window']['title']}")
print(f"  UI元素数量: {len(screen_state['elements'])}")
print(f"  OCR文字数量: {len(screen_state.get('texts', []))}")
print()

# 查找"豆包"
print("【查找\"豆包\"】")
print()

found_results = []

# 方法1: 在UI元素中查找
print("1. 在UI元素中查找...")
elements = screen_state.get("elements", [])
for element in elements:
    name = element.get("name", "")
    if "豆包" in name or "doubao" in name.lower():
        found_results.append({
            "source": "UI元素",
            "name": name,
            "type": element.get("type"),
            "position": element.get("center"),
            "rect": element.get("rect"),
        })
        print(f"   [OK] 找到: {name} ({element.get('type')})")
        print(f"     位置: {element.get('center')}")
        print(f"     矩形: {element.get('rect')}")
        print()

if not found_results:
    print("   [X] UI元素中未找到")
    print()

# 方法2: 在OCR文字中查找
print("2. 在OCR文字中查找...")
texts = screen_state.get("texts", [])
if texts:
    for text_info in texts:
        text = text_info.get("text", "")
        if "豆包" in text or "doubao" in text.lower():
            found_results.append({
                "source": "OCR识别",
                "name": text,
                "confidence": text_info.get("confidence"),
                "position": text_info.get("center"),
                "box": text_info.get("box"),
            })
            print(f"   [OK] 找到: {text}")
            print(f"     置信度: {text_info.get('confidence'):.2f}")
            print(f"     位置: {text_info.get('center')}")
            print()
    
    if not any(r["source"] == "OCR识别" for r in found_results):
        print("   [X] OCR文字中未找到")
        print()
else:
    print("   [!] OCR功能未启用或无结果")
    print()

# 方法3: 使用元素定位器
print("3. 使用元素定位器查找...")
result = locator.locate("豆包", screen_state)
if result["success"]:
    element = result["element"]
    found_results.append({
        "source": "元素定位器",
        "name": element.get("name"),
        "method": result["method"],
        "confidence": result["confidence"],
        "position": element.get("center"),
    })
    print(f"   [OK] 找到: {element.get('name')}")
    print(f"     方法: {result['method']}")
    print(f"     置信度: {result['confidence']:.2f}")
    print(f"     位置: {element.get('center')}")
    print()
else:
    print(f"   [X] {result.get('error', '未找到')}")
    print()

# 汇总结果
print("="*70)
print("  查找结果汇总")
print("="*70)
print()

if found_results:
    print(f"[OK] 共找到 {len(found_results)} 个\"豆包\"相关项:")
    print()
    
    for i, result in enumerate(found_results, 1):
        print(f"{i}. 来源: {result['source']}")
        print(f"   名称: {result['name']}")
        if 'confidence' in result:
            print(f"   置信度: {result['confidence']:.2f}")
        if 'position' in result:
            print(f"   位置: {result['position']}")
        print()
    
    # 保存截图
    if screen_state.get("screenshot"):
        screenshot_path = "screen_doubao_check.png"
        screen_state["screenshot"].save(screenshot_path)
        print(f"[PHOTO] 截图已保存: {screenshot_path}")
        print()
    
else:
    print("[X] 屏幕上未找到\"豆包\"相关的图像或文字")
    print()
    print("可能原因:")
    print("  1. 豆包应用未打开")
    print("  2. 豆包窗口被最小化或隐藏")
    print("  3. 豆包以图标形式存在（需要图像识别）")
    print()

print("="*70)
