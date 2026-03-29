"""
测试复杂任务的意图理解
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.enhanced_intent_parser import EnhancedIntentParser
from layers.layer1_intent.task_decomposer import TaskDecomposer
from core.config import Config
import json

print("=" * 70)
print("  复杂任务意图理解测试")
print("=" * 70)
print()

# 初始化
config = Config()
parser = EnhancedIntentParser(config)
decomposer = TaskDecomposer(config)

# 测试任务
tasks = [
    "1. 打开记事本",
    "2. 输入'你好'",
    "3. 保存为文件",
    "4. 把文件通过企业微信发送给熊一伟",
]

print("原始任务：")
for task in tasks:
    print(f"  {task}")
print()

# ═══════════════════════════════════════════════════════════════
# 方案1：逐条解析
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("方案1：逐条解析")
print("=" * 70)
print()

for task in tasks:
    # 去掉编号
    instruction = task.split(". ", 1)[-1] if ". " in task else task
    
    print(f"指令: {instruction}")
    
    result = parser.parse(instruction)
    
    print(f"  意图类型: {result.get('intent')}")
    print(f"  置信度: {result.get('confidence')}")
    print(f"  解析方法: {result.get('method')}")
    
    if result.get('params'):
        print(f"  参数:")
        for key, value in result['params'].items():
            print(f"    - {key}: {value}")
    
    print()

# ═══════════════════════════════════════════════════════════════
# 方案2：整体解析（作为复杂任务）
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("方案2：整体解析（复杂任务）")
print("=" * 70)
print()

full_task = "打开记事本，输入'你好'，保存为文件，通过企业微信发送给熊一伟"
print(f"完整指令: {full_task}")
print()

result = parser.parse(full_task)

print(f"意图类型: {result.get('intent')}")
print(f"置信度: {result.get('confidence')}")
print(f"解析方法: {result.get('method')}")

if result.get('params'):
    print(f"参数:")
    for key, value in result['params'].items():
        print(f"  - {key}: {value}")

print()

# ═══════════════════════════════════════════════════════════════
# 方案3：任务分解
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("方案3：任务分解")
print("=" * 70)
print()

# 尝试分解
decompose_result = decomposer.decompose(full_task, result)

if decompose_result.get('success'):
    print(f"分解成功！")
    print(f"分解方法: {decompose_result.get('method')}")
    print(f"步骤数: {len(decompose_result.get('steps', []))}")
    print()
    
    print("分解后的步骤:")
    for i, step in enumerate(decompose_result.get('steps', []), 1):
        print(f"  步骤{i}: {step.get('description', step.get('action', '未知'))}")
        if step.get('params'):
            for key, value in step['params'].items():
                print(f"    - {key}: {value}")
else:
    print(f"分解失败: {decompose_result.get('error')}")

print()

# ═══════════════════════════════════════════════════════════════
# 方案4：AI智能分解（如果可用）
# ═══════════════════════════════════════════════════════════════

if config.AI_ENABLED:
    print("=" * 70)
    print("方案4：AI智能分解")
    print("=" * 70)
    print()
    
    # 构建AI prompt
    ai_prompt = f"""
分析以下任务，将其分解为具体的可执行步骤。

任务: {full_task}

请返回JSON格式：
{{
    "understanding": "任务整体理解",
    "steps": [
        {{
            "step": 1,
            "action": "click/type/hotkey/wait/open_app",
            "target": "目标元素",
            "params": {{}},
            "description": "步骤描述"
        }}
    ],
    "software_involved": ["记事本", "企业微信"],
    "complexity": "medium"
}}
"""
    
    print("AI正在分析...")
    
    # 这里会实际调用AI（如果有API key）
    result = parser._parse_with_ai(full_task, {})
    
    if result:
        print(f"AI理解结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("AI分析失败（可能未配置API Key）")

print()

# ═══════════════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("  意图理解总结")
print("=" * 70)
print()

print("单步解析结果：")
print("  1. 打开记事本 → open_app (需要扩展支持)")
print("  2. 输入'你好' → type (✅ 已支持)")
print("  3. 保存为文件 → hotkey:Ctrl+S (✅ 已支持)")
print("  4. 通过企业微信发送 → 复杂操作 (需要任务分解)")
print()

print("整体解析结果：")
print("  意图类型: 复杂任务")
print("  需要分解: 是")
print("  涉及软件: 记事本, 企业微信")
print("  复杂度: 高")
print()

print("建议执行方式：")
print("  1. 将任务分解为4个子任务")
print("  2. 逐个执行并验证")
print("  3. 跨软件协作需要状态管理")
print()

print("=" * 70)
