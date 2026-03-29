"""
Desktop Agent - 审计日志系统
企业级操作审计、日志记录、查询导出
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import csv
from loguru import logger


class AuditAction(Enum):
    """审计操作类型"""
    # 认证相关
    LOGIN = "auth.login"
    LOGOUT = "auth.logout"
    LOGIN_FAILED = "auth.login_failed"
    PASSWORD_CHANGE = "auth.password_change"
    
    # 任务相关
    TASK_CREATE = "task.create"
    TASK_EXECUTE = "task.execute"
    TASK_CANCEL = "task.cancel"
    TASK_DELETE = "task.delete"
    
    # 模板相关
    TEMPLATE_CREATE = "template.create"
    TEMPLATE_UPDATE = "template.update"
    TEMPLATE_DELETE = "template.delete"
    
    # 用户管理
    USER_CREATE = "user.create"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"
    USER_STATUS_CHANGE = "user.status_change"
    
    # 系统相关
    SYSTEM_START = "system.start"
    SYSTEM_STOP = "system.stop"
    SYSTEM_ERROR = "system.error"
    SYSTEM_CONFIG_CHANGE = "system.config_change"


@dataclass
class AuditLog:
    """审计日志模型"""
    log_id: str
    timestamp: str
    user_id: str
    username: str
    action: str
    resource_type: str
    resource_id: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status: str = "success"  # success/failed
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'AuditLog':
        """从字典创建"""
        return AuditLog(**data)


class AuditService:
    """审计服务"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化
        
        Args:
            config: 配置信息
        """
        self.config = config or {}
        self.data_dir = Path(self.config.get('data_dir', 'data/audit'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 日志保留天数
        self.retention_days = self.config.get('retention_days', 90)
        
        # 当前日志文件
        self.current_log_file = self._get_log_file()
        
        # 内存缓存（最近1000条）
        self.cache: List[AuditLog] = []
        self.cache_size = 1000
        
        logger.info(f"审计服务初始化完成，日志目录: {self.data_dir}")
    
    def _get_log_file(self, date: Optional[datetime] = None) -> Path:
        """获取日志文件路径
        
        Args:
            date: 日期（默认今天）
            
        Returns:
            日志文件路径
        """
        if date is None:
            date = datetime.now()
        
        filename = f"audit_{date.strftime('%Y-%m-%d')}.jsonl"
        return self.data_dir / filename
    
    def _generate_log_id(self) -> str:
        """生成日志ID"""
        import secrets
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = secrets.token_urlsafe(4)
        return f"log_{timestamp}_{random_str}"
    
    def log(
        self,
        user_id: str,
        username: str,
        action: AuditAction,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None
    ) -> AuditLog:
        """记录审计日志
        
        Args:
            user_id: 用户ID
            username: 用户名
            action: 操作类型
            resource_type: 资源类型
            resource_id: 资源ID
            details: 详细信息
            ip_address: IP地址
            user_agent: User Agent
            status: 状态（success/failed）
            error_message: 错误消息
            
        Returns:
            审计日志对象
        """
        # 创建日志对象
        audit_log = AuditLog(
            log_id=self._generate_log_id(),
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            username=username,
            action=action.value,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            error_message=error_message
        )
        
        # 写入文件（JSON Lines格式）
        self._write_log(audit_log)
        
        # 添加到缓存
        self.cache.append(audit_log)
        if len(self.cache) > self.cache_size:
            self.cache.pop(0)
        
        logger.debug(f"审计日志: {username} - {action.value}")
        
        return audit_log
    
    def _write_log(self, audit_log: AuditLog):
        """写入日志文件
        
        Args:
            audit_log: 审计日志对象
        """
        try:
            # 检查是否需要切换文件（跨天）
            log_file = self._get_log_file()
            if log_file != self.current_log_file:
                self.current_log_file = log_file
                logger.info(f"切换到新日志文件: {log_file}")
            
            # 追加写入
            with open(self.current_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_log.to_dict(), ensure_ascii=False) + '\n')
        
        except Exception as e:
            logger.error(f"写入审计日志失败: {e}")
    
    def query(
        self,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        action: Optional[AuditAction] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        status: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """查询审计日志
        
        Args:
            user_id: 用户ID过滤
            username: 用户名过滤
            action: 操作类型过滤
            resource_type: 资源类型过滤
            resource_id: 资源ID过滤
            status: 状态过滤
            start_time: 开始时间
            end_time: 结束时间
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            日志列表
        """
        results = []
        
        # 确定要查询的文件
        if start_time and end_time:
            # 查询多天
            days = []
            current = start_time
            while current <= end_time:
                days.append(current)
                current += timedelta(days=1)
            
            log_files = [self._get_log_file(day) for day in days]
        else:
            # 只查询今天
            log_files = [self.current_log_file]
        
        # 读取并过滤
        for log_file in log_files:
            if not log_file.exists():
                continue
            
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            audit_log = AuditLog.from_dict(data)
                            
                            # 应用过滤条件
                            if user_id and audit_log.user_id != user_id:
                                continue
                            if username and audit_log.username != username:
                                continue
                            if action and audit_log.action != action.value:
                                continue
                            if resource_type and audit_log.resource_type != resource_type:
                                continue
                            if resource_id and audit_log.resource_id != resource_id:
                                continue
                            if status and audit_log.status != status:
                                continue
                            if start_time:
                                log_time = datetime.fromisoformat(audit_log.timestamp)
                                if log_time < start_time:
                                    continue
                            if end_time:
                                log_time = datetime.fromisoformat(audit_log.timestamp)
                                if log_time > end_time:
                                    continue
                            
                            results.append(audit_log)
                        
                        except Exception as e:
                            logger.error(f"解析日志行失败: {e}")
                            continue
            
            except Exception as e:
                logger.error(f"读取日志文件失败 {log_file}: {e}")
                continue
        
        # 按时间倒序排序
        results.sort(key=lambda x: x.timestamp, reverse=True)
        
        # 应用分页
        return results[offset:offset+limit]
    
    def get_user_activity(
        self,
        user_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """获取用户活动摘要
        
        Args:
            user_id: 用户ID
            days: 统计天数
            
        Returns:
            活动摘要
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        logs = self.query(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            limit=10000
        )
        
        # 统计
        summary = {
            'user_id': user_id,
            'period_days': days,
            'total_actions': len(logs),
            'success_count': sum(1 for log in logs if log.status == 'success'),
            'failed_count': sum(1 for log in logs if log.status == 'failed'),
            'action_breakdown': {},
            'daily_activity': {},
            'last_login': None,
            'last_action': None
        }
        
        # 操作类型统计
        for log in logs:
            action = log.action
            summary['action_breakdown'][action] = summary['action_breakdown'].get(action, 0) + 1
        
        # 每日活动统计
        for log in logs:
            date = log.timestamp.split('T')[0]
            summary['daily_activity'][date] = summary['daily_activity'].get(date, 0) + 1
        
        # 最后登录
        for log in logs:
            if log.action == AuditAction.LOGIN.value:
                summary['last_login'] = log.timestamp
                break
        
        # 最后操作
        if logs:
            summary['last_action'] = logs[0].timestamp
        
        return summary
    
    def export_csv(
        self,
        output_file: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        user_id: Optional[str] = None
    ) -> int:
        """导出为CSV
        
        Args:
            output_file: 输出文件路径
            start_time: 开始时间
            end_time: 结束时间
            user_id: 用户ID过滤
            
        Returns:
            导出记录数
        """
        logs = self.query(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            limit=100000
        )
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                if not logs:
                    return 0
                
                # 写入表头
                fieldnames = list(logs[0].to_dict().keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                # 写入数据
                for log in logs:
                    writer.writerow(log.to_dict())
            
            logger.info(f"导出审计日志到 {output_file}，共 {len(logs)} 条")
            return len(logs)
        
        except Exception as e:
            logger.error(f"导出CSV失败: {e}")
            return 0
    
    def cleanup_old_logs(self):
        """清理过期日志"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        # 查找所有日志文件
        log_files = list(self.data_dir.glob("audit_*.jsonl"))
        
        deleted_count = 0
        for log_file in log_files:
            try:
                # 从文件名提取日期
                date_str = log_file.stem.split('_')[1]
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                # 检查是否过期
                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    logger.info(f"删除过期日志: {log_file}")
            
            except Exception as e:
                logger.error(f"清理日志失败 {log_file}: {e}")
        
        if deleted_count > 0:
            logger.info(f"清理完成，删除 {deleted_count} 个过期日志文件")
    
    def get_statistics(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """获取统计数据
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            统计数据
        """
        if not start_time:
            start_time = datetime.now() - timedelta(days=7)
        if not end_time:
            end_time = datetime.now()
        
        logs = self.query(
            start_time=start_time,
            end_time=end_time,
            limit=100000
        )
        
        stats = {
            'period': {
                'start': start_time.isoformat(),
                'end': end_time.isoformat()
            },
            'total_logs': len(logs),
            'success_rate': 0,
            'action_breakdown': {},
            'user_activity': {},
            'hourly_distribution': {},
            'daily_distribution': {}
        }
        
        if logs:
            # 成功率
            success_count = sum(1 for log in logs if log.status == 'success')
            stats['success_rate'] = success_count / len(logs) * 100
            
            # 操作类型分布
            for log in logs:
                action = log.action
                stats['action_breakdown'][action] = stats['action_breakdown'].get(action, 0) + 1
            
            # 用户活动统计
            for log in logs:
                username = log.username
                stats['user_activity'][username] = stats['user_activity'].get(username, 0) + 1
            
            # 小时分布
            for log in logs:
                hour = datetime.fromisoformat(log.timestamp).hour
                stats['hourly_distribution'][hour] = stats['hourly_distribution'].get(hour, 0) + 1
            
            # 日期分布
            for log in logs:
                date = log.timestamp.split('T')[0]
                stats['daily_distribution'][date] = stats['daily_distribution'].get(date, 0) + 1
        
        return stats


# 全局审计服务实例
_audit_service: Optional[AuditService] = None


def get_audit_service() -> AuditService:
    """获取审计服务实例"""
    global _audit_service
    if _audit_service is None:
        _audit_service = AuditService()
    return _audit_service


# 便捷函数
def audit_log(
    user_id: str,
    username: str,
    action: AuditAction,
    resource_type: str,
    resource_id: str,
    **kwargs
) -> AuditLog:
    """记录审计日志（便捷函数）
    
    Args:
        user_id: 用户ID
        username: 用户名
        action: 操作类型
        resource_type: 资源类型
        resource_id: 资源ID
        **kwargs: 其他参数
        
    Returns:
        审计日志对象
    """
    service = get_audit_service()
    return service.log(
        user_id=user_id,
        username=username,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        **kwargs
    )


if __name__ == '__main__':
    # 测试代码
    print("\n" + "="*60)
    print("审计日志系统测试")
    print("="*60 + "\n")
    
    # 创建审计服务
    audit = AuditService()
    
    # 测试1：记录登录日志
    print("测试1：记录登录日志")
    log1 = audit.log(
        user_id="user_001",
        username="admin",
        action=AuditAction.LOGIN,
        resource_type="system",
        resource_id="login",
        ip_address="192.168.1.100",
        details={"method": "password"}
    )
    print(f"  ✅ 日志ID: {log1.log_id}")
    
    # 测试2：记录任务执行
    print("\n测试2：记录任务执行")
    log2 = audit.log(
        user_id="user_001",
        username="admin",
        action=AuditAction.TASK_EXECUTE,
        resource_type="task",
        resource_id="task_123",
        details={"instruction": "点击确定按钮", "duration": 2.5}
    )
    print(f"  ✅ 日志ID: {log2.log_id}")
    
    # 测试3：查询日志
    print("\n测试3：查询日志")
    logs = audit.query(username="admin", limit=10)
    print(f"  ✅ 查询到 {len(logs)} 条日志")
    for log in logs[:3]:
        print(f"    - {log.timestamp}: {log.action}")
    
    # 测试4：用户活动摘要
    print("\n测试4：用户活动摘要")
    summary = audit.get_user_activity("user_001")
    print(f"  ✅ 总操作数: {summary['total_actions']}")
    print(f"  ✅ 成功率: {summary['success_count']}/{summary['total_actions']}")
    
    # 测试5：统计数据
    print("\n测试5：统计数据")
    stats = audit.get_statistics()
    print(f"  ✅ 总日志数: {stats['total_logs']}")
    print(f"  ✅ 操作类型: {list(stats['action_breakdown'].keys())}")
    
    print("\n" + "="*60)
    print("✅ 测试完成")
    print("="*60 + "\n")
