"""
意图理解测试 - AI驱动架构
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
print("  AI驱动意图理解测试")
print("=" * 70)
print()

# 初始化
config = Config()
parser = AIDrivenIntentParser(config)

# ═══════════════════════════════════════════════════════════════
# 测试任务
# ═══════════════════════════════════════════════════════════════

test_cases = [
    # 用户的复杂任务
    {
        "name": "复杂任务（用户需求）",
        "instruction": "打开记事本，输入'你好'，保存为文件，通过企业微信发送给熊一伟",
        "expected_steps": 4,
    },
    
    # 简单操作
    {
        "name": "简单点击",
        "instruction": "点击确定按钮",
        "expected_steps": 1,
    },
    
    {
        "name": "简单输入",
        "instruction": "输入'Hello World'",
        "expected_steps": 1,
    },
    
    # 中等复杂度
    {
        "name": "文档工作流",
        "instruction": "打开Word，写一份报告，保存为'月报.docx'",
        "expected_steps": 3,
    },
    
    {
        "name": "沟通协作",
        "instruction": "打开微信，发消息给张三说'明天开会'",
        "expected_steps": 2,
    },
    
    # 复杂任务
    {
        "name": "跨软件协作",
        "instruction": "从Excel复制数据，粘贴到邮件，发送给老板",
        "expected_steps": 3,
    },
]

# 运行测试
results = []

for test in test_cases:
    print(f"\n{'='*70}")
    print(f"测试: {test['name']}")
    print(f"指令: {test['instruction']}")
    print('='*70)
    
    result = parser.parse(test['instruction'])
    
    # 显示结果
    print(f"\n任务类型: {result.get('task_type')}")
    print(f"理解: {result.get('understanding')}")
    print(f"涉及软件: {result.get('software')}")
    print(f"步骤数: {len(result.get('steps', []))}")
    print(f"置信度: {result.get('confidence')}")
    print(f"方法: {result.get('method', 'ai_understand')}")
    
    if result.get('steps'):
        print(f"\n步骤详情:")
        for step in result['steps']:
            print(f"  步骤{step.get('step_id')}: {step.get('description')}")
            print(f"    动作: {step.get('action')}")
            if step.get('params'):
                print(f"    参数: {step.get('params')}")
            if step.get('dependencies'):
                print(f"    依赖: 步骤{step.get('dependencies')}")
    
    if result.get('data_flow'):
        print(f"\n数据流:")
        for src, dst in result['data_flow'].items():
            print(f"  {src} → {dst}")
    
    if result.get('risks'):
        print(f"\n风险:")
        for risk in result['risks']:
            print(f"  - {risk}")
    
    # 评估
    expected = test['expected_steps']
    actual = len(result.get('steps', []))
    success = actual >= expected
    
    results.append({
        "name": test['name'],
        "expected": expected,
        "actual": actual,
        "success": success,
        "task_type": result.get('task_type'),
        "method": result.get('method', 'ai'),
    })
    
    print(f"\n{'✓ 成功' if success else '✗ 失败'}")

# 总结
print("\n" + "=" * 70)
print("  测试总结")
print("=" * 70)
print()

passed = sum(1 for r in results if r['success'])
total = len(results)

print(f"总计: {total}")
print(f"通过: {passed}")
print(f"失败: {total - passed}")
print(f"成功率: {passed/total*100:.1f}%")
print()

print("详细结果:")
for r in results:
    status = "✓" if r['success'] else "✗"
    print(f"  {status} {r['name']}: {r['actual']}/{r['expected']} 步 ({r['method']})")

print()

if passed == total:
    print("[SUCCESS] 所有测试通过！")
elif passed >= total * 0.8:
    print("[GOOD] 大部分测试通过")
else:
    print("[WARNING] 需要改进")

print()
print("=" * 70)
