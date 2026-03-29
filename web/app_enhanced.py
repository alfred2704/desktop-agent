"""
Desktop Agent - 增强Web应用
集成EnhancedAuthService + 所有新功能
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import DesktopAgent
from core.config import Config
from enterprise.auth_enhanced import EnhancedAuthService
from enterprise.audit import AuditService, AuditAction
from loguru import logger


# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'desktop-agent-secret-key-change-in-production'

# 启用CORS
CORS(app)

# SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 全局实例
agent = None
auth_service = None
audit_service = None


def get_agent():
    """获取Agent实例"""
    global agent
    if agent is None:
        config = Config()
        agent = DesktopAgent(config)
    return agent


def get_auth_service():
    """获取增强认证服务实例"""
    global auth_service
    if auth_service is None:
        auth_service = EnhancedAuthService({
            'secret_key': app.config['SECRET_KEY'],
            'data_dir': 'data/auth',
            'min_password_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_digit': True,
            'require_special': False,
            'max_attempts': 5,
            'lockout_duration': 300,
            'refresh_token_expire_days': 7
        })
    return auth_service


def get_audit_service():
    """获取审计服务实例"""
    global audit_service
    if audit_service is None:
        audit_service = AuditService({
            'data_dir': 'data/audit'
        })
    return audit_service


# ==================== 认证路由（增强版） ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册（增强版：密码强度验证）"""
    try:
        data = request.json
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')
        
        if not all([username, email, password]):
            return jsonify({'error': '缺少必填字段'}), 400
        
        auth = get_auth_service()
        result = auth.register(username, email, password, role)
        
        # 记录审计日志
        audit = get_audit_service()
        if result['success']:
            audit.log(
                user_id=result.get('user_id', 'unknown'),
                username=username,
                action=AuditAction.USER_CREATE,
                resource_type='user',
                resource_id=result.get('user_id', 'unknown'),
                ip_address=request.remote_addr,
                details={'email': email, 'role': role}
            )
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        logger.error(f"注册失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录（增强版：登录限制 + 记住我）"""
    try:
        data = request.json
        
        username = data.get('username')
        password = data.get('password')
        remember_me = data.get('remember_me', False)
        
        if not all([username, password]):
            return jsonify({'error': '缺少用户名或密码'}), 400
        
        auth = get_auth_service()
        result = auth.login(username, password, remember_me)
        
        # 记录审计日志
        audit = get_audit_service()
        if result['success']:
            audit.log(
                user_id=result['user']['user_id'],
                username=username,
                action=AuditAction.LOGIN,
                resource_type='system',
                resource_id='login',
                ip_address=request.remote_addr,
                details={'remember_me': remember_me}
            )
            return jsonify(result), 200
        else:
            # 记录登录失败
            audit.log(
                user_id='unknown',
                username=username,
                action=AuditAction.LOGIN_FAILED,
                resource_type='system',
                resource_id='login',
                ip_address=request.remote_addr,
                status='failed',
                details={'reason': result['message']}
            )
            return jsonify(result), 401
    
    except Exception as e:
        logger.error(f"登录失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    """刷新Token（新增）"""
    try:
        data = request.json
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': '缺少refresh_token'}), 400
        
        auth = get_auth_service()
        result = auth.refresh_access_token(refresh_token)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    
    except Exception as e:
        logger.error(f"Token刷新失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/lockout-status', methods=['GET'])
def get_lockout_status():
    """获取账户锁定状态（新增）"""
    try:
        username = request.args.get('username')
        
        if not username:
            return jsonify({'error': '缺少用户名'}), 400
        
        auth = get_auth_service()
        status = auth.get_lockout_status(username)
        
        return jsonify(status), 200
    
    except Exception as e:
        logger.error(f"获取锁定状态失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/change-password', methods=['POST'])
def change_password():
    """修改密码（增强版：密码强度验证）"""
    try:
        # 验证token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': '未提供认证Token'}), 401
        
        token = token[7:]
        auth = get_auth_service()
        verify_result = auth.verify_token(token)
        
        if not verify_result['success']:
            return jsonify({'error': verify_result['message']}), 401
        
        user = verify_result['user']
        
        # 修改密码
        data = request.json
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not all([old_password, new_password]):
            return jsonify({'error': '缺少密码'}), 400
        
        result = auth.change_password_enhanced(
            user['user_id'],
            old_password,
            new_password
        )
        
        # 记录审计日志
        audit = get_audit_service()
        audit.log(
            user_id=user['user_id'],
            username=user['username'],
            action=AuditAction.PASSWORD_CHANGE,
            resource_type='user',
            resource_id=user['user_id'],
            ip_address=request.remote_addr,
            status='success' if result['success'] else 'failed'
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        logger.error(f"修改密码失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/password-strength', methods=['POST'])
def check_password_strength():
    """检查密码强度（新增）"""
    try:
        data = request.json
        password = data.get('password')
        
        if not password:
            return jsonify({'error': '缺少密码'}), 400
        
        auth = get_auth_service()
        result = auth.validate_password_strength(password)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"检查密码强度失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """登录页面（增强版）"""
    return render_template('login_enhanced.html')


# ==================== 健康检查 ====================

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'version': '3.3.1',
        'features': {
            'auth': True,
            'auth_enhanced': True,
            'rbac': True,
            'websocket': True,
            'remember_me': True,
            'password_strength': True,
            'login_limit': True,
            'token_refresh': True
        }
    })


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"服务器错误: {error}")
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Desktop Agent Web Server (v3.3.1 - 增强版)")
    print("="*70)
    print()
    print("✨ 新增功能：")
    print("  ✅ Token自动刷新（记住我7天）")
    print("  ✅ 密码强度验证（8位+大小写+数字）")
    print("  ✅ 登录失败限制（5次锁定5分钟）")
    print("  ✅ 前端表单验证")
    print("  ✅ 密码可见性切换")
    print("  ✅ 账户锁定提示")
    print()
    print("默认管理员账户：")
    print("  用户名: admin")
    print("  密码: admin123")
    print()
    print("访问地址: http://localhost:5000")
    print("="*70)
    print()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
