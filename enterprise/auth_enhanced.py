"""
Desktop Agent - 增强认证系统
Token刷新 + 密码强度验证 + 登录失败限制
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List
import re
from collections import defaultdict
import time

from enterprise.auth import AuthService, User
from loguru import logger


class EnhancedAuthService(AuthService):
    """增强认证服务"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化
        
        Args:
            config: 配置信息
        """
        super().__init__(config)
        
        # 登录失败记录
        self.login_attempts: Dict[str, List[float]] = defaultdict(list)
        self.max_attempts = self.config.get('max_attempts', 5)
        self.lockout_duration = self.config.get('lockout_duration', 300)  # 5分钟
        
        # Token刷新配置
        self.refresh_token_expire_days = self.config.get('refresh_token_expire_days', 7)
        
        # 密码强度配置
        self.min_password_length = self.config.get('min_password_length', 8)
        self.require_uppercase = self.config.get('require_uppercase', True)
        self.require_lowercase = self.config.get('require_lowercase', True)
        self.require_digit = self.config.get('require_digit', True)
        self.require_special = self.config.get('require_special', False)
        
        logger.info("增强认证服务初始化完成")
    
    # ==================== 密码强度验证 ====================
    
    def validate_password_strength(self, password: str) -> Dict:
        """验证密码强度
        
        Args:
            password: 密码
            
        Returns:
            验证结果
        """
        errors = []
        
        # 长度检查
        if len(password) < self.min_password_length:
            errors.append(f"密码至少需要 {self.min_password_length} 个字符")
        
        # 大写字母
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("密码需要包含至少一个大写字母")
        
        # 小写字母
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("密码需要包含至少一个小写字母")
        
        # 数字
        if self.require_digit and not re.search(r'\d', password):
            errors.append("密码需要包含至少一个数字")
        
        # 特殊字符
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("密码需要包含至少一个特殊字符")
        
        # 常见弱密码检查
        weak_passwords = [
            'password', '123456', 'admin', 'root', 'user',
            'login', 'welcome', 'monkey', 'dragon'
        ]
        if password.lower() in weak_passwords:
            errors.append("密码过于简单，请使用更强的密码")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'strength': self._calculate_strength(password)
        }
    
    def _calculate_strength(self, password: str) -> str:
        """计算密码强度
        
        Args:
            password: 密码
            
        Returns:
            强度等级（weak/medium/strong/very_strong）
        """
        score = 0
        
        # 长度加分
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        # 复杂度加分
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 2
        
        # 评分
        if score < 3:
            return 'weak'
        elif score < 5:
            return 'medium'
        elif score < 7:
            return 'strong'
        else:
            return 'very_strong'
    
    # ==================== 登录失败限制 ====================
    
    def _check_login_attempts(self, username: str) -> Dict:
        """检查登录尝试次数
        
        Args:
            username: 用户名
            
        Returns:
            检查结果
        """
        current_time = time.time()
        
        # 清理过期记录
        attempts = self.login_attempts[username]
        self.login_attempts[username] = [
            t for t in attempts 
            if current_time - t < self.lockout_duration
        ]
        
        # 检查是否被锁定
        if len(self.login_attempts[username]) >= self.max_attempts:
            oldest_attempt = min(self.login_attempts[username])
            remaining_time = int(self.lockout_duration - (current_time - oldest_attempt))
            
            return {
                'allowed': False,
                'remaining_time': remaining_time,
                'message': f"账户已锁定，请在 {remaining_time} 秒后重试"
            }
        
        return {
            'allowed': True,
            'remaining_attempts': self.max_attempts - len(self.login_attempts[username])
        }
    
    def _record_failed_attempt(self, username: str):
        """记录失败尝试
        
        Args:
            username: 用户名
        """
        self.login_attempts[username].append(time.time())
        logger.warning(f"登录失败记录: {username}, 尝试次数: {len(self.login_attempts[username])}")
    
    def _clear_failed_attempts(self, username: str):
        """清除失败记录
        
        Args:
            username: 用户名
        """
        if username in self.login_attempts:
            del self.login_attempts[username]
    
    # ==================== Token刷新机制 ====================
    
    def generate_refresh_token(self, user: User) -> str:
        """生成刷新Token
        
        Args:
            user: 用户对象
            
        Returns:
            刷新Token
        """
        payload = {
            'user_id': user.user_id,
            'username': user.username,
            'type': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=self.refresh_token_expire_days),
            'iat': datetime.utcnow(),
        }
        
        if self.__class__.__bases__[0].JWT_AVAILABLE if hasattr(self.__class__.__bases__[0], 'JWT_AVAILABLE') else False:
            import jwt
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        else:
            import base64
            return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    
    def refresh_access_token(self, refresh_token: str) -> Dict:
        """刷新访问Token
        
        Args:
            refresh_token: 刷新Token
            
        Returns:
            新的访问Token
        """
        # 验证刷新Token
        payload = self._verify_token(refresh_token)
        
        if not payload:
            return {
                'success': False,
                'message': '刷新Token无效或已过期'
            }
        
        # 检查Token类型
        if payload.get('type') != 'refresh':
            return {
                'success': False,
                'message': '不是刷新Token'
            }
        
        # 获取用户
        user_id = payload['user_id']
        user = self.users.get(user_id)
        
        if not user:
            return {
                'success': False,
                'message': '用户不存在'
            }
        
        if not user.is_active:
            return {
                'success': False,
                'message': '账户已被禁用'
            }
        
        # 生成新的访问Token
        new_token = self._generate_token(user)
        
        return {
            'success': True,
            'token': new_token,
            'message': 'Token刷新成功'
        }
    
    # ==================== 重写注册和登录方法 ====================
    
    def register(
        self, 
        username: str, 
        email: str, 
        password: str,
        role: str = 'user'
    ) -> Dict:
        """用户注册（增强版：密码强度验证）
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            role: 角色
            
        Returns:
            注册结果
        """
        # 密码强度验证
        strength_check = self.validate_password_strength(password)
        
        if not strength_check['valid']:
            return {
                'success': False,
                'message': '密码强度不足',
                'errors': strength_check['errors'],
                'strength': strength_check['strength']
            }
        
        # 调用父类注册
        result = super().register(username, email, password, role)
        
        # 添加密码强度信息
        if result['success']:
            result['password_strength'] = strength_check['strength']
        
        return result
    
    def login(self, username: str, password: str, remember_me: bool = False) -> Dict:
        """用户登录（增强版：登录限制 + 记住我）
        
        Args:
            username: 用户名
            password: 密码
            remember_me: 记住我
            
        Returns:
            登录结果
        """
        # 检查登录尝试次数
        attempt_check = self._check_login_attempts(username)
        
        if not attempt_check['allowed']:
            return {
                'success': False,
                'message': attempt_check['message'],
                'remaining_time': attempt_check['remaining_time']
            }
        
        # 调用父类登录
        result = super().login(username, password)
        
        if result['success']:
            # 清除失败记录
            self._clear_failed_attempts(username)
            
            # 添加记住我功能
            if remember_me:
                user = self.users.get(result['user']['user_id'])
                if user:
                    refresh_token = self.generate_refresh_token(user)
                    result['refresh_token'] = refresh_token
                    result['refresh_expires_days'] = self.refresh_token_expire_days
            
            # 添加剩余尝试次数
            result['remaining_attempts'] = self.max_attempts
        else:
            # 记录失败尝试
            self._record_failed_attempt(username)
            
            # 添加剩余尝试次数
            result['remaining_attempts'] = attempt_check['remaining_attempts'] - 1
            
            if result['remaining_attempts'] <= 0:
                result['message'] = '登录失败次数过多，账户已锁定5分钟'
        
        return result
    
    # ==================== 新增API ====================
    
    def change_password_enhanced(
        self,
        user_id: str,
        old_password: str,
        new_password: str
    ) -> Dict:
        """修改密码（增强版：密码强度验证）
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            修改结果
        """
        # 密码强度验证
        strength_check = self.validate_password_strength(new_password)
        
        if not strength_check['valid']:
            return {
                'success': False,
                'message': '新密码强度不足',
                'errors': strength_check['errors'],
                'strength': strength_check['strength']
            }
        
        # 调用父类修改密码
        result = super().change_password(user_id, old_password, new_password)
        
        # 添加密码强度信息
        if result['success']:
            result['password_strength'] = strength_check['strength']
        
        return result
    
    def get_lockout_status(self, username: str) -> Dict:
        """获取锁定状态
        
        Args:
            username: 用户名
            
        Returns:
            锁定状态
        """
        attempt_check = self._check_login_attempts(username)
        
        return {
            'is_locked': not attempt_check['allowed'],
            'remaining_time': attempt_check.get('remaining_time', 0),
            'remaining_attempts': attempt_check.get('remaining_attempts', self.max_attempts),
            'max_attempts': self.max_attempts
        }


# 测试代码
if __name__ == '__main__':
    print("\n" + "="*60)
    print("增强认证系统测试")
    print("="*60 + "\n")
    
    # 创建增强认证服务
    auth = EnhancedAuthService({
        'data_dir': 'data/test_enhanced_auth',
        'min_password_length': 8,
        'require_special': False
    })
    
    # 测试1：密码强度验证
    print("测试1：密码强度验证")
    passwords = [
        '123456',          # 太弱
        'password',        # 弱
        'Password1',       # 中等
        'Password123!',    # 强
    ]
    
    for pwd in passwords:
        result = auth.validate_password_strength(pwd)
        print(f"  {pwd:20s} -> {result['strength']:12s} {result['errors']}")
    
    # 测试2：注册（密码强度验证）
    print("\n测试2：注册（密码强度验证）")
    result = auth.register("test_enhanced", "test@example.com", "123456")
    print(f"  弱密码注册: {result['message']}")
    
    result2 = auth.register("test_enhanced", "test@example.com", "StrongPass123")
    print(f"  强密码注册: {result2['message']}, 强度: {result2.get('password_strength')}")
    
    # 测试3：登录失败限制
    print("\n测试3：登录失败限制")
    for i in range(6):
        result = auth.login("admin", "wrong_password")
        print(f"  第{i+1}次失败: {result['message']}, 剩余次数: {result.get('remaining_attempts', 0)}")
    
    # 测试4：锁定状态
    print("\n测试4：锁定状态")
    status = auth.get_lockout_status("admin")
    print(f"  是否锁定: {status['is_locked']}, 剩余时间: {status['remaining_time']}秒")
    
    print("\n" + "="*60)
    print("✅ 测试完成")
    print("="*60 + "\n")
