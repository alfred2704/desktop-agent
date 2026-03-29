"""
Desktop Agent - 核心配置
"""

from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """全局配置"""
    
    # 项目根目录
    ROOT_DIR = Path(__file__).parent.parent
    
    # AI配置
    AI_ENABLED = os.getenv("AI_ENABLED", "true").lower() == "true"
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    AI_MODEL = os.getenv("AI_MODEL", "glm-4")
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.1"))
    
    # Web配置
    WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT = int(os.getenv("WEB_PORT", "5000"))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    # 知识库配置
    KNOWLEDGE_DIR = ROOT_DIR / "knowledge"
    SOFTWARE_KB_DIR = KNOWLEDGE_DIR / "software"
    TEMPLATES_DIR = KNOWLEDGE_DIR / "templates"
    EXPERIENCE_DIR = KNOWLEDGE_DIR / "experience"
    KNOWLEDGE_DB_PATH = os.getenv("KNOWLEDGE_DB_PATH", str(KNOWLEDGE_DIR / "db.sqlite"))
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(KNOWLEDGE_DIR / "vectors"))
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(ROOT_DIR / "logs" / "desktop-agent.log"))
    
    # 执行配置
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30"))
    MAX_RETRY = int(os.getenv("MAX_RETRY", "3"))
    ACTION_DELAY = float(os.getenv("ACTION_DELAY", "0.1"))
    
    # 屏幕感知配置
    SCREENSHOT_QUALITY = 95
    OCR_ENABLED = True
    UI_AUTOMATION_ENABLED = True
    
    # 验证配置
    VERIFICATION_ENABLED = True
    SCREENSHOT_SIMILARITY_THRESHOLD = 0.8
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "ai": {
                "enabled": cls.AI_ENABLED,
                "model": cls.AI_MODEL,
                "temperature": cls.AI_TEMPERATURE,
            },
            "web": {
                "host": cls.WEB_HOST,
                "port": cls.WEB_PORT,
                "debug": cls.DEBUG,
            },
            "execution": {
                "timeout": cls.DEFAULT_TIMEOUT,
                "max_retry": cls.MAX_RETRY,
                "action_delay": cls.ACTION_DELAY,
            },
            "knowledge": {
                "db_path": cls.KNOWLEDGE_DB_PATH,
                "vector_db_path": cls.VECTOR_DB_PATH,
            }
        }


# 层级配置
LAYER_CONFIG = {
    "layer1_intent": {
        "name": "意图理解层",
        "modules": ["intent_parser", "entity_extractor", "task_decomposer", "context_manager"],
        "enabled": True,
    },
    "layer2_perception": {
        "name": "屏幕感知层",
        "modules": ["ui_automation", "screen_capture", "ocr_engine", "element_recognizer"],
        "enabled": True,
    },
    "layer3_planning": {
        "name": "操作规划层",
        "modules": ["action_planner", "template_matcher", "path_reasoner", "knowledge_query"],
        "enabled": True,
    },
    "layer4_execution": {
        "name": "动作执行层",
        "modules": ["mouse_controller", "keyboard_controller", "hotkey_executor", "window_manager"],
        "enabled": True,
    },
    "layer5_verification": {
        "name": "验证反馈层",
        "modules": ["screenshot_comparator", "state_validator", "retry_manager", "error_analyzer"],
        "enabled": True,
    },
    "layer6_knowledge": {
        "name": "知识记忆层",
        "modules": ["software_kb", "task_templates", "experience_memory", "knowledge_retriever"],
        "enabled": True,
    },
}
