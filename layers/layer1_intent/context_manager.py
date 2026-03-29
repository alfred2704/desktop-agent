"""
第1层：意图理解层 - 上下文管理器
管理对话上下文和状态
"""

from typing import Dict, Any, List
from collections import deque
import time


class ContextManager:
    """上下文管理器"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        
        # 对话历史
        self.conversation_history = deque(maxlen=max_history)
        
        # 当前状态
        self.current_state = {
            "active_window": None,
            "last_action": None,
            "last_element": None,
            "variables": {},
        }
        
        # 用户偏好
        self.user_preferences = {}
    
    def update(self, context: Dict[str, Any]):
        """更新上下文"""
        if context:
            self.conversation_history.append({
                "timestamp": time.time(),
                "context": context
            })
            
            # 更新当前状态
            if "active_window" in context:
                self.current_state["active_window"] = context["active_window"]
            
            if "variables" in context:
                self.current_state["variables"].update(context["variables"])
    
    def get(self) -> Dict[str, Any]:
        """获取当前上下文"""
        return {
            "state": self.current_state.copy(),
            "history": list(self.conversation_history),
            "preferences": self.user_preferences.copy(),
        }
    
    def set_variable(self, key: str, value: Any):
        """设置变量"""
        self.current_state["variables"][key] = value
    
    def get_variable(self, key: str) -> Any:
        """获取变量"""
        return self.current_state["variables"].get(key)
    
    def set_last_action(self, action: Dict):
        """记录上一次动作"""
        self.current_state["last_action"] = action
    
    def set_last_element(self, element: Dict):
        """记录上一次操作的元素"""
        self.current_state["last_element"] = element
    
    def clear(self):
        """清空上下文"""
        self.conversation_history.clear()
        self.current_state = {
            "active_window": None,
            "last_action": None,
            "last_element": None,
            "variables": {},
        }
