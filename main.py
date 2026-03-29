"""
Desktop Agent - 启动脚本
快速启动Web界面或命令行
"""

import sys
import argparse
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def start_web():
    """启动Web界面"""
    print("🚀 启动 Web 界面...")
    
    from web.app import app, socketio
    from core.config import Config
    from loguru import logger
    
    config = Config()
    
    logger.info(f"访问地址: http://{config.WEB_HOST}:{config.WEB_PORT}")
    
    try:
        socketio.run(
            app,
            host=config.WEB_HOST,
            port=config.WEB_PORT,
            debug=config.DEBUG
        )
    except KeyboardInterrupt:
        logger.info("Web服务已停止")


def start_cli():
    """启动命令行界面"""
    print("💬 启动命令行界面...")
    
    from tools.cli import CLI
    
    cli = CLI()
    cli.run()


def run_quickstart():
    """运行快速开始示例"""
    print("🎯 运行快速开始示例...")
    
    from examples.quickstart import main
    
    main()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Desktop Agent - 自然语言桌面自动化")
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # Web命令
    web_parser = subparsers.add_parser('web', help='启动Web界面')
    
    # CLI命令
    cli_parser = subparsers.add_parser('cli', help='启动命令行界面')
    
    # Quickstart命令
    quick_parser = subparsers.add_parser('quickstart', help='运行快速开始示例')
    
    # 解析参数
    args = parser.parse_args()
    
    if args.command == 'web':
        start_web()
    elif args.command == 'cli':
        start_cli()
    elif args.command == 'quickstart':
        run_quickstart()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
