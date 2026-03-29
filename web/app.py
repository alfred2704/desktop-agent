"""
Desktop Agent - Web界面
Flask + SocketIO 实时交互
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import DesktopAgent
from core.config import Config
from loguru import logger


# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'desktop-agent-secret'

# 启用CORS
CORS(app)

# SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 全局Agent实例
agent = None


def get_agent():
    """获取Agent实例"""
    global agent
    if agent is None:
        config = Config()
        agent = DesktopAgent(config)
    return agent


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/execute', methods=['POST'])
def execute():
    """执行指令API"""
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


@app.route('/api/history', methods=['GET'])
def history():
    """获取历史API"""
    try:
        limit = int(request.args.get('limit', 10))
        
        agent = get_agent()
        result = agent.get_history(limit)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取历史失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/api/knowledge', methods=['GET'])
def knowledge():
    """获取知识库API"""
    try:
        software = request.args.get('software')
        
        agent = get_agent()
        result = agent.get_knowledge(software)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取知识失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# SocketIO事件
@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    logger.info(f"客户端连接: {request.sid}")
    emit('connected', {'status': 'ok'})


@socketio.on('execute')
def handle_execute(data):
    """实时执行指令"""
    try:
        instruction = data.get('instruction')
        
        if not instruction:
            emit('error', {'message': '缺少指令'})
            return
        
        agent = get_agent()
        
        # 发送开始事件
        emit('status', {'stage': 'start', 'instruction': instruction})
        
        # 执行指令
        result = agent.execute(instruction)
        
        # 发送完成事件
        emit('result', result)
    
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        emit('error', {'message': str(e)})


if __name__ == '__main__':
    config = Config()
    
    logger.info(f"启动Web服务器: http://{config.WEB_HOST}:{config.WEB_PORT}")
    
    socketio.run(
        app,
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        debug=config.DEBUG
    )
