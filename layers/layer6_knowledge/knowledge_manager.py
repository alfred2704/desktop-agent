"""
第6层：知识记忆层 - 知识管理器
管理软件知识、任务模板、经验记忆
"""

from typing import Dict, Any, List
from pathlib import Path
import json
import yaml
import time
from loguru import logger


class KnowledgeManager:
    """知识管理器"""
    
    def __init__(self, config):
        self.config = config
        
        # 知识库路径
        self.knowledge_dir = config.KNOWLEDGE_DIR
        self.software_dir = config.SOFTWARE_KB_DIR
        self.templates_dir = config.TEMPLATES_DIR
        self.experience_dir = config.EXPERIENCE_DIR
        
        # 确保目录存在
        for directory in [self.knowledge_dir, self.software_dir, self.templates_dir, self.experience_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # 经验记忆
        self.experiences = []
        
        # 加载经验
        self._load_experiences()
    
    def _load_experiences(self):
        """加载经验记忆"""
        experience_file = self.experience_dir / "experiences.json"
        
        if experience_file.exists():
            try:
                with open(experience_file, "r", encoding="utf-8") as f:
                    self.experiences = json.load(f)
                logger.info(f"加载 {len(self.experiences)} 条经验记忆")
            except Exception as e:
                logger.warning(f"加载经验记忆失败: {e}")
    
    def save_experience(self, instruction: str, intent: Dict, plan: Dict, results: List[Dict]):
        """保存执行经验"""
        experience = {
            "timestamp": time.time(),
            "instruction": instruction,
            "intent": intent,
            "plan": plan,
            "results": results,
            "success": all(r.get("success") for r in results),
        }
        
        self.experiences.append(experience)
        
        # 持久化
        experience_file = self.experience_dir / "experiences.json"
        
        try:
            with open(experience_file, "w", encoding="utf-8") as f:
                json.dump(self.experiences[-100:], f, ensure_ascii=False, indent=2)  # 只保留最近100条
            
            logger.info(f"保存执行经验: {instruction[:30]}...")
        
        except Exception as e:
            logger.error(f"保存经验失败: {e}")
    
    def get_software_knowledge(self, software_name: str = None) -> Dict[str, Any]:
        """获取软件知识"""
        if software_name:
            # 查询特定软件
            kb_file = self.software_dir / f"{software_name.lower()}.yaml"
            
            if kb_file.exists():
                try:
                    with open(kb_file, "r", encoding="utf-8") as f:
                        return yaml.safe_load(f)
                except Exception as e:
                    logger.warning(f"加载软件知识失败: {e}")
            
            return {"error": f"未找到软件知识: {software_name}"}
        
        else:
            # 返回所有软件列表
            software_list = []
            
            for kb_file in self.software_dir.glob("*.yaml"):
                try:
                    with open(kb_file, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if data:
                            software_list.append({
                                "name": data.get("name"),
                                "version": data.get("version"),
                                "operations_count": len(data.get("operations", [])),
                            })
                except:
                    pass
            
            return {"software_list": software_list}
    
    def learn_from_document(self, doc_path: str) -> Dict[str, Any]:
        """从文档学习"""
        # TODO: 实现文档解析和学习
        logger.info(f"从文档学习: {doc_path}")
        
        return {
            "success": False,
            "error": "功能待实现"
        }
    
    def search_similar_experience(self, instruction: str, limit: int = 5) -> List[Dict]:
        """搜索相似经验"""
        # 简单的关键词匹配
        similar = []
        
        instruction_lower = instruction.lower()
        
        for exp in self.experiences:
            exp_instruction = exp.get("instruction", "").lower()
            
            # 计算相似度（简单版）
            if any(word in exp_instruction for word in instruction_lower.split()):
                similar.append(exp)
        
        return similar[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_experiences": len(self.experiences),
            "successful_experiences": sum(1 for exp in self.experiences if exp.get("success")),
            "software_count": len(list(self.software_dir.glob("*.yaml"))),
            "template_count": len(list(self.templates_dir.glob("*.json"))),
        }
