"""
扫描所有窗口查找豆包
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import uiautomation as auto
    import pyautogui
    from PIL import Image
except ImportError as e:
    print(f"缺少依赖: {e}")
    sys.exit(1)

print("="*70)
print("  全窗口扫描 - 查找\"豆包\"")
print("="*70)
print()

# 方法1: 遍历所有窗口
print("【方法1】遍历所有窗口...")
print()

found_windows = []

# 获取所有顶级窗口
root = auto.GetRootControl()
windows = root.GetChildren()

print(f"发现 {len(windows)} 个顶级窗口")
print()

for i, window in enumerate(windows, 1):
    try:
        name = window.Name
        class_name = window.ClassName
        
        # 检查是否包含"豆包"
        if name and ("豆包" in name or "doubao" in name.lower()):
            rect = window.BoundingRectangle
            
            found_windows.append({
                "name": name,
                "class_name": class_name,
                "handle": window.NativeWindowHandle,
                "rect": (rect.left, rect.top, rect.right, rect.bottom),
                "window": window,
            })
            
            print(f"[OK] 找到豆包窗口!")
            print(f"  标题: {name}")
            print(f"  类名: {class_name}")
            print(f"  句柄: {window.NativeWindowHandle}")
            print(f"  位置: ({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
            print(f"  大小: {rect.right - rect.left} x {rect.bottom - rect.top}")
            print()
        
    except Exception as e:
        pass  # 忽略无法访问的窗口

if not found_windows:
    print("[X] 未找到包含\"豆包\"标题的窗口")
    print()

# 方法2: 搜索窗口内元素
print("【方法2】搜索所有窗口内的UI元素...")
print()

if not found_windows:
    print("遍历前20个窗口的UI元素...")
    print()
    
    for i, window in enumerate(windows[:20], 1):
        try:
            window_name = window.Name or "(无名称)"
            
            # 递归查找包含"豆包"的元素
            found_elements = []
            
            def find_doubao_elements(control, depth=0, max_depth=8):
                if depth > max_depth:
                    return
                
                try:
                    name = control.Name or ""
                    
                    if "豆包" in name or "doubao" in name.lower():
                        rect = control.BoundingRectangle
                        found_elements.append({
                            "name": name,
                            "type": control.ControlTypeName,
                            "rect": (rect.left, rect.top, rect.right, rect.bottom),
                        })
                    
                    # 递归查找子元素
                    for child in control.GetChildren():
                        find_doubao_elements(child, depth + 1, max_depth)
                        
                except Exception:
                    pass
            
            find_doubao_elements(window)
            
            if found_elements:
                print(f"[OK] 在窗口 '{window_name}' 中找到 {len(found_elements)} 个相关元素:")
                for elem in found_elements:
                    print(f"  - {elem['type']}: {elem['name']}")
                    print(f"    位置: {elem['rect']}")
                print()
                
        except Exception as e:
            pass

# 方法3: 截图并分析
print("【方法3】截图分析...")
print()

try:
    # 截取全屏
    screenshot = pyautogui.screenshot()
    screenshot_path = "full_screen_scan.png"
    screenshot.save(screenshot_path)
    print(f"[OK] 截图已保存: {screenshot_path}")
    print(f"  分辨率: {screenshot.size}")
    print()
    
    # 提示：如果有OCR可以进一步分析
    print("[提示] 如需文字识别，请安装PaddleOCR:")
    print("  pip install paddleocr")
    print()
    
except Exception as e:
    print(f"[X] 截图失败: {e}")
    print()

# 方法4: 使用窗口句柄查找
print("【方法4】通过窗口句柄查找...")
print()

try:
    import win32gui
    import win32con
    
    def enum_windows_callback(hwnd, results):
        try:
            title = win32gui.GetWindowText(hwnd)
            if title and ("豆包" in title or "doubao" in title.lower()):
                rect = win32gui.GetWindowRect(hwnd)
                results.append({
                    "hwnd": hwnd,
                    "title": title,
                    "rect": rect,
                })
        except Exception:
            pass
    
    win32_results = []
    win32gui.EnumWindows(enum_windows_callback, win32_results)
    
    if win32_results:
        print(f"[OK] 找到 {len(win32_results)} 个豆包窗口:")
        for result in win32_results:
            print(f"  标题: {result['title']}")
            print(f"  句柄: {result['hwnd']}")
            print(f"  位置: {result['rect']}")
            print()
    else:
        print("[X] 未找到豆包窗口")
        print()
        
except ImportError:
    print("[!] 未安装 pywin32，跳过此方法")
    print("  安装: pip install pywin32")
    print()

# 汇总结果
print("="*70)
print("  扫描结果汇总")
print("="*70)
print()

if found_windows:
    print(f"[OK] 共找到 {len(found_windows)} 个豆包窗口!")
    print()
    
    for i, win in enumerate(found_windows, 1):
        print(f"窗口 {i}:")
        print(f"  标题: {win['name']}")
        print(f"  位置: {win['rect']}")
        print()
else:
    print("[X] 未找到豆包窗口")
    print()
    print("可能的原因:")
    print("  1. 豆包窗口标题不包含\"豆包\"字样")
    print("  2. 豆包以Web方式运行（浏览器标签页）")
    print("  3. 豆包窗口被其他窗口完全遮挡")
    print()
    print("建议:")
    print("  1. 安装PaddleOCR进行文字识别")
    print("  2. 使用图像识别查找豆包Logo")
    print("  3. 手动确认豆包窗口是否可见")
    print()

print("="*70)
