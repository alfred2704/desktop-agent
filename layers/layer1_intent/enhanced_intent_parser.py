"""
第1层：意图理解层 - 增强版意图解析器
覆盖率目标：95%+
"""

from typing import Dict, Any, List, Tuple
import re
import json
from loguru import logger


class EnhancedIntentParser:
    """增强版意图解析器 - 多层策略"""
    
    def __init__(self, config):
        self.config = config
        
        # ═════════════════════════════════════════════════════════
        # 第1层：扩展的正则规则（覆盖45%）
        # ═════════════════════════════════════════════════════════
        
        self.intent_patterns = {
            # ─────────────────────────────────────────────────────
            # 1. 快捷键操作（优先级最高，避免被其他规则误匹配）
            # ─────────────────────────────────────────────────────
            "hotkey": [
                r"^按\s*([A-Za-z0-9+]+)\s*$",  # 纯快捷键，如"按Ctrl+S"
                r"^按下\s*([A-Za-z0-9+]+)\s*$",
                r"^快捷键\s*([A-Za-z0-9+]+)\s*$",
                r"^组合键\s*([A-Za-z0-9+]+)\s*$",
                # 中文别名
                r"^按\s*(复制|粘贴|剪切|全选|撤销|保存|打开|新建|查找|关闭|刷新|截图)\s*$",
            ],
            
            # ─────────────────────────────────────────────────────
            # 2. 相对定位操作（优先级高）
            # ─────────────────────────────────────────────────────
            "click_index": [
                r"点击\s*第\s*(\d+)\s*(.+)",
                r"单击\s*第\s*(\d+)\s*(.+)",
                r"选择\s*第\s*(\d+)\s*(.+)",
            ],
            "click_first": [
                r"点击\s*第一\s*个?\s*(.+)",
                r"单击\s*第一\s*个?\s*(.+)",
                r"选择\s*第一\s*个?\s*(.+)",
            ],
            "click_last": [
                r"点击\s*最后\s*(.+)",
                r"单击\s*最后\s*(.+)",
                r"选择\s*最后\s*(.+)",
            ],
            "click_all": [
                r"点击\s*所有\s*(.+)",
                r"点击\s*全部\s*(.+)",
                r"选择\s*所有\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 3. 循环操作（优先级高）
            # ─────────────────────────────────────────────────────
            "loop_times": [
                r"重复\s*(.+?)\s*(\d+)\s*次",
                r"连续\s*(.+?)\s*(\d+)\s*次",
                r"循环\s*(.+?)\s*(\d+)\s*次",
            ],
            "loop_until": [
                r"重复\s*(.+?)\s*直到\s*(.+)",
                r"一直\s*(.+?)\s*直到\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 4. 条件操作（优先级高）
            # ─────────────────────────────────────────────────────
            "if_exists": [
                r"如果\s*(.+?)\s*(?:存在|出现)?\s*(?:那么|就)?\s*(.+)",
                r"若\s*(.+?)\s*(?:存在|出现)?\s*(?:那么|就)?\s*(.+)",
            ],
            "if_not_exists": [
                r"如果\s*(.+?)\s*(?:不存在|没出现)?\s*(?:那么|就)?\s*(.+)",
                r"若\s*(.+?)\s*(?:不存在|没出现)?\s*(?:那么|就)?\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 5. 菜单操作
            # ─────────────────────────────────────────────────────
            "menu": [
                r"点击\s*(.+?)\s*菜单\s*(?:下\s*)?(?:的\s*)?(.+)",
                r"打开\s*(.+?)\s*菜单\s*(?:下\s*)?(?:的\s*)?(.+)",
                r"选择\s*(.+?)\s*[→>]\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 6. 基础点击操作（优先级较低）
            # ─────────────────────────────────────────────────────
            "click": [
                r"点击\s*(.+)",
                r"单击\s*(.+)",
                r"按\s*(.+)\s*按钮",
                r"选择\s*(.+)",
                r"按下\s*(.+)",
            ],
            "double_click": [
                r"双击\s*(.+)",
                r"连击\s*(.+)",
            ],
            "right_click": [
                r"右键\s*(.+)",
                r"右击\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 7. 输入操作
            # ─────────────────────────────────────────────────────
            "clear_type": [
                r"清空\s*(.+?)\s*(?:并)?输入\s*['\"](.+?)['\"]",
                r"删除\s*(.+?)\s*(?:后)?输入\s*['\"](.+?)['\"]",
            ],
            "type": [
                r"在\s*(.+?)\s*(?:中)?输入\s*['\"](.+?)['\"]",
                r"在\s*(.+?)\s*(?:中)?填写\s*['\"](.+?)['\"]",
                r"输入\s*['\"](.+?)['\"]",
                r"填写\s*['\"](.+?)['\"]",
                r"打字\s*['\"](.+?)['\"]",
            ],
            
            # ─────────────────────────────────────────────────────
            # 3. 快捷键操作
            # ─────────────────────────────────────────────────────
            "hotkey": [
                r"按\s*([A-Za-z0-9+]+)",
                r"按下\s*([A-Za-z0-9+]+)",
                r"快捷键\s*([A-Za-z0-9+]+)",
                r"组合键\s*([A-Za-z0-9+]+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 4. 菜单操作
            # ─────────────────────────────────────────────────────
            "menu": [
                r"点击\s*(.+?)\s*菜单\s*(?:下\s*)?(?:的\s*)?(.+)",
                r"打开\s*(.+?)\s*菜单\s*(?:下\s*)?(?:的\s*)?(.+)",
                r"选择\s*(.+?)\s*[→>]\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 8. 其他操作
            # ─────────────────────────────────────────────────────
            "scroll": [
                r"向\s*上\s*滚\s*动?\s*(\d+)?\s*次?",
                r"向\s*下\s*滚\s*动?\s*(\d+)?\s*次?",
                r"上\s*翻\s*页",
                r"下\s*翻\s*页",
                r"滚\s*动\s*到\s*(.+)",
                r"滚\s*动\s*到\s*最\s*(上|下|左|右)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 9. 等待操作
            # ─────────────────────────────────────────────────────
            "wait": [
                r"等待\s*(.+?)\s*(?:出现|加载)?",
                r"等到\s*(.+?)\s*(?:出现|加载)?",
                r"等\s*(\d+)\s*秒",
                r"暂停\s*(\d+)\s*秒",
            ],
            
            # ─────────────────────────────────────────────────────
            # 10. 查找操作
            # ─────────────────────────────────────────────────────
            "find": [
                r"查找\s*(.+)",
                r"寻找\s*(.+)",
                r"搜索\s*(.+)",
                r"定位\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 11. 拖拽操作
            # ─────────────────────────────────────────────────────
            "drag": [
                r"拖\s*动?\s*(.+?)\s*到\s*(.+)",
                r"拖拽\s*(.+?)\s*到\s*(.+)",
                r"移动\s*(.+?)\s*到\s*(.+)",
            ],
            
            # ─────────────────────────────────────────────────────
            # 12. 截图操作
            # ─────────────────────────────────────────────────────
            "screenshot": [
                r"截\s*图?",
                r"截屏",
                r"抓屏",
                r"保存\s*截图",
            ],
            
            # ─────────────────────────────────────────────────────
            # 13. 变量操作
            # ─────────────────────────────────────────────────────
            "set_variable": [
                r"记住\s*(.+?)\s*(?:是|为)\s*(.+)",
                r"设置\s*(.+?)\s*(?:为|是)\s*(.+)",
                r"把\s*(.+?)\s*(?:保存|存储)\s*(?:为|叫)\s*(.+)",
            ],
            "use_variable": [
                r"使用\s*(.+)",
                r"用\s*(.+)",
                r"输入\s*(.+?)\s*的值",
            ],
            
            # ─────────────────────────────────────────────────────
            # 14. 错误处理
            # ─────────────────────────────────────────────────────
            "retry": [
                r"重试\s*(\d+)?\s*次?",
                r"再试\s*(\d+)?\s*次?",
                r"如果\s*失败\s*(?:就)?\s*(.+)",
            ],
            "skip": [
                r"跳过\s*(.+)?",
                r"忽略\s*(.+)?",
                r"取消\s*(.+)?",
            ],
            
            # ─────────────────────────────────────────────────────
            # 15. 时间操作
            # ─────────────────────────────────────────────────────
            "schedule": [
                r"(\d+)\s*秒\s*后\s*(.+)",
                r"(\d+)\s*分钟\s*后\s*(.+)",
                r"定时\s*(.+)",
            ],
        }
        
        # 中文快捷键别名
        self.hotkey_aliases = {
            # 基础操作
            "复制": ["ctrl", "c"],
            "粘贴": ["ctrl", "v"],
            "剪切": ["ctrl", "x"],
            "全选": ["ctrl", "a"],
            "撤销": ["ctrl", "z"],
            "重做": ["ctrl", "y"],
            
            # 文件操作
            "保存": ["ctrl", "s"],
            "另存为": ["ctrl", "shift", "s"],
            "打开": ["ctrl", "o"],
            "新建": ["ctrl", "n"],
            "关闭": ["ctrl", "w"],
            
            # 编辑操作
            "查找": ["ctrl", "f"],
            "替换": ["ctrl", "h"],
            "定位": ["ctrl", "g"],
            
            # 浏览器操作
            "刷新": ["f5"],
            "强制刷新": ["ctrl", "f5"],
            "后退": ["alt", "left"],
            "前进": ["alt", "right"],
            
            # 系统操作
            "任务管理器": ["ctrl", "shift", "esc"],
            "锁屏": ["win", "l"],
            "运行": ["win", "r"],
            
            # Excel专用
            "筛选": ["ctrl", "shift", "l"],
            "插入行": ["ctrl", "shift", "+"],
            "删除行": ["ctrl", "-"],
            
            # 截图
            "截图": ["win", "shift", "s"],
            "全屏截图": ["printscreen"],
        }
    
    def parse(self, instruction: str, context: Dict = None) -> Dict[str, Any]:
        """
        多层策略解析
        
        第1层：规则匹配（快速、准确）→ 45%覆盖率
        第2层：AI理解（智能、灵活）→ 75%覆盖率
        第3层：交互确认（安全、可控）→ 95%覆盖率
        """
        instruction = instruction.strip()
        context = context or {}
        
        # ═══════════════════════════════════════════════════
        # 第1层：规则匹配（优先）
        # ═══════════════════════════════════════════════════
        result = self._parse_with_rules(instruction)
        if result and result.get('confidence', 0) >= 0.9:
            logger.info(f"[第1层] 规则匹配成功: {result['intent']}")
            return result
        
        # ═══════════════════════════════════════════════════
        # 第2层：AI理解（中等复杂度）
        # ═══════════════════════════════════════════════════
        if self.config.AI_ENABLED:
            result = self._parse_with_ai(instruction, context)
            if result and result.get('confidence', 0) >= 0.7:
                logger.info(f"[第2层] AI理解成功: {result['intent']}")
                return result
        
        # ═══════════════════════════════════════════════════
        # 第3层：交互确认（复杂操作）
        # ═══════════════════════════════════════════════════
        result = self._parse_with_confirmation(instruction, context)
        logger.info(f"[第3层] 需要确认: {result['intent']}")
        return result
    
    def _parse_with_rules(self, instruction: str) -> Dict[str, Any]:
        """使用扩展的规则匹配"""
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, instruction, re.IGNORECASE)
                if match:
                    params = self._extract_params(intent_type, match, instruction)
                    return {
                        "intent": intent_type,
                        "instruction": instruction,
                        "params": params,
                        "confidence": 0.95,
                        "method": "rules",
                    }
        
        return None
    
    def _extract_params(self, intent_type: str, match, instruction: str) -> Dict:
        """提取参数（增强版）"""
        params = {}
        
        # 基础操作
        if intent_type == "click":
            params["target"] = match.group(1).strip()
            params["aliases"] = self._get_target_aliases(params["target"])
        
        elif intent_type == "type":
            if match.lastindex >= 2:
                params["element"] = match.group(1).strip()
                params["text"] = match.group(2).strip()
            else:
                params["text"] = match.group(1).strip()
                params["element"] = None
        
        elif intent_type == "hotkey":
            key_combo = match.group(1).strip()
            if key_combo in self.hotkey_aliases:
                params["keys"] = self.hotkey_aliases[key_combo]
            else:
                params["keys"] = [k.strip() for k in key_combo.split("+")]
        
        # 条件操作
        elif intent_type == "if_exists":
            params["condition"] = match.group(1).strip()
            params["action"] = match.group(2).strip()
        
        # 循环操作
        elif intent_type == "loop_times":
            params["action"] = match.group(1).strip()
            params["times"] = int(match.group(2))
        
        # 相对定位
        elif intent_type == "click_index":
            params["index"] = int(match.group(1))
            params["target"] = match.group(2).strip()
        
        # 变量操作
        elif intent_type == "set_variable":
            params["variable"] = match.group(1).strip()
            params["value"] = match.group(2).strip()
        
        # 拖拽操作
        elif intent_type == "drag":
            params["source"] = match.group(1).strip()
            params["target"] = match.group(2).strip()
        
        # 等待操作
        elif intent_type == "wait":
            if match.group(1).isdigit():
                params["duration"] = int(match.group(1))
            else:
                params["target"] = match.group(1).strip()
                params["timeout"] = 10
        
        return params
    
    def _get_target_aliases(self, target: str) -> List[str]:
        """获取目标的可能别名"""
        aliases = [target]
        
        synonym_map = {
            "确定": ["确定", "确认", "OK", "是", "Yes", "完成"],
            "取消": ["取消", "Cancel", "否", "No", "关闭"],
            "保存": ["保存", "Save", "存储"],
            "关闭": ["关闭", "Close", "×", "取消"],
            "提交": ["提交", "Submit", "发送", "确认"],
            "下一步": ["下一步", "Next", "继续"],
            "上一步": ["上一步", "Previous", "返回"],
        }
        
        for key, values in synonym_map.items():
            if target in values:
                aliases.extend(values)
                break
        
        return list(set(aliases))
    
    def _parse_with_ai(self, instruction: str, context: Dict) -> Dict[str, Any]:
        """使用AI理解（增强版）"""
        try:
            import requests
            
            # 构建增强版prompt
            prompt = self._build_enhanced_prompt(instruction, context)
            
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
                        "temperature": 0.1
                    },
                    timeout=15
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
    
    def _build_enhanced_prompt(self, instruction: str, context: Dict) -> str:
        """构建增强版AI prompt"""
        
        context_str = json.dumps(context, ensure_ascii=False, indent=2)
        
        prompt = f"""你是一个桌面自动化助手。分析用户指令，理解真实意图。

用户指令: "{instruction}"

当前上下文:
{context_str}

请分析用户的真实意图，返回JSON格式：

{{
    "intent": "意图类型",
    "understanding": "用户想要做什么",
    "params": {{
        "target": "目标元素",
        "text": "输入文本",
        "keys": ["快捷键"],
        "condition": "条件",
        "times": 循环次数
    }},
    "needs_confirmation": false,
    "confidence": 0.85
}}

支持的意图类型：
- click/double_click/right_click: 点击操作
- type/clear_type: 输入操作
- hotkey: 快捷键
- menu: 菜单操作
- scroll: 滚动
- wait: 等待
- find: 查找
- if_exists/if_not_exists: 条件操作
- loop_times/loop_until: 循环操作
- click_index/click_first/click_last/click_all: 相对定位
- drag: 拖拽
- set_variable/use_variable: 变量操作
- retry/skip: 错误处理

注意事项：
1. 如果指令模糊或有歧义，设置 needs_confirmation=true
2. 如果无法确定意图，返回 confidence < 0.7
3. 提取所有关键参数（目标、文本、次数等）
4. 理解中文同义词（确定=确认=OK）

只返回JSON，不要其他内容。
"""
        return prompt
    
    def _parse_with_confirmation(self, instruction: str, context: Dict) -> Dict[str, Any]:
        """需要确认的复杂操作"""
        
        # 尝试猜测意图
        guessed_intent = self._guess_intent(instruction)
        
        return {
            "intent": "needs_confirmation",
            "instruction": instruction,
            "understanding": guessed_intent,
            "params": {},
            "needs_confirmation": True,
            "confidence": 0.5,
            "method": "confirmation",
            "question": f"我不太确定您的意思。您是想{guessed_intent}吗？",
            "suggestions": self._generate_suggestions(instruction),
        }
    
    def _guess_intent(self, instruction: str) -> str:
        """猜测用户意图"""
        
        # 简单的关键词匹配
        if any(kw in instruction for kw in ["点击", "按", "选择"]):
            return "点击某个元素"
        elif any(kw in instruction for kw in ["输入", "填写", "打字"]):
            return "在某个位置输入文本"
        elif any(kw in instruction for kw in ["查找", "搜索", "寻找"]):
            return "查找某个元素"
        elif any(kw in instruction for kw in ["等待", "等到"]):
            return "等待某个事件"
        else:
            return "执行某个操作"
    
    def _generate_suggestions(self, instruction: str) -> List[str]:
        """生成建议的指令"""
        
        suggestions = []
        
        # 基于关键词生成建议
        if "点击" in instruction:
            suggestions.append("请明确要点击哪个元素，例如：'点击确定按钮'")
        
        if "输入" in instruction:
            suggestions.append("请明确输入位置和内容，例如：'在搜索框输入\"Python\"'")
        
        if "找" in instruction or "查" in instruction:
            suggestions.append("请明确要查找什么，例如：'查找确定按钮'")
        
        return suggestions
