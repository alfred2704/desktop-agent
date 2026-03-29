"""
第1层：意图理解层 - 复杂任务分解器
将复杂任务分解为简单步骤
"""

from typing import Dict, Any, List
import json
import re
from loguru import logger


class TaskDecomposer:
    """复杂任务分解器"""
    
    def __init__(self, config):
        self.config = config
        
        # 任务模板库
        self.task_templates = {
            # 文件操作模板
            "打开文件": [
                {"action": "hotkey", "keys": ["ctrl", "o"]},
                {"action": "type", "text": "{filename}"},
                {"action": "key", "key": "enter"},
            ],
            
            "保存文件": [
                {"action": "hotkey", "keys": ["ctrl", "s"]},
            ],
            
            "另存为": [
                {"action": "hotkey", "keys": ["ctrl", "shift", "s"]},
                {"action": "type", "text": "{filename}"},
                {"action": "key", "key": "enter"},
            ],
            
            # 查找替换模板
            "查找并替换": [
                {"action": "hotkey", "keys": ["ctrl", "h"]},
                {"action": "type", "element": "查找内容", "text": "{find_text}"},
                {"action": "type", "element": "替换为", "text": "{replace_text}"},
                {"action": "click", "target": "全部替换"},
            ],
            
            # Excel操作模板
            "Excel筛选": [
                {"action": "click", "target": "列标题"},
                {"action": "hotkey", "keys": ["ctrl", "shift", "l"]},
            ],
            
            # 邮件操作模板
            "发送邮件": [
                {"action": "click", "target": "新建邮件"},
                {"action": "type", "element": "收件人", "text": "{recipient}"},
                {"action": "type", "element": "主题", "text": "{subject}"},
                {"action": "type", "element": "正文", "text": "{content}"},
                {"action": "click", "target": "发送"},
            ],
        }
    
    def decompose(self, instruction: str, intent: Dict, context: Dict = None) -> Dict[str, Any]:
        """
        分解复杂任务
        
        Args:
            instruction: 原始指令
            intent: 意图解析结果
            context: 上下文
        
        Returns:
            {
                "success": True,
                "steps": [...],
                "method": "template/ai",
                "confidence": 0.9
            }
        """
        context = context or {}
        
        # 1. 尝试使用模板匹配
        steps = self._match_template(instruction, intent)
        if steps:
            return {
                "success": True,
                "steps": steps,
                "method": "template",
                "confidence": 0.95,
            }
        
        # 2. 使用AI分解
        if self.config.AI_ENABLED:
            steps = self._decompose_with_ai(instruction, intent, context)
            if steps:
                return {
                    "success": True,
                    "steps": steps,
                    "method": "ai",
                    "confidence": 0.8,
                }
        
        # 3. 无法分解
        return {
            "success": False,
            "steps": [],
            "error": "无法分解复杂任务",
        }
    
    def _match_template(self, instruction: str, intent: Dict) -> List[Dict]:
        """匹配任务模板"""
        
        instruction_lower = instruction.lower()
        
        # 查找替换
        if "查找" in instruction and "替换" in instruction:
            match = re.search(r"查找\s*['\"](.+?)['\"]\s*(?:并)?替换\s*(?:为|成)?\s*['\"](.+?)['\"]", instruction)
            if match:
                template = self.task_templates["查找并替换"]
                return self._fill_template(template, {
                    "find_text": match.group(1),
                    "replace_text": match.group(2),
                })
        
        # 打开文件
        if "打开文件" in instruction or "打开" in instruction and "文件" in instruction:
            match = re.search(r"打开\s*(?:文件)?\s*['\"](.+?)['\"]", instruction)
            if match:
                template = self.task_templates["打开文件"]
                return self._fill_template(template, {
                    "filename": match.group(1),
                })
        
        # 保存文件
        if "保存" in instruction and "另存" not in instruction:
            return self.task_templates["保存文件"]
        
        # 另存为
        if "另存为" in instruction or "保存为" in instruction:
            match = re.search(r"(?:另存为|保存为)\s*['\"](.+?)['\"]", instruction)
            if match:
                template = self.task_templates["另存为"]
                return self._fill_template(template, {
                    "filename": match.group(1),
                })
        
        return None
    
    def _fill_template(self, template: List[Dict], params: Dict) -> List[Dict]:
        """填充模板参数"""
        
        filled_steps = []
        
        for step in template:
            filled_step = step.copy()
            
            # 填充文本参数
            if "text" in filled_step:
                text = filled_step["text"]
                for key, value in params.items():
                    text = text.replace(f"{{{key}}}", value)
                filled_step["text"] = text
            
            filled_steps.append(filled_step)
        
        return filled_steps
    
    def _decompose_with_ai(self, instruction: str, intent: Dict, context: Dict) -> List[Dict]:
        """使用AI分解任务"""
        
        prompt = f"""你是一个任务分解专家。将复杂任务分解为简单步骤。

用户指令: "{instruction}"

请将任务分解为最小可执行步骤，返回JSON格式：

{{
    "steps": [
        {{
            "step": 1,
            "action": "click/type/hotkey/wait",
            "params": {{
                "target": "目标元素",
                "text": "输入文本",
                "keys": ["快捷键"],
                "duration": 等待时间
            }},
            "description": "步骤描述"
        }}
    ]
}}

分解原则：
1. 每个步骤只做一件事
2. 步骤顺序清晰
3. 参数明确具体
4. 避免模糊描述

只返回JSON，不要其他内容。
"""
        
        try:
            import requests
            
            response = requests.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config.ZHIPU_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.config.AI_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # 提取JSON
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    parsed = json.loads(json_match.group())
                    return parsed.get("steps", [])
        
        except Exception as e:
            logger.warning(f"AI任务分解失败: {e}")
        
        return None
