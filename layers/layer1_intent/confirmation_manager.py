"""
第1层：意图理解层 - 交互确认管理器
处理需要确认的复杂操作
"""

from typing import Dict, Any, List
from loguru import logger


class ConfirmationManager:
    """交互确认管理器"""
    
    def __init__(self, config):
        self.config = config
        
        # 确认历史（学习用户习惯）
        self.confirmation_history = []
        
        # 用户偏好（记录常见选择）
        self.user_preferences = {}
    
    def needs_confirmation(self, intent: Dict) -> bool:
        """判断是否需要确认"""
        
        # 1. 置信度低
        if intent.get("confidence", 0) < 0.7:
            return True
        
        # 2. 明确标记需要确认
        if intent.get("needs_confirmation", False):
            return True
        
        # 3. 涉及重要操作
        dangerous_actions = ["删除", "清空", "格式化", "关闭所有"]
        instruction = intent.get("instruction", "")
        if any(action in instruction for action in dangerous_actions):
            return True
        
        # 4. 目标不明确
        params = intent.get("params", {})
        if intent["intent"] == "click" and not params.get("target"):
            return True
        
        return False
    
    def create_confirmation(self, intent: Dict) -> Dict[str, Any]:
        """创建确认请求"""
        
        confirmation_type = self._determine_confirmation_type(intent)
        
        if confirmation_type == "ambiguous_target":
            return self._create_target_confirmation(intent)
        
        elif confirmation_type == "dangerous_action":
            return self._create_danger_confirmation(intent)
        
        elif confirmation_type == "multiple_matches":
            return self._create_multiple_matches_confirmation(intent)
        
        else:
            return self._create_general_confirmation(intent)
    
    def _determine_confirmation_type(self, intent: Dict) -> str:
        """确定确认类型"""
        
        instruction = intent.get("instruction", "")
        params = intent.get("params", {})
        
        # 目标模糊
        if intent["intent"] in ["click", "type"] and not params.get("target"):
            return "ambiguous_target"
        
        # 危险操作
        dangerous_keywords = ["删除", "清空", "格式化", "关闭所有"]
        if any(kw in instruction for kw in dangerous_keywords):
            return "dangerous_action"
        
        # 多个匹配
        if params.get("matches") and len(params["matches"]) > 1:
            return "multiple_matches"
        
        return "general"
    
    def _create_target_confirmation(self, intent: Dict) -> Dict:
        """创建目标确认"""
        
        return {
            "type": "target_selection",
            "message": "请选择要操作的目标：",
            "intent": intent,
            "options": [
                {
                    "id": 1,
                    "description": "确定按钮",
                    "action": {"intent": "click", "params": {"target": "确定"}}
                },
                {
                    "id": 2,
                    "description": "取消按钮",
                    "action": {"intent": "click", "params": {"target": "取消"}}
                },
                {
                    "id": 3,
                    "description": "手动选择",
                    "action": {"intent": "manual_select"}
                },
            ],
            "allow_custom": True,
            "custom_prompt": "请输入目标名称：",
        }
    
    def _create_danger_confirmation(self, intent: Dict) -> Dict:
        """创建危险操作确认"""
        
        return {
            "type": "danger_confirmation",
            "message": f"⚠️ 这是一个危险操作，是否继续？",
            "intent": intent,
            "warning": f"您即将执行：{intent.get('instruction', '')}",
            "options": [
                {
                    "id": 1,
                    "description": "确认执行",
                    "action": intent
                },
                {
                    "id": 2,
                    "description": "取消",
                    "action": {"intent": "cancel"}
                },
            ],
        }
    
    def _create_multiple_matches_confirmation(self, intent: Dict) -> Dict:
        """创建多匹配确认"""
        
        matches = intent.get("params", {}).get("matches", [])
        
        options = []
        for i, match in enumerate(matches[:5], 1):
            options.append({
                "id": i,
                "description": f"{match.get('name', '未知')} (位置: {match.get('center', (0,0))})",
                "action": {
                    "intent": intent["intent"],
                    "params": {**intent["params"], "target": match}
                }
            })
        
        return {
            "type": "multiple_selection",
            "message": f"找到 {len(matches)} 个匹配项，请选择：",
            "intent": intent,
            "options": options,
        }
    
    def _create_general_confirmation(self, intent: Dict) -> Dict:
        """创建通用确认"""
        
        return {
            "type": "general_confirmation",
            "message": "请确认您的操作：",
            "intent": intent,
            "understanding": intent.get("understanding", "未知操作"),
            "options": [
                {
                    "id": 1,
                    "description": "确认执行",
                    "action": intent
                },
                {
                    "id": 2,
                    "description": "重新描述",
                    "action": {"intent": "retry"}
                },
                {
                    "id": 3,
                    "description": "取消",
                    "action": {"intent": "cancel"}
                },
            ],
        }
    
    def record_choice(self, confirmation_id: str, choice_id: int, intent: Dict):
        """记录用户选择（用于学习）"""
        
        self.confirmation_history.append({
            "confirmation_id": confirmation_id,
            "choice_id": choice_id,
            "intent": intent,
        })
        
        # 学习用户偏好
        # 例如：如果用户总是选择"确定"而不是"确认"
        # 可以记录这个偏好，下次自动选择
    
    def get_user_preference(self, context: str) -> Dict:
        """获取用户偏好"""
        return self.user_preferences.get(context, {})
