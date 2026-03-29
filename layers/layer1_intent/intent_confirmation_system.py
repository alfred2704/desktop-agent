"""
第1层：意图理解层 - 意图确认系统（完整版）
在AI理解后，加入用户确认环节，确保意图准确
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from loguru import logger


# ═══════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════

class ConfirmationType(Enum):
    """确认类型"""
    UNDERSTANDING = "understanding"              # 理解确认（AI理解是否正确）
    AMBIGUOUS_TARGET = "ambiguous_target"        # 目标模糊
    MULTIPLE_MATCHES = "multiple_matches"        # 多个匹配
    DANGEROUS_ACTION = "dangerous_action"        # 危险操作
    PARAMETER_MISSING = "parameter_missing"      # 参数缺失
    HIGH_RISK_OPERATION = "high_risk_operation"  # 高风险操作
    COMPLEX_TASK = "complex_task"                # 复杂任务分解


class ConfirmationPriority(Enum):
    """确认优先级"""
    LOW = 1       # 可选确认
    MEDIUM = 2    # 建议确认
    HIGH = 3      # 必须确认
    CRITICAL = 4  # 强制确认（不可跳过）


@dataclass
class ConfirmationRequest:
    """确认请求"""
    confirmation_id: str
    confirmation_type: ConfirmationType
    priority: ConfirmationPriority
    message: str
    detail: Dict[str, Any]
    options: List[Dict[str, Any]]
    allow_skip: bool  # 是否允许跳过
    timeout: int  # 超时时间（秒）
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "confirmation_id": self.confirmation_id,
            "type": self.confirmation_type.value,
            "priority": self.priority.value,
            "message": self.message,
            "detail": self.detail,
            "options": self.options,
            "allow_skip": self.allow_skip,
            "timeout": self.timeout,
            "context": self.context,
        }


@dataclass
class ConfirmationResponse:
    """确认响应"""
    confirmation_id: str
    choice_id: int
    choice_description: str
    user_input: Optional[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict:
        return {
            "confirmation_id": self.confirmation_id,
            "choice_id": self.choice_id,
            "choice_description": self.choice_description,
            "user_input": self.user_input,
            "timestamp": self.timestamp.isoformat(),
        }


# ═══════════════════════════════════════════════════════════════
# 意图确认系统
# ═══════════════════════════════════════════════════════════════

class IntentConfirmationSystem:
    """
    意图确认系统
    
    核心能力：
    1. 智能判断是否需要确认
    2. 生成多种类型的确认请求
    3. 学习用户偏好
    4. 自适应确认策略
    """
    
    def __init__(self, config):
        self.config = config
        
        # 用户偏好学习器
        self.user_preference_learner = UserPreferenceLearner()
        
        # 确认历史
        self.confirmation_history = []
        
        # 确认策略配置
        self.confirmation_policy = self._init_confirmation_policy()
    
    def _init_confirmation_policy(self) -> Dict:
        """初始化确认策略"""
        return {
            # 基于置信度的确认
            "confidence_threshold": {
                "high": 0.9,      # > 0.9 不确认
                "medium": 0.7,    # 0.7-0.9 可选确认
                "low": 0.5,       # 0.5-0.7 建议确认
                "very_low": 0.0,  # < 0.5 必须确认
            },
            
            # 高风险操作（强制确认）
            "high_risk_actions": [
                "删除", "清空", "格式化", "关闭所有",
                "发送邮件", "提交", "发布",
                "批量操作", "批量删除",
            ],
            
            # 敏感文件路径
            "sensitive_paths": [
                "C:\\Windows\\",
                "C:\\Program Files\\",
                "/etc/",
                "/usr/bin/",
            ],
            
            # 学习模式（根据历史自动调整）
            "learning_enabled": True,
            
            # 超时设置
            "timeout": {
                "default": 60,      # 默认60秒
                "high_priority": 30, # 高优先级30秒
            },
        }
    
    # ═══════════════════════════════════════════════════════════════
    # 核心方法：判断是否需要确认
    # ═══════════════════════════════════════════════════════════════
    
    def should_confirm(self, parsed_intent: Dict) -> Tuple[bool, ConfirmationType, ConfirmationPriority]:
        """
        判断是否需要确认
        
        Args:
            parsed_intent: 解析后的意图
        
        Returns:
            (是否需要确认, 确认类型, 优先级)
        """
        
        # 1. 置信度检查
        confidence = parsed_intent.get("confidence", 0.5)
        if confidence < 0.5:
            return True, ConfirmationType.UNDERSTANDING, ConfirmationPriority.HIGH
        elif confidence < 0.7:
            return True, ConfirmationType.UNDERSTANDING, ConfirmationPriority.MEDIUM
        
        # 2. 高风险操作检查
        instruction = parsed_intent.get("instruction", "")
        for risk_action in self.confirmation_policy["high_risk_actions"]:
            if risk_action in instruction:
                return True, ConfirmationType.HIGH_RISK_OPERATION, ConfirmationPriority.CRITICAL
        
        # 3. 目标模糊检查
        params = parsed_intent.get("params", {})
        if not params.get("target") and parsed_intent.get("intent") in ["click", "type"]:
            return True, ConfirmationType.AMBIGUOUS_TARGET, ConfirmationPriority.HIGH
        
        # 4. 多个匹配检查
        if params.get("matches") and len(params["matches"]) > 1:
            return True, ConfirmationType.MULTIPLE_MATCHES, ConfirmationPriority.MEDIUM
        
        # 5. 参数缺失检查
        required_params = self._get_required_params(parsed_intent.get("intent", ""))
        missing_params = [p for p in required_params if p not in params]
        if missing_params:
            return True, ConfirmationType.PARAMETER_MISSING, ConfirmationPriority.HIGH
        
        # 6. 复杂任务检查
        steps = parsed_intent.get("steps", [])
        if len(steps) > 3:
            return True, ConfirmationType.COMPLEX_TASK, ConfirmationPriority.LOW
        
        # 7. 用户偏好学习（可选）
        if self.confirmation_policy["learning_enabled"]:
            if self.user_preference_learner.should_confirm_based_on_history(parsed_intent):
                return True, ConfirmationType.UNDERSTANDING, ConfirmationPriority.LOW
        
        return False, None, None
    
    # ═══════════════════════════════════════════════════════════════
    # 核心方法：生成确认请求
    # ═══════════════════════════════════════════════════════════════
    
    def create_confirmation_request(
        self,
        confirmation_type: ConfirmationType,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """
        创建确认请求
        
        Args:
            confirmation_type: 确认类型
            priority: 优先级
            parsed_intent: 解析后的意图
        
        Returns:
            确认请求
        """
        
        confirmation_id = self._generate_confirmation_id()
        
        # 根据类型生成不同的确认请求
        if confirmation_type == ConfirmationType.UNDERSTANDING:
            return self._create_understanding_confirmation(confirmation_id, priority, parsed_intent)
        
        elif confirmation_type == ConfirmationType.AMBIGUOUS_TARGET:
            return self._create_ambiguous_target_confirmation(confirmation_id, priority, parsed_intent)
        
        elif confirmation_type == ConfirmationType.MULTIPLE_MATCHES:
            return self._create_multiple_matches_confirmation(confirmation_id, priority, parsed_intent)
        
        elif confirmation_type == ConfirmationType.HIGH_RISK_OPERATION:
            return self._create_high_risk_confirmation(confirmation_id, priority, parsed_intent)
        
        elif confirmation_type == ConfirmationType.PARAMETER_MISSING:
            return self._create_parameter_missing_confirmation(confirmation_id, priority, parsed_intent)
        
        elif confirmation_type == ConfirmationType.COMPLEX_TASK:
            return self._create_complex_task_confirmation(confirmation_id, priority, parsed_intent)
        
        else:
            return self._create_general_confirmation(confirmation_id, priority, parsed_intent)
    
    # ═══════════════════════════════════════════════════════════════
    # 各种确认类型的生成方法
    # ═══════════════════════════════════════════════════════════════
    
    def _create_understanding_confirmation(
        self,
        confirmation_id: str,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """创建理解确认"""
        
        understanding = parsed_intent.get("understanding", "无法理解")
        confidence = parsed_intent.get("confidence", 0)
        
        return ConfirmationRequest(
            confirmation_id=confirmation_id,
            confirmation_type=ConfirmationType.UNDERSTANDING,
            priority=priority,
            message="🤔 我理解您的意图如下，是否正确？",
            detail={
                "理解": understanding,
                "置信度": f"{confidence * 100:.1f}%",
                "原始指令": parsed_intent.get("instruction", ""),
            },
            options=[
                {
                    "id": 1,
                    "description": "✅ 理解正确，继续执行",
                    "action": "confirm",
                    "value": parsed_intent,
                },
                {
                    "id": 2,
                    "description": "❌ 理解错误，重新描述",
                    "action": "retry",
                    "value": None,
                },
                {
                    "id": 3,
                    "description": "✏️ 修改理解",
                    "action": "modify",
                    "value": None,
                    "allow_custom_input": True,
                    "custom_prompt": "请输入您的实际意图：",
                },
            ],
            allow_skip=(priority != ConfirmationPriority.HIGH),
            timeout=self.confirmation_policy["timeout"]["default"],
            context={"parsed_intent": parsed_intent},
        )
    
    def _create_ambiguous_target_confirmation(
        self,
        confirmation_id: str,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """创建目标模糊确认"""
        
        # 从上下文推测可能的目标
        possible_targets = self._infer_possible_targets(parsed_intent)
        
        options = []
        for i, target in enumerate(possible_targets, 1):
            options.append({
                "id": i,
                "description": f"🎯 {target['name']}",
                "action": "select_target",
                "value": target,
            })
        
        # 添加自定义输入选项
        options.append({
            "id": len(options) + 1,
            "description": "✏️ 其他目标",
            "action": "custom_target",
            "value": None,
            "allow_custom_input": True,
            "custom_prompt": "请指定目标：",
        })
        
        return ConfirmationRequest(
            confirmation_id=confirmation_id,
            confirmation_type=ConfirmationType.AMBIGUOUS_TARGET,
            priority=priority,
            message="🎯 未找到明确的目标，请选择或指定：",
            detail={
                "操作": parsed_intent.get("intent", ""),
                "需要": "目标对象",
            },
            options=options,
            allow_skip=False,
            timeout=self.confirmation_policy["timeout"]["default"],
            context={"parsed_intent": parsed_intent},
        )
    
    def _create_multiple_matches_confirmation(
        self,
        confirmation_id: str,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """创建多匹配确认"""
        
        matches = parsed_intent.get("params", {}).get("matches", [])
        
        options = []
        for i, match in enumerate(matches[:5], 1):  # 最多显示5个
            position = match.get("center", (0, 0))
            options.append({
                "id": i,
                "description": f"📍 {match.get('name', '未知')} (位置: {position})",
                "action": "select_match",
                "value": match,
            })
        
        # 添加手动选择选项
        options.append({
            "id": len(options) + 1,
            "description": "🖱️ 手动选择",
            "action": "manual_select",
            "value": None,
        })
        
        return ConfirmationRequest(
            confirmation_id=confirmation_id,
            confirmation_type=ConfirmationType.MULTIPLE_MATCHES,
            priority=priority,
            message=f"🔍 找到 {len(matches)} 个匹配项，请选择：",
            detail={
                "匹配数量": len(matches),
                "目标": parsed_intent.get("params", {}).get("target", ""),
            },
            options=options,
            allow_skip=False,
            timeout=self.confirmation_policy["timeout"]["default"],
            context={"parsed_intent": parsed_intent, "matches": matches},
        )
    
    def _create_high_risk_confirmation(
        self,
        confirmation_id: str,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """创建高风险操作确认"""
        
        instruction = parsed_intent.get("instruction", "")
        
        return ConfirmationRequest(
            confirmation_id=confirmation_id,
            confirmation_type=ConfirmationType.HIGH_RISK_OPERATION,
            priority=ConfirmationPriority.CRITICAL,
            message="⚠️ 这是一个高风险操作，请确认：",
            detail={
                "操作": instruction,
                "风险等级": "⚠️ 高",
                "影响": "此操作可能造成不可逆的影响",
            },
            options=[
                {
                    "id": 1,
                    "description": "✅ 我已了解风险，继续执行",
                    "action": "confirm_high_risk",
                    "value": parsed_intent,
                    "require_double_confirm": True,  # 需要二次确认
                },
                {
                    "id": 2,
                    "description": "❌ 取消操作",
                    "action": "cancel",
                    "value": None,
                },
            ],
            allow_skip=False,  # 不允许跳过
            timeout=self.confirmation_policy["timeout"]["high_priority"],
            context={"parsed_intent": parsed_intent},
        )
    
    def _create_parameter_missing_confirmation(
        self,
        confirmation_id: str,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """创建参数缺失确认"""
        
        intent = parsed_intent.get("intent", "")
        required_params = self._get_required_params(intent)
        params = parsed_intent.get("params", {})
        missing_params = [p for p in required_params if p not in params]
        
        # 为每个缺失参数生成输入选项
        options = []
        for i, param in enumerate(missing_params, 1):
            param_desc = self._get_param_description(param)
            options.append({
                "id": i,
                "description": f"✏️ 输入 {param_desc}",
                "action": "input_param",
                "value": param,
                "allow_custom_input": True,
                "custom_prompt": f"请输入{param_desc}：",
            })
        
        return ConfirmationRequest(
            confirmation_id=confirmation_id,
            confirmation_type=ConfirmationType.PARAMETER_MISSING,
            priority=priority,
            message=f"📝 缺少必要参数，请补充：",
            detail={
                "操作": intent,
                "缺少参数": ", ".join(missing_params),
            },
            options=options,
            allow_skip=False,
            timeout=self.confirmation_policy["timeout"]["default"],
            context={"parsed_intent": parsed_intent, "missing_params": missing_params},
        )
    
    def _create_complex_task_confirmation(
        self,
        confirmation_id: str,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """创建复杂任务确认"""
        
        steps = parsed_intent.get("steps", [])
        steps_desc = "\n".join([
            f"  {i+1}. {step.get('description', '')}"
            for i, step in enumerate(steps)
        ])
        
        return ConfirmationRequest(
            confirmation_id=confirmation_id,
            confirmation_type=ConfirmationType.COMPLEX_TASK,
            priority=priority,
            message=f"📋 这是一个复杂任务，将分解为 {len(steps)} 步执行：",
            detail={
                "任务": parsed_intent.get("understanding", ""),
                "步骤": steps_desc,
                "预计时间": f"{len(steps) * 2} 秒",
            },
            options=[
                {
                    "id": 1,
                    "description": f"✅ 确认执行（共 {len(steps)} 步）",
                    "action": "confirm",
                    "value": parsed_intent,
                },
                {
                    "id": 2,
                    "description": "👁️ 预览详细步骤",
                    "action": "preview",
                    "value": None,
                },
                {
                    "id": 3,
                    "description": "✏️ 修改步骤",
                    "action": "modify",
                    "value": None,
                },
                {
                    "id": 4,
                    "description": "❌ 取消",
                    "action": "cancel",
                    "value": None,
                },
            ],
            allow_skip=True,
            timeout=self.confirmation_policy["timeout"]["default"],
            context={"parsed_intent": parsed_intent},
        )
    
    def _create_general_confirmation(
        self,
        confirmation_id: str,
        priority: ConfirmationPriority,
        parsed_intent: Dict
    ) -> ConfirmationRequest:
        """创建通用确认"""
        
        return ConfirmationRequest(
            confirmation_id=confirmation_id,
            confirmation_type=ConfirmationType.UNDERSTANDING,
            priority=priority,
            message="🤔 请确认您的操作：",
            detail={
                "理解": parsed_intent.get("understanding", ""),
            },
            options=[
                {
                    "id": 1,
                    "description": "✅ 确认执行",
                    "action": "confirm",
                    "value": parsed_intent,
                },
                {
                    "id": 2,
                    "description": "❌ 取消",
                    "action": "cancel",
                    "value": None,
                },
            ],
            allow_skip=(priority != ConfirmationPriority.HIGH),
            timeout=self.confirmation_policy["timeout"]["default"],
            context={"parsed_intent": parsed_intent},
        )
    
    # ═══════════════════════════════════════════════════════════════
    # 辅助方法
    # ═══════════════════════════════════════════════════════════════
    
    def _generate_confirmation_id(self) -> str:
        """生成确认ID"""
        import uuid
        return f"confirm_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    
    def _get_required_params(self, intent: str) -> List[str]:
        """获取必需参数"""
        required_params_map = {
            "click": ["target"],
            "type": ["text", "target"],
            "open_app": ["app_name"],
            "save": ["file_path"],
            "send": ["recipient", "content"],
        }
        return required_params_map.get(intent, [])
    
    def _infer_possible_targets(self, parsed_intent: Dict) -> List[Dict]:
        """推测可能的目标"""
        # TODO: 从上下文、历史、知识库推测
        return [
            {"name": "确定按钮", "type": "button"},
            {"name": "取消按钮", "type": "button"},
            {"name": "输入框", "type": "edit"},
        ]
    
    def _get_param_description(self, param: str) -> str:
        """获取参数描述"""
        param_desc_map = {
            "target": "目标对象",
            "text": "文本内容",
            "app_name": "应用名称",
            "file_path": "文件路径",
            "recipient": "收件人",
            "content": "内容",
        }
        return param_desc_map.get(param, param)
    
    # ═══════════════════════════════════════════════════════════════
    # 用户响应处理
    # ═══════════════════════════════════════════════════════════════
    
    def handle_user_response(
        self,
        confirmation_request: ConfirmationRequest,
        user_choice: int,
        user_input: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理用户响应
        
        Args:
            confirmation_request: 确认请求
            user_choice: 用户选择的选项ID
            user_input: 用户输入（如果有）
        
        Returns:
            处理结果
        """
        
        # 找到用户选择的选项
        selected_option = None
        for option in confirmation_request.options:
            if option["id"] == user_choice:
                selected_option = option
                break
        
        if not selected_option:
            return {
                "success": False,
                "error": "无效的选择",
            }
        
        # 记录用户选择（用于学习）
        self._record_user_choice(confirmation_request, user_choice, user_input)
        
        # 根据不同的action返回结果
        action = selected_option.get("action")
        
        if action == "confirm":
            return {
                "success": True,
                "action": "proceed",
                "value": selected_option.get("value"),
            }
        
        elif action == "retry":
            return {
                "success": True,
                "action": "retry",
                "message": "请重新描述您的意图",
            }
        
        elif action == "modify":
            return {
                "success": True,
                "action": "modify",
                "user_input": user_input,
            }
        
        elif action == "cancel":
            return {
                "success": True,
                "action": "cancel",
                "message": "操作已取消",
            }
        
        elif action == "select_target":
            return {
                "success": True,
                "action": "update_target",
                "value": selected_option.get("value"),
            }
        
        elif action == "custom_target":
            return {
                "success": True,
                "action": "custom_target",
                "user_input": user_input,
            }
        
        elif action == "input_param":
            return {
                "success": True,
                "action": "update_param",
                "param": selected_option.get("value"),
                "user_input": user_input,
            }
        
        else:
            return {
                "success": True,
                "action": action,
                "value": selected_option.get("value"),
            }
    
    def _record_user_choice(
        self,
        confirmation_request: ConfirmationRequest,
        user_choice: int,
        user_input: Optional[str]
    ):
        """记录用户选择（用于学习）"""
        
        response = ConfirmationResponse(
            confirmation_id=confirmation_request.confirmation_id,
            choice_id=user_choice,
            choice_description=next(
                (opt["description"] for opt in confirmation_request.options if opt["id"] == user_choice),
                ""
            ),
            user_input=user_input,
            timestamp=datetime.now(),
        )
        
        self.confirmation_history.append({
            "request": confirmation_request.to_dict(),
            "response": response.to_dict(),
        })
        
        # 学习用户偏好
        if self.confirmation_policy["learning_enabled"]:
            self.user_preference_learner.learn(
                confirmation_request.context.get("parsed_intent", {}),
                response
            )


