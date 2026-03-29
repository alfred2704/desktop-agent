"""
完整的失败处理和改进机制
演示L5验证反馈层 + L6知识记忆层的协作
"""

import sys
from pathlib import Path
import time
import json
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from core.config import Config

# ═══════════════════════════════════════════════════════════════
# L5 验证反馈层 - 失败处理器
# ═══════════════════════════════════════════════════════════════

class FailureHandler:
    """失败处理器 - L5验证反馈层"""
    
    def __init__(self):
        self.max_retries = 3
        self.retry_count = 0
        self.failure_history = []
    
    def handle_failure(self, task_info: dict, error: Exception) -> dict:
        """
        处理执行失败
        
        Args:
            task_info: 任务信息
            error: 错误信息
        
        Returns:
            {
                "action": "retry|abort|ask_user",
                "suggestions": [...],
                "improvement_plan": {...},
            }
        """
        result = {
            "action": "abort",
            "suggestions": [],
            "improvement_plan": {},
            "retry_count": self.retry_count,
        }
        
        # 记录失败
        failure_record = {
            "timestamp": datetime.now().isoformat(),
            "task": task_info.get("task"),
            "error": str(error),
            "retry_count": self.retry_count,
        }
        self.failure_history.append(failure_record)
        
        # 分析失败原因
        failure_analysis = self._analyze_failure(error)
        
        print("\n" + "="*70)
        print("  【L5 验证反馈层】失败分析")
        print("="*70)
        print()
        
        print(f"任务: {task_info.get('task')}")
        print(f"错误: {str(error)}")
        print(f"重试次数: {self.retry_count}/{self.max_retries}")
        print()
        
        print("失败原因分析:")
        for i, reason in enumerate(failure_analysis["reasons"], 1):
            print(f"  {i}. {reason}")
        print()
        
        # 生成改进建议
        suggestions = self._generate_suggestions(failure_analysis)
        
        print("改进建议:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        print()
        
        # 决定下一步行动
        if self.retry_count < self.max_retries:
            # 尝试自动改进
            improvement_plan = self._create_improvement_plan(failure_analysis)
            
            if improvement_plan["auto_fixable"]:
                result["action"] = "retry"
                result["improvement_plan"] = improvement_plan
                self.retry_count += 1
                
                print("决策: 自动重试（改进策略）")
                print(f"改进方案: {improvement_plan['description']}")
                print()
            else:
                result["action"] = "ask_user"
                result["suggestions"] = suggestions
                
                print("决策: 需要用户介入")
                print()
        else:
            result["action"] = "abort"
            result["suggestions"] = suggestions
            
            print("决策: 超过最大重试次数，中止任务")
            print()
        
        return result
    
    def _analyze_failure(self, error: Exception) -> dict:
        """分析失败原因"""
        error_str = str(error).lower()
        
        analysis = {
            "reasons": [],
            "type": "unknown",
            "auto_fixable": False,
        }
        
        # 分析错误类型
        if "未找到" in error_str or "not found" in error_str:
            analysis["reasons"].append("目标窗口未找到")
            analysis["reasons"].append("应用可能未运行")
            analysis["reasons"].append("窗口标题可能已改变")
            analysis["type"] = "window_not_found"
            analysis["auto_fixable"] = True  # 可以尝试启动应用
            
        elif "超时" in error_str or "timeout" in error_str:
            analysis["reasons"].append("操作超时")
            analysis["reasons"].append("系统响应慢")
            analysis["reasons"].append("应用可能卡死")
            analysis["type"] = "timeout"
            analysis["auto_fixable"] = True  # 可以增加超时时间
            
        elif "权限" in error_str or "permission" in error_str:
            analysis["reasons"].append("权限不足")
            analysis["reasons"].append("需要管理员权限")
            analysis["type"] = "permission_denied"
            analysis["auto_fixable"] = False  # 需要用户手动授权
            
        elif "元素" in error_str or "element" in error_str:
            analysis["reasons"].append("UI元素未找到")
            analysis["reasons"].append("界面可能已变化")
            analysis["reasons"].append("需要重新感知屏幕")
            analysis["type"] = "element_not_found"
            analysis["auto_fixable"] = True  # 可以重新扫描
        
        else:
            analysis["reasons"].append("未知错误")
            analysis["reasons"].append("需要人工分析")
        
        return analysis
    
    def _generate_suggestions(self, failure_analysis: dict) -> list:
        """生成改进建议"""
        suggestions = []
        
        failure_type = failure_analysis["type"]
        
        if failure_type == "window_not_found":
            suggestions.append("启动目标应用")
            suggestions.append("检查应用是否正确安装")
            suggestions.append("尝试使用不同的窗口标题匹配策略")
            suggestions.append("检查应用是否最小化到系统托盘")
            
        elif failure_type == "timeout":
            suggestions.append("增加操作超时时间")
            suggestions.append("检查系统性能")
            suggestions.append("关闭其他占用资源的程序")
            
        elif failure_type == "permission_denied":
            suggestions.append("以管理员身份运行")
            suggestions.append("检查用户权限设置")
            suggestions.append("修改安全策略")
            
        elif failure_type == "element_not_found":
            suggestions.append("重新扫描屏幕")
            suggestions.append("等待界面加载完成")
            suggestions.append("使用OCR作为备选方案")
        
        return suggestions
    
    def _create_improvement_plan(self, failure_analysis: dict) -> dict:
        """创建改进计划"""
        plan = {
            "auto_fixable": False,
            "description": "",
            "actions": [],
        }
        
        failure_type = failure_analysis["type"]
        
        if failure_type == "window_not_found":
            plan["auto_fixable"] = True
            plan["description"] = "尝试启动应用或使用模糊匹配"
            plan["actions"] = [
                "启动目标应用",
                "使用模糊匹配查找窗口",
                "检查进程列表",
            ]
            
        elif failure_type == "timeout":
            plan["auto_fixable"] = True
            plan["description"] = "增加超时时间并重试"
            plan["actions"] = [
                "将超时时间增加50%",
                "添加等待间隔",
            ]
            
        elif failure_type == "element_not_found":
            plan["auto_fixable"] = True
            plan["description"] = "重新感知屏幕并更新元素定位"
            plan["actions"] = [
                "重新扫描屏幕",
                "使用OCR作为备选",
                "降低匹配阈值",
            ]
        
        return plan


# ═══════════════════════════════════════════════════════════════
# L6 知识记忆层 - 经验学习器
# ═══════════════════════════════════════════════════════════════

class ExperienceLearner:
    """经验学习器 - L6知识记忆层"""
    
    def __init__(self):
        self.experience_db = []
        self.knowledge_file = "task_experience.json"
        self._load_experience()
    
    def _load_experience(self):
        """加载历史经验"""
        try:
            if Path(self.knowledge_file).exists():
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    self.experience_db = json.load(f)
        except:
            self.experience_db = []
    
    def record_experience(self, task_info: dict, result: dict):
        """记录执行经验"""
        experience = {
            "timestamp": datetime.now().isoformat(),
            "task": task_info.get("task"),
            "success": result.get("success", False),
            "strategy": task_info.get("strategy"),
            "error": result.get("error"),
            "solution": result.get("solution"),
            "retry_count": result.get("retry_count", 0),
        }
        
        self.experience_db.append(experience)
        self._save_experience()
        
        print("\n" + "="*70)
        print("  【L6 知识记忆层】经验记录")
        print("="*70)
        print()
        
        print(f"任务: {experience['task']}")
        print(f"结果: {'成功' if experience['success'] else '失败'}")
        print(f"策略: {experience['strategy']}")
        if experience.get('error'):
            print(f"错误: {experience['error']}")
        if experience.get('solution'):
            print(f"解决方案: {experience['solution']}")
        print(f"重试次数: {experience['retry_count']}")
        print()
        
        # 分析模式
        self._analyze_patterns()
    
    def _save_experience(self):
        """保存经验到文件"""
        try:
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.experience_db[-100:], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存经验失败: {e}")
    
    def _analyze_patterns(self):
        """分析失败模式"""
        if len(self.experience_db) < 3:
            return
        
        # 统计最近的失败率
        recent = self.experience_db[-10:]
        failure_rate = sum(1 for e in recent if not e.get("success")) / len(recent)
        
        print("经验分析:")
        print(f"  最近10次任务失败率: {failure_rate*100:.1f}%")
        
        if failure_rate > 0.5:
            print("  [!] 警告: 失败率较高，需要优化策略")
        
        print()
    
    def get_similar_experience(self, task_info: dict) -> dict:
        """查询相似任务的经验"""
        task_type = task_info.get("task_type")
        
        # 查找相似的成功案例
        similar = [
            e for e in self.experience_db
            if e.get("task") == task_info.get("task") and e.get("success")
        ]
        
        if similar:
            latest = similar[-1]
            return {
                "found": True,
                "strategy": latest.get("strategy"),
                "solution": latest.get("solution"),
            }
        
        return {"found": False}


# ═══════════════════════════════════════════════════════════════
# 完整的任务执行器（带反馈机制）
# ═══════════════════════════════════════════════════════════════

class SmartTaskExecutor:
    """智能任务执行器 - 集成L5和L6"""
    
    def __init__(self):
        self.config = Config()
        self.perceiver = ScreenPerceiver(self.config)
        self.failure_handler = FailureHandler()
        self.experience_learner = ExperienceLearner()
    
    def execute_with_feedback(self, task_description: str):
        """执行任务（带完整反馈机制）"""
        
        print("="*70)
        print(f"  智能任务执行: {task_description}")
        print("="*70)
        print()
        
        task_info = {
            "task": task_description,
            "task_type": "click_window",
            "strategy": "ai_driven",
        }
        
        # 查询历史经验
        similar_exp = self.experience_learner.get_similar_experience(task_info)
        if similar_exp["found"]:
            print("[L6] 找到相似的成功经验:")
            print(f"  策略: {similar_exp['strategy']}")
            print(f"  解决方案: {similar_exp['solution']}")
            print()
        
        # 执行任务
        try:
            result = self._execute_task(task_info)
            
            # 成功
            result["success"] = True
            self.experience_learner.record_experience(task_info, result)
            
            print("[OK] 任务执行成功!")
            return result
            
        except Exception as e:
            # 失败
            result = {
                "success": False,
                "error": str(e),
            }
            
            # L5: 处理失败
            feedback = self.failure_handler.handle_failure(task_info, e)
            
            # 根据反馈决策
            if feedback["action"] == "retry":
                print(f"\n[L5] 尝试改进后重试... (第{feedback['retry_count']}次)")
                print()
                
                # 执行改进计划
                improvement_plan = feedback["improvement_plan"]
                for action in improvement_plan["actions"]:
                    print(f"  执行: {action}")
                print()
                
                # 递归重试
                return self.execute_with_feedback(task_description)
            
            elif feedback["action"] == "ask_user":
                print("\n[L5] 需要用户介入:")
                print()
                for i, suggestion in enumerate(feedback["suggestions"], 1):
                    print(f"  建议{i}: {suggestion}")
                print()
                
                # 记录失败经验
                result["retry_count"] = feedback["retry_count"]
                self.experience_learner.record_experience(task_info, result)
                
                return result
            
            else:  # abort
                print("\n[L5] 任务中止")
                print()
                
                # 记录失败经验
                result["retry_count"] = feedback["retry_count"]
                self.experience_learner.record_experience(task_info, result)
                
                return result
    
    def _execute_task(self, task_info: dict) -> dict:
        """执行具体任务"""
        task = task_info["task"]
        
        # 示例: 点击窗口
        if "点击" in task and "豆包" in task:
            return self._click_window("豆包")
        
        raise Exception(f"未找到豆包窗口")
    
    def _click_window(self, window_title: str) -> dict:
        """点击窗口"""
        # 查找窗口
        found_windows = self.perceiver.find_window_by_title(window_title)
        
        if not found_windows:
            raise Exception(f"未找到标题包含'{window_title}'的窗口")
        
        # 获取窗口信息
        window = found_windows[0]["window"]
        
        # 计算点击位置
        left, top, right, bottom = window['rect']
        click_x = (left + right) // 2
        click_y = (top + bottom) // 2
        
        # 执行点击
        import pyautogui
        pyautogui.click(click_x, click_y)
        
        return {
            "clicked": True,
            "position": (click_x, click_y),
            "window": window["title"],
        }


# ═══════════════════════════════════════════════════════════════
# 演示完整的反馈机制
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    executor = SmartTaskExecutor()
    
    # 执行任务
    result = executor.execute_with_feedback("点击豆包")
    
    print("="*70)
    print("  最终结果")
    print("="*70)
    print()
    
    if result.get("success"):
        print("[OK] 任务成功完成!")
    else:
        print("[X] 任务失败")
        print(f"原因: {result.get('error')}")
        print(f"重试次数: {result.get('retry_count', 0)}")
    
    print()
