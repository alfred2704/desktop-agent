"""
第3层：操作规划层 - 动作规划器
根据意图生成操作序列
"""

from typing import Dict, Any, List
from loguru import logger


class ActionPlanner:
    """动作规划器"""
    
    def __init__(self, config, knowledge_query):
        self.config = config
        self.knowledge_query = knowledge_query
    
    def plan(self, intent: Dict, screen_state: Dict) -> Dict[str, Any]:
        """
        规划操作序列
        
        Args:
            intent: 解析后的意图
            screen_state: 屏幕状态
        
        Returns:
            {
                "success": True,
                "actions": [...],
                "method": "template/reasoning"
            }
        """
        intent_type = intent.get("intent")
        params = intent.get("params", {})
        
        actions = []
        
        # 根据意图类型生成动作
        if intent_type == "click":
            actions = self._plan_click(params, screen_state)
        
        elif intent_type == "double_click":
            actions = self._plan_double_click(params, screen_state)
        
        elif intent_type == "type":
            actions = self._plan_type(params, screen_state)
        
        elif intent_type == "hotkey":
            actions = self._plan_hotkey(params)
        
        elif intent_type == "menu":
            actions = self._plan_menu(params, screen_state)
        
        elif intent_type == "scroll":
            actions = self._plan_scroll(params)
        
        elif intent_type == "wait":
            actions = self._plan_wait(params, screen_state)
        
        elif intent_type == "find":
            actions = self._plan_find(params, screen_state)
        
        else:
            # 未知意图，尝试用AI推理
            if self.config.AI_ENABLED:
                actions = self._plan_with_ai(intent, screen_state)
        
        return {
            "success": len(actions) > 0,
            "actions": actions,
            "method": "template" if intent_type != "unknown" else "ai",
        }
    
    def _plan_click(self, params: Dict, screen_state: Dict) -> List[Dict]:
        """规划点击操作"""
        target = params.get("target")
        
        return [{
            "type": "click",
            "target": target,
            "aliases": params.get("aliases", []),
            "description": f"点击 {target}",
        }]
    
    def _plan_double_click(self, params: Dict, screen_state: Dict) -> List[Dict]:
        """规划双击操作"""
        target = params.get("target")
        
        return [{
            "type": "double_click",
            "target": target,
            "description": f"双击 {target}",
        }]
    
    def _plan_type(self, params: Dict, screen_state: Dict) -> List[Dict]:
        """规划输入操作"""
        element = params.get("element")
        text = params.get("text")
        
        actions = []
        
        # 如果指定了元素，先点击
        if element:
            actions.append({
                "type": "click",
                "target": element,
                "description": f"点击 {element}",
            })
        
        # 输入文本
        actions.append({
            "type": "type",
            "text": text,
            "clear_first": True,
            "description": f"输入 {text}",
        })
        
        return actions
    
    def _plan_hotkey(self, params: Dict) -> List[Dict]:
        """规划快捷键操作"""
        keys = params.get("keys", [])
        
        return [{
            "type": "hotkey",
            "keys": keys,
            "description": f"快捷键 {'+'.join(keys)}",
        }]
    
    def _plan_menu(self, params: Dict, screen_state: Dict) -> List[Dict]:
        """规划菜单操作"""
        menu_path = params.get("menu_path", [])
        
        actions = []
        
        for i, menu_item in enumerate(menu_path):
            actions.append({
                "type": "click",
                "target": menu_item,
                "description": f"点击菜单 {menu_item}",
                "delay": 0.3 if i > 0 else 0,
            })
        
        return actions
    
    def _plan_scroll(self, params: Dict) -> List[Dict]:
        """规划滚动操作"""
        direction = params.get("direction", "down")
        amount = params.get("amount", 3)
        
        return [{
            "type": "scroll",
            "direction": direction,
            "amount": amount,
            "description": f"向{direction}滚动 {amount} 次",
        }]
    
    def _plan_wait(self, params: Dict, screen_state: Dict) -> List[Dict]:
        """规划等待操作"""
        target = params.get("target")
        timeout = params.get("timeout", 10)
        
        return [{
            "type": "wait",
            "target": target,
            "timeout": timeout,
            "description": f"等待 {target} 出现",
        }]
    
    def _plan_find(self, params: Dict, screen_state: Dict) -> List[Dict]:
        """规划查找操作（只查找不操作）"""
        target = params.get("target")
        
        return [{
            "type": "find",
            "target": target,
            "description": f"查找 {target}",
        }]
    
    def _plan_with_ai(self, intent: Dict, screen_state: Dict) -> List[Dict]:
        """使用AI推理操作序列"""
        # TODO: 实现AI推理
        logger.warning("AI推理操作序列功能待实现")
        return []
