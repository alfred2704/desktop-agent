"""
Desktop Agent - 分级错误处理系统
L1/L2/L3三级错误处理机制
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import time
import traceback
from loguru import logger


# ═══════════════════════════════════════════════════════════════
# 错误级别定义
# ═══════════════════════════════════════════════════════════════

class ErrorLevel(Enum):
    """错误级别"""
    L1_RECOVERABLE = "L1"     # 可重试错误
    L2_RECOVERABLE = "L2"     # 可恢复错误
    L3_FATAL = "L3"           # 致命错误


@dataclass
class ErrorContext:
    """错误上下文"""
    error_level: ErrorLevel
    error_type: str
    error_message: str
    timestamp: float
    step_id: Optional[int] = None
    action: Optional[str] = None
    params: Optional[Dict] = None
    retry_count: int = 0
    stack_trace: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "error_level": self.error_level.value,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "timestamp": self.timestamp,
            "step_id": self.step_id,
            "action": self.action,
            "params": self.params,
            "retry_count": self.retry_count,
            "stack_trace": self.stack_trace
        }


# ═══════════════════════════════════════════════════════════════
# 错误分类器
# ═══════════════════════════════════════════════════════════════

class ErrorClassifier:
    """错误分类器"""
    
    # L1: 可重试错误（自动重试）
    L1_ERRORS = [
        "TimeoutError",
        "ElementNotFoundError",
        "StaleElementReferenceException",
        "WebDriverException",
        "ConnectionError",
        "NetworkError",
        "TemporaryFailure"
    ]
    
    # L2: 可恢复错误（需要处理）
    L2_ERRORS = [
        "PermissionError",
        "FileNotFoundError",
        "FileInUseError",
        "ApplicationNotRespondingError",
        "ValidationError",
        "InsufficientResourcesError"
    ]
    
    # L3: 致命错误（无法恢复）
    L3_ERRORS = [
        "SystemCrashError",
        "CriticalResourceMissingError",
        "UnrecoverableStateError",
        "SecurityViolationError",
        "DataCorruptionError"
    ]
    
    @classmethod
    def classify(cls, error: Exception) -> ErrorLevel:
        """
        分类错误级别
        
        Args:
            error: 异常对象
        
        Returns:
            错误级别
        """
        error_type = type(error).__name__
        
        # 检查L1错误
        if error_type in cls.L1_ERRORS:
            return ErrorLevel.L1_RECOVERABLE
        
        # 检查L2错误
        if error_type in cls.L2_ERRORS:
            return ErrorLevel.L2_RECOVERABLE
        
        # 检查L3错误
        if error_type in cls.L3_ERRORS:
            return ErrorLevel.L3_FATAL
        
        # 默认为L2
        return ErrorLevel.L2_RECOVERABLE
    
    @classmethod
    def create_context(
        cls,
        error: Exception,
        step_id: Optional[int] = None,
        action: Optional[str] = None,
        params: Optional[Dict] = None,
        retry_count: int = 0
    ) -> ErrorContext:
        """
        创建错误上下文
        
        Args:
            error: 异常对象
            step_id: 步骤ID
            action: 动作类型
            params: 参数
            retry_count: 重试次数
        
        Returns:
            错误上下文
        """
        error_level = cls.classify(error)
        
        return ErrorContext(
            error_level=error_level,
            error_type=type(error).__name__,
            error_message=str(error),
            timestamp=time.time(),
            step_id=step_id,
            action=action,
            params=params,
            retry_count=retry_count,
            stack_trace=traceback.format_exc()
        )


# ═══════════════════════════════════════════════════════════════
# 分级错误处理器
# ═══════════════════════════════════════════════════════════════

class HierarchicalErrorHandler:
    """分级错误处理器"""
    
    def __init__(self, config):
        self.config = config
        
        # 重试配置
        self.max_retries = 3
        self.initial_wait = 1.0  # 秒
        self.max_wait = 30.0     # 秒
        self.exponential_base = 2.0
        
        # 错误历史
        self.error_history: List[ErrorContext] = []
    
    def handle(
        self,
        error: Exception,
        step_id: Optional[int] = None,
        action: Optional[str] = None,
        params: Optional[Dict] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        处理错误（根据级别）
        
        Args:
            error: 异常对象
            step_id: 步骤ID
            action: 动作类型
            params: 参数
            retry_count: 当前重试次数
        
        Returns:
            处理结果
        """
        # 创建错误上下文
        error_context = ErrorClassifier.create_context(
            error, step_id, action, params, retry_count
        )
        
        # 记录错误
        self.error_history.append(error_context)
        logger.error(f"[{error_context.error_level.value}] {error_context.error_type}: {error_context.error_message}")
        
        # 根据级别处理
        if error_context.error_level == ErrorLevel.L1_RECOVERABLE:
            return self._handle_l1(error_context)
        
        elif error_context.error_level == ErrorLevel.L2_RECOVERABLE:
            return self._handle_l2(error_context)
        
        else:  # L3
            return self._handle_l3(error_context)
    
    def _handle_l1(self, error_context: ErrorContext) -> Dict[str, Any]:
        """
        处理L1错误：自动重试
        
        策略：
        - 指数退避重试
        - 最多3次
        - 自动恢复
        """
        logger.info(f"[L1] 处理可重试错误（第{error_context.retry_count}次）")
        
        # 检查是否超过最大重试次数
        if error_context.retry_count >= self.max_retries:
            logger.error(f"[L1] 已达最大重试次数 {self.max_retries}，升级为L2")
            # 升级为L2
            error_context.error_level = ErrorLevel.L2_RECOVERABLE
            return self._handle_l2(error_context)
        
        # 计算等待时间（指数退避）
        wait_time = min(
            self.initial_wait * (self.exponential_base ** error_context.retry_count),
            self.max_wait
        )
        
        logger.info(f"[L1] 等待 {wait_time:.1f} 秒后重试...")
        time.sleep(wait_time)
        
        return {
            "success": False,
            "action": "retry",
            "retry_count": error_context.retry_count + 1,
            "wait_time": wait_time,
            "error_context": error_context.to_dict(),
            "message": f"将进行第{error_context.retry_count + 1}次重试"
        }
    
    def _handle_l2(self, error_context: ErrorContext) -> Dict[str, Any]:
        """
        处理L2错误：尝试恢复
        
        策略：
        - 分析错误原因
        - 尝试恢复操作
        - 需要用户确认
        """
        logger.warning(f"[L2] 处理可恢复错误")
        
        # 根据错误类型制定恢复策略
        recovery_strategy = self._get_recovery_strategy(error_context)
        
        logger.info(f"[L2] 恢复策略: {recovery_strategy['strategy']}")
        
        return {
            "success": False,
            "action": "recover",
            "recovery_strategy": recovery_strategy,
            "error_context": error_context.to_dict(),
            "needs_user_input": recovery_strategy.get("needs_user_input", False),
            "message": f"需要执行恢复操作: {recovery_strategy['strategy']}"
        }
    
    def _handle_l3(self, error_context: ErrorContext) -> Dict[str, Any]:
        """
        处理L3错误：停止执行
        
        策略：
        - 立即停止
        - 生成详细报告
        - 人工介入
        """
        logger.critical(f"[L3] 处理致命错误，停止执行")
        
        # 生成错误报告
        error_report = self._generate_error_report(error_context)
        
        return {
            "success": False,
            "action": "abort",
            "error_context": error_context.to_dict(),
            "error_report": error_report,
            "needs_manual_intervention": True,
            "message": "致命错误，需要人工介入"
        }
    
    def _get_recovery_strategy(self, error_context: ErrorContext) -> Dict:
        """获取恢复策略"""
        
        error_type = error_context.error_type
        
        strategies = {
            "PermissionError": {
                "strategy": "request_permission",
                "description": "请求权限",
                "needs_user_input": True,
                "steps": [
                    "检查当前用户权限",
                    "提示用户授权",
                    "重试操作"
                ]
            },
            
            "FileNotFoundError": {
                "strategy": "create_file",
                "description": "创建缺失文件",
                "needs_user_input": False,
                "steps": [
                    "检查文件路径",
                    "创建必要的目录",
                    "创建空文件",
                    "重试操作"
                ]
            },
            
            "FileInUseError": {
                "strategy": "wait_and_retry",
                "description": "等待文件释放",
                "needs_user_input": False,
                "steps": [
                    "等待5秒",
                    "检查文件状态",
                    "重试操作"
                ]
            },
            
            "ApplicationNotRespondingError": {
                "strategy": "restart_app",
                "description": "重启应用",
                "needs_user_input": True,
                "steps": [
                    "关闭无响应应用",
                    "重新启动应用",
                    "等待应用就绪",
                    "重试操作"
                ]
            },
            
            "ValidationError": {
                "strategy": "fix_params",
                "description": "修正参数",
                "needs_user_input": True,
                "steps": [
                    "分析参数错误",
                    "提示用户修正",
                    "使用修正后的参数重试"
                ]
            }
        }
        
        # 返回对应策略，或默认策略
        return strategies.get(error_type, {
            "strategy": "generic_recovery",
            "description": "通用恢复",
            "needs_user_input": True,
            "steps": [
                "分析错误原因",
                "尝试自动修复",
                "如无法修复，请求用户帮助"
            ]
        })
    
    def _generate_error_report(self, error_context: ErrorContext) -> Dict:
        """生成错误报告"""
        
        return {
            "error_level": error_context.error_level.value,
            "error_type": error_context.error_type,
            "error_message": error_context.error_message,
            "timestamp": error_context.timestamp,
            "step_id": error_context.step_id,
            "action": error_context.action,
            "params": error_context.params,
            "retry_count": error_context.retry_count,
            "stack_trace": error_context.stack_trace,
            "suggested_actions": self._get_suggested_actions(error_context),
            "contact_support": True
        }
    
    def _get_suggested_actions(self, error_context: ErrorContext) -> List[str]:
        """获取建议操作"""
        
        return [
            f"1. 检查错误类型: {error_context.error_type}",
            f"2. 查看错误消息: {error_context.error_message}",
            "3. 检查相关参数是否正确",
            "4. 确认环境配置",
            "5. 联系技术支持"
        ]
    
    def get_error_stats(self) -> Dict:
        """获取错误统计"""
        
        if not self.error_history:
            return {
                "total_errors": 0,
                "by_level": {},
                "by_type": {}
            }
        
        # 按级别统计
        by_level = {}
        for error in self.error_history:
            level = error.error_level.value
            by_level[level] = by_level.get(level, 0) + 1
        
        # 按类型统计
        by_type = {}
        for error in self.error_history:
            error_type = error.error_type
            by_type[error_type] = by_type.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "by_level": by_level,
            "by_type": by_type
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from core.config import Config
    
    config = Config()
    handler = HierarchicalErrorHandler(config)
    
    # 测试L1错误
    print("\n=== 测试L1错误（超时）===")
    try:
        raise TimeoutError("元素定位超时")
    except Exception as e:
        result = handler.handle(e, step_id=1, action="click", params={"target": "确定"})
        print(f"处理结果: {result}")
    
    # 测试L2错误
    print("\n=== 测试L2错误（权限不足）===")
    try:
        raise PermissionError("无法访问文件")
    except Exception as e:
        result = handler.handle(e, step_id=2, action="save", params={"file": "test.txt"})
        print(f"处理结果: {result}")
    
    # 测试L3错误
    print("\n=== 测试L3错误（系统崩溃）===")
    try:
        raise Exception("SystemCrashError")
    except Exception as e:
        result = handler.handle(e, step_id=3, action="open_app", params={"app": "Word"})
        print(f"处理结果: {result}")
    
    # 查看统计
    print("\n=== 错误统计 ===")
    stats = handler.get_error_stats()
    print(json.dumps(stats, indent=2))
