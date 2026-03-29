# Desktop Agent - 快速开始指南

**版本：** v3.2  
**更新时间：** 2026-03-27  
**适用于：** 新用户

---

## 🚀 5分钟快速上手

### 第一步：安装

```bash
# 克隆项目
git clone [项目地址]
cd desktop-agent

# 安装依赖
pip install -r requirements.txt
```

### 第二步：启动

```bash
# 命令行模式
python tools/cli.py

# Web界面模式
python web/app.py
# 访问 http://localhost:5000
```

### 第三步：第一个任务

```python
# Python API
from core.agent import DesktopAgent

agent = DesktopAgent()

# 执行简单任务
result = agent.execute("点击确定按钮")
print(result)

# 执行复杂任务
result = agent.execute("""
打开记事本，
输入'Hello World'，
保存为hello.txt
""")
```

---

## 📖 核心概念

### 六层架构

```
Layer 1: 意图理解
  → 将自然语言转换为可执行步骤

Layer 2: 屏幕感知
  → 识别屏幕上的元素（按钮、输入框等）

Layer 3: 操作规划
  → 规划最优操作路径

Layer 4: 动作执行
  → 执行点击、输入等操作

Layer 5: 验证反馈
  → 验证结果，处理错误

Layer 6: 知识记忆
  → 学习和记忆操作经验
```

---

## 🎯 常用操作

### 1. 点击操作

```python
# 点击按钮
agent.execute("点击确定按钮")
agent.execute("点击取消按钮")

# 点击坐标
agent.execute("点击坐标(100, 200)")

# 双击
agent.execute("双击文件")
```

### 2. 输入操作

```python
# 输入文本
agent.execute("输入用户名admin")
agent.execute("在搜索框输入'Python教程'")

# 输入密码
agent.execute("输入密码123456")
```

### 3. 快捷键

```python
# 复制粘贴
agent.execute("按Ctrl+C复制")
agent.execute("按Ctrl+V粘贴")

# 保存
agent.execute("按Ctrl+S保存")

# 全选
agent.execute("按Ctrl+A全选")
```

### 4. 窗口操作

```python
# 打开应用
agent.execute("打开记事本")
agent.execute("打开计算器")

# 关闭窗口
agent.execute("关闭当前窗口")

# 窗口管理
agent.execute("最小化窗口")
agent.execute("最大化窗口")
```

---

## 🔥 进阶用法

### 1. 批量操作

```python
# 批量点击
agent.execute("依次点击确定、取消、保存")

# 批量输入
agent.execute("在所有输入框输入'测试'")
```

### 2. 条件操作

```python
# 条件判断
result = agent.execute("""
如果屏幕上有'确定'按钮，
则点击确定，
否则点击取消
""")
```

### 3. 循环操作

```python
# 循环执行
for i in range(5):
    agent.execute(f"输入第{i+1}行")
```

---

## 🛠️ 高级功能

### 1. 自定义组件

```python
from components.base import BaseComponent, ComponentResult

class MyComponent(BaseComponent):
    @property
    def name(self):
        return "MyComponent"
    
    @property
    def category(self):
        return "custom"
    
    def execute(self, params):
        # 实现你的逻辑
        return ComponentResult(True, {"result": "ok"})

# 注册组件
from components.base import ComponentRegistry
ComponentRegistry.register(MyComponent())
```

### 2. 知识库扩展

```python
# 添加软件知识
agent.learn_from_document("docs/excel_tutorial.md")

# 查询知识
knowledge = agent.get_knowledge("Excel")
print(knowledge)
```

### 3. 流程录制

```python
# 开始录制
agent.start_recording()

# 手动操作...

# 停止录制
flow = agent.stop_recording()

# 重放
agent.execute_flow(flow)
```

---

## ⚠️ 常见问题

### Q1: 元素找不到？

```python
# 尝试多种定位方式
result = agent.execute("""
使用图像识别定位'确定'按钮，
如果失败则使用OCR定位
""")
```

### Q2: 操作太快？

```python
# 添加等待时间
agent.execute("点击确定，等待2秒，点击取消")

# 智能等待
agent.execute("点击确定，等待元素'取消'出现")
```

### Q3: 如何处理错误？

```python
# 自动重试
result = agent.execute("""
点击确定（重试3次）
""")

# 错误恢复
if not result["success"]:
    # 系统会自动尝试恢复
    print(f"错误: {result['error']}")
```

### Q4: 如何提高准确率？

```python
# 使用更具体的描述
# ❌ 不好
agent.execute("点击按钮")

# ✅ 好
agent.execute("点击'确定'按钮（位于对话框底部）")

# 使用上下文
agent.execute("""
在Excel中，
点击数据菜单的筛选按钮
""")
```

---

## 📚 更多资源

### 文档

- [完整API文档](docs/api.md)
- [架构设计文档](architecture.md)
- [组件开发指南](docs/component_development.md)
- [最佳实践](docs/best_practices.md)

### 示例

- [简单示例](examples/simple.py)
- [进阶示例](examples/advanced.py)
- [企业场景](examples/enterprise.py)

### 社区

- [GitHub Issues](https://github.com/...)
- [Discord社区](https://discord.gg/...)
- [文档网站](https://docs.example.com)

---

## 🎓 学习路径

### 初级（1-2天）

```
1. ✅ 完成快速开始
2. ✅ 学习基本操作
3. ✅ 运行示例代码
4. ✅ 完成第一个自动化任务
```

### 中级（1周）

```
1. 学习六层架构
2. 掌握错误处理
3. 使用知识库
4. 开发自定义组件
```

### 高级（1个月）

```
1. 优化性能
2. 扩展知识库
3. 集成到生产环境
4. 贡献代码
```

---

## 💡 最佳实践

### 1. 任务分解

```python
# ❌ 不好：一个复杂任务
agent.execute("打开Excel，处理数据，生成报表，发送邮件")

# ✅ 好：分解为多个步骤
agent.execute("打开Excel")
agent.execute("处理数据")
agent.execute("生成报表")
agent.execute("发送邮件")
```

### 2. 错误处理

```python
# 检查结果
result = agent.execute("点击确定")

if not result["success"]:
    print(f"执行失败: {result['error']}")
    # 处理错误
else:
    print("执行成功")
```

### 3. 性能优化

```python
# 重用Agent实例
agent = DesktopAgent()  # 只创建一次

for task in tasks:
    agent.execute(task)  # 复用
```

### 4. 安全考虑

```python
# 高风险操作需要确认
agent.execute(
    "删除所有文件",
    enable_confirmation=True  # 强制确认
)
```

---

## 🆘 获取帮助

### 遇到问题？

1. **查看日志** - 检查 `logs/` 目录
2. **运行诊断** - `python tools/diagnose.py`
3. **搜索文档** - 查看官方文档
4. **提问** - 在社区提问

### 调试模式

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

agent = DesktopAgent()
result = agent.execute("点击确定")

# 查看详细执行过程
print(json.dumps(result, indent=2))
```

---

## ✅ 下一步

```
□ 完成快速开始
□ 运行示例代码
□ 尝试自己的第一个任务
□ 加入社区讨论
```

---

**祝你使用愉快！** 🎉

如有问题，随时查阅文档或在社区提问。
