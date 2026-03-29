"""
Desktop Agent - 异常处理系统
智能异常分类、自动恢复、日志记录
"""

import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from loguru import logger


class ExceptionType(Enum):
    """异常类型"""
    NETWORK = "network"           # 网络异常
    ELEMENT_NOT_FOUND = "element_not_found"  # 元素定位失败
    PERMISSION = "permission"     # 权限异常
    TIMEOUT = "timeout"          # 超时异常
    SOFTWARE = "software"        # 软件异常
    DATA = "data"                # 数据异常
    UNKNOWN = "unknown"          # 未知异常


class RecoveryStrategy(Enum):
    """恢复策略"""
    RETRY = "retry"              # 重试
    DOWNGRADE = "downgrade"      # 降级执行
    ALTERNATIVE = "alternative"  # 替代方案
    USER_INTERVENTION = "user"   # 用户干预
    ABORT = "abort"              # 终止


class ExceptionHandler:
    """异常处理器"""
    
    def __init__(self, config=None):
        """初始化"""
        self.config = config or {}
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_interval = self.config.get('retry_interval', 2)
        self.enable_logging = self.config.get('enable_logging', True)
        
        # 异常历史记录
        self.exception_history: List[Dict] = []
        
        # 恢复策略映射
        self.strategy_map = {
            ExceptionType.NETWORK: [RecoveryStrategy.RETRY, RecoveryStrategy.USER_INTERVENTION],
            ExceptionType.ELEMENT_NOT_FOUND: [RecoveryStrategy.DOWNGRADE, RecoveryStrategy.ALTERNATIVE, RecoveryStrategy.USER_INTERVENTION],
            ExceptionType.PERMISSION: [RecoveryStrategy.USER_INTERVENTION, RecoveryStrategy.ABORT],
            ExceptionType.TIMEOUT: [RecoveryStrategy.RETRY, RecoveryStrategy.ALTERNATIVE],
            ExceptionType.SOFTWARE: [RecoveryStrategy.USER_INTERVENTION, RecoveryStrategy.ABORT],
            ExceptionType.DATA: [RecoveryStrategy.ALTERNATIVE, RecoveryStrategy.USER_INTERVENTION],
            ExceptionType.UNKNOWN: [RecoveryStrategy.USER_INTERVENTION, RecoveryStrategy.ABORT],
        }
        
        logger.info("异常处理系统初始化完成")
    
    def classify_exception(self, error: Exception) -> ExceptionType:
        """分类异常
        
        Args:
            error: 异常对象
            
        Returns:
            异常类型
        """
        error_str = str(error).lower()
        error_type = type(error).__name__
        
        # 网络异常
        if any(keyword in error_str for keyword in ['network', 'connection', 'timeout', 'http', 'api']):
            return ExceptionType.NETWORK
        
        # 元素定位失败
        if any(keyword in error_str for keyword in ['not found', '元素', 'element', 'locate']):
            return ExceptionType.ELEMENT_NOT_FOUND
        
        # 权限异常
        if any(keyword in error_str for keyword in ['permission', 'denied', '权限', 'access']):
            return ExceptionType.PERMISSION
        
        # 超时异常
        if any(keyword in error_str for keyword in ['timeout', '超时']):
            return ExceptionType.TIMEOUT
        
        # 软件异常
        if any(keyword in error_str for keyword in ['software', 'application', 'process', '程序']):
            return ExceptionType.SOFTWARE
        
        # 数据异常
        if any(keyword in error_str for keyword in ['data', 'format', '数据', '格式']):
            return ExceptionType.DATA
        
        # 未知异常
        return ExceptionType.UNKNOWN
    
    def get_recovery_strategies(self, exception_type: ExceptionType) -> List[RecoveryStrategy]:
        """获取恢复策略
        
        Args:
            exception_type: 异常类型
            
        Returns:
            恢复策略列表
        """
        return self.strategy_map.get(exception_type, [RecoveryStrategy.USER_INTERVENTION])
    
    def execute_recovery(
        self, 
        exception_type: ExceptionType, 
        strategy: RecoveryStrategy,
        context: Dict[str, Any],
        retry_func: Optional[callable] = None
    ) -> Dict[str, Any]:
        """执行恢复策略
        
        Args:
            exception_type: 异常类型
            strategy: 恢复策略
            context: 上下文信息
            retry_func: 重试函数
            
        Returns:
            恢复结果
        """
        result = {
            'success': False,
            'strategy': strategy.value,
            'message': '',
            'data': None
        }
        
        try:
            if strategy == RecoveryStrategy.RETRY:
                # 重试机制
                result = self._retry_execution(retry_func, context)
            
            elif strategy == RecoveryStrategy.DOWNGRADE:
                # 降级执行
                result = self._downgrade_execution(context)
            
            elif strategy == RecoveryStrategy.ALTERNATIVE:
                # 替代方案
                result = self._try_alternative(context)
            
            elif strategy == RecoveryStrategy.USER_INTERVENTION:
                # 用户干预
                result = self._request_user_intervention(context)
            
            elif strategy == RecoveryStrategy.ABORT:
                # 终止
                result = self._abort_execution(context)
        
        except Exception as e:
            logger.error(f"恢复策略执行失败: {e}")
            result['message'] = f"恢复失败: {str(e)}"
        
        return result
    
    def _retry_execution(self, retry_func: Optional[callable], context: Dict) -> Dict:
        """重试执行"""
        if not retry_func:
            return {
                'success': False,
                'message': '未提供重试函数',
                'strategy': RecoveryStrategy.RETRY.value
            }
        
        for attempt in range(self.max_retries):
            logger.info(f"第 {attempt + 1} 次重试...")
            time.sleep(self.retry_interval)
            
            try:
                result = retry_func()
                return {
                    'success': True,
                    'message': f'第 {attempt + 1} 次重试成功',
                    'data': result,
                    'strategy': RecoveryStrategy.RETRY.value
                }
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次重试失败: {e}")
                if attempt == self.max_retries - 1:
                    return {
                        'success': False,
                        'message': f'重试 {self.max_retries} 次均失败',
                        'strategy': RecoveryStrategy.RETRY.value
                    }
    
    def _downgrade_execution(self, context: Dict) -> Dict:
        """降级执行
        
        执行优先级：
        1. API级（最稳定）
        2. 控件级（较稳定）
        3. 屏幕级（最通用）
        """
        current_method = context.get('method', 'unknown')
        
        # 降级顺序
        downgrade_map = {
            'api': 'control',
            'control': 'screen',
            'screen': None
        }
        
        next_method = downgrade_map.get(current_method)
        
        if next_method:
            return {
                'success': True,
                'message': f'降级到 {next_method} 级执行',
                'data': {'method': next_method},
                'strategy': RecoveryStrategy.DOWNGRADE.value
            }
        else:
            return {
                'success': False,
                'message': '已到最低级别，无法继续降级',
                'strategy': RecoveryStrategy.DOWNGRADE.value
            }
    
    def _try_alternative(self, context: Dict) -> Dict:
        """尝试替代方案
        
        示例：
        - 点击"确定"失败 → 尝试点击"OK"
        - 输入框定位失败 → 尝试Tab键切换
        """
        alternatives = context.get('alternatives', [])
        
        if not alternatives:
            return {
                'success': False,
                'message': '无可用替代方案',
                'strategy': RecoveryStrategy.ALTERNATIVE.value
            }
        
        # 返回第一个替代方案
        return {
            'success': True,
            'message': '找到替代方案',
            'data': {'alternative': alternatives[0]},
            'strategy': RecoveryStrategy.ALTERNATIVE.value
        }
    
    def _request_user_intervention(self, context: Dict) -> Dict:
        """请求用户干预"""
        return {
            'success': False,
            'need_user_help': True,
            'message': '需要用户手动干预',
            'context': context,
            'strategy': RecoveryStrategy.USER_INTERVENTION.value
        }
    
    def _abort_execution(self, context: Dict) -> Dict:
        """终止执行"""
        return {
            'success': False,
            'message': '执行已终止',
            'strategy': RecoveryStrategy.ABORT.value
        }
    
    def log_exception(
        self, 
        error: Exception, 
        exception_type: ExceptionType,
        context: Dict,
        recovery_result: Optional[Dict] = None
    ):
        """记录异常日志
        
        Args:
            error: 异常对象
            exception_type: 异常类型
            context: 上下文信息
            recovery_result: 恢复结果
        """
        exception_record = {
            'timestamp': datetime.now().isoformat(),
            'type': exception_type.value,
            'error': str(error),
            'error_class': type(error).__name__,
            'context': context,
            'recovery': recovery_result,
            'stack_trace': self._get_stack_trace()
        }
        
        # 添加到历史
        self.exception_history.append(exception_record)
        
        # 写入日志文件
        if self.enable_logging:
            self._write_log(exception_record)
        
        logger.error(f"异常记录: {exception_type.value} - {str(error)}")
    
    def _get_stack_trace(self) -> str:
        """获取堆栈跟踪"""
        import traceback
        return traceback.format_exc()
    
    def _write_log(self, record: Dict):
        """写入日志文件"""
        try:
            log_dir = Path('data/exceptions')
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"exceptions_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        except Exception as e:
            logger.error(f"写入异常日志失败: {e}")
    
    def handle_exception(
        self, 
        error: Exception, 
        context: Dict,
        retry_func: Optional[callable] = None
    ) -> Dict[str, Any]:
        """处理异常（主入口）
        
        Args:
            error: 异常对象
            context: 上下文信息
            retry_func: 重试函数
            
        Returns:
            处理结果
        """
        # 1. 分类异常
        exception_type = self.classify_exception(error)
        logger.info(f"异常类型: {exception_type.value}")
        
        # 2. 获取恢复策略
        strategies = self.get_recovery_strategies(exception_type)
        logger.info(f"可用策略: {[s.value for s in strategies]}")
        
        # 3. 依次尝试恢复策略
        for strategy in strategies:
            logger.info(f"尝试策略: {strategy.value}")
            
            recovery_result = self.execute_recovery(
                exception_type, 
                strategy, 
                context,
                retry_func
            )
            
            # 如果成功，记录并返回
            if recovery_result.get('success'):
                self.log_exception(error, exception_type, context, recovery_result)
                return recovery_result
            
            # 如果需要用户干预，记录并返回
            if recovery_result.get('need_user_help'):
                self.log_exception(error, exception_type, context, recovery_result)
                return recovery_result
        
        # 所有策略都失败
        final_result = {
            'success': False,
            'message': '所有恢复策略均失败',
            'strategy': 'exhausted'
        }
        
        self.log_exception(error, exception_type, context, final_result)
        return final_result
    
    def get_exception_stats(self) -> Dict:
        """获取异常统计"""
        if not self.exception_history:
            return {
                'total': 0,
                'by_type': {},
                'recovery_rate': 0
            }
        
        # 按类型统计
        by_type = {}
        recovered = 0
        
        for record in self.exception_history:
            exception_type = record['type']
            by_type[exception_type] = by_type.get(exception_type, 0) + 1
            
            if record.get('recovery', {}).get('success'):
                recovered += 1
        
        return {
            'total': len(self.exception_history),
            'by_type': by_type,
            'recovery_rate': recovered / len(self.exception_history) if self.exception_history else 0
        }


