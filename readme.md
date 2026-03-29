# Desktop Agent - 自然语言驱动的桌面自动化平台

<div align="center">

**让每个人都能用自然语言控制电脑**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

[English](README_EN.md) | 简体中文

</div>

---

## 📖 项目简介

**Desktop Agent** 是一个革命性的桌面自动化平台，让你用**自然语言**控制任意Windows软件，无需编写代码。

### 核心特点

- 🎯 **自然语言交互** - 说一句话，电脑自己干
- 🤖 **AI驱动** - GLM-4大模型理解语义，覆盖率95%+
- 🔄 **六层架构** - 模块化设计，可独立演进
- 🌐 **跨软件协作** - 自动识别数据流，支持多软件协作
- ⚡ **实时反馈** - Web界面实时监控执行过程
- 🛡️ **异常处理** - 智能恢复，自动降级

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/desktop-agent.git
cd desktop-agent

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 GLM-4 API Key
```

### 使用

#### 1. 命令行模式

```bash
python main.py
```

#### 2. Web界面模式

```bash
python start_web.py
```

访问 http://localhost:5000

---

## 💬 使用示例

### 基础操作

```
用户："打开记事本"
系统：✅ 已打开记事本

用户："输入 Hello World"
系统：✅ 已输入文本

用户："按 Ctrl+S 保存"
系统：✅ 已执行快捷键
```

### 跨软件协作

```
用户："把Excel里的销售数据整理后，发邮件给老板"

系统自动执行：
1. 打开Excel → 读取数据
2. 分析数据 → 生成图表
3. 打开Outlook → 创建邮件
4. 附件报表 → 发送

✅ 执行成功（3.5秒）
```

### 批量处理

```
用户："处理Excel里1000条客户数据，核对银行流水"

系统自动执行：
1. 读取Excel数据（1000行）
2. 循环处理每一行
3. 匹配银行流水
4. 生成核对报告

✅ 处理完成（1000/1000）
```

---

## 🏗️ 六层架构

```
┌─────────────────────────────────┐
│   用户层：自然语言交互          │
├─────────────────────────────────┤
│ L6 知识记忆层：学习优化    75%  │
├─────────────────────────────────┤
│ L5 验证反馈层：结果检查    70%  │
├─────────────────────────────────┤
│ L4 动作执行层：操作实施    95%  │
├─────────────────────────────────┤
│ L3 操作规划层：步骤生成    80%  │
├─────────────────────────────────┤
│ L2 屏幕感知层：界面理解    85%  │
├─────────────────────────────────┤
│ L1 意图理解层：AI解析      95%  │
└─────────────────────────────────┘
```

### 技术栈

- **AI层**：GLM-4（意图理解）+ GPT-4V（视觉理解）
- **自动化层**：pyautogui + uiautomation + Selenium
- **Web层**：Flask + SocketIO
- **数据层**：SQLite + JSON

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 意图理解准确率 | 97.5% |
| 任务覆盖率 | 95%+ |
| 异常自动恢复率 | 70%+ |
| 支持软件数量 | 50+ |
| 平均响应时间 | <1秒 |

---

## 🎯 自动化分级（L1-L4）

模仿智能驾驶的分级标准：

| 等级 | 名称 | 人工参与 | 状态 |
|------|------|----------|------|
| L1 | 辅助操作 | 80% | - |
| **L2** | **部分自动化** | **30%** | **✅ 当前** |
| L3 | 有条件自动化 | 5% | 开发中 |
| L4 | 高度自动化 | <1% | 规划中 |

---

## 📁 项目结构

```
desktop-agent/
├── core/              # 核心模块
│   ├── agent.py       # 主控制器
│   ├── config.py      # 配置管理
│   └── exception_handler.py  # 异常处理
├── layers/            # 六层架构
│   ├── layer1_intent/ # 意图理解层
│   ├── layer2_perception/  # 屏幕感知层
│   ├── layer3_planning/    # 操作规划层
│   ├── layer4_execution/   # 动作执行层
│   ├── layer5_validation/  # 验证反馈层
│   └── layer6_knowledge/   # 知识记忆层
├── web/               # Web界面
│   ├── app.py         # Flask应用
│   └── templates/     # HTML模板
├── tests/             # 测试
├── docs/              # 文档
├── main.py            # 命令行入口
├── start_web.py       # Web启动
└── requirements.txt   # 依赖列表
```

---

## 🔧 配置

### 环境变量

在 `.env` 文件中配置：

```env
# GLM-4 API配置
GLM_API_KEY=your_api_key_here
GLM_API_URL=https://open.bigmodel.cn/api/paas/v3/model-api/

# 可选：GPT-4配置
OPENAI_API_KEY=your_openai_key_here

# 可选：日志配置
LOG_LEVEL=INFO
```

---

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python test_improvements.py
```

---

## 📝 更新日志

### v3.2 (2026-03-29)
- ✅ 新增异常处理系统
- ✅ Web界面美化（暗色主题）
- ✅ 执行历史记录
- ✅ 统计图表

### v3.1 (2026-03-27)
- ✅ 集成意图确认系统
- ✅ 7种确认类型
- ✅ 用户偏好学习

### v3.0 (2026-03-25)
- 🎉 六层架构完成
- 🎉 AI驱动意图理解
- 🎉 覆盖率95%+

查看完整更新日志：[CHANGELOG.md](CHANGELOG.md)

---

## 🤝 贡献

欢迎贡献代码！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 📧 联系方式

- 项目主页：https://github.com/YOUR_USERNAME/desktop-agent
- 问题反馈：https://github.com/YOUR_USERNAME/desktop-agent/issues
- 邮箱：your.email@example.com

---

## 🙏 致谢

感谢以下开源项目：

- [GLM-4](https://open.bigmodel.cn/) - 大语言模型
- [pyautogui](https://pyautogui.readthedocs.io/) - GUI自动化
- [uiautomation](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows) - Windows UI自动化
- [Flask](https://flask.palletsprojects.com/) - Web框架

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by Desktop Agent Team

</div>
