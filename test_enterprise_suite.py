"""
企业级意图理解测试套件
覆盖5大维度：准确性、完整性、鲁棒性、适应性、性能
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from core.config import Config

# ═══════════════════════════════════════════════════════════════
# 测试套件配置
# ═══════════════════════════════════════════════════════════════

class EnterpriseTestSuite:
    """企业级测试套件"""
    
    def __init__(self):
        self.config = Config()
        self.parser = AIDrivenIntentParser(self.config)
        self.results = {
            "accuracy": [],      # 准确性测试
            "completeness": [],  # 完整性测试
            "robustness": [],    # 鲁棒性测试
            "adaptability": [],  # 适应性测试
            "performance": [],   # 性能测试
        }
        self.start_time = datetime.now()
    
    # ═══════════════════════════════════════════════════════════
    # 1. 准确性测试（30%）
    # ═══════════════════════════════════════════════════════════
    
    def test_accuracy(self):
        """测试意图识别准确性"""
        print("\n" + "="*70)
        print("  维度1：准确性测试（权重30%）")
        print("="*70 + "\n")
        
        test_cases = [
            # 基础操作
            {
                "category": "基础操作",
                "instruction": "打开记事本",
                "expected_intent": "open_app",
                "expected_confidence": 0.8,
            },
            {
                "category": "基础操作",
                "instruction": "点击确定按钮",
                "expected_intent": "click",
                "expected_confidence": 0.9,
            },
            {
                "category": "基础操作",
                "instruction": "输入'Hello World'",
                "expected_intent": "type",
                "expected_confidence": 0.9,
            },
            
            # 文档处理
            {
                "category": "文档处理",
                "instruction": "打开Word，写一份报告，保存为'月报.docx'",
                "expected_intent": "document_workflow",
                "expected_steps": 3,
                "expected_confidence": 0.75,
            },
            {
                "category": "文档处理",
                "instruction": "从Excel复制数据，粘贴到Word文档",
                "expected_intent": "data_transfer",
                "expected_steps": 2,
                "expected_confidence": 0.75,
            },
            
            # 沟通协作
            {
                "category": "沟通协作",
                "instruction": "打开企业微信，发消息给张三说'明天开会'",
                "expected_intent": "send_message",
                "expected_steps": 2,
                "expected_confidence": 0.8,
            },
            {
                "category": "沟通协作",
                "instruction": "通过邮件发送Excel报表给老板",
                "expected_intent": "send_email",
                "expected_steps": 2,
                "expected_confidence": 0.75,
            },
            
            # 数据处理
            {
                "category": "数据处理",
                "instruction": "从数据库导出数据到Excel",
                "expected_intent": "data_export",
                "expected_steps": 2,
                "expected_confidence": 0.75,
            },
            {
                "category": "数据处理",
                "instruction": "将CSV文件转换为Excel格式",
                "expected_intent": "file_conversion",
                "expected_steps": 2,
                "expected_confidence": 0.8,
            },
            
            # 财务对账
            {
                "category": "财务对账",
                "instruction": "登录工商银行网银下载流水",
                "expected_intent": "bank_operation",
                "expected_steps": 2,
                "expected_confidence": 0.75,
            },
            {
                "category": "财务对账",
                "instruction": "将银行流水与ERP收款记录核对",
                "expected_intent": "reconciliation",
                "expected_steps": 3,
                "expected_confidence": 0.7,
            },
            
            # 系统管理
            {
                "category": "系统管理",
                "instruction": "备份C盘重要文件到D盘",
                "expected_intent": "file_backup",
                "expected_steps": 2,
                "expected_confidence": 0.75,
            },
            {
                "category": "系统管理",
                "instruction": "清理系统临时文件",
                "expected_intent": "system_cleanup",
                "expected_steps": 1,
                "expected_confidence": 0.8,
            },
        ]
        
        for test in test_cases:
            print(f"\n[{test['category']}] {test['instruction']}")
            
            result = self.parser.parse(test['instruction'])
            
            # 评估准确性
            actual_intent = result.get('task_type', 'unknown')
            actual_confidence = result.get('confidence', 0)
            steps_count = len(result.get('steps', []))
            
            # 计算得分
            intent_match = actual_intent == test.get('expected_intent') or \
                          test.get('expected_intent') in actual_intent.lower()
            
            confidence_pass = actual_confidence >= test.get('expected_confidence', 0.7)
            steps_pass = steps_count >= test.get('expected_steps', 1)
            
            score = 0
            if intent_match:
                score += 40
            if confidence_pass:
                score += 30
            if steps_pass:
                score += 30
            
            status = "✓" if score >= 70 else "✗"
            
            print(f"  意图: {actual_intent} {'✓' if intent_match else '✗'}")
            print(f"  置信度: {actual_confidence:.2f} {'✓' if confidence_pass else '✗'}")
            print(f"  步骤数: {steps_count} {'✓' if steps_pass else '✗'}")
            print(f"  得分: {score}/100 {status}")
            
            self.results["accuracy"].append({
                "category": test["category"],
                "instruction": test["instruction"],
                "expected_intent": test.get("expected_intent"),
                "actual_intent": actual_intent,
                "expected_confidence": test.get("expected_confidence", 0.7),
                "actual_confidence": actual_confidence,
                "score": score,
                "passed": score >= 70,
            })
    
    # ═══════════════════════════════════════════════════════════
    # 2. 完整性测试（25%）
    # ═══════════════════════════════════════════════════════════
    
    def test_completeness(self):
        """测试步骤分解完整性"""
        print("\n" + "="*70)
        print("  维度2：完整性测试（权重25%）")
        print("="*70 + "\n")
        
        test_cases = [
            {
                "name": "跨软件数据流转",
                "instruction": "从Excel复制客户名单，粘贴到邮件，发送给销售团队",
                "expected_components": {
                    "steps": 3,
                    "software": ["Excel", "邮件"],
                    "data_flow": True,
                    "dependencies": True,
                }
            },
            {
                "name": "多步骤工作流",
                "instruction": "打开Photoshop，处理图片，保存为PNG，上传到云盘",
                "expected_components": {
                    "steps": 4,
                    "software": ["Photoshop", "云盘"],
                    "data_flow": True,
                }
            },
            {
                "name": "条件分支任务",
                "instruction": "如果文件存在就打开，否则创建新文件",
                "expected_components": {
                    "steps": 2,
                    "has_condition": True,
                }
            },
            {
                "name": "循环处理任务",
                "instruction": "遍历文件夹中的所有Excel文件，提取数据并汇总",
                "expected_components": {
                    "steps": 3,
                    "has_loop": True,
                }
            },
            {
                "name": "复杂企业任务",
                "instruction": "登录ERP系统，导出销售报表，与财务系统数据核对，生成差异报告",
                "expected_components": {
                    "steps": 4,
                    "software": ["ERP", "财务系统"],
                    "data_flow": True,
                    "risks": True,
                }
            },
        ]
        
        for test in test_cases:
            print(f"\n[{test['name']}]")
            print(f"  任务: {test['instruction']}")
            
            result = self.parser.parse(test['instruction'])
            
            # 检查完整性
            expected = test['expected_components']
            checks = []
            
            # 检查步骤数
            if 'steps' in expected:
                actual_steps = len(result.get('steps', []))
                steps_ok = actual_steps >= expected['steps']
                checks.append(("步骤数", steps_ok, f"{actual_steps}/{expected['steps']}"))
            
            # 检查软件识别
            if 'software' in expected:
                actual_software = result.get('software', [])
                software_ok = all(s in actual_software for s in expected['software'])
                checks.append(("软件识别", software_ok, f"{actual_software}"))
            
            # 检查数据流
            if expected.get('data_flow'):
                has_data_flow = bool(result.get('data_flow'))
                checks.append(("数据流", has_data_flow, "有" if has_data_flow else "无"))
            
            # 检查条件分支
            if expected.get('has_condition'):
                has_condition = any('if' in str(s).lower() for s in result.get('steps', []))
                checks.append(("条件分支", has_condition, "有" if has_condition else "无"))
            
            # 检查循环
            if expected.get('has_loop'):
                has_loop = 'repeat' in str(result).lower() or 'loop' in str(result).lower()
                checks.append(("循环结构", has_loop, "有" if has_loop else "无"))
            
            # 检查风险评估
            if expected.get('risks'):
                has_risks = bool(result.get('risks'))
                checks.append(("风险评估", has_risks, f"{len(result.get('risks', []))}个风险"))
            
            # 计算得分
            passed_count = sum(1 for _, passed, _ in checks if passed)
            score = int((passed_count / len(checks)) * 100) if checks else 0
            
            print(f"  完整性检查:")
            for check_name, passed, detail in checks:
                print(f"    - {check_name}: {detail} {'✓' if passed else '✗'}")
            print(f"  得分: {score}/100 {'✓' if score >= 70 else '✗'}")
            
            self.results["completeness"].append({
                "name": test["name"],
                "instruction": test["instruction"],
                "checks": checks,
                "score": score,
                "passed": score >= 70,
            })
    
    # ═══════════════════════════════════════════════════════════
    # 3. 鲁棒性测试（20%）
    # ═══════════════════════════════════════════════════════════
    
    def test_robustness(self):
        """测试异常场景处理能力"""
        print("\n" + "="*70)
        print("  维度3：鲁棒性测试（权重20%）")
        print("="*70 + "\n")
        
        test_cases = [
            {
                "name": "模糊描述",
                "instruction": "帮我处理一下那个文件",
                "should_ask_clarification": True,
            },
            {
                "name": "信息缺失",
                "instruction": "发送邮件",
                "should_ask_clarification": True,
            },
            {
                "name": "矛盾指令",
                "instruction": "打开不存在的文件并保存",
                "should_detect_risk": True,
            },
            {
                "name": "超长指令",
                "instruction": "打开" + "A" * 500 + "文件",
                "should_handle_gracefully": True,
            },
            {
                "name": "多语言混合",
                "instruction": "Open the Excel and 导出数据 to PDF",
                "should_understand": True,
            },
            {
                "name": "口语化表达",
                "instruction": "那个啥，把表里的东西弄到邮件里发出去",
                "should_understand": True,
            },
            {
                "name": "错别字",
                "instruction": "打楷Excel并保存",
                "should_understand": True,
            },
            {
                "name": "危险操作",
                "instruction": "删除所有文件",
                "should_detect_risk": True,
            },
        ]
        
        for test in test_cases:
            print(f"\n[{test['name']}]")
            print(f"  输入: {test['instruction'][:50]}...")
            
            try:
                result = self.parser.parse(test['instruction'])
                
                # 检查处理情况
                checks = []
                
                if test.get('should_ask_clarification'):
                    needs_confirm = result.get('needs_confirmation', False)
                    checks.append(("请求确认", needs_confirm))
                
                if test.get('should_detect_risk'):
                    has_risks = bool(result.get('risks'))
                    checks.append(("风险检测", has_risks))
                
                if test.get('should_handle_gracefully'):
                    has_result = result is not None and 'task_type' in result
                    checks.append(("优雅处理", has_result))
                
                if test.get('should_understand'):
                    confidence = result.get('confidence', 0)
                    checks.append(("理解成功", confidence > 0.5))
                
                # 计算得分
                passed_count = sum(1 for _, passed in checks if passed)
                score = int((passed_count / len(checks)) * 100) if checks else 100
                
                print(f"  鲁棒性检查:")
                for check_name, passed in checks:
                    print(f"    - {check_name}: {'✓' if passed else '✗'}")
                print(f"  得分: {score}/100 {'✓' if score >= 70 else '✗'}")
                
                self.results["robustness"].append({
                    "name": test["name"],
                    "instruction": test["instruction"],
                    "checks": checks,
                    "score": score,
                    "passed": score >= 70,
                })
                
            except Exception as e:
                print(f"  ✗ 异常: {str(e)}")
                self.results["robustness"].append({
                    "name": test["name"],
                    "instruction": test["instruction"],
                    "error": str(e),
                    "score": 0,
                    "passed": False,
                })
    
    # ═══════════════════════════════════════════════════════════
    # 4. 适应性测试（15%）
    # ═══════════════════════════════════════════════════════════
    
    def test_adaptability(self):
        """测试新场景适应能力"""
        print("\n" + "="*70)
        print("  维度4：适应性测试（权重15%）")
        print("="*70 + "\n")
        
        # 这些是系统可能没见过的新场景
        test_cases = [
            {
                "name": "新软件-Notion",
                "instruction": "在Notion中创建新页面，添加待办事项列表",
                "expected_steps": 2,
            },
            {
                "name": "新场景-直播",
                "instruction": "打开OBS，开始直播，录制视频",
                "expected_steps": 3,
            },
            {
                "name": "新领域-AI绘画",
                "instruction": "打开Midjourney，输入提示词生成图片",
                "expected_steps": 2,
            },
            {
                "name": "新工作流-自动化测试",
                "instruction": "运行Selenium测试脚本，收集测试结果，生成报告",
                "expected_steps": 3,
            },
            {
                "name": "新业务-客户管理",
                "instruction": "在CRM系统中添加新客户，设置跟进提醒",
                "expected_steps": 2,
            },
        ]
        
        for test in test_cases:
            print(f"\n[{test['name']}]")
            print(f"  任务: {test['instruction']}")
            
            result = self.parser.parse(test['instruction'])
            
            # 评估适应性
            actual_steps = len(result.get('steps', []))
            confidence = result.get('confidence', 0)
            
            steps_ok = actual_steps >= test['expected_steps']
            confidence_ok = confidence >= 0.6
            
            score = 0
            if steps_ok:
                score += 50
            if confidence_ok:
                score += 50
            
            print(f"  步骤数: {actual_steps}/{test['expected_steps']} {'✓' if steps_ok else '✗'}")
            print(f"  置信度: {confidence:.2f} {'✓' if confidence_ok else '✗'}")
            print(f"  得分: {score}/100 {'✓' if score >= 70 else '✗'}")
            
            self.results["adaptability"].append({
                "name": test["name"],
                "instruction": test["instruction"],
                "actual_steps": actual_steps,
                "expected_steps": test["expected_steps"],
                "confidence": confidence,
                "score": score,
                "passed": score >= 70,
            })
    
    # ═══════════════════════════════════════════════════════════
    # 5. 性能测试（10%）
    # ═══════════════════════════════════════════════════════════
    
    def test_performance(self):
        """测试响应性能"""
        print("\n" + "="*70)
        print("  维度5：性能测试（权重10%）")
        print("="*70 + "\n")
        
        test_cases = [
            "打开记事本",
            "点击确定按钮",
            "输入'Hello World'",
            "打开Excel，处理数据，保存文件",
            "登录银行系统，下载流水，与ERP数据核对",
        ]
        
        response_times = []
        
        for instruction in test_cases:
            print(f"\n任务: {instruction[:40]}...")
            
            start = time.time()
            result = self.parser.parse(instruction)
            elapsed = time.time() - start
            
            response_times.append(elapsed)
            
            # 性能标准
            if elapsed < 1.0:
                grade = "优秀"
                score = 100
            elif elapsed < 2.0:
                grade = "良好"
                score = 80
            elif elapsed < 3.0:
                grade = "合格"
                score = 60
            else:
                grade = "需优化"
                score = 40
            
            print(f"  响应时间: {elapsed:.2f}s")
            print(f"  性能评级: {grade}")
            
            self.results["performance"].append({
                "instruction": instruction,
                "response_time": elapsed,
                "grade": grade,
                "score": score,
                "passed": score >= 60,
            })
        
        # 统计
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        print(f"\n性能统计:")
        print(f"  平均响应时间: {avg_time:.2f}s")
        print(f"  最快响应: {min_time:.2f}s")
        print(f"  最慢响应: {max_time:.2f}s")
    
    # ═══════════════════════════════════════════════════════════
    # 生成报告
    # ═══════════════════════════════════════════════════════════
    
    def generate_report(self):
        """生成测试报告"""
        print("\n\n")
        print("="*70)
        print("  企业级测试报告")
        print("="*70)
        print(f"测试时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试工具: AI驱动意图理解层 v1.0")
        print("="*70 + "\n")
        
        # 各维度得分
        dimensions = [
            ("准确性", "accuracy", 30),
            ("完整性", "completeness", 25),
            ("鲁棒性", "robustness", 20),
            ("适应性", "adaptability", 15),
            ("性能", "performance", 10),
        ]
        
        total_weighted_score = 0
        total_weight = 0
        
        print("【各维度得分】\n")
        for name, key, weight in dimensions:
            results = self.results[key]
            if results:
                passed = sum(1 for r in results if r.get('passed'))
                total = len(results)
                pass_rate = (passed / total) * 100 if total > 0 else 0
                
                avg_score = sum(r.get('score', 0) for r in results) / total if total > 0 else 0
                
                weighted_score = (avg_score / 100) * weight
                total_weighted_score += weighted_score
                total_weight += weight
                
                print(f"{name}（权重{weight}%）:")
                print(f"  通过率: {passed}/{total} ({pass_rate:.1f}%)")
                print(f"  平均分: {avg_score:.1f}/100")
                print(f"  加权分: {weighted_score:.2f}/{weight}")
                print()
        
        # 总分
        final_score = (total_weighted_score / total_weight) * 100 if total_weight > 0 else 0
        
        print("="*70)
        print(f"【综合评分】{final_score:.1f}/100")
        print("="*70)
        
        if final_score >= 90:
            level = "⭐⭐⭐⭐⭐ 生产就绪"
        elif final_score >= 80:
            level = "⭐⭐⭐⭐ 优秀"
        elif final_score >= 70:
            level = "⭐⭐⭐ 良好"
        elif final_score >= 60:
            level = "⭐⭐ 合格"
        else:
            level = "⭐ 需改进"
        
        print(f"成熟度评级: {level}")
        print()
        
        # 建议
        print("【改进建议】\n")
        
        if final_score < 90:
            for name, key, _ in dimensions:
                results = self.results[key]
                if results:
                    failed = [r for r in results if not r.get('passed')]
                    if failed:
                        print(f"- {name}: 有{len(failed)}个测试用例未通过，需要优化")
        
        print()
        
        # 保存报告
        report_data = {
            "timestamp": self.start_time.isoformat(),
            "dimensions": {},
            "final_score": final_score,
            "level": level,
        }
        
        for name, key, weight in dimensions:
            results = self.results[key]
            if results:
                report_data["dimensions"][key] = {
                    "name": name,
                    "weight": weight,
                    "total": len(results),
                    "passed": sum(1 for r in results if r.get('passed')),
                    "avg_score": sum(r.get('score', 0) for r in results) / len(results),
                    "details": results,
                }
        
        # 保存到文件
        report_file = Path(__file__).parent / "test_reports" / f"enterprise_test_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"详细报告已保存: {report_file}")
        print()
        
        return final_score
    
    # ═══════════════════════════════════════════════════════════
    # 运行所有测试
    # ═══════════════════════════════════════════════════════════
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n")
        print("╔" + "═"*68 + "╗")
        print("║" + " "*15 + "企业级意图理解层测试套件" + " "*27 + "║")
        print("║" + " "*68 + "║")
        print("║  测试维度: 准确性 | 完整性 | 鲁棒性 | 适应性 | 性能" + " "*11 + "║")
        print("╚" + "═"*68 + "╝")
        
        try:
            self.test_accuracy()
            self.test_completeness()
            self.test_robustness()
            self.test_adaptability()
            self.test_performance()
            
            return self.generate_report()
            
        except KeyboardInterrupt:
            print("\n\n测试被用户中断")
            return None
        except Exception as e:
            print(f"\n\n测试过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    suite = EnterpriseTestSuite()
    final_score = suite.run_all_tests()
    
    if final_score is not None:
        print("\n测试完成！")
        if final_score >= 80:
            print("✅ 系统已达到企业级应用标准")
        else:
            print("⚠️  系统需要进一步优化")
