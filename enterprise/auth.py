"""
Desktop Agent - 企业级安全认证系统
JWT认证 + 用户管理 + RBAC权限控制
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List
import hashlib
import secrets
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# JWT相关（如果未安装，使用简单实现）
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("警告: jwt未安装，使用简化版认证")

from loguru import logger


class UserRole(Enum):
    """用户角色"""
    ADMIN = "admin"           # 管理员（100%权限）
    DEVELOPER = "developer"   # 开发者（80%权限）
    USER = "user"            # 普通用户（50%权限）
    VIEWER = "viewer"        # 观察者（20%权限）


class Permission(Enum):
    """权限定义"""
    # 任务相关
    TASK_CREATE = "task:create"
    TASK_EXECUTE = "task:execute"
    TASK_READ = "task:read"
    TASK_DELETE = "task:delete"
    
    # 模板相关
    TEMPLATE_CREATE = "template:create"
    TEMPLATE_READ = "template:read"
    TEMPLATE_UPDATE = "template:update"
    TEMPLATE_DELETE = "template:delete"
    
    # 用户管理
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    
    # 系统管理
    SYSTEM_CONFIG = "system:config"
    SYSTEM_MONITOR = "system:monitor"
    SYSTEM_LOG = "system:log"


# 角色权限映射
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.TASK_CREATE, Permission.TASK_EXECUTE, Permission.TASK_READ, Permission.TASK_DELETE,
        Permission.TEMPLATE_CREATE, Permission.TEMPLATE_READ, Permission.TEMPLATE_UPDATE, Permission.TEMPLATE_DELETE,
        Permission.USER_CREATE, Permission.USER_READ, Permission.USER_UPDATE, Permission.USER_DELETE,
        Permission.SYSTEM_CONFIG, Permission.SYSTEM_MONITOR, Permission.SYSTEM_LOG,
    ],
    UserRole.DEVELOPER: [
        Permission.TASK_CREATE, Permission.TASK_EXECUTE, Permission.TASK_READ, Permission.TASK_DELETE,
        Permission.TEMPLATE_CREATE, Permission.TEMPLATE_READ, Permission.TEMPLATE_UPDATE,
        Permission.USER_READ,
        Permission.SYSTEM_MONITOR, Permission.SYSTEM_LOG,
    ],
    UserRole.USER: [
        Permission.TASK_CREATE, Permission.TASK_EXECUTE, Permission.TASK_READ,
        Permission.TEMPLATE_CREATE, Permission.TEMPLATE_READ,
    ],
    UserRole.VIEWER: [
        Permission.TASK_READ,
        Permission.TEMPLATE_READ,
    ],
}


@dataclass
class User:
    """用户模型"""
    user_id: str
    username: str
    email: str
    password_hash: str
    salt: str
    role: str
    is_active: bool
    created_at: str
    last_login: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'User':
        """从字典创建"""
        return User(**data)


class AuthService:
    """认证服务"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化
        
        Args:
            config: 配置信息
        """
        self.config = config or {}
        self.secret_key = self.config.get('secret_key', secrets.token_urlsafe(32))
        self.token_expire_hours = self.config.get('token_expire_hours', 24)
        self.data_dir = Path(self.config.get('data_dir', 'data/auth'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 用户数据文件
        self.users_file = self.data_dir / 'users.json'
        
        # 加载用户数据
        self.users: Dict[str, User] = self._load_users()
        
        # Token黑名单（用于登出）
        self.token_blacklist: set = set()
        
        logger.info(f"认证服务初始化完成，用户数: {len(self.users)}")
    
    def _load_users(self) -> Dict[str, User]:
        """加载用户数据"""
        if not self.users_file.exists():
            # 创建默认管理员
            default_admin = self._create_default_admin()
            return {default_admin.user_id: default_admin}
        
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {user_id: User.from_dict(user_data) 
                       for user_id, user_data in data.items()}
        except Exception as e:
            logger.error(f"加载用户数据失败: {e}")
            return {}
    
    def _save_users(self):
        """保存用户数据"""
        try:
            data = {user_id: user.to_dict() 
                   for user_id, user in self.users.items()}
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"用户数据已保存，共 {len(self.users)} 个用户")
        except Exception as e:
            logger.error(f"保存用户数据失败: {e}")
    
    def _create_default_admin(self) -> User:
        """创建默认管理员"""
        user_id = self._generate_user_id()
        password = "admin123"  # 默认密码
        salt = secrets.token_urlsafe(16)
        password_hash = self._hash_password(password, salt)
        
        admin = User(
            user_id=user_id,
            username="admin",
            email="admin@example.com",
            password_hash=password_hash,
            salt=salt,
            role=UserRole.ADMIN.value,
            is_active=True,
            created_at=datetime.now().isoformat()
        )
        
        logger.warning("已创建默认管理员账户：admin / admin123")
        logger.warning("请及时修改默认密码！")
        
        return admin
    
    def _generate_user_id(self) -> str:
        """生成用户ID"""
        return f"user_{secrets.token_urlsafe(8)}"
    
    def _hash_password(self, password: str, salt: str) -> str:
        """密码加密
        
        Args:
            password: 原始密码
            salt: 盐值
            
        Returns:
            加密后的密码
        """
        # 使用 SHA256 + salt
        combined = f"{password}{salt}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """验证密码
        
        Args:
            password: 待验证密码
            password_hash: 存储的密码哈希
            salt: 盐值
            
        Returns:
            是否匹配
        """
        return self._hash_password(password, salt) == password_hash
    
    def _generate_token(self, user: User) -> str:
        """生成JWT Token
        
        Args:
            user: 用户对象
            
        Returns:
            JWT Token
        """
        payload = {
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=self.token_expire_hours),
            'iat': datetime.utcnow(),
        }
        
        if JWT_AVAILABLE:
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        else:
            # 简化版：base64编码
            import base64
            return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    
    def _verify_token(self, token: str) -> Optional[Dict]:
        """验证JWT Token
        
        Args:
            token: JWT Token
            
        Returns:
            解码后的payload，失败返回None
        """
        # 检查黑名单
        if token in self.token_blacklist:
            logger.warning("Token已被注销")
            return None
        
        try:
            if JWT_AVAILABLE:
                payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            else:
                # 简化版：base64解码
                import base64
                payload = json.loads(base64.urlsafe_b64decode(token).decode())
            
            # 检查过期时间
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                logger.warning("Token已过期")
                return None
            
            return payload
        
        except Exception as e:
            logger.error(f"Token验证失败: {e}")
            return None
    
    def register(
        self, 
        username: str, 
        email: str, 
        password: str,
        role: str = UserRole.USER.value
    ) -> Dict:
        """用户注册
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            role: 角色
            
        Returns:
            注册结果
        """
        # 检查用户名是否已存在
        for user in self.users.values():
            if user.username == username:
                return {
                    'success': False,
                    'message': '用户名已存在'
                }
            if user.email == email:
                return {
                    'success': False,
                    'message': '邮箱已被注册'
                }
        
        # 验证角色
        if role not in [r.value for r in UserRole]:
            return {
                'success': False,
                'message': f'无效的角色: {role}'
            }
        
        # 创建用户
        user_id = self._generate_user_id()
        salt = secrets.token_urlsafe(16)
        password_hash = self._hash_password(password, salt)
        
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt,
            role=role,
            is_active=True,
            created_at=datetime.now().isoformat()
        )
        
        # 保存
        self.users[user_id] = user
        self._save_users()
        
        logger.info(f"用户注册成功: {username} ({role})")
        
        return {
            'success': True,
            'message': '注册成功',
            'user_id': user_id
        }
    
    def login(self, username: str, password: str) -> Dict:
        """用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            登录结果（包含token）
        """
        # 查找用户
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            return {
                'success': False,
                'message': '用户名或密码错误'
            }
        
        # 检查账户状态
        if not user.is_active:
            return {
                'success': False,
                'message': '账户已被禁用'
            }
        
        # 验证密码
        if not self._verify_password(password, user.password_hash, user.salt):
            return {
                'success': False,
                'message': '用户名或密码错误'
            }
        
        # 生成Token
        token = self._generate_token(user)
        
        # 更新最后登录时间
        user.last_login = datetime.now().isoformat()
        self._save_users()
        
        logger.info(f"用户登录成功: {username}")
        
        return {
            'success': True,
            'message': '登录成功',
            'token': token,
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
        }
    
    def logout(self, token: str) -> Dict:
        """用户登出
        
        Args:
            token: JWT Token
            
        Returns:
            登出结果
        """
        # 加入黑名单
        self.token_blacklist.add(token)
        
        logger.info("用户已登出")
        
        return {
            'success': True,
            'message': '登出成功'
        }
    
    def verify_token(self, token: str) -> Dict:
        """验证Token
        
        Args:
            token: JWT Token
            
        Returns:
            验证结果
        """
        payload = self._verify_token(token)
        
        if not payload:
            return {
                'success': False,
                'message': 'Token无效或已过期'
            }
        
        return {
            'success': True,
            'message': 'Token有效',
            'user': payload
        }
    
    def change_password(
        self, 
        user_id: str, 
        old_password: str, 
        new_password: str
    ) -> Dict:
        """修改密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            修改结果
        """
        user = self.users.get(user_id)
        
        if not user:
            return {
                'success': False,
                'message': '用户不存在'
            }
        
        # 验证旧密码
        if not self._verify_password(old_password, user.password_hash, user.salt):
            return {
                'success': False,
                'message': '旧密码错误'
            }
        
        # 更新密码
        new_salt = secrets.token_urlsafe(16)
        new_hash = self._hash_password(new_password, new_salt)
        
        user.salt = new_salt
        user.password_hash = new_hash
        
        self._save_users()
        
        logger.info(f"用户 {user.username} 修改密码成功")
        
        return {
            'success': True,
            'message': '密码修改成功'
        }
    
    def has_permission(self, role: str, permission: Permission) -> bool:
        """检查权限
        
        Args:
            role: 用户角色
            permission: 权限
            
        Returns:
            是否有权限
        """
        try:
            user_role = UserRole(role)
            role_permissions = ROLE_PERMISSIONS.get(user_role, [])
            return permission in role_permissions
        except ValueError:
            return False
    
    def get_users(self, role_filter: Optional[str] = None) -> List[Dict]:
        """获取用户列表
        
        Args:
            role_filter: 角色过滤
            
        Returns:
            用户列表
        """
        users = []
        for user in self.users.values():
            if role_filter and user.role != role_filter:
                continue
            
            users.append({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at,
                'last_login': user.last_login,
            })
        
        return users
    
    def update_user_status(self, user_id: str, is_active: bool) -> Dict:
        """更新用户状态
        
        Args:
            user_id: 用户ID
            is_active: 是否激活
            
        Returns:
            更新结果
        """
        user = self.users.get(user_id)
        
        if not user:
            return {
                'success': False,
                'message': '用户不存在'
            }
        
        user.is_active = is_active
        self._save_users()
        
        logger.info(f"用户 {user.username} 状态更新为: {is_active}")
        
        return {
            'success': True,
            'message': '状态更新成功'
        }


# 装饰器：需要认证
def require_auth(auth_service: AuthService):
    """认证装饰器
    
    Args:
        auth_service: 认证服务实例
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 从kwargs中获取token
            token = kwargs.get('token')
            
            if not token:
                return {
                    'success': False,
                    'message': '未提供认证Token'
                }
            
            # 验证token
            result = auth_service.verify_token(token)
            
            if not result['success']:
                return result
            
            # 将用户信息传递给函数
            kwargs['current_user'] = result['user']
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# 装饰器：需要权限
def require_permission(auth_service: AuthService, permission: Permission):
    """权限装饰器
    
    Args:
        auth_service: 认证服务实例
        permission: 所需权限
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 从kwargs中获取token
            token = kwargs.get('token')
            
            if not token:
                return {
                    'success': False,
                    'message': '未提供认证Token'
                }
            
            # 验证token
            result = auth_service.verify_token(token)
            
            if not result['success']:
                return result
            
            user = result['user']
            
            # 检查权限
            if not auth_service.has_permission(user['role'], permission):
                return {
                    'success': False,
                    'message': f'权限不足，需要: {permission.value}'
                }
            
            # 将用户信息传递给函数
            kwargs['current_user'] = user
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


if __name__ == '__main__':
    # 测试代码
    print("\n" + "="*60)
    print("认证系统测试")
    print("="*60 + "\n")
    
    # 创建认证服务
    auth = AuthService()
    
    # 测试1：登录（使用默认管理员）
    print("测试1：登录")
    result = auth.login("admin", "admin123")
    print(f"  结果: {result}")
    
    if result['success']:
        token = result['token']
        
        # 测试2：验证Token
        print("\n测试2：验证Token")
        verify_result = auth.verify_token(token)
        print(f"  结果: {verify_result}")
        
        # 测试3：检查权限
        print("\n测试3：检查权限")
        has_perm = auth.has_permission("admin", Permission.TASK_CREATE)
        print(f"  admin 有 task:create 权限: {has_perm}")
        
        has_perm2 = auth.has_permission("viewer", Permission.TASK_CREATE)
        print(f"  viewer 有 task:create 权限: {has_perm2}")
        
        # 测试4：登出
        print("\n测试4：登出")
        logout_result = auth.logout(token)
        print(f"  结果: {logout_result}")
        
        # 测试5：使用已登出的Token
        print("\n测试5：使用已登出的Token")
        verify_result2 = auth.verify_token(token)
        print(f"  结果: {verify_result2}")
    
    # 测试6：注册新用户
    print("\n测试6：注册新用户")
    register_result = auth.register(
        username="test_user",
        email="test@example.com",
        password="test123",
        role="user"
    )
    print(f"  结果: {register_result}")
    
    # 测试7：获取用户列表
    print("\n测试7：获取用户列表")
    users = auth.get_users()
    print(f"  用户数: {len(users)}")
    for user in users:
        print(f"    - {user['username']} ({user['role']})")
    
    print("\n" + "="*60)
    print("✅ 测试完成")
    print("="*60 + "\n")
