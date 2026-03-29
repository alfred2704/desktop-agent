"""
第1层：意图理解层 - 带确认的意图解析器（集成版）
将确认系统集成到AI驱动的意图解析器中
"""

from typing import Dict, Any, Optional
from loguru import logger
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from layers.layer1_intent.intent_confirmation_system import (
    IntentConfirmationSystem,
    ConfirmationType,
    ConfirmationPriority,
)
from core.config import Config


class IntentParserWithConfirmation:
    """
    带确认的意图解析器
    
    流程：
    1. AI解析意图
    2. 判断是否需要确认
    3. 生成确认请求（如果需要）
    4. 等待用户响应
    5. 根据响应调整意图
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        
        # AI驱动的意图解析器
        self.intent_parser = AIDrivenIntentParser(self.config)
        
        # 意图确认系统
        self.confirmation_system = IntentConfirmationSystem(self.config)
        
        # 确认处理器（可由外部设置，如Web界面、命令行等）
        self.confirmation_handler = None
    
    def set_confirmation_handler(self, handler):
        """
        设置确认处理器
        
        Args:
            handler: 确认处理函数，签名: (ConfirmationRequest) -> (int, Optional[str])
                    返回 (choice_id, user_input)
        """
        self.confirmation_handler = handler
    
    def parse_with_confirmation(
        self,
        instruction: str,
        context: Dict = None,
        auto_confirm_threshold: float = 0.95
    ) -> Dict[str, Any]:
        """
        解析意图（带确认）
        
        Args:
            instruction: 自然语言指令
            context: 上下文
            auto_confirm_threshold: 自动确认的置信度阈值（> 此值不确认）
        
        Returns:
            最终确认后的意图
        """
        
        logger.info(f"解析指令（带确认）: {instruction}")
        
        # ═════════════════════════════════════════════════════════
        # 第1步：AI解析意图
        # ═════════════════════════════════════════════════════════
        parsed_intent = self.intent_parser.parse(instruction, context)
        
        logger.info(f"AI解析结果: {parsed_intent.get('understanding', '')}")
        logger.info(f"置信度: {parsed_intent.get('confidence', 0):.2%}")
        
        # ═════════════════════════════════════════════════════════
        # 第2步：判断是否需要确认
        # ═════════════════════════════════════════════════════════
        
        # 如果置信度非常高，且不是高风险操作，可以跳过确认
        if parsed_intent.get("confidence", 0) >= auto_confirm_threshold:
            # 再次检查是否是高风险操作
            instruction_text = parsed_intent.get("instruction", "")
            if not any(risk in instruction_text for risk in ["删除", "清空", "格式化"]):
                logger.info("置信度很高且非高风险操作，跳过确认")
                return parsed_intent
        
        # 判断是否需要确认
        should_confirm, conf_type, priority = self.confirmation_system.should_confirm(parsed_intent)
        
        if not should_confirm:
            logger.info("不需要确认，直接返回")
            return parsed_intent
        
        # ═════════════════════════════════════════════════════════
        # 第3步：生成确认请求
        # ═════════════════════════════════════════════════════════
        logger.info(f"需要确认: {conf_type.value}, 优先级: {priority.value}")
        
        confirmation_request = self.confirmation_system.create_confirmation_request(
            conf_type,
            priority,
            parsed_intent
        )
        
        # ═════════════════════════════════════════════════════════
        # 第4步：等待用户响应
        # ═════════════════════════════════════════════════════════
        
        if self.confirmation_handler:
            # 使用外部处理器（如Web界面）
            user_choice, user_input = self.confirmation_handler(confirmation_request)
        else:
            # 默认使用命令行交互
            user_choice, user_input = self._cli_confirmation(confirmation_request)
        
        # ═════════════════════════════════════════════════════════
        # 第5步：处理用户响应
        # ═════════════════════════════════════════════════════════
        
        response_result = self.confirmation_system.handle_user_response(
            confirmation_request,
            user_choice,
            user_input
        )
        
        # 根据响应结果调整意图
        if response_result["success"]:
            action = response_result.get("action")
            
            if action == "proceed":
                # 用户确认，继续执行
                logger.info("用户确认，继续执行")
                return response_result.get("value", parsed_intent)
            
            elif action == "retry":
                # 用户要求重新描述
                logger.info("用户要求重新描述")
                new_instruction = input("请重新描述您的意图: ")
                return self.parse_with_confirmation(new_instruction, context)
            
            elif action == "modify":
                # 用户修改理解
                logger.info(f"用户修改理解: {user_input}")
                # 重新解析用户输入
                return self.parse_with_confirmation(user_input, context)
            
            elif action == "cancel":
                # 用户取消
                logger.info("用户取消操作")
                return {
                    "intent": "cancel",
                    "understanding": "用户取消操作",
                    "confidence": 1.0,
                }
            
            elif action == "update_target":
                # 更新目标
                logger.info(f"更新目标: {response_result['value']}")
                parsed_intent["params"]["target"] = response_result["value"]
                return parsed_intent
            
            elif action == "custom_target":
                # 自定义目标
                logger.info(f"使用自定义目标: {user_input}")
                parsed_intent["params"]["target"] = user_input
                return parsed_intent
            
            elif action == "update_param":
                # 更新参数
                logger.info(f"更新参数 {response_result['param']}: {user_input}")
                parsed_intent["params"][response_result["param"]] = user_input
                return parsed_intent
            
            else:
                return parsed_intent
        else:
            # 响应处理失败
            logger.error(f"响应处理失败: {response_result.get('error')}")
            return parsed_intent
    
    def _cli_confirmation(self, request) -> tuple:
        """
        命令行确认交互
        
        Args:
            request: ConfirmationRequest
        
        Returns:
            (choice_id, user_input)
        """
        
        print("\n" + "=" * 60)
        print(request.message)
        print("=" * 60)
        
        # 显示详细信息
        for key, value in request.detail.items():
            print(f"{key}: {value}")
        
        print("\n选项:")
        for option in request.options:
            print(f"  [{option['id']}] {option['description']}")
        
        if request.allow_skip:
            print(f"  [0] 跳过确认")
        
        # 获取用户选择
        while True:
            try:
                choice = input("\n请选择 [默认: 1]: ").strip()
                
                if not choice:
                    choice = "1"
                
                choice_id = int(choice)
                
                # 检查是否是跳过
                if choice_id == 0 and request.allow_skip:
                    return 1, None  # 默认选择第一个选项
                
                # 检查是否有效
                valid_ids = [opt["id"] for opt in request.options]
                if choice_id in valid_ids:
                    # 检查是否需要用户输入
                    selected_option = next(
                        opt for opt in request.options if opt["id"] == choice_id
                    )
                    
                    if selected_option.get("allow_custom_input"):
                        user_input = input(f"{selected_option['custom_prompt']}: ").strip()
                        return choice_id, user_input
                    else:
                        return choice_id, None
                else:
                    print("❌ 无效选择，请重试")
            
            except ValueError:
                print("❌ 请输入数字")
            except KeyboardInterrupt:
                print("\n\n❌ 用户取消")
                return 2, None  # 默认选择取消


# ═══════════════════════════════════════════════════════════════
# Web界面确认处理器示例
# ═══════════════════════════════════════════════════════════════

class WebConfirmationHandler:
    """Web界面确认处理器"""
    
    def __init__(self):
        self.pending_confirmations = {}  # 等待中的确认请求
        self.confirmation_responses = {}  # 用户响应
    
    def __call__(self, request):
        """处理确认请求"""
        
        # 1. 保存确认请求（等待用户响应）
        self.pending_confirmations[request.confirmation_id] = request
        
        # 2. 推送到Web界面（这里简化为等待）
        # 实际实现中，这里应该通过WebSocket推送到前端
        # 然后阻塞等待用户响应
        
        # 模拟等待（实际应该用异步等待）
        import time
        timeout = request.timeout
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 检查是否有响应
            if request.confirmation_id in self.confirmation_responses:
                response = self.confirmation_responses.pop(request.confirmation_id)
                self.pending_confirmations.pop(request.confirmation_id)
                return response["choice_id"], response.get("user_input")
            
            time.sleep(0.1)
        
        # 超时，默认选择第一个选项
        self.pending_confirmations.pop(request.confirmation_id)
        return 1, None
    
    def submit_response(self, confirmation_id: str, choice_id: int, user_input: str = None):
        """提交用户响应（从Web界面调用）"""
        
        self.confirmation_responses[confirmation_id] = {
            "choice_id": choice_id,
            "user_input": user_input,
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 创建配置
    config = Config()
    
    # 创建带确认的解析器
    parser = IntentParserWithConfirmation(config)
    
    print("\n" + "=" * 60)
    print("意图确认系统 - 演示")
    print("=" * 60)
    
    # 示例1：简单操作（高置信度）
    print("\n### 示例1：简单操作（高置信度，可能跳过确认）")
    result1 = parser.parse_with_confirmation(
        "点击确定按钮",
        auto_confirm_threshold=0.99  # 设置很高的阈值，强制确认
    )
    print(f"\n最终意图: {result1}")
    
    # 示例2：模糊目标
    print("\n### 示例2：目标模糊")
    result2 = parser.parse_with_confirmation(
        "点击按钮",  # 没有指定哪个按钮
        auto_confirm_threshold=0.99
    )
    print(f"\n最终意图: {result2}")
    
    # 示例3：高风险操作
    print("\n### 示例3：高风险操作")
    result3 = parser.parse_with_confirmation(
        "删除所有文件",
        auto_confirm_threshold=0.99
    )
    print(f"\n最终意图: {result3}")
