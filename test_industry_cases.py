"""
行业测试用例集
覆盖：金融、制造、电商三大行业
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from core.config import Config
import json

# ═══════════════════════════════════════════════════════════════
# 测试用例配置
# ═══════════════════════════════════════════════════════════════

INDUSTRY_TEST_CASES = {
    # ═══════════════════════════════════════════════════════════
    # 金融行业（15个典型任务）
    # ═══════════════════════════════════════════════════════════
    "finance": {
        "name": "金融行业",
        "icon": "💰",
        "test_cases": [
            {
                "id": "FIN001",
                "category": "银行对账",
                "difficulty": "高",
                "instruction": "登录工商银行网银，下载本月流水，与ERP系统中的收款记录进行核对，标记差异项",
                "expected": {
                    "steps": 5,
                    "software": ["工商银行网银", "ERP系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "月度财务对账，确保账实相符",
            },
            {
                "id": "FIN002",
                "category": "银行对账",
                "difficulty": "高",
                "instruction": "从建设银行下载对账单，从农业银行下载对账单，将两个银行的对账单合并到Excel中进行比对",
                "expected": {
                    "steps": 4,
                    "software": ["建设银行", "农业银行", "Excel"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "多银行账户管理",
            },
            {
                "id": "FIN003",
                "category": "客户开户",
                "difficulty": "中",
                "instruction": "在CRM系统中创建新客户，填写客户信息，上传身份证照片，提交审核",
                "expected": {
                    "steps": 4,
                    "software": ["CRM系统"],
                    "risks": True,
                    "confidence": 0.8,
                },
                "business_context": "客户开户流程自动化",
            },
            {
                "id": "FIN004",
                "category": "贷款审批",
                "difficulty": "高",
                "instruction": "从征信系统查询客户信用报告，从收入系统获取收入证明，将两份资料汇总到审批表中",
                "expected": {
                    "steps": 4,
                    "software": ["征信系统", "收入系统", "审批表"],
                    "data_flow": True,
                    "confidence": 0.7,
                },
                "business_context": "贷款审批资料收集",
            },
            {
                "id": "FIN005",
                "category": "财务报表",
                "difficulty": "中",
                "instruction": "从财务系统导出资产负债表、利润表、现金流量表，合并到月报Excel中",
                "expected": {
                    "steps": 4,
                    "software": ["财务系统", "Excel"],
                    "data_flow": True,
                    "confidence": 0.8,
                },
                "business_context": "月度财务报表编制",
            },
            {
                "id": "FIN006",
                "category": "财务报表",
                "difficulty": "中",
                "instruction": "打开财务软件，生成季度损益表，导出为PDF，通过邮件发送给财务总监",
                "expected": {
                    "steps": 4,
                    "software": ["财务软件", "邮件"],
                    "confidence": 0.8,
                },
                "business_context": "季度报表报送",
            },
            {
                "id": "FIN007",
                "category": "风险管理",
                "difficulty": "高",
                "instruction": "从风险系统导出逾期客户清单，从催收系统获取催收记录，生成风险分析报告",
                "expected": {
                    "steps": 4,
                    "software": ["风险系统", "催收系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "逾期风险分析",
            },
            {
                "id": "FIN008",
                "category": "投资管理",
                "difficulty": "高",
                "instruction": "从交易系统下载股票交易记录，从行情系统获取当日收盘价，计算投资组合市值",
                "expected": {
                    "steps": 4,
                    "software": ["交易系统", "行情系统", "Excel"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "投资组合管理",
            },
            {
                "id": "FIN009",
                "category": "税务管理",
                "difficulty": "中",
                "instruction": "从开票系统导出发票数据，从税务系统获取进项发票，计算应缴税额",
                "expected": {
                    "steps": 4,
                    "software": ["开票系统", "税务系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "税务申报准备",
            },
            {
                "id": "FIN010",
                "category": "资金管理",
                "difficulty": "中",
                "instruction": "从各银行账户下载余额信息，汇总到资金日报表，发送给财务经理",
                "expected": {
                    "steps": 3,
                    "software": ["银行账户", "Excel", "邮件"],
                    "data_flow": True,
                    "confidence": 0.8,
                },
                "business_context": "资金日报编制",
            },
            {
                "id": "FIN011",
                "category": "审计支持",
                "difficulty": "高",
                "instruction": "从凭证系统导出会计凭证，从银行系统下载回单，将凭证与回单进行匹配归档",
                "expected": {
                    "steps": 4,
                    "software": ["凭证系统", "银行系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "审计资料准备",
            },
            {
                "id": "FIN012",
                "category": "客户服务",
                "difficulty": "中",
                "instruction": "从客服系统导出客户投诉记录，分类统计投诉类型，生成投诉分析报告",
                "expected": {
                    "steps": 3,
                    "software": ["客服系统"],
                    "confidence": 0.8,
                },
                "business_context": "客户投诉分析",
            },
            {
                "id": "FIN013",
                "category": "合规检查",
                "difficulty": "高",
                "instruction": "从交易系统导出大额交易记录，与反洗钱规则进行比对，标记可疑交易",
                "expected": {
                    "steps": 3,
                    "software": ["交易系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "反洗钱合规",
            },
            {
                "id": "FIN014",
                "category": "报销管理",
                "difficulty": "中",
                "instruction": "从报销系统导出待审批报销单，核对发票真伪，审批通过后提交财务付款",
                "expected": {
                    "steps": 4,
                    "software": ["报销系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "报销审批流程",
            },
            {
                "id": "FIN015",
                "category": "预算管理",
                "difficulty": "中",
                "instruction": "从预算系统导出预算执行情况，从财务系统获取实际支出，生成预算执行分析报告",
                "expected": {
                    "steps": 4,
                    "software": ["预算系统", "财务系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "预算执行分析",
            },
        ],
    },
    
    # ═══════════════════════════════════════════════════════════
    # 制造行业（15个典型任务）
    # ═══════════════════════════════════════════════════════════
    "manufacturing": {
        "name": "制造行业",
        "icon": "🏭",
        "test_cases": [
            {
                "id": "MFG001",
                "category": "生产计划",
                "difficulty": "高",
                "instruction": "从ERP系统导出销售订单，根据产能计算生产计划，将计划导入MES系统",
                "expected": {
                    "steps": 3,
                    "software": ["ERP系统", "MES系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "生产计划排程",
            },
            {
                "id": "MFG002",
                "category": "生产计划",
                "difficulty": "高",
                "instruction": "从MES系统获取生产线状态，从ERP获取物料库存，调整生产排程优化产能利用率",
                "expected": {
                    "steps": 3,
                    "software": ["MES系统", "ERP系统"],
                    "data_flow": True,
                    "confidence": 0.7,
                },
                "business_context": "产能优化调度",
            },
            {
                "id": "MFG003",
                "category": "质量管理",
                "difficulty": "中",
                "instruction": "从质检系统导出质检记录，统计不合格品数量，生成质量分析报告",
                "expected": {
                    "steps": 3,
                    "software": ["质检系统"],
                    "confidence": 0.8,
                },
                "business_context": "质量数据分析",
            },
            {
                "id": "MFG004",
                "category": "质量管理",
                "difficulty": "高",
                "instruction": "从检测设备导出测量数据，与质量标准进行比对，标记超差产品并通知生产线",
                "expected": {
                    "steps": 4,
                    "software": ["检测设备", "质量系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "在线质量监控",
            },
            {
                "id": "MFG005",
                "category": "库存管理",
                "difficulty": "中",
                "instruction": "从WMS系统导出库存清单，与盘点记录进行比对，生成盘点差异报告",
                "expected": {
                    "steps": 3,
                    "software": ["WMS系统"],
                    "data_flow": True,
                    "confidence": 0.8,
                },
                "business_context": "库存盘点核对",
            },
            {
                "id": "MFG006",
                "category": "库存管理",
                "difficulty": "中",
                "instruction": "从ERP系统获取物料需求计划，从WMS查询库存，生成采购申请单",
                "expected": {
                    "steps": 3,
                    "software": ["ERP系统", "WMS系统"],
                    "data_flow": True,
                    "confidence": 0.8,
                },
                "business_context": "物料采购申请",
            },
            {
                "id": "MFG007",
                "category": "设备管理",
                "difficulty": "中",
                "instruction": "从设备监控系统获取运行数据，分析设备利用率，生成设备维护计划",
                "expected": {
                    "steps": 3,
                    "software": ["设备监控系统"],
                    "confidence": 0.8,
                },
                "business_context": "设备维护管理",
            },
            {
                "id": "MFG008",
                "category": "设备管理",
                "difficulty": "高",
                "instruction": "从传感器采集设备温度数据，判断是否超过阈值，如果超标则发送报警邮件",
                "expected": {
                    "steps": 3,
                    "software": ["传感器系统", "邮件"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "设备异常监控",
            },
            {
                "id": "MFG009",
                "category": "供应链",
                "difficulty": "高",
                "instruction": "从SRM系统获取供应商交货记录，评估供应商绩效，更新供应商评级",
                "expected": {
                    "steps": 3,
                    "software": ["SRM系统"],
                    "confidence": 0.75,
                },
                "business_context": "供应商绩效评估",
            },
            {
                "id": "MFG010",
                "category": "供应链",
                "difficulty": "中",
                "instruction": "从采购系统导出采购订单，从物流系统获取在途信息，更新到货预期",
                "expected": {
                    "steps": 3,
                    "software": ["采购系统", "物流系统"],
                    "data_flow": True,
                    "confidence": 0.8,
                },
                "business_context": "采购到货跟踪",
            },
            {
                "id": "MFG011",
                "category": "工艺管理",
                "difficulty": "中",
                "instruction": "从PLM系统导出工艺路线，从MES获取实际工时数据，优化工艺参数",
                "expected": {
                    "steps": 3,
                    "software": ["PLM系统", "MES系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "工艺参数优化",
            },
            {
                "id": "MFG012",
                "category": "成本管理",
                "difficulty": "高",
                "instruction": "从财务系统获取原材料成本，从MES获取消耗数据，计算产品成本差异",
                "expected": {
                    "steps": 3,
                    "software": ["财务系统", "MES系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "产品成本核算",
            },
            {
                "id": "MFG013",
                "category": "追溯管理",
                "difficulty": "高",
                "instruction": "从MES系统导出生产批次记录，从质量系统获取检验数据，建立产品追溯档案",
                "expected": {
                    "steps": 3,
                    "software": ["MES系统", "质量系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "产品追溯管理",
            },
            {
                "id": "MFG014",
                "category": "能耗管理",
                "difficulty": "中",
                "instruction": "从能耗监测系统导出用电数据，分析能耗趋势，生成节能建议报告",
                "expected": {
                    "steps": 3,
                    "software": ["能耗监测系统"],
                    "confidence": 0.8,
                },
                "business_context": "能源消耗分析",
            },
            {
                "id": "MFG015",
                "category": "报表管理",
                "difficulty": "中",
                "instruction": "从MES系统导出生产日报，从ERP获取销售数据，生成经营分析报表",
                "expected": {
                    "steps": 3,
                    "software": ["MES系统", "ERP系统"],
                    "data_flow": True,
                    "confidence": 0.8,
                },
                "business_context": "经营数据汇总",
            },
        ],
    },
    
    # ═══════════════════════════════════════════════════════════
    # 电商行业（15个典型任务）
    # ═══════════════════════════════════════════════════════════
    "ecommerce": {
        "name": "电商行业",
        "icon": "🛒",
        "test_cases": [
            {
                "id": "ECM001",
                "category": "订单处理",
                "difficulty": "中",
                "instruction": "从电商平台导出今日订单，按地区分类统计，生成发货计划",
                "expected": {
                    "steps": 3,
                    "software": ["电商平台"],
                    "confidence": 0.8,
                },
                "business_context": "订单统计分类",
            },
            {
                "id": "ECM002",
                "category": "订单处理",
                "difficulty": "高",
                "instruction": "从淘宝导出订单，从京东导出订单，合并到ERP系统中统一处理",
                "expected": {
                    "steps": 3,
                    "software": ["淘宝", "京东", "ERP系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "多平台订单整合",
            },
            {
                "id": "ECM003",
                "category": "订单处理",
                "difficulty": "高",
                "instruction": "从OMS系统获取待发货订单，从WMS查询库存，如果库存不足则生成采购申请",
                "expected": {
                    "steps": 3,
                    "software": ["OMS系统", "WMS系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "订单库存匹配",
            },
            {
                "id": "ECM004",
                "category": "商品管理",
                "difficulty": "中",
                "instruction": "从ERP系统导出新商品资料，批量上传到淘宝店铺，设置商品属性",
                "expected": {
                    "steps": 3,
                    "software": ["ERP系统", "淘宝"],
                    "confidence": 0.8,
                },
                "business_context": "商品批量上架",
            },
            {
                "id": "ECM005",
                "category": "商品管理",
                "difficulty": "中",
                "instruction": "从竞品监控系统获取价格数据，与本店价格比对，生成调价建议",
                "expected": {
                    "steps": 3,
                    "software": ["竞品监控系统"],
                    "confidence": 0.8,
                },
                "business_context": "竞品价格分析",
            },
            {
                "id": "ECM006",
                "category": "价格管理",
                "difficulty": "中",
                "instruction": "从促销系统获取活动价格，批量更新到电商平台，设置生效时间",
                "expected": {
                    "steps": 3,
                    "software": ["促销系统", "电商平台"],
                    "data_flow": True,
                    "confidence": 0.8,
                },
                "business_context": "促销价格设置",
            },
            {
                "id": "ECM007",
                "category": "价格管理",
                "difficulty": "高",
                "instruction": "从多个电商平台导出商品价格，对比价格差异，统一调整价格策略",
                "expected": {
                    "steps": 3,
                    "software": ["电商平台"],
                    "confidence": 0.75,
                },
                "business_context": "多平台价格同步",
            },
            {
                "id": "ECM008",
                "category": "客户服务",
                "difficulty": "中",
                "instruction": "从客服系统导出咨询记录，统计常见问题，生成客服FAQ文档",
                "expected": {
                    "steps": 3,
                    "software": ["客服系统"],
                    "confidence": 0.8,
                },
                "business_context": "客服知识库建设",
            },
            {
                "id": "ECM009",
                "category": "客户服务",
                "difficulty": "高",
                "instruction": "从评价系统导出差评记录，分析差评原因，生成改进建议报告",
                "expected": {
                    "steps": 3,
                    "software": ["评价系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "差评分析改进",
            },
            {
                "id": "ECM010",
                "category": "客户服务",
                "difficulty": "中",
                "instruction": "从售后系统导出退货申请，审核退货原因，更新库存并处理退款",
                "expected": {
                    "steps": 4,
                    "software": ["售后系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "退货处理流程",
            },
            {
                "id": "ECM011",
                "category": "营销活动",
                "difficulty": "高",
                "instruction": "从营销系统导出优惠券使用数据，分析转化率，优化优惠券策略",
                "expected": {
                    "steps": 3,
                    "software": ["营销系统"],
                    "confidence": 0.75,
                },
                "business_context": "营销效果分析",
            },
            {
                "id": "ECM012",
                "category": "营销活动",
                "difficulty": "中",
                "instruction": "从CRM系统筛选目标客户，批量发送促销短信，统计发送结果",
                "expected": {
                    "steps": 3,
                    "software": ["CRM系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "精准营销推送",
            },
            {
                "id": "ECM013",
                "category": "数据分析",
                "difficulty": "高",
                "instruction": "从电商平台导出销售数据，从流量系统获取访问数据，分析转化漏斗",
                "expected": {
                    "steps": 3,
                    "software": ["电商平台", "流量系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                },
                "business_context": "销售转化分析",
            },
            {
                "id": "ECM014",
                "category": "数据分析",
                "difficulty": "中",
                "instruction": "从BI系统导出月度销售报表，生成数据可视化图表，发送给管理层",
                "expected": {
                    "steps": 3,
                    "software": ["BI系统", "邮件"],
                    "confidence": 0.8,
                },
                "business_context": "经营数据汇报",
            },
            {
                "id": "ECM015",
                "category": "库存管理",
                "difficulty": "高",
                "instruction": "从WMS系统导出库存预警商品，自动生成补货计划，提交采购审批",
                "expected": {
                    "steps": 3,
                    "software": ["WMS系统"],
                    "risks": True,
                    "confidence": 0.75,
                },
                "business_context": "智能补货管理",
            },
        ],
    },
}


# ═══════════════════════════════════════════════════════════════
# 测试执行函数
# ═══════════════════════════════════════════════════════════════

def run_industry_tests(industry_key=None):
    """运行行业测试"""
    
    config = Config()
    parser = AIDrivenIntentParser(config)
    
    # 选择要测试的行业
    if industry_key:
        industries = {industry_key: INDUSTRY_TEST_CASES[industry_key]}
    else:
        industries = INDUSTRY_TEST_CASES
    
    all_results = {}
    
    for industry_key, industry_data in industries.items():
        print("\n" + "="*70)
        print(f"  {industry_data['icon']} {industry_data['name']}测试")
        print("="*70)
        
        results = []
        
        for test_case in industry_data['test_cases']:
            print(f"\n[{test_case['id']}] {test_case['category']} - {test_case['difficulty']}")
            print(f"任务: {test_case['instruction'][:60]}...")
            
            # 解析任务
            result = parser.parse(test_case['instruction'])
            
            # 评估结果
            actual_steps = len(result.get('steps', []))
            actual_confidence = result.get('confidence', 0)
            actual_software = result.get('software', [])
            has_data_flow = bool(result.get('data_flow'))
            has_risks = bool(result.get('risks'))
            
            # 计算得分
            expected = test_case['expected']
            checks = []
            
            # 步骤数检查
            steps_ok = actual_steps >= expected.get('steps', 1)
            checks.append(("步骤数", steps_ok, f"{actual_steps}/{expected.get('steps', '?')}"))
            
            # 置信度检查
            conf_ok = actual_confidence >= expected.get('confidence', 0.7)
            checks.append(("置信度", conf_ok, f"{actual_confidence:.2f}/{expected.get('confidence', 0.7):.2f}"))
            
            # 软件识别检查
            if 'software' in expected:
                software_ok = all(s in actual_software for s in expected['software'])
                checks.append(("软件识别", software_ok, f"{actual_software}"))
            
            # 数据流检查
            if expected.get('data_flow'):
                checks.append(("数据流", has_data_flow, "有" if has_data_flow else "无"))
            
            # 风险评估检查
            if expected.get('risks'):
                checks.append(("风险评估", has_risks, "有" if has_risks else "无"))
            
            # 计算总分
            passed_count = sum(1 for _, passed, _ in checks if passed)
            score = int((passed_count / len(checks)) * 100) if checks else 0
            
            # 显示结果
            print(f"  评估结果:")
            for check_name, passed, detail in checks:
                print(f"    - {check_name}: {detail} {'✓' if passed else '✗'}")
            print(f"  得分: {score}/100 {'✓' if score >= 70 else '✗'}")
            
            results.append({
                "id": test_case['id'],
                "category": test_case['category'],
                "instruction": test_case['instruction'],
                "expected": expected,
                "actual": {
                    "steps": actual_steps,
                    "confidence": actual_confidence,
                    "software": actual_software,
                    "has_data_flow": has_data_flow,
                    "has_risks": has_risks,
                },
                "checks": checks,
                "score": score,
                "passed": score >= 70,
            })
        
        # 统计结果
        passed = sum(1 for r in results if r['passed'])
        total = len(results)
        avg_score = sum(r['score'] for r in results) / total if total > 0 else 0
        
        print(f"\n{industry_data['name']}测试结果:")
        print(f"  通过率: {passed}/{total} ({passed/total*100:.1f}%)")
        print(f"  平均分: {avg_score:.1f}/100")
        
        all_results[industry_key] = {
            "industry": industry_data['name'],
            "total": total,
            "passed": passed,
            "avg_score": avg_score,
            "results": results,
        }
    
    return all_results


def generate_summary_report(all_results):
    """生成汇总报告"""
    print("\n\n" + "="*70)
    print("  行业测试汇总报告")
    print("="*70 + "\n")
    
    for industry_key, data in all_results.items():
        status = "✓" if data['avg_score'] >= 80 else "⚠"
        print(f"{status} {data['industry']}: {data['passed']}/{data['total']} 通过, 平均分 {data['avg_score']:.1f}")
    
    # 总体统计
    total_cases = sum(d['total'] for d in all_results.values())
    total_passed = sum(d['passed'] for d in all_results.values())
    overall_avg = sum(d['avg_score'] for d in all_results.values()) / len(all_results)
    
    print(f"\n总计: {total_passed}/{total_cases} ({total_passed/total_cases*100:.1f}%)")
    print(f"平均分: {overall_avg:.1f}/100")
    
    if overall_avg >= 85:
        level = "⭐⭐⭐⭐⭐ 企业级就绪"
    elif overall_avg >= 75:
        level = "⭐⭐⭐⭐ 优秀"
    elif overall_avg >= 65:
        level = "⭐⭐⭐ 良好"
    else:
        level = "⭐⭐ 需优化"
    
    print(f"成熟度: {level}")


# ═══════════════════════════════════════════════════════════════
# 导出测试用例（供审阅）
# ═══════════════════════════════════════════════════════════════

def export_test_cases_for_review():
    """导出测试用例供审阅"""
    print("\n" + "="*70)
    print("  行业测试用例清单（供审阅）")
    print("="*70 + "\n")
    
    for industry_key, industry_data in INDUSTRY_TEST_CASES.items():
        print(f"\n{industry_data['icon']} {industry_data['name']} ({len(industry_data['test_cases'])}个用例)\n")
        print("-" * 70)
        
        for i, test_case in enumerate(industry_data['test_cases'], 1):
            print(f"\n{i}. [{test_case['id']}] {test_case['category']} ({test_case['difficulty']})")
            print(f"   任务: {test_case['instruction']}")
            print(f"   业务场景: {test_case['business_context']}")
            print(f"   预期:")
            print(f"     - 步骤数: {test_case['expected'].get('steps', '?')}")
            print(f"     - 软件: {', '.join(test_case['expected'].get('software', []))}")
            print(f"     - 置信度: {test_case['expected'].get('confidence', 0.7):.2f}")
            if test_case['expected'].get('data_flow'):
                print(f"     - 数据流: 需要")
            if test_case['expected'].get('risks'):
                print(f"     - 风险评估: 需要")


# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--review":
            # 仅导出测试用例供审阅
            export_test_cases_for_review()
        elif sys.argv[1] in ["finance", "manufacturing", "ecommerce"]:
            # 测试特定行业
            results = run_industry_tests(sys.argv[1])
            generate_summary_report(results)
    else:
        # 运行所有测试
        results = run_industry_tests()
        generate_summary_report(results)
