"""
第2层：屏幕感知层 - 屏幕感知器
整合UI Automation、OCR、截图等能力
"""

from typing import Dict, Any, List, Tuple
from pathlib import Path
import time
from loguru import logger

try:
    import uiautomation as auto
    import pyautogui
    from PIL import Image
    import io
except ImportError as e:
    logger.warning(f"缺少依赖: {e}")


class ScreenPerceiver:
    """屏幕感知器"""
    
    def __init__(self, config):
        self.config = config
        
        # UI Automation
        try:
            self.root = auto.GetRootControl()
        except:
            self.root = None
            logger.warning("无法初始化UI Automation")
        
        # 屏幕尺寸
        try:
            self.screen_width, self.screen_height = pyautogui.size()
        except:
            self.screen_width, self.screen_height = 1920, 1080
            logger.warning("无法获取屏幕尺寸")
    
    def perceive(self, region: Tuple[int, int, int, int] = None) -> Dict[str, Any]:
        """
        感知当前屏幕状态
        
        Args:
            region: 感知区域 (left, top, right, bottom)
        
        Returns:
            {
                "success": True,
                "active_window": {...},
                "elements": [...],
                "screenshot": PIL.Image,
                "texts": [...],
            }
        """
        result = {
            "success": True,
            "active_window": None,
            "elements": [],
            "screenshot": None,
            "texts": [],
            "timestamp": time.time(),
        }
        
        try:
            # 1. 获取活动窗口
            result["active_window"] = self._get_active_window()
            
            # 2. 截图
            result["screenshot"] = self._capture_screen(region)
            
            # 3. 获取UI元素
            result["elements"] = self._get_ui_elements()
            
            # 4. OCR文字识别（可选）
            if self.config.OCR_ENABLED:
                result["texts"] = self._ocr_recognize(result["screenshot"])
            
        except Exception as e:
            logger.error(f"屏幕感知失败: {e}", exc_info=True)
            result["success"] = False
            result["error"] = str(e)
        
        return result
    
    def _get_active_window(self) -> Dict[str, Any]:
        """获取活动窗口信息"""
        try:
            window = auto.GetForegroundControl()
            if window:
                rect = window.BoundingRectangle
                return {
                    "title": window.Name,
                    "class_name": window.ClassName,
                    "handle": window.NativeWindowHandle,
                    "rect": (rect.left, rect.top, rect.right, rect.bottom),
                }
        except Exception as e:
            logger.warning(f"获取活动窗口失败: {e}")
        
        return None
    
    def _capture_screen(self, region: Tuple[int, int, int, int] = None) -> Image.Image:
        """捕获屏幕"""
        try:
            if region:
                left, top, right, bottom = region
                screenshot = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
            else:
                screenshot = pyautogui.screenshot()
            
            return screenshot
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    def _get_ui_elements(self) -> List[Dict[str, Any]]:
        """获取UI元素"""
        elements = []
        
        try:
            window = auto.GetForegroundControl()
            if not window:
                return elements
            
            # 可交互的控件类型
            interactive_types = {
                'ButtonControl',
                'CheckBoxControl',
                'ComboBoxControl',
                'EditControl',
                'HyperlinkControl',
                'ListItemControl',
                'MenuItemControl',
                'RadioButtonControl',
                'TextControl',
                'WindowControl',
            }
            
            def traverse(control, depth=0, max_depth=10):
                if depth > max_depth:
                    return
                
                try:
                    rect = control.BoundingRectangle
                    
                    # 过滤无效元素
                    width = rect.right - rect.left
                    height = rect.bottom - rect.top
                    
                    if width > 0 and height > 0 and control.ControlTypeName in interactive_types:
                        elements.append({
                            "type": control.ControlTypeName,
                            "name": control.Name or "",
                            "class_name": control.ClassName or "",
                            "automation_id": control.AutomationId or "",
                            "rect": (rect.left, rect.top, rect.right, rect.bottom),
                            "center": ((rect.left + rect.right) // 2, (rect.top + rect.bottom) // 2),
                            "enabled": control.IsEnabled,
                            "visible": not control.IsOffscreen,
                            "depth": depth,
                        })
                    
                    # 递归遍历子元素
                    for child in control.GetChildren():
                        traverse(child, depth + 1, max_depth)
                        
                except Exception:
                    pass  # 忽略无法访问的元素
            
            traverse(window)
            
        except Exception as e:
            logger.warning(f"获取UI元素失败: {e}")
        
        return elements
    
    def _ocr_recognize(self, screenshot: Image.Image) -> List[Dict[str, Any]]:
        """OCR文字识别"""
        texts = []
        
        try:
            from paddleocr import PaddleOCR
            
            ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
            
            # 转换为numpy数组
            import numpy as np
            img_array = np.array(screenshot)
            
            # OCR识别
            result = ocr.ocr(img_array, cls=True)
            
            if result and result[0]:
                for line in result[0]:
                    box = line[0]
                    text_info = line[1]
                    
                    texts.append({
                        "text": text_info[0],
                        "confidence": text_info[1],
                        "box": box,
                        "center": (
                            int((box[0][0] + box[2][0]) / 2),
                            int((box[0][1] + box[2][1]) / 2)
                        )
                    })
        
        except ImportError:
            logger.warning("PaddleOCR未安装，跳过OCR识别")
        except Exception as e:
            logger.warning(f"OCR识别失败: {e}")
        
        return texts
    
    def find_element_at_position(self, x: int, y: int) -> Dict[str, Any]:
        """获取指定位置的元素"""
        state = self.perceive()
        
        for element in state.get("elements", []):
            left, top, right, bottom = element["rect"]
            if left <= x <= right and top <= y <= bottom:
                return element
        
        return None
    
    def perceive_all_windows(self) -> Dict[str, Any]:
        """
        扫描所有可见窗口（改进版）
        
        Returns:
            {
                "success": True,
                "windows": [...],
                "total_count": 14,
                "active_window": {...},
            }
        """
        result = {
            "success": True,
            "windows": [],
            "total_count": 0,
            "active_window": self._get_active_window(),
            "timestamp": time.time(),
        }
        
        try:
            if not self.root:
                logger.warning("无法获取根控件")
                return result
            
            # 获取所有顶级窗口
            top_level_windows = self.root.GetChildren()
            
            for window in top_level_windows:
                try:
                    # 过滤不可见窗口
                    if window.IsOffscreen:
                        continue
                    
                    rect = window.BoundingRectangle
                    name = window.Name or ""
                    
                    # 添加到结果
                    result["windows"].append({
                        "title": name,
                        "class_name": window.ClassName,
                        "handle": window.NativeWindowHandle,
                        "rect": (rect.left, rect.top, rect.right, rect.bottom),
                        "width": rect.right - rect.left,
                        "height": rect.bottom - rect.top,
                        "enabled": window.IsEnabled,
                    })
                    
                except Exception as e:
                    logger.debug(f"跳过窗口: {e}")
                    continue
            
            result["total_count"] = len(result["windows"])
            
        except Exception as e:
            logger.error(f"扫描所有窗口失败: {e}", exc_info=True)
            result["success"] = False
            result["error"] = str(e)
        
        return result
    
    def find_window_by_title(self, keyword: str, all_windows_result=None) -> List[Dict[str, Any]]:
        """
        通过标题关键词查找窗口
        
        Args:
            keyword: 搜索关键词（如"豆包"、"记事本"）
            all_windows_result: perceive_all_windows()的结果（可选）
        
        Returns:
            [
                {
                    "title": "豆包",
                    "match_score": 1.0,
                    "window": {...}
                },
                ...
            ]
        """
        # 如果没有提供扫描结果，先扫描
        if not all_windows_result:
            all_windows_result = self.perceive_all_windows()
        
        if not all_windows_result.get("success"):
            return []
        
        windows = all_windows_result.get("windows", [])
        found_windows = []
        keyword_lower = keyword.lower()
        
        for window in windows:
            title = window.get("title", "")
            if not title:
                continue
            
            # 精确匹配
            if keyword_lower == title.lower():
                match_score = 1.0
            # 包含匹配
            elif keyword_lower in title.lower():
                match_score = 0.8
            # 模糊匹配（使用difflib）
            else:
                from difflib import SequenceMatcher
                match_score = SequenceMatcher(None, keyword_lower, title.lower()).ratio()
            
            # 只返回匹配度>=0.5的窗口
            if match_score >= 0.5:
                found_windows.append({
                    "title": title,
                    "match_score": match_score,
                    "window": window,
                })
        
        # 按匹配度排序
        found_windows.sort(key=lambda x: x["match_score"], reverse=True)
        
        return found_windows
    
    def get_window_elements(self, window_handle=None, window_title=None, max_depth=10) -> Dict[str, Any]:
        """
        获取指定窗口的UI元素
        
        Args:
            window_handle: 窗口句柄
            window_title: 窗口标题（通过标题查找）
            max_depth: 最大遍历深度
        
        Returns:
            {
                "success": True,
                "window": {...},
                "elements": [...],
                "element_count": 0,
            }
        """
        result = {
            "success": True,
            "window": None,
            "elements": [],
            "element_count": 0,
            "timestamp": time.time(),
        }
        
        try:
            # 方法1: 通过句柄获取窗口
            if window_handle:
                window = auto.ControlFromHandle(window_handle)
            # 方法2: 通过标题查找窗口
            elif window_title:
                found_windows = self.find_window_by_title(window_title)
                if found_windows:
                    handle = found_windows[0]["window"]["handle"]
                    window = auto.ControlFromHandle(handle)
                else:
                    result["success"] = False
                    result["error"] = f"未找到标题包含\"{window_title}\"的窗口"
                    return result
            else:
                result["success"] = False
                result["error"] = "必须提供window_handle或window_title"
                return result
            
            if not window:
                result["success"] = False
                result["error"] = "无法获取窗口对象"
                return result
            
            # 获取窗口信息
            rect = window.BoundingRectangle
            result["window"] = {
                "title": window.Name,
                "class_name": window.ClassName,
                "handle": window.NativeWindowHandle,
                "rect": (rect.left, rect.top, rect.right, rect.bottom),
            }
            
            # 获取UI元素
            elements = self._get_window_elements_recursive(window, max_depth)
            result["elements"] = elements
            result["element_count"] = len(elements)
            
        except Exception as e:
            logger.error(f"获取窗口UI元素失败: {e}", exc_info=True)
            result["success"] = False
            result["error"] = str(e)
        
        return result
    
    def _get_window_elements_recursive(self, window, max_depth=10) -> List[Dict[str, Any]]:
        """递归获取窗口的所有UI元素"""
        elements = []
        
        if not window:
            return elements
        
        # 可交互的控件类型
        interactive_types = {
            'ButtonControl',
            'CheckBoxControl',
            'ComboBoxControl',
            'EditControl',
            'HyperlinkControl',
            'ListItemControl',
            'MenuItemControl',
            'RadioButtonControl',
            'TextControl',
            'WindowControl',
        }
        
        def traverse(control, depth=0):
            if depth > max_depth:
                return
            
            try:
                rect = control.BoundingRectangle
                
                # 过滤无效元素
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                
                if width > 0 and height > 0 and control.ControlTypeName in interactive_types:
                    elements.append({
                        "type": control.ControlTypeName,
                        "name": control.Name or "",
                        "class_name": control.ClassName or "",
                        "automation_id": control.AutomationId or "",
                        "rect": (rect.left, rect.top, rect.right, rect.bottom),
                        "center": ((rect.left + rect.right) // 2, (rect.top + rect.bottom) // 2),
                        "enabled": control.IsEnabled,
                        "visible": not control.IsOffscreen,
                        "depth": depth,
                    })
                
                # 递归遍历子元素
                for child in control.GetChildren():
                    traverse(child, depth + 1)
                    
            except Exception:
                pass
        
        traverse(window)
        return elements
    
    def activate_window(self, window_handle=None, window_title=None) -> Dict[str, Any]:
        """
        激活指定窗口
        
        Args:
            window_handle: 窗口句柄
            window_title: 窗口标题（通过标题查找）
        
        Returns:
            {
                "success": True,
                "window": {...},
            }
        """
        result = {
            "success": True,
            "window": None,
        }
        
        try:
            # 方法1: 通过句柄激活
            if window_handle:
                window = auto.ControlFromHandle(window_handle)
            # 方法2: 通过标题查找并激活
            elif window_title:
                found_windows = self.find_window_by_title(window_title)
                if found_windows:
                    handle = found_windows[0]["window"]["handle"]
                    window = auto.ControlFromHandle(handle)
                else:
                    result["success"] = False
                    result["error"] = f"未找到标题包含\"{window_title}\"的窗口"
                    return result
            else:
                result["success"] = False
                result["error"] = "必须提供window_handle或window_title"
                return result
            
            if not window:
                result["success"] = False
                result["error"] = "无法获取窗口对象"
                return result
            
            # 激活窗口
            window.SetActive()
            
            # 获取窗口信息
            rect = window.BoundingRectangle
            result["window"] = {
                "title": window.Name,
                "class_name": window.ClassName,
                "handle": window.NativeWindowHandle,
                "rect": (rect.left, rect.top, rect.right, rect.bottom),
            }
            
        except Exception as e:
            logger.error(f"激活窗口失败: {e}", exc_info=True)
            result["success"] = False
            result["error"] = str(e)
        
        return result
