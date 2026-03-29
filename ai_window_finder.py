"""
AI驱动的智能窗口查找
结合意图理解层(L1)和屏幕感知层(L2)
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer2_perception.screen_perceiver import ScreenPerceiver
from core.config import Config
import time

class AIWindowFinder:
    """AI驱动的窗口查找器"""
    
    def __init__(self):
        self.config = Config()
        self.perceiver = ScreenPerceiver(self.config)
    
    def find_window_with_ai(self, user_intent: str) -> dict:
        """
        AI驱动的窗口查找
        
        Args:
            user_intent: 用户意图（如"找到豆包窗口"、"打开记事本"）
        
        Returns:
            {
                "success": True,
                "window": {...},
                "ai_analysis": {...},
                "search_strategies": [...],
            }
        """
        result = {
            "success": False,
            "window": None,
            "ai_analysis": None,
            "search_strategies": [],
        }
        
        print("="*70)
        print(f"  AI窗口查找: {user_intent}")
        print("="*70)
        print()
        
        # 步骤1: AI理解用户意图
        print("[步骤1] AI理解用户意图...")
        print("-" * 70)
        print()
        
        ai_analysis = self._ai_understand_intent(user_intent)
        result["ai_analysis"] = ai_analysis
        
        print(f"AI理解结果:")
        print(f"  目标应用: {ai_analysis['target_app']}")
        print(f"  可能的别名: {ai_analysis['possible_names']}")
        print(f"  搜索策略: {ai_analysis['search_strategy']}")
        print(f"  置信度: {ai_analysis['confidence']:.2f}")
        print()
        
        # 步骤2: 扫描所有窗口
        print("[步骤2] 扫描所有窗口...")
        print("-" * 70)
        print()
        
        all_windows_result = self.perceiver.perceive_all_windows()
        
        if not all_windows_result["success"]:
            result["error"] = "窗口扫描失败"
            return result
        
        windows = all_windows_result["windows"]
        print(f"发现 {len(windows)} 个窗口")
        print()
        
        # 步骤3: 多策略查找
        print("[步骤3] 多策略智能查找...")
        print("-" * 70)
        print()
        
        candidates = []
        
        # 策略1: 精确标题匹配
        print("策略1: 精确标题匹配")
        for name in ai_analysis["possible_names"]:
            matches = self._find_by_title(windows, name, exact=True)
            if matches:
                print(f"  [OK] 找到 {len(matches)} 个精确匹配: {name}")
                for match in matches:
                    match["strategy"] = "exact_title"
                    match["score"] = 1.0
                    candidates.append(match)
        print()
        
        # 策略2: 模糊标题匹配
        if not candidates:
            print("策略2: 模糊标题匹配")
            for name in ai_analysis["possible_names"]:
                matches = self._find_by_title(windows, name, exact=False)
                if matches:
                    print(f"  [OK] 找到 {len(matches)} 个模糊匹配: {name}")
                    for match in matches:
                        match["strategy"] = "fuzzy_title"
                        match["score"] = 0.8
                        candidates.append(match)
            print()
        
        # 策略3: 类名匹配
        if not candidates and ai_analysis.get("possible_classes"):
            print("策略3: 类名匹配")
            for class_name in ai_analysis["possible_classes"]:
                matches = self._find_by_class(windows, class_name)
                if matches:
                    print(f"  [OK] 找到 {len(matches)} 个类名匹配: {class_name}")
                    for match in matches:
                        match["strategy"] = "class_name"
                        match["score"] = 0.7
                        candidates.append(match)
            print()
        
        # 策略4: 关键词搜索
        if not candidates:
            print("策略4: 关键词搜索")
            keywords = ai_analysis["keywords"]
            matches = self._find_by_keywords(windows, keywords)
            if matches:
                print(f"  [OK] 找到 {len(matches)} 个关键词匹配")
                for match in matches:
                    match["strategy"] = "keywords"
                    match["score"] = 0.6
                    candidates.append(match)
            print()
        
        # 步骤4: 选择最佳匹配
        print("[步骤4] 选择最佳匹配...")
        print("-" * 70)
        print()
        
        if candidates:
            # 去重并按得分排序
            unique_candidates = {}
            for candidate in candidates:
                handle = candidate["window"]["handle"]
                if handle not in unique_candidates or candidate["score"] > unique_candidates[handle]["score"]:
                    unique_candidates[handle] = candidate
            
            # 排序
            sorted_candidates = sorted(
                unique_candidates.values(),
                key=lambda x: x["score"],
                reverse=True
            )
            
            best_match = sorted_candidates[0]
            result["success"] = True
            result["window"] = best_match["window"]
            result["search_strategies"] = [
                {
                    "strategy": c["strategy"],
                    "score": c["score"],
                    "title": c["window"]["title"],
                }
                for c in sorted_candidates[:3]
            ]
            
            print(f"[OK] 找到最佳匹配:")
            print(f"  标题: {best_match['window']['title']}")
            print(f"  匹配策略: {best_match['strategy']}")
            print(f"  置信度: {best_match['score']:.2f}")
            print(f"  位置: {best_match['window']['rect']}")
            print()
        else:
            print("[X] 未找到匹配窗口")
            print()
        
        return result
    
    def _ai_understand_intent(self, user_intent: str) -> dict:
        """
        AI理解用户意图
        
        在实际应用中，这里会调用L1意图理解层的AI
        这里使用规则引擎模拟AI理解
        """
        intent_lower = user_intent.lower()
        
        # 预定义的应用知识库
        app_knowledge = {
            "豆包": {
                "target_app": "豆包",
                "possible_names": ["豆包", "Doubao", "DOUBAO"],
                "possible_classes": ["Chrome_WidgetWin_1"],  # Chromium应用
                "keywords": ["豆包", "doubao", "字节", "AI助手"],
                "search_strategy": "title_first",
                "confidence": 0.9,
            },
            "飞书": {
                "target_app": "飞书",
                "possible_names": ["飞书", "Lark", "Feishu"],
                "possible_classes": ["LarkWindow"],
                "keywords": ["飞书", "lark", "feishu"],
                "search_strategy": "title_first",
                "confidence": 0.9,
            },
            "记事本": {
                "target_app": "记事本",
                "possible_names": ["记事本", "Notepad"],
                "possible_classes": ["Notepad"],
                "keywords": ["记事本", "notepad"],
                "search_strategy": "title_first",
                "confidence": 0.95,
            },
            "浏览器": {
                "target_app": "浏览器",
                "possible_names": ["Chrome", "Edge", "Firefox"],
                "possible_classes": ["Chrome_WidgetWin_1", "EdgeWindow"],
                "keywords": ["浏览器", "chrome", "edge"],
                "search_strategy": "class_first",
                "confidence": 0.8,
            },
        }
        
        # 匹配应用知识
        for app_name, knowledge in app_knowledge.items():
            if app_name in intent_lower or any(name.lower() in intent_lower for name in knowledge["possible_names"]):
                return knowledge
        
        # 未匹配到预定义应用，使用通用策略
        return {
            "target_app": user_intent,
            "possible_names": [user_intent],
            "possible_classes": [],
            "keywords": [user_intent],
            "search_strategy": "fuzzy_first",
            "confidence": 0.6,
        }
    
    def _find_by_title(self, windows: list, keyword: str, exact: bool = False) -> list:
        """通过标题查找窗口"""
        matches = []
        keyword_lower = keyword.lower()
        
        for window in windows:
            title = window.get("title", "")
            if not title:
                continue
            
            if exact:
                if keyword_lower == title.lower():
                    matches.append({"window": window})
            else:
                if keyword_lower in title.lower():
                    matches.append({"window": window})
        
        return matches
    
    def _find_by_class(self, windows: list, class_name: str) -> list:
        """通过类名查找窗口"""
        matches = []
        
        for window in windows:
            if window.get("class_name") == class_name:
                matches.append({"window": window})
        
        return matches
    
    def _find_by_keywords(self, windows: list, keywords: list) -> list:
        """通过关键词查找窗口"""
        matches = []
        
        for window in windows:
            title = window.get("title", "").lower()
            class_name = window.get("class_name", "").lower()
            
            # 检查是否包含任意关键词
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in title or keyword_lower in class_name:
                    matches.append({"window": window})
                    break
        
        return matches


# 测试AI窗口查找
if __name__ == "__main__":
    finder = AIWindowFinder()
    
    # 测试1: 查找豆包
    result1 = finder.find_window_with_ai("找到豆包窗口")
    
    print("\n" + "="*70)
    print("  测试完成")
    print("="*70)
    print()
    
    if result1["success"]:
        print("[OK] AI成功找到豆包窗口!")
        print()
        print("搜索过程:")
        for i, strategy in enumerate(result1["search_strategies"], 1):
            print(f"  {i}. {strategy['strategy']}: {strategy['title']} (得分: {strategy['score']:.2f})")
        print()
    else:
        print("[X] AI未找到豆包窗口")
        print()