# ═══════════════════════════════════════════════════════════════
# 用户偏好学习器
# ═══════════════════════════════════════════════════════════════

class UserPreferenceLearner:
    """用户偏好学习器"""
    
    def __init__(self):
        self.preferences = {
            # 例如：用户总是选择"确定"而不是"确认"
            "button_preference": {},
            # 用户对某些操作总是跳过确认
            "skip_confirmation_patterns": [],
            # 用户的常用目标
            "common_targets": {},
        }
    
    def should_confirm_based_on_history(self, parsed_intent: Dict) -> bool:
        """基于历史判断是否需要确认"""
        
        # 如果用户之前多次跳过类似操作的确认，可以自动跳过
        instruction = parsed_intent.get("instruction", "")
        
        for pattern in self.preferences["skip_confirmation_patterns"]:
            if pattern in instruction:
                return False  # 不需要确认
        
        return False  # 默认不强制确认
    
    def learn(self, parsed_intent: Dict, response: ConfirmationResponse):
        """学习用户偏好"""
        
        # 学习用户的跳过确认模式
        if response.choice_description == "跳过确认":
            instruction = parsed_intent.get("instruction", "")
            # 提取关键词
            keywords = self._extract_keywords(instruction)
            self.preferences["skip_confirmation_patterns"].extend(keywords)
        
        # 学习用户的常用目标选择
        # TODO: 实现更复杂的学习逻辑
        pass
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简化实现
        return [word for word in text.split() if len(word) > 2]


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from core.config import Config
    
    config = Config()
    confirmation_system = IntentConfirmationSystem(config)
    
    # 示例1：理解确认
    print("=== 示例1：理解确认 ===")
    parsed_intent = {
        "instruction": "点击确定按钮",
        "intent": "click",
        "understanding": "点击名为'确定'的按钮",
        "confidence": 0.65,
        "params": {"target": "确定"},
    }
    
    should_confirm, conf_type, priority = confirmation_system.should_confirm(parsed_intent)
    print(f"需要确认: {should_confirm}, 类型: {conf_type}, 优先级: {priority}")
    
    if should_confirm:
        request = confirmation_system.create_confirmation_request(conf_type, priority, parsed_intent)
        print(f"\n确认请求:\n{json.dumps(request.to_dict(), ensure_ascii=False, indent=2)}")
    
    # 示例2：高风险操作
    print("\n=== 示例2：高风险操作 ===")
    parsed_intent = {
        "instruction": "删除所有文件",
        "intent": "delete",
        "understanding": "删除所有文件",
        "confidence": 0.95,
        "params": {"target": "所有文件"},
    }
    
    should_confirm, conf_type, priority = confirmation_system.should_confirm(parsed_intent)
    print(f"需要确认: {should_confirm}, 类型: {conf_type}, 优先级: {priority}")
    
    if should_confirm:
        request = confirmation_system.create_confirmation_request(conf_type, priority, parsed_intent)
        print(f"\n确认请求:\n{json.dumps(request.to_dict(), ensure_ascii=False, indent=2)}")
