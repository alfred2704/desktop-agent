"""
Desktop Agent - 错误恢复管理器
检查点、回滚、状态恢复
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
import time
import os
from pathlib import Path
from loguru import logger


# ═══════════════════════════════════════════════════════════════
# 检查点数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class Checkpoint:
    """检查点"""
    checkpoint_id: str
    timestamp: float
    step_id: int
    action: str
    params: Dict[str, Any]
    
    # 执行前状态
    before_state: Dict[str, Any]
    
    # 执行后状态
    after_state: Optional[Dict[str, Any]] = None
    
    # 是否成功
    success: bool = False
    
    # 错误信息
    error: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# 状态快照
# ═══════════════════════════════════════════════════════════════

class StateSnapshot:
    """状态快照管理器"""
    
    def __init__(self, snapshot_dir: str = "checkpoints"):
        """
        初始化快照管理器
        
        Args:
            snapshot_dir: 快照存储目录
        """
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    def capture(self) -> Dict[str, Any]:
        """
        捕获当前状态快照
        
        Returns:
            状态快照
        """
        try:
            import pyautogui
            
            snapshot = {
                "timestamp": time.time(),
                "mouse_position": pyautogui.position(),
                "active_window": self._get_active_window(),
                "screenshot": self._capture_screenshot()
            }
            
            return snapshot
        
        except Exception as e:
            logger.warning(f"捕获状态快照失败: {e}")
            return {
                "timestamp": time.time(),
                "error": str(e)
            }
    
    def _get_active_window(self) -> Dict[str, Any]:
        """获取活动窗口信息"""
        try:
            import win32gui
            
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            
            return {
                "hwnd": hwnd,
                "title": title
            }
        
        except:
            return {}
    
    def _capture_screenshot(self) -> Optional[str]:
        """捕获屏幕截图"""
        try:
            import pyautogui
            
            screenshot = pyautogui.screenshot()
            screenshot_path = self.snapshot_dir / f"screenshot_{int(time.time())}.png"
            screenshot.save(screenshot_path)
            
            return str(screenshot_path)
        
        except Exception as e:
            logger.warning(f"捕获截图失败: {e}")
            return None


# ═══════════════════════════════════════════════════════════════
# 检查点管理器
# ═══════════════════════════════════════════════════════════════

class CheckpointManager:
    """检查点管理器"""
    
    def __init__(self, checkpoint_dir: str = "checkpoints"):
        """
        初始化检查点管理器
        
        Args:
            checkpoint_dir: 检查点存储目录
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        self.checkpoints: List[Checkpoint] = []
        self.state_snapshot = StateSnapshot(str(self.checkpoint_dir / "snapshots"))
    
    def create_checkpoint(
        self,
        step_id: int,
        action: str,
        params: Dict[str, Any],
        before_state: Optional[Dict] = None
    ) -> Checkpoint:
        """
        创建检查点
        
        Args:
            step_id: 步骤ID
            action: 动作类型
            params: 参数
            before_state: 执行前状态
        
        Returns:
            检查点对象
        """
        checkpoint_id = f"cp_{int(time.time())}_{step_id}"
        
        # 捕获执行前状态
        if before_state is None:
            before_state = self.state_snapshot.capture()
        
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            timestamp=time.time(),
            step_id=step_id,
            action=action,
            params=params,
            before_state=before_state
        )
        
        self.checkpoints.append(checkpoint)
        
        # 保存到文件
        self._save_checkpoint(checkpoint)
        
        logger.info(f"✅ 创建检查点: {checkpoint_id} (步骤{step_id})")
        
        return checkpoint
    
    def update_checkpoint(
        self,
        checkpoint_id: str,
        after_state: Dict[str, Any],
        success: bool,
        error: Optional[str] = None
    ):
        """
        更新检查点
        
        Args:
            checkpoint_id: 检查点ID
            after_state: 执行后状态
            success: 是否成功
            error: 错误信息
        """
        for cp in self.checkpoints:
            if cp.checkpoint_id == checkpoint_id:
                cp.after_state = after_state
                cp.success = success
                cp.error = error
                
                # 更新文件
                self._save_checkpoint(cp)
                
                logger.info(f"✅ 更新检查点: {checkpoint_id} (成功={success})")
                break
    
    def get_last_checkpoint(self) -> Optional[Checkpoint]:
        """获取最后一个检查点"""
        return self.checkpoints[-1] if self.checkpoints else None
    
    def get_checkpoint(self, step_id: int) -> Optional[Checkpoint]:
        """获取指定步骤的检查点"""
        for cp in self.checkpoints:
            if cp.step_id == step_id:
                return cp
        return None
    
    def _save_checkpoint(self, checkpoint: Checkpoint):
        """保存检查点到文件"""
        checkpoint_file = self.checkpoint_dir / f"{checkpoint.checkpoint_id}.json"
        
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump({
                "checkpoint_id": checkpoint.checkpoint_id,
                "timestamp": checkpoint.timestamp,
                "step_id": checkpoint.step_id,
                "action": checkpoint.action,
                "params": checkpoint.params,
                "before_state": checkpoint.before_state,
                "after_state": checkpoint.after_state,
                "success": checkpoint.success,
                "error": checkpoint.error
            }, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
# 恢复管理器
# ═══════════════════════════════════════════════════════════════

class RecoveryManager:
    """错误恢复管理器"""
    
    def __init__(self):
        """初始化恢复管理器"""
        self.checkpoint_manager = CheckpointManager()
        
        # 回滚操作映射
        self.rollback_actions = {
            "click": self._rollback_click,
            "type": self._rollback_type,
            "open_app": self._rollback_open_app,
            "save": self._rollback_save,
            "delete": self._rollback_delete
        }
    
    def recover_from_error(
        self,
        error: Exception,
        step_id: int,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        从错误中恢复
        
        Args:
            error: 错误对象
            step_id: 步骤ID
            action: 动作类型
            params: 参数
        
        Returns:
            恢复结果
        """
        logger.info(f"🔄 尝试从错误恢复: {type(error).__name__}")
        
        # 1. 获取最近的检查点
        last_checkpoint = self.checkpoint_manager.get_last_checkpoint()
        
        if not last_checkpoint:
            logger.warning("❌ 没有检查点，无法恢复")
            return {
                "success": False,
                "message": "没有检查点，无法恢复"
            }
        
        # 2. 尝试回滚
        rollback_result = self._rollback(last_checkpoint)
        
        if not rollback_result["success"]:
            logger.warning(f"❌ 回滚失败: {rollback_result['message']}")
            return rollback_result
        
        # 3. 恢复状态
        state_result = self._restore_state(last_checkpoint)
        
        if not state_result["success"]:
            logger.warning(f"❌ 状态恢复失败: {state_result['message']}")
            return state_result
        
        logger.info("✅ 成功恢复到上一个检查点")
        
        return {
            "success": True,
            "message": "成功恢复",
            "checkpoint": last_checkpoint.checkpoint_id,
            "rollback_result": rollback_result,
            "state_result": state_result
        }
    
    def _rollback(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """
        执行回滚操作
        
        Args:
            checkpoint: 检查点
        
        Returns:
            回滚结果
        """
        logger.info(f"🔙 执行回滚: {checkpoint.action}")
        
        # 获取回滚操作
        rollback_func = self.rollback_actions.get(checkpoint.action)
        
        if not rollback_func:
            logger.warning(f"⚠️  没有回滚操作: {checkpoint.action}")
            return {
                "success": False,
                "message": f"没有回滚操作: {checkpoint.action}"
            }
        
        # 执行回滚
        try:
            rollback_result = rollback_func(checkpoint)
            return {
                "success": True,
                "result": rollback_result
            }
        
        except Exception as e:
            logger.error(f"❌ 回滚失败: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    def _restore_state(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """
        恢复状态
        
        Args:
            checkpoint: 检查点
        
        Returns:
            恢复结果
        """
        logger.info("🔄 恢复状态...")
        
        try:
            before_state = checkpoint.before_state
            
            # 恢复鼠标位置
            if "mouse_position" in before_state:
                import pyautogui
                pyautogui.moveTo(*before_state["mouse_position"])
            
            # 恢复活动窗口
            if "active_window" in before_state:
                # TODO: 恢复窗口
                pass
            
            return {
                "success": True,
                "message": "状态已恢复"
            }
        
        except Exception as e:
            logger.error(f"❌ 状态恢复失败: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    # ═══════════════════════════════════════════════════════════════
    # 回滚操作实现
    # ═══════════════════════════════════════════════════════════════
    
    def _rollback_click(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """回滚点击操作"""
        # 点击操作通常不需要回滚
        return {"action": "click", "rolled_back": True}
    
    def _rollback_type(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """回滚输入操作"""
        # 输入操作：删除输入的内容
        try:
            import pyautogui
            
            # Ctrl+A全选
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # Delete删除
            pyautogui.press('delete')
            
            return {"action": "type", "rolled_back": True}
        
        except Exception as e:
            raise Exception(f"回滚输入失败: {e}")
    
    def _rollback_open_app(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """回滚打开应用"""
        # 关闭应用
        try:
            import pyautogui
            
            # Alt+F4关闭
            pyautogui.hotkey('alt', 'f4')
            
            return {"action": "open_app", "rolled_back": True}
        
        except Exception as e:
            raise Exception(f"回滚打开应用失败: {e}")
    
    def _rollback_save(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """回滚保存操作"""
        # 保存操作通常不需要回滚（或删除已保存的文件）
        return {"action": "save", "rolled_back": True}
    
    def _rollback_delete(self, checkpoint: Checkpoint) -> Dict[str, Any]:
        """回滚删除操作"""
        # 删除操作无法回滚（这是高风险操作）
        logger.warning("⚠️  删除操作无法回滚")
        return {
            "action": "delete",
            "rolled_back": False,
            "reason": "删除操作不可逆"
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n=== 错误恢复管理器测试 ===\n")
    
    manager = RecoveryManager()
    
    # 创建检查点
    print("1. 创建检查点...")
    cp = manager.checkpoint_manager.create_checkpoint(
        step_id=1,
        action="type",
        params={"text": "Hello"}
    )
    print(f"✅ 检查点已创建: {cp.checkpoint_id}")
    
    # 更新检查点
    print("\n2. 更新检查点...")
    manager.checkpoint_manager.update_checkpoint(
        cp.checkpoint_id,
        after_state={"status": "success"},
        success=True
    )
    print(f"✅ 检查点已更新")
    
    # 尝试恢复
    print("\n3. 尝试恢复...")
    result = manager.recover_from_error(
        error=Exception("测试错误"),
        step_id=2,
        action="click",
        params={"target": "确定"}
    )
    print(f"恢复结果: {result}")
    
    print("\n✅ 测试完成")
