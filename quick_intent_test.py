"""
快速意图识别测试
测试几个典型任务的识别结果
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from core.config import Config
import json

print("\n" + "="*70)
print("  意图识别测试 - 复杂企业级任务")
print("="*70 + "\n")

# 初始化解析器
config = Config()
parser = AIDrivenIntentParser(config)

# ═══════════════════════════════════════════════════════════════
# 测试用例
# ═══════════════════════════════════════════════════════════════

test_cases = [
    {
        "name": "金融-月度财务对账（25步骤）",
        "expected_steps": 25,
        "instruction": """
        月度财务对账全流程任务：
        
        1. 登录工商银行企业网银系统
        2. 导航到账户管理页面
        3. 选择本月时间范围
        4. 下载本月所有银行流水明细（Excel格式）
        5. 退出工商银行网银
        
        6. 登录建设银行企业网银系统
        7. 下载建设银行本月流水
        8. 退出建设银行网银
        
        9. 登录农业银行企业网银系统
        10. 下载农业银行本月流水
        11. 退出农业银行网银
        
        12. 打开ERP财务系统
        13. 导出本月所有收款记录
        14. 导出本月所有付款记录
        15. 退出ERP系统
        
        16. 打开Excel，创建新工作簿
        17. 将三个银行流水合并到一个工作表
        18. 将ERP收款记录导入第二个工作表
        19. 使用VLOOKUP函数匹配银行流水与ERP记录
        20. 标记所有未匹配项（差异项）
        21. 对差异项进行分类（时间性差异、记账错误、未达账项）
        22. 生成差异调节表
        23. 创建月度对账报告
        24. 保存对账文件
        25. 通过邮件发送给财务总监审核
        """,
    },
    {
        "name": "制造-生产计划排程（26步骤）",
        "expected_steps": 26,
        "instruction": """
        生产计划排程优化全流程：
        
        1. 登录ERP系统
        2. 导出未来30天销售订单
        3. 按产品类型分类
        4. 按交货期排序
        5. 退出ERP系统
        
        6. 登录MES系统
        7. 查询各产线当前状态
        8. 查询各产线产能数据
        9. 查询设备维护计划
        10. 退出MES系统
        
        11. 登录WMS系统
        12. 查询成品库存
        13. 查询原材料库存
        14. 查询在制品数量
        15. 退出WMS系统
        
        16. 打开Excel排程工具
        17. 导入销售订单数据
        18. 导入产能数据
        19. 导入库存数据
        20. 计算净需求量
        21. 运行排程算法
        22. 生成生产计划表
        23. 生成物料需求计划
        24. 保存排程文件
        
        25. 登录MES系统
        26. 导入生产计划并发布到各产线
        """,
    },
    {
        "name": "电商-大促活动全流程（28步骤）",
        "expected_steps": 28,
        "instruction": """
        双十一大促活动全流程管理：
        
        1. 登录淘宝卖家中心
        2. 创建双十一活动页面
        3. 设置活动商品
        4. 设置促销价格
        5. 设置优惠券
        6. 退出淘宝
        
        7. 登录京东商家后台
        8. 创建京东双十一活动
        9. 设置活动商品
        10. 设置促销价格
        11. 退出京东
        
        12. 登录拼多多商家后台
        13. 创建拼多多活动
        14. 设置活动商品
        15. 退出拼多多
        
        16. 登录ERP系统
        17. 导出商品库存
        18. 计算活动备货量
        19. 生成采购计划
        20. 退出ERP系统
        
        21. 登录CRM系统
        22. 筛选目标客户
        23. 设置营销短信
        24. 退出CRM系统
        
        25. 登录BI系统
        26. 创建活动监控看板
        27. 设置实时预警
        28. 发送活动准备完成通知
        """,
    },
]

# ═══════════════════════════════════════════════════════════════
# 运行测试
# ═══════════════════════════════════════════════════════════════

results = []

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*70}")
    print(f"测试 {i}: {test['name']}")
    print(f"{'='*70}\n")
    
    print(f"预期步骤数: {test['expected_steps']}")
    print(f"\n开始解析...\n")
    
    # 解析任务
    result = parser.parse(test['instruction'])
    
    # 显示结果
    print(f"【任务理解】")
    print(f"  类型: {result.get('task_type', 'unknown')}")
    print(f"  理解: {result.get('understanding', 'N/A')[:100]}...")
    print(f"  置信度: {result.get('confidence', 0):.2f}")
    print(f"  方法: {result.get('method', 'ai')}")
    print()
    
    # 步骤
    steps = result.get('steps', [])
    print(f"【步骤分解】实际: {len(steps)} 步 / 预期: {test['expected_steps']} 步")
    
    if steps:
        print("\n前10个步骤:")
        for step in steps[:10]:
            step_id = step.get('step_id', '?')
            action = step.get('action', '?')
            description = step.get('description', '?')
            print(f"  {step_id}. {action}: {description[:50]}...")
        
        if len(steps) > 10:
            print(f"  ... 还有 {len(steps) - 10} 个步骤")
    print()
    
    # 软件
    software = result.get('software', [])
    print(f"【涉及软件】({len(software)}个)")
    for s in software:
        print(f"  - {s}")
    print()
    
    # 数据流
    data_flow = result.get('data_flow', {})
    print(f"【数据流】")
    if data_flow:
        for src, dst in list(data_flow.items())[:5]:
            print(f"  {src} → {dst}")
        if len(data_flow) > 5:
            print(f"  ... 还有 {len(data_flow) - 5} 条数据流")
    else:
        print("  (未识别)")
    print()
    
    # 风险
    risks = result.get('risks', [])
    print(f"【风险评估】({len(risks)}个)")
    if risks:
        for risk in risks[:3]:
            print(f"  [!] {risk}")
        if len(risks) > 3:
            print(f"  ... 还有 {len(risks) - 3} 个风险")
    else:
        print("  (未识别)")
    print()
    
    # 评分
    steps_score = min(len(steps) / test['expected_steps'], 1.0) * 40 if test['expected_steps'] > 0 else 0
    confidence_score = (result.get('confidence', 0) / 1.0) * 30
    software_score = min(len(software) / 3, 1.0) * 20
    data_flow_score = 10 if data_flow else 0
    
    total_score = steps_score + confidence_score + software_score + data_flow_score
    
    print(f"【评分】")
    print(f"  步骤准确性: {steps_score:.1f}/40")
    print(f"  置信度: {confidence_score:.1f}/30")
    print(f"  软件识别: {software_score:.1f}/20")
    print(f"  数据流: {data_flow_score:.1f}/10")
    print(f"  ─────────────────")
    print(f"  总分: {total_score:.1f}/100")
    
    if total_score >= 80:
        grade = "[5星] 优秀"
    elif total_score >= 70:
        grade = "[4星] 良好"
    elif total_score >= 60:
        grade = "[3星] 合格"
    else:
        grade = "[2星] 需改进"
    
    print(f"  评级: {grade}")
    
    results.append({
        "name": test['name'],
        "expected_steps": test['expected_steps'],
        "actual_steps": len(steps),
        "confidence": result.get('confidence', 0),
        "software_count": len(software),
        "score": total_score,
        "grade": grade,
    })

# ═══════════════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════════════

print("\n\n" + "="*70)
print("  测试总结")
print("="*70 + "\n")

for r in results:
    print(f"{r['name']}")
    print(f"  步骤: {r['actual_steps']}/{r['expected_steps']} | 置信度: {r['confidence']:.2f} | 得分: {r['score']:.1f} | {r['grade']}")
    print()

avg_score = sum(r['score'] for r in results) / len(results)
print(f"平均分: {avg_score:.1f}/100")
print()

if avg_score >= 80:
    print("✅ 系统已达到企业级应用标准")
elif avg_score >= 70:
    print("✅ 系统表现良好，可应用于大部分企业场景")
else:
    print("⚠️  系统需要进一步优化")

print("\n" + "="*70)
