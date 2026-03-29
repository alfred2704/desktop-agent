"""
L6 知识记忆层 - 长期记忆系统设计
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import pickle

# ═══════════════════════════════════════════════════════════════
# 长期记忆系统架构
# ═══════════════════════════════════════════════════════════════

class LongTermMemory:
    """长期记忆系统"""
    
    def __init__(self, db_path: str = "memory/long_term.db"):
        """
        初始化长期记忆系统
        
        存储结构:
        1. 任务历史 (task_history)
        2. 软件知识 (software_knowledge)
        3. 错误模式 (error_patterns)
        4. 用户偏好 (user_preferences)
        5. 性能数据 (performance_metrics)
        6. 改进历史 (improvement_history)
        7. 知识图谱 (knowledge_graph)
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self.conn = sqlite3.connect(str(self.db_path))
        self._create_tables()
    
    def _create_tables(self):
        """创建数据库表"""
        
        # 1. 任务历史表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                task_type TEXT NOT NULL,
                task_description TEXT,
                status TEXT CHECK(status IN ('success', 'failed', 'retry')),
                retry_count INTEGER DEFAULT 0,
                execution_time REAL,
                strategy_used TEXT,
                error_message TEXT,
                improvement_applied TEXT,
                metadata JSON
            )
        """)
        
        # 2. 软件知识表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS software_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                software_name TEXT NOT NULL UNIQUE,
                software_type TEXT,
                window_class TEXT,
                common_operations JSON,
                best_practices JSON,
                known_issues JSON,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                success_rate REAL,
                avg_execution_time REAL,
                usage_count INTEGER DEFAULT 0
            )
        """)
        
        # 3. 错误模式表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS error_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                error_signature TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                common_causes JSON,
                solutions JSON,
                prevention_measures JSON,
                success_rate REAL
            )
        """)
        
        # 4. 用户偏好表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value JSON,
                confidence REAL DEFAULT 0.5,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                update_count INTEGER DEFAULT 1
            )
        """)
        
        # 5. 性能指标表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                task_type TEXT NOT NULL,
                total_tasks INTEGER DEFAULT 0,
                successful_tasks INTEGER DEFAULT 0,
                failed_tasks INTEGER DEFAULT 0,
                avg_execution_time REAL,
                avg_retry_count REAL,
                most_common_error TEXT,
                improvement_suggestions JSON,
                UNIQUE(date, task_type)
            )
        """)
        
        # 6. 改进历史表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS improvement_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                improvement_type TEXT NOT NULL,
                description TEXT,
                before_state JSON,
                after_state JSON,
                impact_metrics JSON,
                success BOOLEAN
            )
        """)
        
        # 7. 知识图谱表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_graph (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL,
                entity_name TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                related_entity_type TEXT NOT NULL,
                related_entity_name TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                evidence_count INTEGER DEFAULT 1,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(entity_type, entity_name, relation_type, related_entity_type, related_entity_name)
            )
        """)
        
        # 创建索引
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_task_timestamp ON task_history(timestamp)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_task_type ON task_history(task_type)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_software_name ON software_knowledge(software_name)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_error_type ON error_patterns(error_type)")
        
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════════
    # 1. 任务历史记录
    # ═══════════════════════════════════════════════════════════════
    
    def record_task(self, task_info: Dict[str, Any]) -> int:
        """
        记录任务执行历史
        
        Args:
            task_info: {
                "task_type": "click_window",
                "task_description": "点击豆包窗口",
                "status": "failed",
                "retry_count": 3,
                "execution_time": 2.5,
                "strategy_used": "ai_driven",
                "error_message": "未找到窗口",
                "improvement_applied": "启动应用",
                "metadata": {...}
            }
        """
        cursor = self.conn.execute("""
            INSERT INTO task_history 
            (task_type, task_description, status, retry_count, execution_time, 
             strategy_used, error_message, improvement_applied, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_info.get("task_type"),
            task_info.get("task_description"),
            task_info.get("status"),
            task_info.get("retry_count", 0),
            task_info.get("execution_time"),
            task_info.get("strategy_used"),
            task_info.get("error_message"),
            task_info.get("improvement_applied"),
            json.dumps(task_info.get("metadata", {}))
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_task_history(self, task_type: str = None, days: int = 30) -> List[Dict]:
        """获取任务历史"""
        query = """
            SELECT * FROM task_history 
            WHERE timestamp >= datetime('now', ?)
        """
        params = [f'-{days} days']
        
        if task_type:
            query += " AND task_type = ?"
            params.append(task_type)
        
        query += " ORDER BY timestamp DESC"
        
        cursor = self.conn.execute(query, params)
        rows = cursor.fetchall()
        
        return [self._row_to_dict(row, "task_history") for row in rows]
    
    # ═══════════════════════════════════════════════════════════════
    # 2. 软件知识管理
    # ═══════════════════════════════════════════════════════════════
    
    def update_software_knowledge(self, software_name: str, knowledge: Dict[str, Any]):
        """
        更新软件知识
        
        Args:
            software_name: "豆包"
            knowledge: {
                "software_type": "AI助手",
                "window_class": "Chrome_WidgetWin_1",
                "common_operations": ["聊天", "搜索"],
                "best_practices": ["使用模糊匹配查找窗口"],
                "known_issues": ["窗口标题可能变化"]
            }
        """
        # 检查是否已存在
        cursor = self.conn.execute(
            "SELECT id, usage_count FROM software_knowledge WHERE software_name = ?",
            (software_name,)
        )
        row = cursor.fetchone()
        
        if row:
            # 更新
            self.conn.execute("""
                UPDATE software_knowledge 
                SET software_type = ?, window_class = ?, common_operations = ?,
                    best_practices = ?, known_issues = ?, last_updated = CURRENT_TIMESTAMP,
                    usage_count = usage_count + 1
                WHERE software_name = ?
            """, (
                knowledge.get("software_type"),
                knowledge.get("window_class"),
                json.dumps(knowledge.get("common_operations", [])),
                json.dumps(knowledge.get("best_practices", [])),
                json.dumps(knowledge.get("known_issues", [])),
                software_name
            ))
        else:
            # 插入
            self.conn.execute("""
                INSERT INTO software_knowledge
                (software_name, software_type, window_class, common_operations, best_practices, known_issues)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                software_name,
                knowledge.get("software_type"),
                knowledge.get("window_class"),
                json.dumps(knowledge.get("common_operations", [])),
                json.dumps(knowledge.get("best_practices", [])),
                json.dumps(knowledge.get("known_issues", []))
            ))
        
        self.conn.commit()
    
    def get_software_knowledge(self, software_name: str) -> Dict:
        """获取软件知识"""
        cursor = self.conn.execute(
            "SELECT * FROM software_knowledge WHERE software_name = ?",
            (software_name,)
        )
        row = cursor.fetchone()
        
        if row:
            return self._row_to_dict(row, "software_knowledge")
        return None
    
    def update_software_stats(self, software_name: str, success: bool, execution_time: float):
        """更新软件统计信息"""
        cursor = self.conn.execute(
            "SELECT success_rate, avg_execution_time, usage_count FROM software_knowledge WHERE software_name = ?",
            (software_name,)
        )
        row = cursor.fetchone()
        
        if row:
            old_rate, old_time, count = row
            new_count = count + 1
            
            # 计算新的成功率（移动平均）
            if success:
                new_rate = (old_rate * count + 1.0) / new_count
            else:
                new_rate = (old_rate * count) / new_count
            
            # 计算新的平均执行时间
            new_time = (old_time * count + execution_time) / new_count
            
            self.conn.execute("""
                UPDATE software_knowledge 
                SET success_rate = ?, avg_execution_time = ?, usage_count = ?
                WHERE software_name = ?
            """, (new_rate, new_time, new_count, software_name))
            
            self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════════
    # 3. 错误模式管理
    # ═══════════════════════════════════════════════════════════════
    
    def record_error_pattern(self, error_type: str, error_signature: str, 
                            causes: List[str], solutions: List[str]):
        """记录错误模式"""
        cursor = self.conn.execute(
            "SELECT id, frequency FROM error_patterns WHERE error_signature = ?",
            (error_signature,)
        )
        row = cursor.fetchone()
        
        if row:
            # 更新频率
            self.conn.execute("""
                UPDATE error_patterns 
                SET frequency = frequency + 1, last_seen = CURRENT_TIMESTAMP
                WHERE error_signature = ?
            """, (error_signature,))
        else:
            # 新增
            self.conn.execute("""
                INSERT INTO error_patterns
                (error_type, error_signature, common_causes, solutions)
                VALUES (?, ?, ?, ?)
            """, (
                error_type,
                error_signature,
                json.dumps(causes),
                json.dumps(solutions)
            ))
        
        self.conn.commit()
    
    def find_similar_errors(self, error_message: str) -> List[Dict]:
        """查找相似错误"""
        cursor = self.conn.execute("""
            SELECT * FROM error_patterns 
            WHERE ? LIKE '%' || error_signature || '%'
            ORDER BY frequency DESC
            LIMIT 5
        """, (error_message,))
        
        rows = cursor.fetchall()
        return [self._row_to_dict(row, "error_patterns") for row in rows]
    
    # ═══════════════════════════════════════════════════════════════
    # 4. 用户偏好学习
    # ═══════════════════════════════════════════════════════════════
    
    def learn_preference(self, key: str, value: Any, confidence: float = 0.7):
        """学习用户偏好"""
        cursor = self.conn.execute(
            "SELECT value, confidence, update_count FROM user_preferences WHERE key = ?",
            (key,)
        )
        row = cursor.fetchone()
        
        if row:
            old_value, old_confidence, count = row
            new_count = count + 1
            
            # 如果新值与旧值一致，增加置信度
            if value == old_value:
                new_confidence = min(old_confidence + 0.1, 1.0)
            else:
                # 值改变了，降低置信度
                new_confidence = max(old_confidence - 0.1, 0.1)
            
            self.conn.execute("""
                UPDATE user_preferences 
                SET value = ?, confidence = ?, update_count = ?, last_updated = CURRENT_TIMESTAMP
                WHERE key = ?
            """, (json.dumps(value), new_confidence, new_count, key))
        else:
            self.conn.execute("""
                INSERT INTO user_preferences (key, value, confidence)
                VALUES (?, ?, ?)
            """, (key, json.dumps(value), confidence))
        
        self.conn.commit()
    
    def get_preference(self, key: str) -> Any:
        """获取用户偏好"""
        cursor = self.conn.execute(
            "SELECT value, confidence FROM user_preferences WHERE key = ?",
            (key,)
        )
        row = cursor.fetchone()
        
        if row:
            return json.loads(row[0])
        return None
    
    # ═══════════════════════════════════════════════════════════════
    # 5. 性能数据分析
    # ═══════════════════════════════════════════════════════════════
    
    def record_daily_metrics(self, date: str, task_type: str, metrics: Dict):
        """记录每日性能指标"""
        self.conn.execute("""
            INSERT OR REPLACE INTO performance_metrics
            (date, task_type, total_tasks, successful_tasks, failed_tasks, 
             avg_execution_time, avg_retry_count, most_common_error, improvement_suggestions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date,
            task_type,
            metrics.get("total_tasks", 0),
            metrics.get("successful_tasks", 0),
            metrics.get("failed_tasks", 0),
            metrics.get("avg_execution_time"),
            metrics.get("avg_retry_count"),
            metrics.get("most_common_error"),
            json.dumps(metrics.get("improvement_suggestions", []))
        ))
        
        self.conn.commit()
    
    def get_performance_trend(self, task_type: str, days: int = 30) -> List[Dict]:
        """获取性能趋势"""
        cursor = self.conn.execute("""
            SELECT * FROM performance_metrics 
            WHERE task_type = ? AND date >= date('now', ?)
            ORDER BY date ASC
        """, (task_type, f'-{days} days'))
        
        rows = cursor.fetchall()
        return [self._row_to_dict(row, "performance_metrics") for row in rows]
    
    # ═══════════════════════════════════════════════════════════════
    # 6. 改进历史跟踪
    # ═══════════════════════════════════════════════════════════════
    
    def record_improvement(self, improvement_type: str, description: str,
                         before: Dict, after: Dict, impact: Dict):
        """记录系统改进"""
        self.conn.execute("""
            INSERT INTO improvement_history
            (improvement_type, description, before_state, after_state, impact_metrics)
            VALUES (?, ?, ?, ?, ?)
        """, (
            improvement_type,
            description,
            json.dumps(before),
            json.dumps(after),
            json.dumps(impact)
        ))
        
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════════
    # 7. 知识图谱构建
    # ═══════════════════════════════════════════════════════════════
    
    def add_knowledge_relation(self, entity_type: str, entity_name: str,
                             relation: str, related_type: str, related_name: str):
        """添加知识关系"""
        self.conn.execute("""
            INSERT OR REPLACE INTO knowledge_graph
            (entity_type, entity_name, relation_type, related_entity_type, related_entity_name,
             confidence, evidence_count, last_updated)
            VALUES (?, ?, ?, ?, ?, 
                    COALESCE((SELECT confidence FROM knowledge_graph 
                             WHERE entity_type = ? AND entity_name = ? 
                             AND relation_type = ? 
                             AND related_entity_type = ? AND related_entity_name = ?), 0.5) + 0.1,
                    COALESCE((SELECT evidence_count FROM knowledge_graph 
                             WHERE entity_type = ? AND entity_name = ? 
                             AND relation_type = ? 
                             AND related_entity_type = ? AND related_entity_name = ?), 0) + 1,
                    CURRENT_TIMESTAMP)
        """, (
            entity_type, entity_name, relation, related_type, related_name,
            entity_type, entity_name, relation, related_type, related_name,
            entity_type, entity_name, relation, related_type, related_name
        ))
        
        self.conn.commit()
    
    def query_knowledge_graph(self, entity_type: str, entity_name: str) -> List[Dict]:
        """查询知识图谱"""
        cursor = self.conn.execute("""
            SELECT * FROM knowledge_graph 
            WHERE entity_type = ? AND entity_name = ?
            ORDER BY confidence DESC, evidence_count DESC
        """, (entity_type, entity_name))
        
        rows = cursor.fetchall()
        return [self._row_to_dict(row, "knowledge_graph") for row in rows]
    
    # ═══════════════════════════════════════════════════════════════
    # 辅助方法
    # ═══════════════════════════════════════════════════════════════
    
    def _row_to_dict(self, row, table_name: str) -> Dict:
        """将数据库行转换为字典"""
        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        result = {}
        for i, col in enumerate(columns):
            value = row[i]
            
            # 解析JSON字段
            if col in ['metadata', 'common_operations', 'best_practices', 'known_issues',
                      'common_causes', 'solutions', 'prevention_measures', 'value',
                      'improvement_suggestions', 'before_state', 'after_state', 'impact_metrics']:
                try:
                    value = json.loads(value) if value else {}
                except:
                    pass
            
            result[col] = value
        
        return result
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 初始化长期记忆系统
    memory = LongTermMemory()
    
    print("="*70)
    print("  L6 知识记忆层 - 长期记忆系统")
    print("="*70)
    print()
    
    # 示例1: 记录任务历史
    print("【示例1】记录任务历史")
    print("-" * 70)
    print()
    
    task_id = memory.record_task({
        "task_type": "click_window",
        "task_description": "点击豆包窗口",
        "status": "failed",
        "retry_count": 3,
        "execution_time": 2.5,
        "strategy_used": "ai_driven",
        "error_message": "未找到标题包含'豆包'的窗口",
        "improvement_applied": "自动启动应用",
        "metadata": {"window_expected": "豆包", "actual_windows": 8}
    })
    
    print(f"[OK] 任务已记录，ID: {task_id}")
    print()
    
    # 示例2: 更新软件知识
    print("【示例2】更新软件知识")
    print("-" * 70)
    print()
    
    memory.update_software_knowledge("豆包", {
        "software_type": "AI助手",
        "window_class": "Chrome_WidgetWin_1",
        "common_operations": ["聊天", "搜索", "文件管理"],
        "best_practices": ["使用模糊匹配查找窗口", "窗口可能最小化到托盘"],
        "known_issues": ["窗口标题可能变化", "需要启动应用"]
    })
    
    print("[OK] 软件知识已更新")
    print()
    
    # 示例3: 记录错误模式
    print("【示例3】记录错误模式")
    print("-" * 70)
    print()
    
    memory.record_error_pattern(
        "window_not_found",
        "未找到标题包含'X'的窗口",
        ["应用未运行", "窗口标题已改变", "最小化到托盘"],
        ["启动应用", "使用模糊匹配", "检查系统托盘"]
    )
    
    print("[OK] 错误模式已记录")
    print()
    
    # 示例4: 学习用户偏好
    print("【示例4】学习用户偏好")
    print("-" * 70)
    print()
    
    memory.learn_preference("favorite_apps", ["飞书", "豆包", "记事本"], confidence=0.8)
    memory.learn_preference("retry_enabled", True, confidence=0.9)
    
    print("[OK] 用户偏好已学习")
    print()
    
    # 示例5: 查询知识
    print("【示例5】查询知识")
    print("-" * 70)
    print()
    
    # 查询软件知识
    knowledge = memory.get_software_knowledge("豆包")
    if knowledge:
        print(f"豆包软件知识:")
        print(f"  类型: {knowledge['software_type']}")
        print(f"  常见操作: {knowledge['common_operations']}")
        print(f"  最佳实践: {knowledge['best_practices']}")
    print()
    
    # 查询相似错误
    errors = memory.find_similar_errors("未找到窗口")
    print(f"找到 {len(errors)} 个相似错误模式")
    print()
    
    # 示例6: 知识图谱
    print("【示例6】构建知识图谱")
    print("-" * 70)
    print()
    
    memory.add_knowledge_relation(
        "software", "豆包", 
        "belongs_to", "company", "字节跳动"
    )
    
    memory.add_knowledge_relation(
        "software", "豆包",
        "uses_technology", "technology", "Chromium"
    )
    
    memory.add_knowledge_relation(
        "software", "豆包",
        "common_operation", "operation", "窗口点击"
    )
    
    print("[OK] 知识图谱已构建")
    print()
    
    # 查询知识图谱
    relations = memory.query_knowledge_graph("software", "豆包")
    print(f"豆包的相关知识 ({len(relations)} 条):")
    for rel in relations:
        print(f"  - {rel['relation_type']}: {rel['related_entity_name']}")
    print()
    
    print("="*70)
    print("  长期记忆系统演示完成")
    print("="*70)
    print()
    
    memory.close()
