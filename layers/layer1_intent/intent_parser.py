"""
第1层：意图理解层 - 意图解析器
将自然语言指令解析为结构化意图
"""

from typing import Dict, Any, List
import re
import json
from loguru import logger


class IntentParser:
    """意图解析器"""
    
    def __init__(self, config):
        self.config = config
        
        # 意图模式（规则匹配）
        self.intent_patterns = {
            # 点击操作
            "click": [
                r"点击\s*(.+)",
                r"单击\s*(.+)",
                r"按\s*(.+)\s*按钮",
                r"选择\s*(.+)",
            ],
            "double_click": [
                r"双击\s*(.+)",
            ],
            "right_click": [
                r"右键\s*(.+)",
                r"右击\s*(.+)",
            ],
            
            # 输入操作
            "type": [
                r"在\s*(.+?)\s*输入\s*['\"](.+?)['\"]",
                r"在\s*(.+?)\s*填写\s*['\"](.+?)['\"]",
                r"输入\s*['\"](.+?)['\"]",
            ],
            
            # 快捷键
            "hotkey": [
                r"按\s*([A-Za-z+]+)",
                r"按下\s*([A-Za-z+]+)",
                r"快捷键\s*([A-Za-z+]+)",
            ],
            
            # 菜单
            "menu": [
                r"点击\s*(.+?)\s*菜单\s*(?:下\s*)?(?:的\s*)?(.+)",
                r"打开\s*(.+?)\s*菜单\s*(?:下\s*)?(?:的\s*)?(.+)",
            ],
            
            # 滚动
            "scroll": [
                r"向上\s*滚动",
                r"向下\s*滚动",
                r"上翻页",
                r"下翻页",
            ],
            
            # 等待
            "wait": [
                r"等待\s*(.+)",
                r"等到\s*(.+)\s*出现",
            ],
            
            # 查找
            "find": [
                r"查找\s*(.+)",
                r"寻找\s*(.+)",
            ],
        }
        
        # 快捷键别名
        self.hotkey_aliases = {
            "复制": ["ctrl", "c"],
            "粘贴": ["ctrl", "v"],
            "剪切": ["ctrl", "x"],
            "全选": ["ctrl", "a"],
            "撤销": ["ctrl", "z"],
            "保存": ["ctrl", "s"],
            "打开": ["ctrl", "o"],
            "新建": ["ctrl", "n"],
            "查找": ["ctrl", "f"],
            "关闭": ["ctrl", "w"],
            "刷新": ["f5"],
        }
    
    def parse(self, instruction: str, context: Dict = None) -> Dict[str, Any]:
        """
        解析自然语言指令
        
        Args:
            instruction: 自然语言指令
            context: 上下文
        
        Returns:
            {
                "intent": "click/type/hotkey/...",
                "target": "目标元素",
                "params": {...},
                "confidence": 0.9
            }
        """
        instruction = instruction.strip()
        context = context or {}
        
        # 尝试规则匹配
        result = self._parse_with_rules(instruction)
        
        if result:
            return result
        
        # 如果规则匹配失败，尝试AI解析
        if self.config.AI_ENABLED:
            result = self._parse_with_ai(instruction, context)
            if result:
                return result
        
        # 默认：未知意图
        return {
            "intent": "unknown",
            "instruction": instruction,
            "confidence": 0.0,
        }
    
    def _parse_with_rules(self, instruction: str) -> Dict[str, Any]:
        """使用规则匹配解析"""
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, instruction, re.IGNORECASE)
                if match:
                    params = self._extract_params(intent_type, match, instruction)
                    return {
                        "intent": intent_type,
                        "instruction": instruction,
                        "params": params,
                        "confidence": 0.9,
                        "method": "rules",
                    }
        
        return None
    
    def _extract_params(self, intent_type: str, match, instruction: str) -> Dict:
        """提取参数"""
        params = {}
        
        if intent_type == "click":
            params["target"] = match.group(1).strip()
            params["aliases"] = self._get_target_aliases(params["target"])
        
        elif intent_type == "double_click":
            params["target"] = match.group(1).strip()
            params["aliases"] = self._get_target_aliases(params["target"])
        
        elif intent_type == "right_click":
            params["target"] = match.group(1).strip()
        
        elif intent_type == "type":
            if match.lastindex >= 2:
                params["element"] = match.group(1).strip()
                params["text"] = match.group(2).strip()
            else:
                params["text"] = match.group(1).strip()
                params["element"] = None
        
        elif intent_type == "hotkey":
            key_combo = match.group(1).strip()
            # 检查是否是中文别名
            if key_combo in self.hotkey_aliases:
                params["keys"] = self.hotkey_aliases[key_combo]
            else:
                params["keys"] = [k.strip() for k in key_combo.split("+")]
        
        elif intent_type == "menu":
            params["menu_path"] = [match.group(1).strip(), match.group(2).strip()]
        
        elif intent_type == "scroll":
            direction = "up" if "上" in instruction else "down"
            params["direction"] = direction
            params["amount"] = 3
        
        elif intent_type == "wait":
            params["target"] = match.group(1).strip()
            params["timeout"] = 10
        
        elif intent_type == "find":
            params["target"] = match.group(1).strip()
        
        return params
    
    def _get_target_aliases(self, target: str) -> List[str]:
        """获取目标的可能别名"""
        aliases = [target]
        
        # 常见同义词
        synonym_map = {
            "确定": ["确定", "确认", "OK", "是", "Yes"],
            "取消": ["取消", "Cancel", "否", "No"],
            "保存": ["保存", "Save"],
            "关闭": ["关闭", "Close", "×"],
            "提交": ["提交", "Submit", "发送"],
        }
        
        for key, values in synonym_map.items():
            if target in values:
                aliases.extend(values)
                break
        
        return list(set(aliases))
    
    def _parse_with_ai(self, instruction: str, context: Dict) -> Dict[str, Any]:
        """使用AI解析"""
        try:
            import requests
            
            prompt = f"""
分析用户指令，返回JSON格式的意图分析结果。

用户指令: "{instruction}"
当前上下文: {json.dumps(context, ensure_ascii=False)}

返回格式:
{{
    "intent": "动作类型(click/type/hotkey/menu/scroll/wait/find)",
    "target": "主要目标",
    "params": {{
        "element": "目标元素",
        "text": "输入文本",
        "keys": ["快捷键"],
        "menu_path": ["菜单路径"]
    }},
    "confidence": 0.9
}}

只返回JSON，不要其他内容。
"""
            
            # 调用智谱AI
            if self.config.ZHIPU_API_KEY:
                response = requests.post(
                    "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.config.ZHIPU_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.config.AI_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": self.config.AI_TEMPERATURE
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # 提取JSON
                    json_match = re.search(r'\{[\s\S]*\}', content)
                    if json_match:
                        parsed = json.loads(json_match.group())
                        parsed["method"] = "ai"
                        return parsed
        
        except Exception as e:
            logger.warning(f"AI解析失败: {e}")
        
        return None
