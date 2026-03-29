"""
第3层：操作规划层 - 知识查询器
从知识库查询软件操作知识
"""

from typing import Dict, Any, List
from pathlib import Path
import json
import yaml
from loguru import logger


class KnowledgeQuery:
    """知识查询器"""
    
    def __init__(self, config):
        self.config = config
        
        # 知识库路径
        self.software_kb_dir = config.SOFTWARE_KB_DIR
        self.templates_dir = config.TEMPLATES_DIR
        
        # 加载知识库
        self.software_kb = {}
        self.task_templates = {}
        
        self._load_knowledge()
    
    def _load_knowledge(self):
        """加载知识库"""
        # 加载软件知识
        if self.software_kb_dir.exists():
            for kb_file in self.software_kb_dir.glob("*.yaml"):
                try:
                    with open(kb_file, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if data:
                            app_name = data.get("name", kb_file.stem)
                            self.software_kb[app_name.lower()] = data
                except Exception as e:
                    logger.warning(f"加载软件知识失败 {kb_file}: {e}")
        
        # 加载任务模板
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob("*.json"):
                try:
                    with open(template_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data:
                            template_name = data.get("name", template_file.stem)
                            self.task_templates[template_name] = data
                except Exception as e:
                    logger.warning(f"加载任务模板失败 {template_file}: {e}")
        
        logger.info(f"加载 {len(self.software_kb)} 个软件知识，{len(self.task_templates)} 个任务模板")
    
    def query_software(self, software_name: str) -> Dict[str, Any]:
        """查询软件知识"""
        return self.software_kb.get(software_name.lower())
    
    def query_operation(self, software_name: str, operation_name: str) -> Dict[str, Any]:
        """查询软件的特定操作"""
        software = self.query_software(software_name)
        
        if not software:
            return None
        
        operations = software.get("operations", [])
        
        for op in operations:
            if operation_name.lower() in op.get("name", "").lower():
                return op
        
        return None
    
    def query_shortcut(self, software_name: str, action: str) -> List[str]:
        """查询快捷键"""
        software = self.query_software(software_name)
        
        if not software:
            return None
        
        shortcuts = software.get("shortcuts", {})
        
        return shortcuts.get(action)
    
    def query_template(self, template_name: str) -> Dict[str, Any]:
        """查询任务模板"""
        return self.task_templates.get(template_name)
    
    def get_all_software(self) -> List[str]:
        """获取所有已知软件"""
        return list(self.software_kb.keys())
    
    def get_all_templates(self) -> List[str]:
        """获取所有任务模板"""
        return list(self.task_templates.keys())
