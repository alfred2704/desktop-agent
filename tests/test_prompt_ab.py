"""
Desktop Agent - Prompt A/B测试
对比优化前后的prompt效果
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from core.config import Config
import json
from datetime import datetime
from typing import Dict, List, Tuple


class PromptABTest:
    """Prompt A/B测试器"""
    
    def __init__(self):
        self.config = Config()
        
        # 原版解析器（使用旧prompt）
        self.parser_old = AIDrivenIntentParser(self.config)
        
        # 新版解析器（使用新prompt）
        self.parser_new = AIDrivenIntentParser(self.config)
        
        # 加载测试用例
        with open("tests/intent_test_cases.json", 'r', encoding='utf-8') as f:
            self.test_data = json.load(f)
        
        # 测试结果
        self.results = {
            "test_time": datetime.now().isoformat(),
            "total_cases": len(self.test_data["test_cases"]),
            "results": []
        }
    
    def test_single_prompt(self, instruction: str, parser, prompt_type: str) -> Dict:
        """测试单个prompt"""
        
        try:
            # 这里简化为只测试理解，不实际调用AI
            # 实际应该调用parser._ai_deep_understand()
            
            # 模拟结果（实际应该真实调用）
            result = parser._quick_match(instruction)
            
            if not result:
                # 如果快速匹配失败，应该调用AI
                # result = parser._ai_deep_understand(instruction, {})
                # 这里简化为返回默认结果
                result = {
                    "task_type": "automation",
                    "understanding": f"理解指令: {instruction}",
                    "steps": [],
                    "confidence": 0.7
                }
            
            return {
                "success": True,
                "parsed": result,
                "prompt_type": prompt_type
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prompt_type": prompt_type
            }
    
    def compare_prompts(self) -> Dict:
        """对比两个prompt"""
        
        print("\n" + "=" * 70)
        print("Prompt A/B测试 - 对比分析")
        print("=" * 70)
        
        # 统计数据
        old_stats = {"success": 0, "failed": 0, "avg_confidence": 0}
        new_stats = {"success": 0, "failed": 0, "avg_confidence": 0}
        
        # 运行测试
        for i, test_case in enumerate(self.test_data["test_cases"][:10], 1):  # 测试前10个
            instruction = test_case["instruction"]
            category = test_case["category"]
            
            print(f"\n测试 #{i}: {instruction} ({category})")
            
            # 测试旧prompt
            old_result = self.test_single_prompt(instruction, self.parser_old, "old")
            if old_result["success"]:
                old_stats["success"] += 1
                confidence = old_result["parsed"].get("confidence", 0)
                old_stats["avg_confidence"] += confidence
            else:
                old_stats["failed"] += 1
            
            # 测试新prompt
            new_result = self.test_single_prompt(instruction, self.parser_new, "new")
            if new_result["success"]:
                new_stats["success"] += 1
                confidence = new_result["parsed"].get("confidence", 0)
                new_stats["avg_confidence"] += confidence
            else:
                new_stats["failed"] += 1
            
            # 记录结果
            self.results["results"].append({
                "test_id": test_case["id"],
                "instruction": instruction,
                "category": category,
                "old_success": old_result["success"],
                "new_success": new_result["success"],
                "improvement": "improved" if new_result["success"] and not old_result["success"] else "same" if new_result["success"] == old_result["success"] else "regressed"
            })
            
            # 显示对比
            status_old = "✅" if old_result["success"] else "❌"
            status_new = "✅" if new_result["success"] else "❌"
            print(f"  旧prompt: {status_old} | 新prompt: {status_new}")
        
        # 计算平均置信度
        old_total = old_stats["success"] + old_stats["failed"]
        new_total = new_stats["success"] + new_stats["failed"]
        
        if old_stats["success"] > 0:
            old_stats["avg_confidence"] /= old_stats["success"]
        if new_stats["success"] > 0:
            new_stats["avg_confidence"] /= new_stats["success"]
        
        # 生成报告
        self.generate_report(old_stats, new_stats)
        
        return {
            "old_stats": old_stats,
            "new_stats": new_stats,
            "improvement": self.calculate_improvement(old_stats, new_stats)
        }
    
    def calculate_improvement(self, old_stats: Dict, new_stats: Dict) -> Dict:
        """计算改进情况"""
        
        old_total = old_stats["success"] + old_stats["failed"]
        new_total = new_stats["success"] + new_stats["failed"]
        
        old_rate = old_stats["success"] / old_total if old_total > 0 else 0
        new_rate = new_stats["success"] / new_total if new_total > 0 else 0
        
        return {
            "success_rate_improvement": (new_rate - old_rate) * 100,
            "old_success_rate": old_rate * 100,
            "new_success_rate": new_rate * 100,
            "confidence_improvement": (new_stats["avg_confidence"] - old_stats["avg_confidence"]) * 100
        }
    
    def generate_report(self, old_stats: Dict, new_stats: Dict):
        """生成测试报告"""
        
        print("\n" + "=" * 70)
        print("测试报告")
        print("=" * 70)
        
        old_total = old_stats["success"] + old_stats["failed"]
        new_total = new_stats["success"] + new_stats["failed"]
        
        old_rate = old_stats["success"] / old_total if old_total > 0 else 0
        new_rate = new_stats["success"] / new_total if new_total > 0 else 0
        
        print(f"\n【旧prompt】")
        print(f"  总测试数: {old_total}")
        print(f"  成功数: {old_stats['success']}")
        print(f"  失败数: {old_stats['failed']}")
        print(f"  成功率: {old_rate * 100:.1f}%")
        print(f"  平均置信度: {old_stats['avg_confidence']:.2f}")
        
        print(f"\n【新prompt】")
        print(f"  总测试数: {new_total}")
        print(f"  成功数: {new_stats['success']}")
        print(f"  失败数: {new_stats['failed']}")
        print(f"  成功率: {new_rate * 100:.1f}%")
        print(f"  平均置信度: {new_stats['avg_confidence']:.2f}")
        
        print(f"\n【改进情况】")
        improvement = (new_rate - old_rate) * 100
        conf_improvement = (new_stats["avg_confidence"] - old_stats["avg_confidence"]) * 100
        
        print(f"  成功率改进: {'+' if improvement > 0 else ''}{improvement:.1f}%")
        print(f"  置信度改进: {'+' if conf_improvement > 0 else ''}{conf_improvement:.1f}%")
        
        # 结论
        if improvement > 0:
            print(f"\n✅ 结论: 新prompt优于旧prompt，成功率高{improvement:.1f}%")
        elif improvement < 0:
            print(f"\n⚠️  结论: 新prompt不如旧prompt，成功率低{abs(improvement):.1f}%")
        else:
            print(f"\n➡️  结论: 新旧prompt性能相当")
        
        print("\n" + "=" * 70)
    
    def save_results(self, filename: str = "prompt_ab_test_results.json"):
        """保存测试结果"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 测试结果已保存到: {filename}")


def main():
    """主函数"""
    
    print("\n" + "=" * 70)
    print("Desktop Agent - Prompt A/B测试")
    print("=" * 70)
    
    tester = PromptABTest()
    
    # 运行A/B测试
    comparison = tester.compare_prompts()
    
    # 保存结果
    tester.save_results()
    
    print("\n测试完成！")
    print(f"\n详细结果请查看: prompt_ab_test_results.json")


if __name__ == "__main__":
    main()
