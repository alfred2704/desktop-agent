"""
AI驱动的智能窗口查找（简化版）
直接使用uiautomation，避免依赖问题
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import uiautomation as auto
except ImportError:
    print("[错误] 未安装uiautomation，请运行: pip install uiautomation")
    sys.exit(1)

print("="*70)
print("  AI驱动的智能窗口查找")
print("="*70)
print()

# AI理解的用户意图
user_intent = "找到豆包窗口"

print(f"[用户意图] {user_intent}")
print()

# 步骤1: AI理解意图
print("="*70)
print("步骤1: AI理解用户意图")
print("="*70)
print()

# AI知识库（模拟L1意图理解层）
ai_knowledge = {
    "豆包": {
        "target_app": "豆包",
        "possible_names": ["豆包", "Doubao", "DOUBAO"],
        "possible_classes": ["Chrome_WidgetWin_1"],
        "keywords": ["豆包", "doubao"],
        "confidence": 0.9,
    },
}

# 匹配知识库
target_info = None
for app_name, info in ai_knowledge.items():
    if app_name in user_intent:
        target_info = info
        break

if target_info:
    print(f"[AI理解结果]")
    print(f"  目标应用: {target_info['target_app']}")
    print(f"  可能的标题: {target_info['possible_names']}")
    print(f"  可能的类名: {target_info['possible_classes']}")
    print(f"  搜索关键词: {target_info['keywords']}")
    print(f"  置信度: {target_info['confidence']:.2f}")
    print()
else:
    print("[AI理解] 未找到匹配的应用知识，使用通用搜索")
    target_info = {
        "target_app": user_intent,
        "possible_names": [user_intent],
        "possible_classes": [],
        "keywords": [user_intent],
        "confidence": 0.5,
    }
    print()

# 步骤2: 扫描所有窗口
print("="*70)
print("步骤2: 扫描所有窗口")
print("="*70)
print()

try:
    # 获取根控件
    root = auto.GetRootControl()
    
    if not root:
        print("[错误] 无法获取根控件")
        sys.exit(1)
    
    # 获取所有顶级窗口
    windows = root.GetChildren()
    
    print(f"[扫描结果] 发现 {len(windows)} 个顶级窗口")
    print()
    
    # 显示所有窗口（前20个）
    print("窗口列表（前20个）:")
    print()
    
    for i, window in enumerate(windows[:20], 1):
        try:
            title = window.Name or "(无标题)"
            class_name = window.ClassName or "(无)"
            
            print(f"{i}. [{title[:40]}]")
            print(f"   类名: {class_name}")
            print()
        except:
            pass
    
    if len(windows) > 20:
        print(f"... 还有 {len(windows) - 20} 个窗口")
        print()
    
except Exception as e:
    print(f"[错误] 扫描窗口失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 步骤3: 多策略查找
print("="*70)
print("步骤3: 多策略智能查找")
print("="*70)
print()

found_windows = []

# 策略1: 精确标题匹配
print("策略1: 精确标题匹配")
for name in target_info["possible_names"]:
    for window in windows:
        try:
            title = window.Name or ""
            if title.lower() == name.lower():
                rect = window.BoundingRectangle
                found_windows.append({
                    "window": window,
                    "title": title,
                    "class_name": window.ClassName,
                    "handle": window.NativeWindowHandle,
                    "rect": (rect.left, rect.top, rect.right, rect.bottom),
                    "match_strategy": "exact_title",
                    "match_score": 1.0,
                })
                print(f"  [OK] 找到精确匹配: {title}")
        except:
            pass
print()

# 策略2: 模糊标题匹配
if not found_windows:
    print("策略2: 模糊标题匹配")
    for name in target_info["possible_names"]:
        for window in windows:
            try:
                title = window.Name or ""
                if name.lower() in title.lower():
                    rect = window.BoundingRectangle
                    found_windows.append({
                        "window": window,
                        "title": title,
                        "class_name": window.ClassName,
                        "handle": window.NativeWindowHandle,
                        "rect": (rect.left, rect.top, rect.right, rect.bottom),
                        "match_strategy": "fuzzy_title",
                        "match_score": 0.8,
                    })
                    print(f"  [OK] 找到模糊匹配: {title}")
            except:
                pass
    print()

# 策略3: 类名匹配
if not found_windows and target_info.get("possible_classes"):
    print("策略3: 类名匹配")
    for class_name in target_info["possible_classes"]:
        for window in windows:
            try:
                if window.ClassName == class_name:
                    rect = window.BoundingRectangle
                    found_windows.append({
                        "window": window,
                        "title": window.Name,
                        "class_name": window.ClassName,
                        "handle": window.NativeWindowHandle,
                        "rect": (rect.left, rect.top, rect.right, rect.bottom),
                        "match_strategy": "class_name",
                        "match_score": 0.7,
                    })
                    print(f"  [OK] 找到类名匹配: {window.Name}")
            except:
                pass
    print()

# 策略4: 关键词搜索
if not found_windows:
    print("策略4: 关键词搜索")
    for keyword in target_info["keywords"]:
        for window in windows:
            try:
                title = window.Name or ""
                class_name = window.ClassName or ""
                
                if keyword.lower() in title.lower() or keyword.lower() in class_name.lower():
                    rect = window.BoundingRectangle
                    found_windows.append({
                        "window": window,
                        "title": title,
                        "class_name": class_name,
                        "handle": window.NativeWindowHandle,
                        "rect": (rect.left, rect.top, rect.right, rect.bottom),
                        "match_strategy": "keyword",
                        "match_score": 0.6,
                    })
                    print(f"  [OK] 找到关键词匹配: {title}")
            except:
                pass
    print()

# 步骤4: 选择最佳匹配
print("="*70)
print("步骤4: 选择最佳匹配")
print("="*70)
print()

if found_windows:
    # 去重
    unique_windows = {}
    for found in found_windows:
        handle = found["handle"]
        if handle not in unique_windows or found["match_score"] > unique_windows[handle]["match_score"]:
            unique_windows[handle] = found
    
    # 排序
    sorted_windows = sorted(
        unique_windows.values(),
        key=lambda x: x["match_score"],
        reverse=True
    )
    
    best_match = sorted_windows[0]
    
    print(f"[OK] AI成功找到最佳匹配!")
    print()
    print(f"窗口信息:")
    print(f"  标题: {best_match['title']}")
    print(f"  类名: {best_match['class_name']}")
    print(f"  句柄: {best_match['handle']}")
    print(f"  位置: {best_match['rect']}")
    print(f"  匹配策略: {best_match['match_strategy']}")
    print(f"  置信度: {best_match['match_score']:.2f}")
    print()
    
    print(f"AI查找过程:")
    for i, found in enumerate(sorted_windows[:3], 1):
        print(f"  {i}. {found['match_strategy']}: {found['title']} (得分: {found['match_score']:.2f})")
    print()
    
else:
    print("[X] AI未找到匹配窗口")
    print()
    print("建议:")
    print("  1. 确认豆包应用已打开")
    print("  2. 检查窗口标题是否正确")
    print("  3. 尝试使用其他搜索词")
    print()

print("="*70)
print("  AI窗口查找完成")
print("="*70)
