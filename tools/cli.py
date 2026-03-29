"""
Desktop Agent - 命令行工具
交互式命令行界面
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import DesktopAgent
from core.config import Config
from loguru import logger


class CLI:
    """命令行界面"""
    
    def __init__(self):
        self.config = Config()
        self.agent = DesktopAgent(self.config)
        self.running = True
        
        self.commands = {
            "help": self.cmd_help,
            "h": self.cmd_help,
            "?": self.cmd_help,
            "sense": self.cmd_sense,
            "s": self.cmd_sense,
            "find": self.cmd_find,
            "f": self.cmd_find,
            "history": self.cmd_history,
            "hist": self.cmd_history,
            "knowledge": self.cmd_knowledge,
            "kb": self.cmd_knowledge,
            "stats": self.cmd_stats,
            "quit": self.cmd_quit,
            "q": self.cmd_quit,
            "exit": self.cmd_quit,
        }
    
    def run(self):
        """运行CLI"""
        print("=" * 70)
        print("  🎯 Desktop Agent - 自然语言桌面自动化")
        print("  输入自然语言指令或命令")
        print("=" * 70)
        print()
        
        while self.running:
            try:
                cmd = input("💬 >>> ").strip()
                
                if not cmd:
                    continue
                
                # 检查是否是命令
                if cmd.startswith("/"):
                    self.execute_command(cmd[1:])
                elif cmd in self.commands:
                    self.commands[cmd]("")
                else:
                    # 执行自然语言指令
                    self.execute_instruction(cmd)
            
            except KeyboardInterrupt:
                print("\n\n使用 'quit' 退出")
            except EOFError:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    def execute_command(self, cmd: str):
        """执行命令"""
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command in self.commands:
            self.commands[command](args)
        else:
            print(f"❌ 未知命令: {command}")
            print("输入 'help' 查看命令列表")
    
    def execute_instruction(self, instruction: str):
        """执行自然语言指令"""
        print(f"\n🚀 执行: {instruction}")
        
        result = self.agent.execute(instruction)
        
        if result.get("success"):
            print(f"✅ 执行成功")
        else:
            print(f"❌ 执行失败: {result.get('error', '未知错误')}")
        
        print(f"⏱️  耗时: {result.get('execution_time', 0):.2f}秒\n")
    
    def cmd_help(self, args: str):
        """显示帮助"""
        print("""
命令列表:
  <自然语言>      执行自然语言指令
  /sense /s       感知当前屏幕
  /find <描述>    查找元素
  /history        查看执行历史
  /knowledge      查看知识库
  /stats          查看统计信息
  /help /h /?     显示帮助
  /quit /q /exit  退出

示例:
  >>> 点击确定按钮
  >>> 在搜索框输入'Python'
  >>> 按Ctrl+S
  >>> /sense
  >>> /find 确定
""")
    
    def cmd_sense(self, args: str):
        """感知屏幕"""
        print("\n👁️  感知屏幕...")
        
        result = self.agent.sense_screen()
        
        if result.get("success"):
            print(f"✓ 检测到 {len(result.get('elements', []))} 个元素")
            print(f"✓ 检测到 {len(result.get('texts', []))} 个文字")
            
            window = result.get("active_window")
            if window:
                print(f"✓ 活动窗口: {window.get('title')}")
        else:
            print(f"❌ 感知失败: {result.get('error')}")
        
        print()
    
    def cmd_find(self, args: str):
        """查找元素"""
        if not args:
            print("用法: /find <元素描述>")
            return
        
        print(f"\n🔍 查找: {args}")
        
        result = self.agent.find_element(args)
        
        if result.get("success"):
            element = result.get("element")
            print(f"✓ 找到元素:")
            print(f"  类型: {element.get('type')}")
            print(f"  名称: {element.get('name')}")
            print(f"  位置: {element.get('center')}")
        else:
            print(f"❌ 未找到: {result.get('error')}")
        
        print()
    
    def cmd_history(self, args: str):
        """查看历史"""
        print("\n📜 执行历史:")
        
        history = self.agent.get_history(10)
        
        if not history:
            print("  暂无历史记录")
        else:
            for i, record in enumerate(history, 1):
                status = "✅" if record.get("success") else "❌"
                print(f"  [{i}] {status} {record.get('instruction', '')[:50]}")
        
        print()
    
    def cmd_knowledge(self, args: str):
        """查看知识库"""
        print("\n📚 知识库信息:")
        
        kb = self.agent.get_knowledge(args if args else None)
        
        if args:
            print(json.dumps(kb, ensure_ascii=False, indent=2))
        else:
            software_list = kb.get("software_list", [])
            print(f"  已知软件: {len(software_list)} 个")
            for sw in software_list:
                print(f"    - {sw.get('name')} ({sw.get('operations_count')} 个操作)")
        
        print()
    
    def cmd_stats(self, args: str):
        """查看统计"""
        print("\n📊 统计信息:")
        
        stats = self.agent.knowledge_manager.get_statistics()
        
        print(f"  总执行次数: {len(self.agent.execution_history)}")
        print(f"  成功次数: {sum(1 for h in self.agent.execution_history if h.get('success'))}")
        print(f"  经验记忆: {stats.get('total_experiences', 0)} 条")
        print(f"  软件知识: {stats.get('software_count', 0)} 个")
        print(f"  任务模板: {stats.get('template_count', 0)} 个")
        
        print()
    
    def cmd_quit(self, args: str):
        """退出"""
        print("\n👋 再见!")
        self.running = False


def main():
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
