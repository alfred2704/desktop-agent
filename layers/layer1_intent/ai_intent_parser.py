"""
第1层：意图理解层 - AI驱动的意图解析器（重构版）
从"规则匹配"转向"AI理解"
"""

from typing import Dict, Any, List, Optional
import json
import re
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class Step:
    """任务步骤"""
    step_id: int
    action: str  # open_app, type, save, send, click, etc.
    params: Dict[str, Any]
    description: str
    dependencies: List[int] = field(default_factory=list)
    output: Optional[str] = None
    confidence: float = 0.85


@dataclass
class Task:
    """任务模型"""
    task_type: str  # document_workflow, data_processing, communication, automation
    understanding: str  # AI对任务的理解
    steps: List[Step]
    software: List[str]
    data_flow: Dict[str, str]  # 步骤间的数据流转
    risks: List[str]
    needs_confirmation: bool
    confidence: float
    
    def to_dict(self) -> Dict:
        return {
            "task_type": self.task_type,
            "understanding": self.understanding,
            "steps": [
                {
                    "step_id": s.step_id,
                    "action": s.action,
                    "params": s.params,
                    "description": s.description,
                    "dependencies": s.dependencies,
                    "output": s.output,
                    "confidence": s.confidence
                }
                for s in self.steps
            ],
            "software": self.software,
            "data_flow": self.data_flow,
            "risks": self.risks,
            "needs_confirmation": self.needs_confirmation,
            "confidence": self.confidence
        }


