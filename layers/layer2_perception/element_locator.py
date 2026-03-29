"""
第2层：屏幕感知层 - 元素定位器
通过描述定位UI元素
"""

from typing import Dict, Any, List
from loguru import logger
from difflib import SequenceMatcher


class ElementLocator:
    """元素定位器"""
    
    def __init__(self, config):
        self.config = config
    
    def locate(self, description: str, screen_state: Dict) -> Dict[str, Any]:
        """
        通过描述定位元素
        
        Args:
            description: 元素描述（如"确定按钮"、"搜索框"）
            screen_state: 屏幕状态
        
        Returns:
            {
                "success": True,
                "element": {...},
                "method": "exact/fuzzy/ocr",
                "confidence": 0.9
            }
        """
        elements = screen_state.get("elements", [])
        texts = screen_state.get("texts", [])
        
        # 方法1：精确匹配
        element = self._exact_match(description, elements)
        if element:
            return {
                "success": True,
                "element": element,
                "method": "exact",
                "confidence": 1.0,
            }
        
        # 方法2：模糊匹配
        element = self._fuzzy_match(description, elements)
        if element:
            return {
                "success": True,
                "element": element,
                "method": "fuzzy",
                "confidence": 0.8,
            }
        
        # 方法3：OCR文字定位
        element = self._ocr_match(description, texts, elements)
        if element:
            return {
                "success": True,
                "element": element,
                "method": "ocr",
                "confidence": 0.7,
            }
        
        return {
            "success": False,
            "error": f"未找到元素: {description}",
        }
    
    def _exact_match(self, description: str, elements: List[Dict]) -> Dict:
        """精确匹配"""
        description_lower = description.lower()
        
        for element in elements:
            name = element.get("name", "").lower()
            
            if description_lower == name:
                return element
        
        return None
    
    def _fuzzy_match(self, description: str, elements: List[Dict]) -> Dict:
        """模糊匹配"""
        best_match = None
        best_score = 0.6  # 最低匹配阈值
        
        for element in elements:
            name = element.get("name", "")
            
            if not name:
                continue
            
            # 计算相似度
            score = SequenceMatcher(None, description.lower(), name.lower()).ratio()
            
            # 检查是否包含
            if description.lower() in name.lower():
                score = max(score, 0.8)
            
            if name.lower() in description.lower():
                score = max(score, 0.75)
            
            if score > best_score:
                best_score = score
                best_match = element
        
        return best_match
    
    def _ocr_match(self, description: str, texts: List[Dict], elements: List[Dict]) -> Dict:
        """通过OCR文字定位元素"""
        description_lower = description.lower()
        
        for text_info in texts:
            text = text_info.get("text", "").lower()
            
            if description_lower in text or text in description_lower:
                # 找到匹配的文字，尝试关联到最近的元素
                text_center = text_info.get("center")
                
                if text_center:
                    # 找最近的元素
                    closest_element = self._find_closest_element(text_center, elements)
                    if closest_element:
                        return closest_element
        
        return None
    
    def _find_closest_element(self, position: tuple, elements: List[Dict]) -> Dict:
        """找到距离指定位置最近的元素"""
        if not elements:
            return None
        
        x, y = position
        min_distance = float('inf')
        closest_element = None
        
        for element in elements:
            center = element.get("center", (0, 0))
            distance = ((center[0] - x) ** 2 + (center[1] - y) ** 2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_element = element
        
        # 只返回距离足够近的元素（100像素内）
        if min_distance < 100:
            return closest_element
        
        return None
    
    def locate_by_type(self, element_type: str, screen_state: Dict) -> List[Dict]:
        """通过类型定位所有元素"""
        elements = screen_state.get("elements", [])
        
        type_map = {
            "按钮": "ButtonControl",
            "输入框": "EditControl",
            "菜单": "MenuItemControl",
            "列表": "ListControl",
            "复选框": "CheckBoxControl",
            "单选框": "RadioButtonControl",
            "文本": "TextControl",
        }
        
        target_type = type_map.get(element_type, element_type)
        
        return [
            el for el in elements
            if el.get("type") == target_type
        ]
