"""
Desktop Agent - Web应用（集成认证系统）
Flask + SocketIO + JWT认证
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import sys
from pathlib import Path
from functools import wraps

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import DesktopAgent
from core.config import Config
from enterprise.auth import AuthService, Permission
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


def get_agent():
    """获取Agent实例"""
    global agent
    if agent is None:
        config = Config()
        agent = DesktopAgent(config)
    return agent


def get_auth_service():
    """获取认证服务实例"""
    global auth_service
    if auth_service is None:
        auth_service = AuthService({
            'secret_key': app.config['SECRET_KEY'],
            'data_dir': 'data/auth'
        })
    return auth_service


def token_required(f):
    """Token验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # 移除 'Bearer ' 前缀
        if token.startswith('Bearer '):
            token = token[7:]
        
        auth = get_auth_service()
        result = auth.verify_token(token)
        
        if not result['success']:
            return jsonify({'error': result['message']}), 401
        
        # 将用户信息添加到请求上下文
        request.current_user = result['user']
        
        return f(*args, **kwargs)
    
    return decorated


def permission_required(permission: Permission):
    """权限验证装饰器"""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            auth = get_auth_service()
            
            if not auth.has_permission(request.current_user['role'], permission):
                return jsonify({
                    'error': f'Permission denied. Required: {permission.value}'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator


# ==================== 认证路由 ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.json
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        auth = get_auth_service()
        result = auth.register(username, email, password, role)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        logger.error(f"注册失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.json
        
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error': 'Missing username or password'}), 400
        
        auth = get_auth_service()
        result = auth.login(username, password)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    
    except Exception as e:
        logger.error(f"登录失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout():
    """用户登出"""
    try:
        token = request.headers.get('Authorization')
        if token.startswith('Bearer '):
            token = token[7:]
        
        auth = get_auth_service()
        result = auth.logout(token)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"登出失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify_token():
    """验证Token"""
    return jsonify({
        'success': True,
        'user': request.current_user
    }), 200


@app.route('/api/auth/change-password', methods=['POST'])
@token_required
def change_password():
    """修改密码"""
    try:
        data = request.json
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not all([old_password, new_password]):
            return jsonify({'error': 'Missing passwords'}), 400
        
        auth = get_auth_service()
        result = auth.change_password(
            request.current_user['user_id'],
            old_password,
            new_password
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        logger.error(f"修改密码失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/users', methods=['GET'])
@permission_required(Permission.USER_READ)
def get_users():
    """获取用户列表（需要权限）"""
    try:
        role_filter = request.args.get('role')
        
        auth = get_auth_service()
        users = auth.get_users(role_filter)
        
        return jsonify({
            'success': True,
            'users': users
        }), 200
    
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """登录页面"""
    return render_template('login.html')


# ==================== API路由 ====================

@app.route('/api/execute', methods=['POST'])
@token_required
@permission_required(Permission.TASK_EXECUTE)
def execute():
    """执行指令API（需要认证和执行权限）"""
    try:
        data = request.json
        instruction = data.get('instruction')
        
        if not instruction:
            return jsonify({"error": "缺少指令"}), 400
        
        agent = get_agent()
        result = agent.execute(instruction)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/api/sense', methods=['GET'])
@token_required
def sense():
    """感知屏幕API"""
    try:
        agent = get_agent()
        result = agent.sense_screen()
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"感知失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/api/find', methods=['POST'])
@token_required
def find():
    """查找元素API"""
    try:
        data = request.json
        description = data.get('description')
        
        if not description:
            return jsonify({"error": "缺少描述"}), 400
        
        agent = get_agent()
        result = agent.find_element(description)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"查找失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# ==================== SocketIO事件 ====================

@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    logger.info(f"客户端连接: {request.sid}")
    emit('connected', {'status': 'ok'})


@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开"""
    logger.info(f"客户端断开: {request.sid}")


@socketio.on('execute_task')
def handle_execute_task(data):
    """执行任务（SocketIO）"""
    try:
        instruction = data.get('instruction')
        token = data.get('token')
        
        # 验证Token
        auth = get_auth_service()
        result = auth.verify_token(token)
        
        if not result['success']:
            emit('error', {'message': result['message']})
            return
        
        # 检查权限
        user = result['user']
        if not auth.has_permission(user['role'], Permission.TASK_EXECUTE):
            emit('error', {'message': '权限不足'})
            return
        
        # 执行任务
        agent = get_agent()
        
        # 发送开始事件
        emit('task_started', {
            'instruction': instruction,
            'user': user['username']
        })
        
        # 执行（这里可以添加进度更新）
        result = agent.execute(instruction)
        
        # 发送完成事件
        emit('task_completed', result)
    
    except Exception as e:
        logger.error(f"任务执行失败: {e}", exc_info=True)
        emit('error', {'message': str(e)})


# ==================== 健康检查 ====================

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'version': '3.3.0',
        'features': {
            'auth': True,
            'rbac': True,
            'websocket': True
        }
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Desktop Agent Web Server (v3.3 - 认证版)")
    print("="*60)
    print()
    print("默认管理员账户：")
    print("  用户名: admin")
    print("  密码: admin123")
    print()
    print("访问地址: http://localhost:5000")
    print("="*60)
    print()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
