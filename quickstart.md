# Desktop Agent - 快速启动指南

## 🚀 快速开始（3步）

### 第1步：安装依赖

```bash
cd desktop-agent
pip install -r requirements.txt
```

如果安装PaddleOCR失败，可以跳过OCR功能：

```bash
pip install uiautomation Pillow pyautogui Flask Flask-SocketIO Flask-CORS requests openai PyYAML easydict python-dotenv loguru pyperclip
```

### 第2步：配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，至少配置：

```env
# AI配置（可选，不配置则只使用规则解析）
ZHIPU_API_KEY=your_api_key_here
AI_MODEL=glm-4

# Web配置
WEB_HOST=0.0.0.0
WEB_PORT=5000
DEBUG=True
```

### 第3步：启动

#### 方式1：Web界面（推荐）
```bash
python main.py web
```
然后访问 http://localhost:5000

#### 方式2：命令行
```bash
python main.py cli
```

#### 方式3：运行示例
```bash
python main.py quickstart
```

---

## 💬 使用示例

### Web界面

1. 打开 http://localhost:5000
2. 在输入框输入指令，例如：
   - "点击确定按钮"
   - "在搜索框输入'Python'"
   - "按Ctrl+S保存"
3. 点击"执行"按钮

### 命令行

```
>>> 点击确定按钮
>>> /sense           # 感知屏幕
>>> /find 确定       # 查找元素
>>> /history         # 查看历史
>>> /quit            # 退出
```

### Python API

```python
from core.agent import DesktopAgent

agent = DesktopAgent()
result = agent.execute("点击确定按钮")
print(result)
```

---

## 📚 功能说明

### 支持的指令类型

| 类型 | 示例 |
|------|------|
| 点击 | "点击确定按钮" |
| 双击 | "双击文件" |
| 右键 | "右键桌面" |
| 输入 | "在搜索框输入'Python'" |
| 快捷键 | "按Ctrl+S" |
| 菜单 | "点击文件菜单下的保存" |
| 滚动 | "向下滚动" |
| 等待 | "等待确定按钮出现" |

### 支持的快捷键

- 复制/粘贴/剪切
- 保存/打开/新建
- 撤销/重做
- 全选/查找/替换

### 支持的软件

- Windows原生应用（记事本、计算器等）
- Office套件（Word、Excel、PPT）
- WinForms/WPF应用
- Electron应用

---

## ⚙️ 高级配置

### 添加软件知识库

在 `knowledge/software/` 下创建YAML文件：

```yaml
name: 软件名称
version: 版本号
operations:
  - name: 操作名称
    steps: [...]
shortcuts:
  操作名: ["快捷键组合"]
```

### 调试模式

在 `.env` 中设置：
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### 禁用AI

如果不想使用AI解析：
```env
AI_ENABLED=false
```

---

## ❓ 常见问题

### Q: 安装PaddleOCR失败？
A: 可以先不安装，只使用UI Automation和OCR功能会跳过。

### Q: 执行失败？
A: 检查：
1. 元素名称是否正确
2. 是否需要管理员权限
3. 软件是否支持UI Automation

### Q: 如何查看日志？
A: 日志保存在 `logs/desktop-agent.log`

### Q: 如何重置配置？
A: 删除 `.env` 文件，重新从 `.env.example` 复制

---

## 📖 更多文档

- [项目总结](docs/PROJECT_SUMMARY.md)
- [架构说明](docs/ARCHITECTURE.md)
- [API文档](docs/API.md)
- [故障排查](docs/TROUBLESHOOTING.md)

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License
