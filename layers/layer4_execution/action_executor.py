"""
第4层：动作执行层 - 动作执行器
执行具体操作：点击、输入、快捷键等
"""

from typing import Dict, Any
import time
from loguru import logger

try:
    import pyautogui
    import pyperclip
    from PIL import Image
except ImportError as e:
    logger.warning(f"缺少依赖: {e}")


class ActionExecutor:
    """动作执行器"""
    
    def __init__(self, config):
        self.config = config
        
        # 配置pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = config.ACTION_DELAY
        
        # 屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()
    
    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个动作
        
        Args:
            action: 动作描述
        
        Returns:
            {
                "success": True,
                "action": action,
                "result": {...},
                "execution_time": 0.1
            }
        """
        start_time = time.time()
        
        action_type = action.get("type")
        
        result = {
            "success": False,
            "action": action,
            "result": None,
            "execution_time": 0,
            "error": None,
        }
        
        try:
            if action_type == "click":
                success = self._execute_click(action)
            elif action_type == "double_click":
                success = self._execute_double_click(action)
            elif action_type == "right_click":
                success = self._execute_right_click(action)
            elif action_type == "type":
                success = self._execute_type(action)
            elif action_type == "hotkey":
                success = self._execute_hotkey(action)
            elif action_type == "scroll":
                success = self._execute_scroll(action)
            elif action_type == "wait":
                success = self._execute_wait(action)
            elif action_type == "find":
                success = True  # 查找操作不执行动作
            else:
                raise ValueError(f"未知动作类型: {action_type}")
            
            result["success"] = success
            
        except Exception as e:
            logger.error(f"执行动作失败: {e}", exc_info=True)
            result["error"] = str(e)
        
        result["execution_time"] = time.time() - start_time
        
        return result
    
    def _execute_click(self, action: Dict) -> bool:
        """执行点击"""
        target = action.get("target")
        position = action.get("position")
        
        if position:
            # 直接点击坐标
            x, y = position
            pyautogui.click(x, y)
            logger.info(f"点击坐标 ({x}, {y})")
            return True
        
        elif target:
            # 需要元素定位（由调用方提供坐标）
            element = action.get("element")
            if element:
                x, y = element.get("center", (0, 0))
                pyautogui.click(x, y)
                logger.info(f"点击元素 '{target}' @ ({x}, {y})")
                return True
            else:
                logger.error(f"点击失败：未找到元素 '{target}'")
                return False
        
        return False
    
    def _execute_double_click(self, action: Dict) -> bool:
        """执行双击"""
        target = action.get("target")
        element = action.get("element")
        
        if element:
            x, y = element.get("center", (0, 0))
            pyautogui.doubleClick(x, y)
            logger.info(f"双击元素 '{target}' @ ({x}, {y})")
            return True
        
        return False
    
    def _execute_right_click(self, action: Dict) -> bool:
        """执行右键点击"""
        target = action.get("target")
        element = action.get("element")
        
        if element:
            x, y = element.get("center", (0, 0))
            pyautogui.rightClick(x, y)
            logger.info(f"右键点击元素 '{target}' @ ({x}, {y})")
            return True
        
        return False
    
    def _execute_type(self, action: Dict) -> bool:
        """执行输入"""
        text = action.get("text", "")
        clear_first = action.get("clear_first", False)
        
        if clear_first:
            # 清空并输入
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
        
        # 判断是否包含中文
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            # 使用剪贴板输入中文
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
            logger.info(f"输入中文: {text}")
        else:
            # 直接输入英文
            pyautogui.typewrite(text)
            logger.info(f"输入文本: {text}")
        
        return True
    
    def _execute_hotkey(self, action: Dict) -> bool:
        """执行快捷键"""
        keys = action.get("keys", [])
        
        if keys:
            pyautogui.hotkey(*keys)
            logger.info(f"快捷键: {'+'.join(keys)}")
            return True
        
        return False
    
    def _execute_scroll(self, action: Dict) -> bool:
        """执行滚动"""
        direction = action.get("direction", "down")
        amount = action.get("amount", 3)
        
        clicks = amount if direction == "up" else -amount
        
        pyautogui.scroll(clicks)
        logger.info(f"向{direction}滚动 {amount} 次")
        
        return True
    
    def _execute_wait(self, action: Dict) -> bool:
        """执行等待"""
        duration = action.get("duration", 1)
        
        time.sleep(duration)
        logger.info(f"等待 {duration} 秒")
        
        return True
    
    def get_cursor_position(self):
        """获取鼠标位置"""
        return pyautogui.position()
    
    def screenshot(self):
        """截图"""
        return pyautogui.screenshot()