# 装饰器：自动异常处理
def handle_exceptions(func):
    """异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 获取异常处理器（如果存在）
            handler = kwargs.get('exception_handler') or ExceptionHandler()
            
            # 处理异常
            result = handler.handle_exception(
                e,
                context={
                    'function': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                },
                retry_func=lambda: func(*args, **kwargs)
            )
            
            return result
    
    return wrapper


if __name__ == '__main__':
    # 测试代码
    print("\n" + "="*60)
    print("异常处理系统测试")
    print("="*60 + "\n")
    
    handler = ExceptionHandler()
    
    # 测试1：分类异常
    print("测试1：异常分类")
    errors = [
        Exception("network connection failed"),
        Exception("element not found: 确定"),
        Exception("permission denied"),
        Exception("timeout after 30 seconds"),
    ]
    
    for error in errors:
        exception_type = handler.classify_exception(error)
        print(f"  {error} → {exception_type.value}")
    
    print("\n测试2：恢复策略")
    error = Exception("element not found: 确定")
    exception_type = handler.classify_exception(error)
    strategies = handler.get_recovery_strategies(exception_type)
    print(f"  可用策略: {[s.value for s in strategies]}")
    
    print("\n测试3：降级执行")
    result = handler._downgrade_execution({'method': 'api'})
    print(f"  结果: {result}")
    
    print("\n测试4：异常统计")
    # 模拟一些异常记录
    handler.handle_exception(
        Exception("element not found"),
        context={'test': 'case1'}
    )
    handler.handle_exception(
        Exception("timeout"),
        context={'test': 'case2'}
    )
    
    stats = handler.get_exception_stats()
    print(f"  统计: {stats}")
    
    print("\n" + "="*60)
    print("✅ 测试完成")
    print("="*60 + "\n")
