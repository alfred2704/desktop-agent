# Desktop Agent - 快速启动指南

## 🎉 项目已就绪！

所有问题已修复，所有测试通过，可以立即使用！

---

## 🚀 三种使用方式

### 1️⃣ Web界面（推荐新手）

```bash
python main.py web
```

**访问地址：** http://localhost:5000

**功能：**
- 💬 自然语言指令输入
- 👁️ 实时屏幕元素可视化
- 📊 执行历史查看
- 🎛️ 知识库管理

---

### 2️⃣ 命令行（适合调试）

```bash
python main.py cli
```

**示例指令：**
```
>>> 点击确定按钮
>>> 在搜索框输入'Python'
>>> 按Ctrl+S
>>> /sense              # 感知屏幕
>>> /find 确定          # 查找元素
>>> /history            # 查看历史
>>> /quit               # 退出
```

---

### 3️⃣ Python API（适合集成）

```python
from core.agent import DesktopAgent

# 创建Agent
agent = DesktopAgent()

# 执行自然语言指令
result = agent.execute("点击确定按钮")

if result['success']:
    print("执行成功！")
else:
    print(f"执行失败: {result['error']}")
```

---

## 💡 快速示例

### 示例1：简单点击

```python
from core.agent import DesktopAgent

agent = DesktopAgent()

# 点击确定按钮
agent.execute("点击确定按钮")

# 点击文件菜单下的保存
agent.execute("点击文件菜单下的保存")
```

### 示例2：输入文本

```python
# 在搜索框输入内容
agent.execute("在搜索框输入'Python教程'")

# 填写表单
agent.execute("在用户名输入框输入'admin'")
agent.execute("在密码输入框输入'123456'")
```

### 示例3：快捷键操作

```python
# 保存
agent.execute("按Ctrl+S")

# 复制粘贴
agent.execute("按Ctrl+C")
agent.execute("按Ctrl+V")

# 自定义快捷键
agent.execute("按Ctrl+Alt+Delete")
```

### 示例4：复杂任务

```python
# 打开文件并编辑
agent.execute([
    "按Ctrl+O",
    "在文件名输入框输入'document.txt'",
    "按Enter",
    "在第一行输入'Hello World'",
    "按Ctrl+S"
])
```

---

## 📖 支持的指令类型

| 类型 | 格式 | 示例 |
|------|------|------|
| 点击 | 点击{元素} | 点击确定按钮 |
| 双击 | 双击{元素} | 双击文件 |
| 右键 | 右键{元素} | 右键桌面 |
| 输入 | 在{元素}输入'{文本}' | 在搜索框输入'Python' |
| 快捷键 | 按{组合键} | 按Ctrl+S |
| 菜单 | 点击{菜单}菜单下的{项} | 点击文件菜单下的保存 |
| 滚动 | 向{方向}滚动 | 向下滚动 |
| 等待 | 等待{元素}出现 | 等待确定按钮出现 |
| 查找 | 查找{元素} | 查找确定按钮 |

---

## 🎯 支持的软件

### ✅ 已内置知识库
- Microsoft Excel
- 记事本

### ✅ 自动支持
- Windows原生应用
- Office套件
- WinForms/WPF应用
- Electron应用

### 🔧 添加新软件

在 `knowledge/software/` 创建YAML文件：

```yaml
name: 软件名称
version: 版本号
operations:
  - name: 操作名称
    steps:
      - action: click
        target: 目标元素
shortcuts:
  保存: ["ctrl", "s"]
```

---

## 🛠️ 高级功能

### 1. 屏幕感知

```python
# 感知当前屏幕
state = agent.sense_screen()

print(f"活动窗口: {state['active_window']['title']}")
print(f"检测到元素: {len(state['elements'])} 个")
```

### 2. 元素查找

```python
# 查找元素
result = agent.find_element("确定")

if result['success']:
    element = result['element']
    print(f"元素位置: {element['center']}")
```

### 3. 知识查询

```python
# 获取软件知识
kb = agent.get_knowledge("excel")
print(kb)
```

### 4. 执行历史

```python
# 查看历史
history = agent.get_history(limit=10)

for record in history:
    print(f"{record['instruction']}: {'成功' if record['success'] else '失败'}")
```

---

## ⚙️ 配置选项

编辑 `.env` 文件：

```env
# AI配置
AI_ENABLED=true
ZHIPU_API_KEY=your_key_here
AI_MODEL=glm-4

# Web配置
WEB_HOST=0.0.0.0
WEB_PORT=5000
DEBUG=true

# 执行配置
MAX_RETRY=3
ACTION_DELAY=0.1
```

---

## ❓ 常见问题

### Q: 指令执行失败？
A: 
1. 确保元素名称正确
2. 检查元素是否可见
3. 尝试先执行 `/sense` 查看当前元素

### Q: 找不到元素？
A:
1. 使用 `/find` 命令搜索
2. 使用 `/sense` 查看所有元素
3. 尝试模糊名称（如"确"可以匹配"确定"）

### Q: Web界面无法访问？
A:
1. 检查端口5000是否被占用
2. 确认防火墙设置
3. 尝试更改 `.env` 中的端口

---

## 📞 获取帮助

- 📖 查看文档：`docs/` 目录
- 💻 运行示例：`python main.py quickstart`
- 🔍 自检项目：`python check_project.py`
- 🧪 功能测试：`python simple_test.py`

---

## 🎊 开始使用

```bash
# 启动Web界面
python main.py web

# 或命令行
python main.py cli

# 然后输入自然语言指令，控制你的电脑！
```

**祝你使用愉快！🚀**
