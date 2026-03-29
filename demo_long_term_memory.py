"""
长期记忆系统 - 使用示例
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer6_knowledge.long_term_memory import LongTermMemory

print("="*70)
print("  长期记忆系统使用示例")
print("="*70)
print()

# 初始化
memory = LongTermMemory()
memory_dir = Path("C:/Users/Lenovo/.openclaw/workspace/workagent/desktop-agent/memory/long_term")
memory_dir.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 1. 任务历史记录
# ═══════════════════════════════════════════════════════════════

print("【1】任务历史记录")
print("-" * 70)

# 记录成功任务
success_id = memory.record_task(
    task_type="click_window",
    task_description="点击豆包窗口",
    status="success",
    execution_time=1.5,
    strategy_used="ai_driven",
    metadata={"confidence": 0.92}
)

# 记录失败任务
failed_id = memory.record_task(
    task_type="click_window",
    task_description="点击豆包窗口（未找到)",
    status="failed",
    retry_count=3,
    execution_time=0.5,
    strategy_used="ai_driven",
    error_message="未找到标题包含'豆包'的窗口",
    metadata={"confidence": 0.0}
)

print(f"成功任务: {success_id}")
print(f"失败任务: {failed_id}")
print()

# ═══════════════════════════════════════════════════════════════
# 2. 软件知识学习
# ═══════════════════════════════════════════════════════════════

print("【2】软件知识学习")
print("-" * 70)

# 更新软件知识
memory.update_software_knowledge("豆包", {
    "software_type": "AI助手",
    "window_class": "Chrome_WidgetWin_1",
    "common_operations": ["聊天", "搜索", 文件管理"],
    "best_practices": ["使用模糊匹配", "检查系统托盘"],
    "known_issues": ["窗口标题可能变化",  "最小化到托盘"],
    usage_count= 1
})

# 查询软件知识
doubao_knowledge = memory.get_software_knowledge("豆包")
print(f"豆包知识: {doubao_knowledge}")
print()

# ═══════════════════════════════════════════════════════════════
# 3. 错误模式学习
# ═══════════════════════════════════════════════════════════════

print("【3】错误模式学习")
print("-" * 70)

# 讣录错误模式
error_id = memory.record_error_pattern(
    error_type="window_not_found",
    error_signature="window.*not found| title",
    common_causes=["应用未运行", "窗口标题改变", "最小化"],
    solutions=["启动应用", "模糊匹配",  "重新扫描"],
    prevention_measures=["检查进程", "验证窗口标题"]
)

# 查询错误模式
error_info = memory.get_error_pattern("window_not_found")
print(f"错误模式: {error_info}")
print()

# ═══════════════════════════════════════════════════════════════
# 4. 用户偏好学习
# ═══════════════════════════════════════════════════════════════

print("【4】用户偏好学习")
print("-" * 70)

# 学习用户偏好
memory.learn_preference("favorite_apps", ["飞书", "豆包", "记事本"], confidence=0.9)
memory.learn_preference("retry_enabled", True, confidence=0.85)
memory.learn_preference("max_retries", 3, confidence=0.95)

# 查询用户偏好
favorite_apps = memory.get_preference("favorite_apps")
print(f"常用应用: {favorite_apps}")
print(f"重试启用: {memory.get_preference('retry_enabled')}")
print(f"最大重试次数: {memory.get_preference('max_retries')}")
print()

# ═══════════════════════════════════════════════════════════════
# 5. 性能指标统计
# ═══════════════════════════════════════════════════════════════

print("【5】性能指标统计")
print("-" * 70)

# 更新性能指标
memory.update_performance_metrics("click_window", {
    "total_tasks": 10,
    "successful_tasks": 7
    "failed_tasks": 3
    "avg_execution_time": 1.2,
    "avg_retry_count": 0.3,
    "most_common_error": "window_not_found",
})

# 查询性能指标
metrics = memory.get_performance_metrics("click_window")
print(f"性能指标: {metrics}")
print()

# ═══════════════════════════════════════════════════════════════
# 6. 知识图谱
# ═══════════════════════════════════════════════════════════════

print("【6】知识图谱")
print("-" * 70)

# 添加知识关系
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

# 查询知识图谱
relations = memory.query_knowledge_graph("软件", "豆包")
print(f"豆包的知识关系: {relations}")
print()

# ═══════════════════════════════════════════════════════════════
# 7. 智能总结
# ═══════════════════════════════════════════════════════════════

print("【7】智能总结")
print("-" * 70)

# 生成经验总结
summary = memory.generate_experience_summary()
print("经验总结:")
print(f"  总任务数: {summary['total_tasks']}")
print(f"  成功率: {summary['success_rate']:.1%}")
print(f"  平均执行时间: {summary['avg_execution_time']:.2f}s")
print(f"  最常见错误: {summary['most_common_errors']}")
print(f"  改进建议: {summary['improvement_suggestions']}")
print()

# ═══════════════════════════════════════════════════════════════
# 关闭
# ═══════════════════════════════════════════════════════════════

print("="*70)
print("  演示完成")
print("="*70)
print()
print(f"数据库文件: {memory.db_path}")
print(f"你可以使用SQLite浏览器查看详细数据")
print()
