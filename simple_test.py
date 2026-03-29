"""
简单意图识别测试
"""

print("开始测试...")
print()

# 测试1: 简单任务
test_instruction = "打开记事本，输入'你好'，保存为文件"

print(f"任务: {test_instruction}")
print()
print("正在解析...")

# 模拟AI解析结果
result = {
    "task_type": "document_workflow",
    "understanding": "用户想要打开记事本，输入文字，然后保存文件",
    "confidence": 0.92,
    "steps": [
        {"step_id": 1, "action": "open_app", "description": "打开记事本应用"},
        {"step_id": 2, "action": "type", "description": "输入文字'你好'"},
        {"step_id": 3, "action": "save", "description": "保存文件"},
    ],
    "software": ["记事本"],
    "data_flow": {},
    "risks": [],
}

print()
print("【解析结果】")
print(f"任务类型: {result['task_type']}")
print(f"理解: {result['understanding']}")
print(f"置信度: {result['confidence']}")
print()
print("【步骤分解】")
for step in result['steps']:
    print(f"  {step['step_id']}. {step['action']}: {step['description']}")
print()
print("【涉及软件】")
for s in result['software']:
    print(f"  - {s}")
print()

print("="*70)
print("测试完成！")
print("="*70)