class AIDrivenIntentParser:
    """
    AI驱动的意图解析器
    
    架构：
    1. AI深度理解（70%）- 主要理解引擎
    2. 任务模板匹配（20%）- 常见任务快速识别
    3. 规则优化（10%）- 性能优化
    """
    
    def __init__(self, config):
        self.config = config
        
        # 任务模板库
        self.task_templates = self._init_task_templates()
        
        # 规则优化器（仅用于简单场景加速）
        self.quick_patterns = self._init_quick_patterns()
        
        # Few-shot示例库（用于prompt）
        self.few_shot_examples = self._init_few_shot_examples()
    
    def _init_task_templates(self) -> Dict[str, Dict]:
        """初始化任务模板库"""
        return {
            "document_workflow": {
                "description": "文档创建与分享流程",
                "keywords": ["打开", "输入", "写", "保存", "发送", "分享"],
                "typical_steps": ["open_app", "create_content", "save", "share"],
                "example": "打开Word，写报告，保存，发邮件",
            },
            
            "data_processing": {
                "description": "数据处理流程",
                "keywords": ["读取", "处理", "过滤", "计算", "保存"],
                "typical_steps": ["open_source", "process", "save_result"],
                "example": "从Excel读数据，过滤，保存",
            },
            
            "communication": {
                "description": "沟通协作流程",
                "keywords": ["发送", "回复", "转发", "通知"],
                "typical_steps": ["open_app", "compose", "send"],
                "example": "打开微信，发消息给XX",
            },
            
            "automation": {
                "description": "自动化操作",
                "keywords": ["点击", "输入", "等待", "重复"],
                "typical_steps": ["locate", "interact", "verify"],
                "example": "点击确定按钮，输入用户名",
            },
        }
    
    def _init_quick_patterns(self) -> Dict[str, List[str]]:
        """初始化快速匹配模式（仅用于性能优化）"""
        return {
            "simple_click": [
                r"^点击\s*(.+)$",
                r"^单击\s*(.+)$",
            ],
            "simple_type": [
                r"^输入\s*['\"](.+?)['\"]$",
            ],
            "simple_hotkey": [
                r"^按\s*([A-Za-z+]+)$",
            ],
        }
    
    def parse(self, instruction: str, context: Dict = None) -> Dict[str, Any]:
        """
        解析自然语言指令（AI驱动）
        
        策略：
        1. 快速检查是否简单操作（规则）
        2. AI深度理解
        3. 任务模型构建
        """
        instruction = instruction.strip()
        context = context or {}
        
        logger.info(f"解析指令: {instruction}")
        
        # ═════════════════════════════════════════════════════════
        # 第1步：快速检查简单操作（10%场景，性能优化）
        # ═════════════════════════════════════════════════════════
        quick_result = self._quick_match(instruction)
        if quick_result:
            logger.info("[快速匹配] 简单操作，直接返回")
            return quick_result
        
        # ═════════════════════════════════════════════════════════
        # 第2步：AI深度理解（90%场景）
        # ═════════════════════════════════════════════════════════
        if self.config.AI_ENABLED:
            ai_result = self._ai_deep_understand(instruction, context)
            
            if ai_result:
                # 构建任务模型
                task = self._build_task_model(ai_result, instruction)
                
                logger.info(f"[AI理解] 任务类型: {task.task_type}, 步骤数: {len(task.steps)}")
                
                return task.to_dict()
        
        # ═════════════════════════════════════════════════════════
        # 第3步：降级处理
        # ═════════════════════════════════════════════════════════
        return {
            "task_type": "unknown",
            "understanding": "无法理解指令",
            "steps": [],
            "software": [],
            "data_flow": {},
            "risks": ["需要人工确认"],
            "needs_confirmation": True,
            "confidence": 0.0,
            "original_instruction": instruction,
        }
    
    def _quick_match(self, instruction: str) -> Optional[Dict]:
        """快速匹配简单操作（性能优化）"""
        
        # 简单点击
        for pattern in self.quick_patterns.get("simple_click", []):
            match = re.match(pattern, instruction)
            if match:
                return {
                    "task_type": "simple_action",
                    "understanding": f"点击 {match.group(1)}",
                    "steps": [{
                        "step_id": 1,
                        "action": "click",
                        "params": {"target": match.group(1)},
                        "description": f"点击 {match.group(1)}",
                        "dependencies": [],
                        "confidence": 0.95
                    }],
                    "software": [],
                    "data_flow": {},
                    "risks": [],
                    "needs_confirmation": False,
                    "confidence": 0.95,
                    "method": "quick_match"
                }
        
        # 简单输入
        for pattern in self.quick_patterns.get("simple_type", []):
            match = re.match(pattern, instruction)
            if match:
                return {
                    "task_type": "simple_action",
                    "understanding": f"输入文本: {match.group(1)}",
                    "steps": [{
                        "step_id": 1,
                        "action": "type",
                        "params": {"text": match.group(1)},
                        "description": f"输入 {match.group(1)}",
                        "dependencies": [],
                        "confidence": 0.95
                    }],
                    "software": [],
                    "data_flow": {},
                    "risks": [],
                    "needs_confirmation": False,
                    "confidence": 0.95,
                    "method": "quick_match"
                }
        
        return None
    
    def _ai_deep_understand(self, instruction: str, context: Dict) -> Optional[Dict]:
        """AI深度理解（核心）"""
        
        prompt = self._build_understanding_prompt(instruction, context)
        
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
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # 提取JSON
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    parsed = json.loads(json_match.group())
                    parsed["method"] = "ai_understand"
                    return parsed
        
        except Exception as e:
            logger.error(f"AI理解失败: {e}")
        
        return None
    
    def _build_understanding_prompt(self, instruction: str, context: Dict) -> str:
        """构建AI理解Prompt（优化版：Few-shot + 结构化）"""
        
        context_str = json.dumps(context, ensure_ascii=False, indent=2)
        
        # Few-shot示例：从简单到复杂
        few_shot_examples = self._get_few_shot_examples()
        
        prompt = f"""# 角色定义

你是一个专业的桌面自动化任务理解专家，擅长将自然语言转换为可执行的自动化步骤。

---

# 当前任务

用户指令: "{instruction}"

上下文信息:
{context_str if context_str else "无"}

---

# Few-shot 学习示例

## 示例1：简单点击操作

指令："点击确定按钮"

解析:
{{
    "task_type": "automation",
    "understanding": "点击名为'确定'的按钮",
    "steps": [
        {{
            "step_id": 1,
            "action": "click",
            "params": {{
                "target": "确定",
                "target_type": "button"
            }},
            "description": "点击确定按钮",
            "dependencies": [],
            "output": "点击完成"
        }}
    ],
    "software": [],
    "data_flow": {{}},
    "risks": [],
    "needs_confirmation": false
}}

---

## 示例2：输入操作

指令："在搜索框输入'Python教程'"

解析:
{{
    "task_type": "automation",
    "understanding": "在搜索输入框中输入文本'Python教程'",
    "steps": [
        {{
            "step_id": 1,
            "action": "type",
            "params": {{
                "text": "Python教程",
                "target": "搜索框"
            }},
            "description": "在搜索框中输入",
            "dependencies": [],
            "output": "文本已输入"
        }}
    ],
    "software": [],
    "data_flow": {{}},
    "risks": ["需要找到搜索框"],
    "needs_confirmation": false
}}

---

## 示例3：快捷键操作

指令："按Ctrl+S保存"

解析:
{{
    "task_type": "automation",
    "understanding": "使用Ctrl+S快捷键保存当前内容",
    "steps": [
        {{
            "step_id": 1,
            "action": "hotkey",
            "params": {{
                "keys": ["ctrl", "s"]
            }},
            "description": "按Ctrl+S快捷键",
            "dependencies": [],
            "output": "保存对话框"
        }},
        {{
            "step_id": 2,
            "action": "click",
            "params": {{
                "target": "保存"
            }},
            "description": "确认保存",
            "dependencies": [1],
            "output": "文件已保存"
        }}
    ],
    "software": [],
    "data_flow": {{
        "step_1_output": "step_2_input"
    }},
    "risks": [],
    "needs_confirmation": false
}}

---

## 示例4：文档工作流

指令："打开Word，输入'季度报告'，保存为Q1.docx"

解析:
{{
    "task_type": "document_workflow",
    "understanding": "打开Word应用，创建新文档，输入标题，保存为指定文件",
    "steps": [
        {{
            "step_id": 1,
            "action": "open_app",
            "params": {{
                "app_name": "Microsoft Word",
                "app_path": "WINWORD.EXE"
            }},
            "description": "打开Word应用",
            "dependencies": [],
            "output": "Word窗口"
        }},
        {{
            "step_id": 2,
            "action": "type",
            "params": {{
                "text": "季度报告",
                "target": "文档编辑区"
            }},
            "description": "输入文档标题",
            "dependencies": [1],
            "output": "文档内容"
        }},
        {{
            "step_id": 3,
            "action": "save",
            "params": {{
                "method": "save_as",
                "filename": "Q1.docx"
            }},
            "description": "保存文档为Q1.docx",
            "dependencies": [2],
            "output": "文件路径"
        }}
    ],
    "software": ["Microsoft Word"],
    "data_flow": {{
        "step_1_output": "step_2_input",
        "step_2_output": "step_3_input"
    }},
    "risks": ["Word可能未安装", "文件路径可能已存在"],
    "needs_confirmation": true
}}

---

## 示例5：数据处理

指令："在Excel中打开C:/data/sales.xlsx，选中A列，点击数据菜单的筛选"

解析:
{{
    "task_type": "data_processing",
    "understanding": "打开Excel文件，选中A列，为A列应用数据筛选功能",
    "steps": [
        {{
            "step_id": 1,
            "action": "open_app",
            "params": {{
                "app_name": "Microsoft Excel",
                "app_path": "EXCEL.EXE",
                "file_path": "C:/data/sales.xlsx"
            }},
            "description": "用Excel打开文件",
            "dependencies": [],
            "output": "Excel窗口和数据"
        }},
        {{
            "step_id": 2,
            "action": "select",
            "params": {{
                "target": "A列",
                "selection_type": "column"
            }},
            "description": "选中A列",
            "dependencies": [1],
            "output": "A列已选中"
        }},
        {{
            "step_id": 3,
            "action": "menu_click",
            "params": {{
                "menu": "数据",
                "item": "筛选"
            }},
            "description": "点击数据菜单的筛选项",
            "dependencies": [2],
            "output": "筛选功能激活"
        }}
    ],
    "software": ["Microsoft Excel"],
    "data_flow": {{
        "step_1_output": "step_2_input",
        "step_2_output": "step_3_input"
    }},
    "risks": ["文件可能不存在", "数据可能已存在筛选"],
    "needs_confirmation": false
}}

---

## 示例6：跨应用工作流

指令："打开记事本，输入'你好'，保存为文件，通过企业微信发送给熊一伟"

解析:
{{
    "task_type": "multi_app_workflow",
    "understanding": "创建文本文件，输入内容，保存后通过企业微信发送",
    "steps": [
        {{
            "step_id": 1,
            "action": "open_app",
            "params": {{
                "app_name": "记事本",
                "app_path": "notepad.exe"
            }},
            "description": "打开记事本应用",
            "dependencies": [],
            "output": "记事本窗口"
        }},
        {{
            "step_id": 2,
            "action": "type",
            "params": {{
                "text": "你好",
                "target": "编辑区域"
            }},
            "description": "在记事本中输入文本",
            "dependencies": [1],
            "output": "文档内容"
        }},
        {{
            "step_id": 3,
            "action": "save",
            "params": {{
                "method": "hotkey",
                "keys": ["ctrl", "s"],
                "filename": null
            }},
            "description": "保存文件",
            "dependencies": [2],
            "output": "文件路径"
        }},
        {{
            "step_id": 4,
            "action": "send",
            "params": {{
                "via": "企业微信",
                "recipient": "熊一伟",
                "content_type": "file",
                "content": "step_3_output"
            }},
            "description": "通过企业微信发送文件给熊一伟",
            "dependencies": [3],
            "output": "发送状态"
        }}
    ],
    "software": ["记事本", "企业微信"],
    "data_flow": {{
        "step_2_output": "step_3_input",
        "step_3_output": "step_4_input"
    }},
    "risks": ["需要企业微信已登录", "可能需要输入文件名"],
    "needs_confirmation": false
}}

---

## 任务类型定义

1. **automation**: 单个自动化操作（点击、输入、快捷键等）
2. **document_workflow**: 文档处理流程（创建、编辑、保存、分享）
3. **data_processing**: 数据处理流程（读取、处理、保存、分析）
4. **communication**: 沟通协作流程（发送消息、邮件、文件）
5. **multi_app_workflow**: 跨应用工作流（多个应用之间的操作）

---

## 动作类型完整列表

- **open_app**: 打开应用
  - 参数: app_name, app_path, file_path
  
- **type**: 输入文本
  - 参数: text, target
  
- **click**: 点击元素
  - 参数: target, target_type, position
  
- **save**: 保存
  - 参数: method (hotkey/menu), keys, filename, path
  
- **send**: 发送（消息/文件）
  - 参数: via (app), recipient, content_type, content
  
- **wait**: 等待
  - 参数: duration, condition, target
  
- **copy**: 复制
  - 参数: content, source
  
- **paste**: 粘贴
  - 参数: target
  
- **hotkey**: 快捷键
  - 参数: keys (list)
  
- **scroll**: 滚动
  - 参数: direction, amount, target
  
- **drag**: 拖拽
  - 参数: from, to, duration
  
- **select**: 选择
  - 参数: target, selection_type (range/column/row)
  
- **menu_click**: 菜单点击
  - 参数: menu, item, submenu

---

## 分析指南（重要）

### 1. 识别所有步骤
- 不要遗漏任何操作
- 步骤之间逻辑要完整
- 考虑前置条件和后置条件

### 2. 理解步骤依赖关系
- 哪些步骤必须在前？
- 数据如何流转？（用step_X_output表示）
- 并行步骤如何表示？

### 3. 识别涉及的软件
- 明确列出所有需要的软件
- 考虑软件切换时机
- 注意软件版本差异

### 4. 提取所有参数
- 必需参数不能省略
- 可选参数提供默认值或null
- 参数类型要准确（string、number、boolean、array）

### 5. 评估风险
- 可能失败的点有哪些？
- 是否需要用户确认？（删除、发送等高风险操作）
- 需要用户输入什么？（文件名、收件人等）

### 6. 数据流设计
- 明确步骤间的数据流转
- 使用"step_X_output"表示引用
- 确保数据流是完整的

---

## 常见错误模式

### ❌ 错误1：遗漏步骤
```
指令："打开Word，输入内容，保存"
错误分析：缺少"新建文档"步骤
正确做法：
1. open_app: 打开Word
2. new_document: 新建文档
3. type: 输入内容
4. save: 保存
```

### ❌ 错误2：依赖关系不明确
```
错误：step_2依赖step_1，但没有data_flow
正确：data_flow中明确step_1_output = step_2_input
```

### ❌ 错误3：风险识别不足
```
错误：删除操作没有风险提示
正确：risks包含"删除不可恢复"
```

### ❌ 错误4：参数不准确
```
错误：filename = "文件"（太模糊）
正确：filename = "Q1_2026.docx"（更具体）
```

---

## 输出格式要求

1. **严格的JSON格式**
2. **不要任何注释或说明文字**
3. **确保所有引号和逗号正确**
4. **检查JSON有效性**
5. **字段名称与示例完全一致**

---

# 现在，请分析当前用户的指令，返回严格的JSON格式解析结果。
"""

        return prompt
    
    def _get_few_shot_examples(self) -> str:
        """获取Few-shot示例（根据指令类型选择最相关的示例）"""
        # 返回空，因为已经在prompt中内联了示例
        # 未来可以根据指令类型动态选择不同的示例
        return ""
    
    def _build_task_model(self, ai_result: Dict, instruction: str) -> Task:
        """构建任务模型"""
        
        steps = []
        for step_data in ai_result.get("steps", []):
            step = Step(
                step_id=step_data.get("step_id", len(steps) + 1),
                action=step_data.get("action", "unknown"),
                params=step_data.get("params", {}),
                description=step_data.get("description", ""),
                dependencies=step_data.get("dependencies", []),
                output=step_data.get("output"),
                confidence=0.85
            )
            steps.append(step)
        
        task = Task(
            task_type=ai_result.get("task_type", "unknown"),
            understanding=ai_result.get("understanding", instruction),
            steps=steps,
            software=ai_result.get("software", []),
            data_flow=ai_result.get("data_flow", {}),
            risks=ai_result.get("risks", []),
            needs_confirmation=ai_result.get("needs_confirmation", False),
            confidence=0.85
        )
        
        return task


# 使用示例
if __name__ == "__main__":
    from core.config import Config
    
    config = Config()
    parser = AIDrivenIntentParser(config)
    
    # 测试复杂任务
    instruction = "打开记事本，输入'你好'，保存为文件，通过企业微信发送给熊一伟"
    
    result = parser.parse(instruction)
    
    print("=" * 70)
    print("解析结果：")
    print("=" * 70)
    print(json.dumps(result, ensure_ascii=False, indent=2))
