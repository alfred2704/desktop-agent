"""
测试任务：Excel数据与银行流水比对（1000条数据）
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from core.config import Config
import json

print("=" * 70)
print("  Excel数据与银行流水比对任务 - 意图理解测试")
print("=" * 70)
print()

# 初始化
config = Config()
parser = AIDrivenIntentParser(config)

# ═══════════════════════════════════════════════════════════════
# 用户任务
# ═══════════════════════════════════════════════════════════════

instruction = "打开Excel表，将Excel表里的收货日期、收货的数目以及金额进行整理匹配。同工商银行的网上下载的流水进行比对，数据有1000条，请重复这个过程"

print(f"任务: {instruction}")
print()
print("=" * 70)
print()

# 解析任务
result = parser.parse(instruction)

# ═══════════════════════════════════════════════════════════════
# 显示结果
# ═══════════════════════════════════════════════════════════════

print("【任务理解】")
print(f"  类型: {result.get('task_type')}")
print(f"  理解: {result.get('understanding')}")
print(f"  置信度: {result.get('confidence')}")
print()

print("【涉及软件】")
for software in result.get('software', []):
    print(f"  - {software}")
print()

print("【步骤分解】")
print("-" * 70)
for step in result.get('steps', []):
    step_id = step.get('step_id', '?')
    action = step.get('action', '?')
    description = step.get('description', '?')
    params = step.get('params', {})
    dependencies = step.get('dependencies', [])
    output = step.get('output', '')
    
    print(f"步骤{step_id}: {description}")
    print(f"  动作: {action}")
    if params:
        print(f"  参数:")
        for key, value in params.items():
            print(f"    - {key}: {value}")
    if dependencies:
        print(f"  依赖: 步骤{dependencies}")
    if output:
        print(f"  输出: {output}")
    print()

print("【数据流】")
print("-" * 70)
data_flow = result.get('data_flow', {})
if data_flow:
    for src, dst in data_flow.items():
        print(f"  {src} -> {dst}")
else:
    print("  (无数据流)")
print()

print("【风险评估】")
print("-" * 70)
risks = result.get('risks', [])
if risks:
    for i, risk in enumerate(risks, 1):
        print(f"  {i}. {risk}")
else:
    print("  (无风险)")
print()

print("【特殊要求】")
print("-" * 70)
print(f"  数据量: 1000条")
print(f"  重复处理: 是")
print()

print("=" * 70)
print("  完整JSON结果")
print("=" * 70)
print()
print(json.dumps(result, ensure_ascii=False, indent=2))
