"""
Desktop Agent - 意图识别系统化测试集
=====================================

测试集结构：
1. 基础操作（20个）- 单步简单操作
2. 中等复杂度（15个）- 多步骤流程
3. 高复杂度（10个）- 跨软件协作
4. 企业级场景（5个）- 真实业务场景
5. 边界情况（10个）- 异常/特殊场景

总计：60个测试用例
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from core.config import Config
import json
from datetime import datetime

print("=" * 70)
print("  Desktop Agent - 意图识别系统化测试集")
print("=" * 70)
print()

# 初始化
config = Config()
parser = AIDrivenIntentParser(config)

# ═══════════════════════════════════════════════════════════════
# 测试集定义
# ═══════════════════════════════════════════════════════════════

TEST_SUITE = {
    # ─────────────────────────────────────────────────────────────
    # 第1组：基础操作（20个）
    # ─────────────────────────────────────────────────────────────
    "基础操作": {
        "description": "单步简单操作，应该快速匹配",
        "cases": [
            {
                "id": "BASIC_001",
                "instruction": "点击确定按钮",
                "expected": {"action": "click", "steps": 1, "method": "quick_match"},
            },
            {
                "id": "BASIC_002",
                "instruction": "双击文件",
                "expected": {"action": "double_click", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_003",
                "instruction": "右键菜单",
                "expected": {"action": "right_click", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_004",
                "instruction": "输入'Hello World'",
                "expected": {"action": "type", "steps": 1, "method": "quick_match"},
            },
            {
                "id": "BASIC_005",
                "instruction": "在搜索框输入'Python'",
                "expected": {"action": "type", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_006",
                "instruction": "按Ctrl+S",
                "expected": {"action": "hotkey", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_007",
                "instruction": "向上滚动",
                "expected": {"action": "scroll", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_008",
                "instruction": "等待5秒",
                "expected": {"action": "wait", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_009",
                "instruction": "查找确定按钮",
                "expected": {"action": "find", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_010",
                "instruction": "点击文件菜单下的保存",
                "expected": {"action": "menu", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_011",
                "instruction": "复制选中内容",
                "expected": {"action": "copy", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_012",
                "instruction": "粘贴到编辑框",
                "expected": {"action": "paste", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_013",
                "instruction": "拖动文件到文件夹",
                "expected": {"action": "drag", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_014",
                "instruction": "点击第一个按钮",
                "expected": {"action": "click_index", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_015",
                "instruction": "点击最后一个文件",
                "expected": {"action": "click_last", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_016",
                "instruction": "清空输入框",
                "expected": {"action": "clear", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_017",
                "instruction": "截图保存",
                "expected": {"action": "screenshot", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_018",
                "instruction": "关闭窗口",
                "expected": {"action": "close", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_019",
                "instruction": "最大化窗口",
                "expected": {"action": "maximize", "steps": 1, "method": "ai"},
            },
            {
                "id": "BASIC_020",
                "instruction": "最小化窗口",
                "expected": {"action": "minimize", "steps": 1, "method": "ai"},
            },
        ],
    },
    
    # ─────────────────────────────────────────────────────────────
    # 第2组：中等复杂度（15个）
    # ─────────────────────────────────────────────────────────────
    "中等复杂度": {
        "description": "多步骤流程（2-5步）",
        "cases": [
            {
                "id": "MEDIUM_001",
                "instruction": "打开记事本，输入'你好'，保存文件",
                "expected": {"steps": 3, "software": ["记事本"]},
            },
            {
                "id": "MEDIUM_002",
                "instruction": "打开Word，写一份报告，保存为'月报.docx'",
                "expected": {"steps": 3, "software": ["Word"]},
            },
            {
                "id": "MEDIUM_003",
                "instruction": "打开微信，发消息给张三说'明天开会'",
                "expected": {"steps": 2, "software": ["微信"]},
            },
            {
                "id": "MEDIUM_004",
                "instruction": "打开浏览器，搜索'Python教程'，打开第一个结果",
                "expected": {"steps": 3, "software": ["浏览器"]},
            },
            {
                "id": "MEDIUM_005",
                "instruction": "打开Excel，在A1输入'姓名'，B1输入'年龄'",
                "expected": {"steps": 3, "software": ["Excel"]},
            },
            {
                "id": "MEDIUM_006",
                "instruction": "点击文件，选择另存为，输入文件名'测试'，点击保存",
                "expected": {"steps": 4},
            },
            {
                "id": "MEDIUM_007",
                "instruction": "选中所有文本，复制，打开新文档，粘贴",
                "expected": {"steps": 4},
            },
            {
                "id": "MEDIUM_008",
                "instruction": "打开计算器，输入5+3，按等号",
                "expected": {"steps": 3, "software": ["计算器"]},
            },
            {
                "id": "MEDIUM_009",
                "instruction": "打开邮件，新建邮件，输入收件人，发送",
                "expected": {"steps": 4, "software": ["邮件"]},
            },
            {
                "id": "MEDIUM_010",
                "instruction": "打开设置，找到网络，打开WiFi，连接到'HomeWiFi'",
                "expected": {"steps": 4, "software": ["设置"]},
            },
            {
                "id": "MEDIUM_011",
                "instruction": "打开文件夹，选中所有文件，复制到另一个文件夹",
                "expected": {"steps": 3},
            },
            {
                "id": "MEDIUM_012",
                "instruction": "打开播放器，添加文件'音乐.mp3'，播放",
                "expected": {"steps": 3, "software": ["播放器"]},
            },
            {
                "id": "MEDIUM_013",
                "instruction": "打开图片，调整大小为800x600，保存",
                "expected": {"steps": 3},
            },
            {
                "id": "MEDIUM_014",
                "instruction": "打开PDF，跳转到第10页，截图，保存",
                "expected": {"steps": 4, "software": ["PDF"]},
            },
            {
                "id": "MEDIUM_015",
                "instruction": "打开命令行，输入'ping google.com'，等待结果",
                "expected": {"steps": 3, "software": ["命令行"]},
            },
        ],
    },
    
    # ─────────────────────────────────────────────────────────────
    # 第3组：高复杂度（10个）
    # ─────────────────────────────────────────────────────────────
    "高复杂度": {
        "description": "跨软件协作（5-10步）",
        "cases": [
            {
                "id": "HIGH_001",
                "instruction": "从Excel复制数据，粘贴到Word，保存，发送邮件给老板",
                "expected": {"steps": 4, "software": ["Excel", "Word", "邮件"]},
            },
            {
                "id": "HIGH_002",
                "instruction": "打开浏览器，搜索产品信息，截图，保存到Word文档",
                "expected": {"steps": 4, "software": ["浏览器", "Word"]},
            },
            {
                "id": "HIGH_003",
                "instruction": "打开记事本，输入代码，保存为.py文件，运行Python",
                "expected": {"steps": 4, "software": ["记事本", "Python"]},
            },
            {
                "id": "HIGH_004",
                "instruction": "打开ERP系统，查询订单，导出Excel，发送给客户",
                "expected": {"steps": 4, "software": ["ERP", "Excel", "邮件"]},
            },
            {
                "id": "HIGH_005",
                "instruction": "打开微信，接收文件，保存到桌面，用Excel打开",
                "expected": {"steps": 4, "software": ["微信", "Excel"]},
            },
            {
                "id": "HIGH_006",
                "instruction": "打开数据库工具，执行查询，导出结果，生成报告",
                "expected": {"steps": 4, "software": ["数据库工具"]},
            },
            {
                "id": "HIGH_007",
                "instruction": "打开Photoshop，调整图片，导出PNG，上传到网站",
                "expected": {"steps": 4, "software": ["Photoshop", "网站"]},
            },
            {
                "id": "HIGH_008",
                "instruction": "打开视频编辑器，剪辑视频，添加字幕，导出MP4",
                "expected": {"steps": 4, "software": ["视频编辑器"]},
            },
            {
                "id": "HIGH_009",
                "instruction": "打开企业微信，创建群聊，邀请3个人，发送消息",
                "expected": {"steps": 4, "software": ["企业微信"]},
            },
            {
                "id": "HIGH_010",
                "instruction": "打开浏览器，登录网站，填写表单，提交，截图确认",
                "expected": {"steps": 5, "software": ["浏览器"]},
            },
        ],
    },
    
    # ─────────────────────────────────────────────────────────────
    # 第4组：企业级场景（5个）
    # ─────────────────────────────────────────────────────────────
    "企业级场景": {
        "description": "真实业务场景（10+步，复杂逻辑）",
        "cases": [
            {
                "id": "ENTERPRISE_001",
                "instruction": "帮我登录工商银行网银下载流水，把流水与ERP中的客户收款信息进行核对",
                "expected": {"steps": 10, "software": ["工商银行网银", "ERP"]},
            },
            {
                "id": "ENTERPRISE_002",
                "instruction": "打开Excel表，将Excel表里的收货日期、收货的数目以及金额进行整理匹配。同工商银行的网上下载的流水进行比对，数据有1000条，请重复这个过程",
                "expected": {"steps": 8, "software": ["Excel", "工商银行网银"], "loop": True},
            },
            {
                "id": "ENTERPRISE_003",
                "instruction": "从CRM系统导出客户名单，筛选出本月新增客户，生成Excel报表，发送给销售经理",
                "expected": {"steps": 5, "software": ["CRM", "Excel", "邮件"]},
            },
            {
                "id": "ENTERPRISE_004",
                "instruction": "打开财务系统，核对本月发票，与银行对账单比对，标记差异项，生成差异报告",
                "expected": {"steps": 6, "software": ["财务系统", "银行对账单"]},
            },
            {
                "id": "ENTERPRISE_005",
                "instruction": "从生产系统读取数据，分析良品率，生成图表，插入PPT，发送周报邮件",
                "expected": {"steps": 6, "software": ["生产系统", "PPT", "邮件"]},
            },
        ],
    },
    
    # ─────────────────────────────────────────────────────────────
    # 第5组：边界情况（10个）
    # ─────────────────────────────────────────────────────────────
    "边界情况": {
        "description": "异常/特殊场景",
        "cases": [
            {
                "id": "EDGE_001",
                "instruction": "如果找到确定按钮就点击，否则继续搜索",
                "expected": {"action": "if_exists", "conditional": True},
            },
            {
                "id": "EDGE_002",
                "instruction": "重复点击确定按钮3次",
                "expected": {"action": "repeat", "loop": True, "times": 3},
            },
            {
                "id": "EDGE_003",
                "instruction": "如果价格小于100就购买，否则跳过",
                "expected": {"conditional": True},
            },
            {
                "id": "EDGE_004",
                "instruction": "等待10秒后继续",
                "expected": {"action": "wait"},
            },
            {
                "id": "EDGE_005",
                "instruction": "循环处理所有文件直到完成",
                "expected": {"loop": True},
            },
            {
                "id": "EDGE_006",
                "instruction": "如果失败就重试5次",
                "expected": {"conditional": True, "retry": True},
            },
            {
                "id": "EDGE_007",
                "instruction": "同时打开3个Excel文件",
                "expected": {"parallel": True},
            },
            {
                "id": "EDGE_008",
                "instruction": "弹出对话框让用户确认",
                "expected": {"needs_confirmation": True},
            },
            {
                "id": "EDGE_009",
                "instruction": "点击那个红色的按钮",
                "expected": {"visual": True},
            },
            {
                "id": "EDGE_010",
                "instruction": "把刚才复制的内容粘贴到这里",
                "expected": {"context_aware": True},
            },
        ],
    },
}

# ═══════════════════════════════════════════════════════════════
# 运行测试
# ═══════════════════════════════════════════════════════════════

print("开始测试...")
print()

results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "groups": {},
}

start_time = datetime.now()

for group_name, group_data in TEST_SUITE.items():
    print(f"\n{'='*70}")
    print(f"测试组: {group_name}")
    print(f"说明: {group_data['description']}")
    print(f"用例数: {len(group_data['cases'])}")
    print('='*70)
    
    group_results = {
        "total": len(group_data["cases"]),
        "passed": 0,
        "failed": 0,
        "details": [],
    }
    
    for case in group_data["cases"]:
        case_id = case["id"]
        instruction = case["instruction"]
        expected = case["expected"]
        
        print(f"\n[{case_id}] {instruction}")
        
        # 解析
        result = parser.parse(instruction)
        
        # 评估
        success = True
        
        # 检查步骤数
        if "steps" in expected:
            actual_steps = len(result.get("steps", []))
            if actual_steps < expected["steps"]:
                success = False
                print(f"  [FAIL] 步骤数不足: 期望>={expected['steps']}, 实际={actual_steps}")
        
        # 检查软件
        if "software" in expected:
            actual_software = result.get("software", [])
            for sw in expected["software"]:
                if not any(sw.lower() in s.lower() for s in actual_software):
                    success = False
                    print(f"  [FAIL] 缺少软件: {sw}")
        
        # 检查循环
        if expected.get("loop"):
            has_loop = any(s.get("action") == "repeat" for s in result.get("steps", []))
            if not has_loop:
                success = False
                print(f"  [FAIL] 未识别循环需求")
        
        # 检查条件
        if expected.get("conditional"):
            has_condition = any("if" in s.get("action", "").lower() or 
                              "condition" in str(s.get("params", {})).lower() 
                              for s in result.get("steps", []))
            if not has_condition:
                success = False
                print(f"  [FAIL] 未识别条件逻辑")
        
        # 简单检查：只要解析成功就算通过
        if result.get("task_type") and result.get("task_type") != "unknown":
            if success:  # 如果上面的检查都通过
                group_results["passed"] += 1
                print(f"  [OK] 通过 (步骤数: {len(result.get('steps', []))})")
            else:
                group_results["failed"] += 1
        else:
            success = False
            group_results["failed"] += 1
            print(f"  [FAIL] 解析失败")
        
        group_results["details"].append({
            "id": case_id,
            "instruction": instruction,
            "success": success,
            "steps": len(result.get("steps", [])),
            "software": result.get("software", []),
            "task_type": result.get("task_type"),
        })
    
    results["groups"][group_name] = group_results
    results["total"] += group_results["total"]
    results["passed"] += group_results["passed"]
    results["failed"] += group_results["failed"]

end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

# ═══════════════════════════════════════════════════════════════
# 显示总结
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("  测试总结")
print("=" * 70)
print()

print(f"总测试用例: {results['total']}")
print(f"通过: {results['passed']}")
print(f"失败: {results['failed']}")
print(f"成功率: {results['passed']/results['total']*100:.1f}%")
print(f"耗时: {duration:.1f}秒")
print()

print("分组详情:")
print("-" * 70)
for group_name, group_data in results["groups"].items():
    passed = group_data["passed"]
    total = group_data["total"]
    rate = (passed / total * 100) if total > 0 else 0
    print(f"  {group_name:15s} {passed:2d}/{total:2d} ({rate:5.1f}%)")

print()

if results["passed"] == results["total"]:
    print("[SUCCESS] 所有测试通过！")
elif results["passed"] >= results["total"] * 0.9:
    print("[GOOD] 90%以上测试通过")
elif results["passed"] >= results["total"] * 0.8:
    print("[OK] 80%以上测试通过")
else:
    print("[WARNING] 需要改进")

print()
print("=" * 70)

# 保存测试报告
report = {
    "timestamp": start_time.isoformat(),
    "duration_seconds": duration,
    "summary": {
        "total": results["total"],
        "passed": results["passed"],
        "failed": results["failed"],
        "success_rate": results["passed"] / results["total"],
    },
    "groups": results["groups"],
}

with open("test_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("测试报告已保存: test_report.json")
