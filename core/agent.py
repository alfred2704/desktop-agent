"""
Desktop Agent - 主控制器
整合六层架构，提供统一接口
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import time
import json
from loguru import logger

# 导入配置
from core.config import Config

# 导入六层模块
# 使用带确认的意图解析器（增强可靠性）
from layers.layer1_intent.intent_parser_with_confirmation import IntentParserWithConfirmation
from layers.layer1_intent.context_manager import ContextManager

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from layers.layer2_perception.element_locator import ElementLocator

from layers.layer3_planning.action_planner import ActionPlanner
from layers.layer3_planning.knowledge_query import KnowledgeQuery

from layers.layer4_execution.action_executor import ActionExecutor

from layers.layer5_verification.verification_manager import VerificationManager

from layers.layer6_knowledge.knowledge_manager import KnowledgeManager


class DesktopAgent:
    """
    Desktop Agent 主控制器
    
    整合六层架构，提供统一执行接口
    """
    
    def __init__(self, config: Config = None):
        """初始化Agent"""
        self.config = config or Config()
        
        # 初始化六层模块
        logger.info("初始化 Desktop Agent...")
        
        # 第1层：意图理解（带确认）
        self.intent_parser = IntentParserWithConfirmation(self.config)
        self.context_manager = ContextManager()
        
        logger.info("✅ 已启用意图确认系统")
        
        # 第2层：屏幕感知
        self.screen_perceiver = ScreenPerceiver(self.config)
        self.element_locator = ElementLocator(self.config)
        
        # 第3层：操作规划
        self.knowledge_query = KnowledgeQuery(self.config)
        self.action_planner = ActionPlanner(self.config, self.knowledge_query)
        
        # 第4层：动作执行
        self.action_executor = ActionExecutor(self.config)
        
        # 第5层：验证反馈
        self.verification_manager = VerificationManager(self.config)
        
        # 第6层：知识记忆
        self.knowledge_manager = KnowledgeManager(self.config)
        
        # 执行历史
        self.execution_history = []
        
        logger.info("Desktop Agent 初始化完成")
    
    def execute(
        self, 
        instruction: str, 
        context: Dict = None,
        enable_confirmation: bool = True,
        auto_confirm_threshold: float = 0.95
    ) -> Dict[str, Any]:
        """
        执行自然语言指令
        
        Args:
            instruction: 自然语言指令
            context: 上下文信息
            enable_confirmation: 是否启用意图确认（默认启用）
            auto_confirm_threshold: 自动确认的置信度阈值
        
        Returns:
            执行结果
        """
        start_time = time.time()
        
        logger.info(f"收到指令: {instruction}")
        
        result = {
            "instruction": instruction,
            "success": False,
            "layers": {},
            "execution_time": 0,
            "error": None,
            "confirmed": False,  # 新增：是否经过确认
        }
        
        try:
            # ═══════════════════════════════════════════════════
            # 第1层：意图理解（带确认）
            # ═══════════════════════════════════════════════════
            logger.info("[第1层] 意图理解（带确认）...")
            
            # 更新上下文
            if context:
                self.context_manager.update(context)
            
            # 解析意图（如果启用确认，会自动与用户交互）
            if enable_confirmation:
                intent = self.intent_parser.parse_with_confirmation(
                    instruction, 
                    self.context_manager.get(),
                    auto_confirm_threshold
                )
                result["confirmed"] = True
            else:
                # 不启用确认，直接解析
                intent = self.intent_parser.intent_parser.parse(
                    instruction, 
                    self.context_manager.get()
                )
                result["confirmed"] = False
            
            # 检查用户是否取消
            if intent.get("intent") == "cancel":
                result["error"] = "用户取消操作"
                result["execution_time"] = time.time() - start_time
                logger.info("用户取消操作")
                return result
            
            result["layers"]["intent"] = {
                "parsed": intent,
                "success": True,
            }
            
            logger.info(f"意图解析结果: {intent}")
            
            # ═══════════════════════════════════════════════════
            # 第2层：屏幕感知
            # ═══════════════════════════════════════════════════
            logger.info("[第2层] 屏幕感知...")
            
            # 感知当前屏幕
            screen_state = self.screen_perceiver.perceive()
            
            result["layers"]["perception"] = {
                "active_window": screen_state.get("active_window"),
                "element_count": len(screen_state.get("elements", [])),
                "success": True,
            }
            
            logger.info(f"检测到 {len(screen_state.get('elements', []))} 个元素")
            
            # ═══════════════════════════════════════════════════
            # 第3层：操作规划
            # ═══════════════════════════════════════════════════
            logger.info("[第3层] 操作规划...")
            
            # 规划操作序列
            plan = self.action_planner.plan(intent, screen_state)
            
            result["layers"]["planning"] = {
                "action_count": len(plan.get("actions", [])),
                "actions": plan.get("actions", []),
                "success": True,
            }
            
            logger.info(f"生成 {len(plan.get('actions', []))} 个操作步骤")
            
            # ═══════════════════════════════════════════════════
            # 第4层：动作执行
            # ═══════════════════════════════════════════════════
            logger.info("[第4层] 动作执行...")
            
            execution_results = []
            
            for i, action in enumerate(plan.get("actions", [])):
                logger.info(f"执行步骤 {i+1}/{len(plan['actions'])}: {action.get('type')}")
                
                # 执行单个动作
                exec_result = self.action_executor.execute(action)
                execution_results.append(exec_result)
                
                # 如果执行失败且无法重试
                if not exec_result.get("success"):
                    logger.error(f"步骤 {i+1} 执行失败: {exec_result.get('error')}")
                    
                    # 第5层：验证反馈（失败处理）
                    verification = self.verification_manager.verify_and_retry(
                        action, 
                        exec_result, 
                        self.action_executor
                    )
                    
                    if not verification.get("success"):
                        result["error"] = f"步骤 {i+1} 执行失败: {exec_result.get('error')}"
                        break
                
                # 感知新状态
                time.sleep(self.config.ACTION_DELAY)
                screen_state = self.screen_perceiver.perceive()
            
            result["layers"]["execution"] = {
                "results": execution_results,
                "success": all(r.get("success") for r in execution_results),
            }
            
            # ═══════════════════════════════════════════════════
            # 第5层：验证反馈
            # ═══════════════════════════════════════════════════
            logger.info("[第5层] 验证反馈...")
            
            # 最终验证
            final_verification = self.verification_manager.verify_final(
                intent, 
                screen_state
            )
            
            result["layers"]["verification"] = final_verification
            
            # ═══════════════════════════════════════════════════
            # 第6层：知识记忆
            # ═══════════════════════════════════════════════════
            logger.info("[第6层] 知识记忆...")
            
            # 保存执行经验
            if final_verification.get("success"):
                self.knowledge_manager.save_experience(
                    instruction, 
                    intent, 
                    plan, 
                    execution_results
                )
            
            result["success"] = final_verification.get("success", False)
            
        except Exception as e:
            logger.error(f"执行异常: {str(e)}", exc_info=True)
            result["error"] = str(e)
            result["success"] = False
        
        # 记录执行时间
        result["execution_time"] = time.time() - start_time
        
        # 保存到历史
        self.execution_history.append(result)
        
        logger.info(f"执行完成: {'成功' if result['success'] else '失败'}, 耗时 {result['execution_time']:.2f}秒")
        
        return result
    
    def learn_from_document(self, doc_path: str) -> Dict[str, Any]:
        """从文档学习"""
        logger.info(f"从文档学习: {doc_path}")
        return self.knowledge_manager.learn_from_document(doc_path)
    
    def get_knowledge(self, software: str = None) -> Dict[str, Any]:
        """获取知识库信息"""
        return self.knowledge_manager.get_software_knowledge(software)
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """获取执行历史"""
        return self.execution_history[-limit:]
    
    def sense_screen(self) -> Dict[str, Any]:
        """感知当前屏幕（调试用）"""
        return self.screen_perceiver.perceive()
    
    def find_element(self, description: str) -> Dict[str, Any]:
        """查找元素（调试用）"""
        screen_state = self.screen_perceiver.perceive()
        return self.element_locator.locate(description, screen_state)


# 使用示例
if __name__ == "__main__":
    agent = DesktopAgent()
    
    # 执行简单任务
    result = agent.execute("点击确定按钮")
    print(json.dumps(result, ensure_ascii=False, indent=2))
