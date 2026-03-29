"""
企业级复杂任务测试用例集（增强版）
所有用例：10+ 步骤
1/3用例：20+ 步骤
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from layers.layer1_intent.ai_intent_parser import AIDrivenIntentParser
from core.config import Config
import json

# ═══════════════════════════════════════════════════════════════
# 复杂测试用例配置
# ═══════════════════════════════════════════════════════════════

COMPLEX_INDUSTRY_TEST_CASES = {
    # ═══════════════════════════════════════════════════════════
    # 金融行业（15个复杂任务）
    # 5个用例：20+步骤（高复杂度）
    # 10个用例：10-19步骤（中高复杂度）
    # ═══════════════════════════════════════════════════════════
    "finance": {
        "name": "金融行业",
        "icon": "💰",
        "test_cases": [
            # ═════════════════════════════════════════════════
            # 超复杂任务（20+步骤）- 5个
            # ═════════════════════════════════════════════════
            {
                "id": "FIN001",
                "category": "月度财务对账与报表",
                "difficulty": "极高",
                "steps_count": 25,
                "instruction": """
                月度财务对账全流程任务：
                
                1. 登录工商银行企业网银系统
                2. 导航到账户管理页面
                3. 选择本月时间范围
                4. 下载本月所有银行流水明细（Excel格式）
                5. 退出工商银行网银
                
                6. 登录建设银行企业网银系统
                7. 下载建设银行本月流水
                8. 退出建设银行网银
                
                9. 登录农业银行企业网银系统
                10. 下载农业银行本月流水
                11. 退出农业银行网银
                
                12. 打开ERP财务系统
                13. 导出本月所有收款记录
                14. 导出本月所有付款记录
                15. 退出ERP系统
                
                16. 打开Excel，创建新工作簿
                17. 将三个银行流水合并到一个工作表
                18. 将ERP收款记录导入第二个工作表
                19. 使用VLOOKUP函数匹配银行流水与ERP记录
                20. 标记所有未匹配项（差异项）
                21. 对差异项进行分类（时间性差异、记账错误、未达账项）
                22. 生成差异调节表
                23. 创建月度对账报告
                24. 保存对账文件
                25. 通过邮件发送给财务总监审核
                """,
                "expected": {
                    "steps": 25,
                    "software": ["工商银行网银", "建设银行网银", "农业银行网银", "ERP系统", "Excel", "邮件"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                    "loop_required": False,
                    "condition_required": True,
                },
                "business_context": "月度多银行账户与ERP系统全面对账",
            },
            {
                "id": "FIN002",
                "category": "贷款审批全流程",
                "difficulty": "极高",
                "steps_count": 22,
                "instruction": """
                企业贷款审批自动化流程：
                
                1. 登录CRM系统
                2. 搜索申请人企业信息
                3. 导出企业基本信息表
                4. 导出企业股东信息表
                5. 退出CRM系统
                
                6. 登录征信查询系统
                7. 输入企业统一社会信用代码
                8. 下载企业征信报告
                9. 下载企业法定代表人征信报告
                10. 退出征信系统
                
                11. 登录税务查询系统
                12. 下载企业近三年纳税记录
                13. 下载企业纳税信用等级
                14. 退出税务系统
                
                15. 登录工商查询系统
                16. 下载企业工商登记信息
                17. 下载企业股权结构图
                18. 退出工商系统
                
                19. 打开Excel审批模板
                20. 整合所有资料到审批表
                21. 使用风控模型计算风险评分
                22. 生成审批建议报告并提交审批
                """,
                "expected": {
                    "steps": 22,
                    "software": ["CRM系统", "征信系统", "税务系统", "工商系统", "Excel"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "企业贷款审批多系统资料收集与风险评估",
            },
            {
                "id": "FIN003",
                "category": "季度财务报表编制",
                "difficulty": "极高",
                "steps_count": 23,
                "instruction": """
                季度财务报表编制与审计准备：
                
                1. 登录财务系统
                2. 导出资产负债表
                3. 导出利润表
                4. 导出现金流量表
                5. 导出所有者权益变动表
                6. 退出财务系统
                
                7. 登录工商银行网银
                8. 下载季度银行对账单
                9. 下载银行回单
                10. 退出网银系统
                
                11. 登录税务系统
                12. 导出增值税申报表
                13. 导出所得税申报表
                14. 退出税务系统
                
                15. 打开Excel
                16. 创建季度报表工作簿
                17. 将四大报表导入对应工作表
                18. 计算关键财务指标（流动比率、速动比率、资产负债率等）
                19. 生成财务分析说明
                20. 创建审计调整分录表
                21. 准备审计所需备查资料清单
                22. 保存季度报表文件
                23. 通过邮件发送给审计机构
                """,
                "expected": {
                    "steps": 23,
                    "software": ["财务系统", "工商银行网银", "税务系统", "Excel", "邮件"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "季度财务报表编制与审计资料准备",
            },
            {
                "id": "FIN004",
                "category": "年度预算编制",
                "difficulty": "极高",
                "steps_count": 28,
                "instruction": """
                年度预算编制全流程：
                
                1. 登录ERP系统
                2. 导出去年销售数据
                3. 导出去年成本数据
                4. 导出去年费用数据
                5. 导出去年利润数据
                6. 退出ERP系统
                
                7. 登录HR系统
                8. 导出员工薪酬数据
                9. 导出部门人员编制
                10. 退出HR系统
                
                11. 登录CRM系统
                12. 导出客户数据
                13. 导出销售预测数据
                14. 退出CRM系统
                
                15. 打开Excel预算模板
                16. 导入历史数据到对应工作表
                17. 计算收入增长率
                18. 计算成本变化趋势
                19. 编制收入预算表
                20. 编制成本预算表
                21. 编制费用预算表
                22. 编制资本支出预算
                23. 编制现金流预算
                24. 汇总生成预算资产负债表
                25. 汇总生成预算利润表
                26. 保存预算文件
                27. 通过邮件发送给各部门负责人
                28. 收集反馈并修订预算
                """,
                "expected": {
                    "steps": 28,
                    "software": ["ERP系统", "HR系统", "CRM系统", "Excel", "邮件"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                    "loop_required": False,
                },
                "business_context": "年度全面预算编制与审批流程",
            },
            {
                "id": "FIN005",
                "category": "反洗钱合规审查",
                "difficulty": "极高",
                "steps_count": 24,
                "instruction": """
                反洗钱合规审查全流程：
                
                1. 登录交易系统
                2. 设置大额交易筛选条件（单笔≥5万或当日累计≥20万）
                3. 导出大额交易清单
                4. 导出可疑交易标记记录
                5. 退出交易系统
                
                6. 登录客户信息系统
                7. 导出高风险客户名单
                8. 导出客户身份信息
                9. 导出客户交易历史
                10. 退出客户系统
                
                11. 打开Excel
                12. 创建反洗钱分析工作表
                13. 将大额交易与客户信息匹配
                14. 标记异常交易模式（频繁小额后大额、快进快出等）
                15. 对标记交易进行风险评分
                16. 生成可疑交易报告
                17. 准备客户尽职调查资料
                
                18. 登录反洗钱报送系统
                19. 上传可疑交易报告
                20. 填写报送说明
                21. 提交审核
                22. 退出报送系统
                
                23. 保存审查记录
                24. 通过邮件通知合规部门
                """,
                "expected": {
                    "steps": 24,
                    "software": ["交易系统", "客户信息系统", "Excel", "反洗钱报送系统", "邮件"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                    "condition_required": True,
                },
                "business_context": "反洗钱合规审查与可疑交易报送",
            },
            
            # ═════════════════════════════════════════════════
            # 高复杂度任务（10-19步骤）- 10个
            # ═════════════════════════════════════════════════
            {
                "id": "FIN006",
                "category": "税务申报",
                "difficulty": "高",
                "steps_count": 16,
                "instruction": """
                月度税务申报流程：
                
                1. 登录开票系统
                2. 导出本月所有开票记录
                3. 按税率分类统计
                4. 退出开票系统
                
                5. 登录进项发票管理系统
                6. 导出本月认证通过的进项发票
                7. 按税率分类统计
                8. 退出进项系统
                
                9. 打开Excel税务计算表
                10. 输入销项税额
                11. 输入进项税额
                12. 计算应纳税额
                13. 生成增值税申报表
                
                14. 登录电子税务局
                15. 上传申报表并提交
                16. 下载申报回执并保存
                """,
                "expected": {
                    "steps": 16,
                    "software": ["开票系统", "进项发票管理系统", "Excel", "电子税务局"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "月度增值税申报",
            },
            {
                "id": "FIN007",
                "category": "客户开户全流程",
                "difficulty": "高",
                "steps_count": 14,
                "instruction": """
                企业客户开户流程：
                
                1. 登录CRM系统
                2. 创建新客户档案
                3. 录入企业基本信息
                4. 上传营业执照扫描件
                5. 上传法定代表人身份证
                6. 录入股东信息
                7. 上传公司章程
                
                8. 登录工商查询系统
                9. 核实企业工商信息
                10. 退出工商系统
                
                11. 返回CRM系统
                12. 完成尽职调查表
                13. 提交开户申请审批
                14. 发送审批通知给客户经理
                """,
                "expected": {
                    "steps": 14,
                    "software": ["CRM系统", "工商查询系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "企业客户开户与尽职调查",
            },
            {
                "id": "FIN008",
                "category": "投资组合管理",
                "difficulty": "高",
                "steps_count": 18,
                "instruction": """
                投资组合日常管理：
                
                1. 登录交易系统
                2. 导出持仓明细
                3. 导出今日交易记录
                4. 退出交易系统
                
                5. 登录行情系统
                6. 获取所有持仓股票收盘价
                7. 导出市场指数数据
                8. 退出行情系统
                
                9. 打开Excel
                10. 更新持仓市值
                11. 计算当日盈亏
                12. 计算累计盈亏
                13. 计算投资组合收益率
                14. 与基准指数对比
                15. 生成投资组合日报
                
                16. 保存日报文件
                17. 通过邮件发送给投资经理
                18. 备份数据到云盘
                """,
                "expected": {
                    "steps": 18,
                    "software": ["交易系统", "行情系统", "Excel", "邮件", "云盘"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "投资组合日常监控与报告",
            },
            {
                "id": "FIN009",
                "category": "报销审批流程",
                "difficulty": "高",
                "steps_count": 13,
                "instruction": """
                员工报销审批流程：
                
                1. 登录报销系统
                2. 导出待审批报销单列表
                3. 选择第一张报销单
                
                对于每张报销单：
                4. 检查发票真伪（登录税务发票查验系统）
                5. 核对发票金额与报销金额
                6. 检查报销项目是否符合政策
                7. 审批通过或退回
                
                8. 退出发票查验系统
                9. 返回报销系统继续处理下一张
                10. 批量审批完成后退出
                
                11. 登录财务系统
                12. 生成付款指令
                13. 提交财务审核
                """,
                "expected": {
                    "steps": 13,
                    "software": ["报销系统", "税务发票查验系统", "财务系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                    "loop_required": True,
                },
                "business_context": "批量报销审批与付款处理",
            },
            {
                "id": "FIN010",
                "category": "资金调拨",
                "difficulty": "高",
                "steps_count": 15,
                "instruction": """
                跨银行资金调拨流程：
                
                1. 登录工商银行网银
                2. 查询账户余额
                3. 导出账户余额截图
                4. 退出工商银行网银
                
                5. 登录建设银行网银
                6. 查询账户余额
                7. 导出账户余额截图
                8. 退出建设银行网银
                
                9. 打开Excel
                10. 创建资金分布表
                11. 计算各账户资金占比
                12. 制定资金调拨方案
                
                13. 登录资金管理系统
                14. 提交资金调拨申请
                15. 发送审批通知给财务总监
                """,
                "expected": {
                    "steps": 15,
                    "software": ["工商银行网银", "建设银行网银", "Excel", "资金管理系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "多银行账户资金管理与调拨",
            },
            {
                "id": "FIN011",
                "category": "风险预警处理",
                "difficulty": "高",
                "steps_count": 14,
                "instruction": """
                逾期客户风险预警处理：
                
                1. 登录风险管理系统
                2. 导出逾期客户清单
                3. 按逾期天数分类
                4. 退出风险系统
                
                5. 登录催收系统
                6. 导出催收记录
                7. 查看催收进展
                8. 退出催收系统
                
                9. 打开Excel
                10. 匹配逾期客户与催收记录
                11. 计算逾期金额汇总
                12. 生成风险预警报告
                
                13. 通过邮件发送给风控部门
                14. 通过企业微信通知相关客户经理
                """,
                "expected": {
                    "steps": 14,
                    "software": ["风险管理系统", "催收系统", "Excel", "邮件", "企业微信"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "逾期风险监控与预警",
            },
            {
                "id": "FIN012",
                "category": "凭证归档",
                "difficulty": "高",
                "steps_count": 12,
                "instruction": """
                会计凭证归档流程：
                
                1. 登录凭证管理系统
                2. 导出本月所有会计凭证
                3. 按凭证号排序
                4. 退出凭证系统
                
                5. 登录银行网银
                6. 下载所有银行回单
                7. 退出网银系统
                
                8. 打开文件夹
                9. 将凭证与回单一一匹配
                10. 扫描未电子化的纸质凭证
                
                11. 登录档案管理系统
                12. 上传所有电子凭证并归档
                """,
                "expected": {
                    "steps": 12,
                    "software": ["凭证管理系统", "银行网银", "档案管理系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "会计凭证电子化归档",
            },
            {
                "id": "FIN013",
                "category": "客户投诉处理",
                "difficulty": "高",
                "steps_count": 11,
                "instruction": """
                客户投诉处理流程：
                
                1. 登录客服系统
                2. 导出本月投诉记录
                3. 按投诉类型分类
                4. 退出客服系统
                
                5. 打开Excel
                6. 统计各类型投诉数量
                7. 计算投诉处理时效
                8. 生成投诉分析报告
                
                9. 登录CRM系统
                10. 更新投诉客户标签
                11. 发送改进建议给相关部门
                """,
                "expected": {
                    "steps": 11,
                    "software": ["客服系统", "Excel", "CRM系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "客户投诉分析与改进",
            },
            {
                "id": "FIN014",
                "category": "内部审计",
                "difficulty": "高",
                "steps_count": 16,
                "instruction": """
                内部审计流程：
                
                1. 登录财务系统
                2. 导出本月所有凭证
                3. 导出科目余额表
                4. 退出财务系统
                
                5. 登录采购系统
                6. 导出采购订单
                7. 导出供应商信息
                8. 退出采购系统
                
                9. 打开Excel
                10. 抽取10%凭证进行详细审查
                11. 核对凭证与原始单据
                12. 检查审批流程完整性
                13. 记录审计发现
                14. 生成审计工作底稿
                
                15. 保存审计文件
                16. 通过邮件发送给审计主管
                """,
                "expected": {
                    "steps": 16,
                    "software": ["财务系统", "采购系统", "Excel", "邮件"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "内部审计与工作底稿编制",
            },
            {
                "id": "FIN015",
                "category": "监管报表报送",
                "difficulty": "高",
                "steps_count": 17,
                "instruction": """
                监管报表报送流程：
                
                1. 登录核心业务系统
                2. 导出贷款余额数据
                3. 导出存款余额数据
                4. 导出资产质量数据
                5. 退出核心系统
                
                6. 登录风险管理系统
                7. 导出资本充足率数据
                8. 导出流动性指标数据
                9. 退出风险系统
                
                10. 打开Excel监管报表模板
                11. 填写G01资产负债表
                12. 填写G11资产质量表
                13. 填写G41资本充足率表
                14. 校验报表逻辑关系
                
                15. 登录监管报送系统
                16. 上传监管报表
                17. 提交报送并下载回执
                """,
                "expected": {
                    "steps": 17,
                    "software": ["核心业务系统", "风险管理系统", "Excel", "监管报送系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "银行业监管报表编制与报送",
            },
        ],
    },
    
    # ═══════════════════════════════════════════════════════════
    # 制造行业（15个复杂任务）
    # 5个用例：20+步骤
    # 10个用例：10-19步骤
    # ═══════════════════════════════════════════════════════════
    "manufacturing": {
        "name": "制造行业",
        "icon": "🏭",
        "test_cases": [
            # ═════════════════════════════════════════════════
            # 超复杂任务（20+步骤）- 5个
            # ═════════════════════════════════════════════════
            {
                "id": "MFG001",
                "category": "生产计划排程优化",
                "difficulty": "极高",
                "steps_count": 26,
                "instruction": """
                生产计划排程优化全流程：
                
                1. 登录ERP系统
                2. 导出未来30天销售订单
                3. 按产品类型分类
                4. 按交货期排序
                5. 退出ERP系统
                
                6. 登录MES系统
                7. 查询各产线当前状态
                8. 查询各产线产能数据
                9. 查询设备维护计划
                10. 退出MES系统
                
                11. 登录WMS系统
                12. 查询成品库存
                13. 查询原材料库存
                14. 查询在制品数量
                15. 退出WMS系统
                
                16. 打开Excel排程工具
                17. 导入销售订单数据
                18. 导入产能数据
                19. 导入库存数据
                20. 计算净需求量
                21. 运行排程算法
                22. 生成生产计划表
                23. 生成物料需求计划
                24. 保存排程文件
                
                25. 登录MES系统
                26. 导入生产计划并发布到各产线
                """,
                "expected": {
                    "steps": 26,
                    "software": ["ERP系统", "MES系统", "WMS系统", "Excel"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "多系统集成生产计划排程优化",
            },
            {
                "id": "MFG002",
                "category": "全面质量管理",
                "difficulty": "极高",
                "steps_count": 24,
                "instruction": """
                全面质量管理体系：
                
                1. 登录MES系统
                2. 导出本月生产批次记录
                3. 导出各批次质检数据
                4. 退出MES系统
                
                5. 登录质量管理系统
                6. 导出不良品记录
                7. 导出返工记录
                8. 导出报废记录
                9. 退出质量系统
                
                10. 登录客户投诉系统
                11. 导出质量相关投诉
                12. 退出投诉系统
                
                13. 打开Excel质量分析模板
                14. 汇总所有质量数据
                15. 计算不良率
                16. 计算返工率
                17. 计算报废率
                18. 统计不良原因分布
                19. 使用帕累托图分析主要问题
                20. 生成质量月报
                
                21. 登录质量管理系统
                22. 录入纠正预防措施
                23. 创建质量改进项目
                24. 通过邮件发送报告给质量总监
                """,
                "expected": {
                    "steps": 24,
                    "software": ["MES系统", "质量管理系统", "客户投诉系统", "Excel", "邮件"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "全面质量管理与持续改进",
            },
            {
                "id": "MFG003",
                "category": "供应链协同管理",
                "difficulty": "极高",
                "steps_count": 25,
                "instruction": """
                供应链协同管理流程：
                
                1. 登录ERP系统
                2. 导出物料需求计划
                3. 导出采购申请单
                4. 退出ERP系统
                
                5. 登录WMS系统
                6. 查询各物料库存
                7. 查询安全库存设置
                8. 导出库存预警清单
                9. 退出WMS系统
                
                10. 登录SRM系统
                11. 导出供应商清单
                12. 导出供应商绩效评分
                13. 导出在途订单
                14. 退出SRM系统
                
                15. 登录物流系统
                16. 查询在途物料位置
                17. 预计到货时间
                18. 退出物流系统
                
                19. 打开Excel采购计划表
                20. 计算净采购需求
                21. 分配供应商
                22. 生成采购订单
                
                23. 登录采购系统
                24. 导入采购订单
                25. 批量发送给供应商
                """,
                "expected": {
                    "steps": 25,
                    "software": ["ERP系统", "WMS系统", "SRM系统", "物流系统", "Excel", "采购系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "供应链计划与采购协同",
            },
            {
                "id": "MFG004",
                "category": "设备全生命周期管理",
                "difficulty": "极高",
                "steps_count": 22,
                "instruction": """
                设备全生命周期管理：
                
                1. 登录设备管理系统
                2. 导出设备台账
                3. 导出设备运行记录
                4. 导出设备故障记录
                5. 导出设备维护记录
                6. 退出设备系统
                
                7. 登录SCADA系统
                8. 采集设备实时运行数据
                9. 导出设备OEE数据
                10. 退出SCADA系统
                
                11. 打开Excel设备分析模板
                12. 计算设备利用率
                13. 计算设备故障率
                14. 分析故障原因
                15. 制定预防性维护计划
                16. 生成设备状态报告
                
                17. 登录备件管理系统
                18. 查询备件库存
                19. 生成备件采购申请
                
                20. 登录设备管理系统
                21. 导入维护计划
                22. 发送维护通知给维修部门
                """,
                "expected": {
                    "steps": 22,
                    "software": ["设备管理系统", "SCADA系统", "Excel", "备件管理系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "设备监控与维护管理",
            },
            {
                "id": "MFG005",
                "category": "成本核算与分析",
                "difficulty": "极高",
                "steps_count": 23,
                "instruction": """
                产品成本核算与分析：
                
                1. 登录财务系统
                2. 导出原材料成本数据
                3. 导出人工成本数据
                4. 导出制造费用数据
                5. 退出财务系统
                
                6. 登录MES系统
                7. 导出各产品工时数据
                8. 导出各产品物料消耗
                9. 退出MES系统
                
                10. 登录WMS系统
                11. 导出原材料领用记录
                12. 退出WMS系统
                
                13. 打开Excel成本计算模板
                14. 汇总所有成本数据
                15. 计算直接材料成本
                16. 计算直接人工成本
                17. 分配制造费用
                18. 计算产品单位成本
                19. 与标准成本对比
                20. 分析成本差异原因
                21. 生成成本分析报告
                
                22. 保存成本文件
                23. 通过邮件发送给财务经理
                """,
                "expected": {
                    "steps": 23,
                    "software": ["财务系统", "MES系统", "WMS系统", "Excel", "邮件"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "产品成本核算与差异分析",
            },
            
            # ═════════════════════════════════════════════════
            # 高复杂度任务（10-19步骤）- 10个
            # ═════════════════════════════════════════════════
            {
                "id": "MFG006",
                "category": "生产进度跟踪",
                "difficulty": "高",
                "steps_count": 15,
                "instruction": """
                生产进度跟踪与调度：
                
                1. 登录MES系统
                2. 查询各产线当前工单
                3. 导出生产进度数据
                4. 查询异常停机记录
                5. 退出MES系统
                
                6. 登录ERP系统
                7. 导出销售订单交期
                8. 退出ERP系统
                
                9. 打开Excel进度跟踪表
                10. 计算各订单完成率
                11. 识别延期风险订单
                12. 生成生产进度报告
                
                13. 登录MES系统
                14. 调整生产优先级
                15. 通知产线主管
                """,
                "expected": {
                    "steps": 15,
                    "software": ["MES系统", "ERP系统", "Excel"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "生产进度监控与调度调整",
            },
            {
                "id": "MFG007",
                "category": "质量追溯",
                "difficulty": "高",
                "steps_count": 14,
                "instruction": """
                产品质量追溯流程：
                
                1. 登录MES系统
                2. 输入产品批次号
                3. 导出生产过程记录
                4. 导出质检数据
                5. 退出MES系统
                
                6. 登录WMS系统
                7. 查询该批次原材料来源
                8. 导出供应商信息
                9. 退出WMS系统
                
                10. 打开Excel追溯报告模板
                11. 整合生产与物料信息
                12. 生成产品追溯档案
                
                13. 保存追溯文件
                14. 通过邮件发送给质量部门
                """,
                "expected": {
                    "steps": 14,
                    "software": ["MES系统", "WMS系统", "Excel", "邮件"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "产品质量追溯与档案管理",
            },
            {
                "id": "MFG008",
                "category": "库存盘点",
                "difficulty": "高",
                "steps_count": 16,
                "instruction": """
                月度库存盘点流程：
                
                1. 登录WMS系统
                2. 导出库存清单
                3. 导出库位清单
                4. 退出WMS系统
                
                5. 打印盘点单
                
                6. 登录手持终端系统
                7. 扫描各库位物料
                8. 录入实盘数量
                9. 退出终端系统
                
                10. 登录WMS系统
                11. 导入盘点数据
                12. 系统自动对比
                13. 生成盘点差异报告
                14. 审批盘点调整
                
                15. 保存盘点文件
                16. 发送盘点报告给财务部门
                """,
                "expected": {
                    "steps": 16,
                    "software": ["WMS系统", "手持终端系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "月度库存盘点与差异处理",
            },
            {
                "id": "MFG009",
                "category": "供应商绩效评估",
                "difficulty": "高",
                "steps_count": 13,
                "instruction": """
                供应商季度绩效评估：
                
                1. 登录SRM系统
                2. 导出供应商交货记录
                3. 导出质量检验记录
                4. 导出价格变动记录
                5. 退出SRM系统
                
                6. 打开Excel评估模板
                7. 计算交货及时率
                8. 计算质量合格率
                9. 计算价格竞争力
                10. 综合评分并排名
                11. 生成供应商绩效报告
                
                12. 登录SRM系统
                13. 更新供应商评级
                """,
                "expected": {
                    "steps": 13,
                    "software": ["SRM系统", "Excel"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "供应商绩效评估与分级管理",
            },
            {
                "id": "MFG010",
                "category": "工艺优化",
                "difficulty": "高",
                "steps_count": 15,
                "instruction": """
                工艺参数优化流程：
                
                1. 登录PLM系统
                2. 导出产品工艺路线
                3. 导出标准工时
                4. 退出PLM系统
                
                5. 登录MES系统
                6. 导出实际工时数据
                7. 导出设备参数记录
                8. 退出MES系统
                
                9. 打开Excel分析工具
                10. 对比标准与实际工时
                11. 分析效率损失原因
                12. 模拟优化方案
                13. 生成工艺优化建议
                
                14. 登录PLM系统
                15. 更新工艺参数
                """,
                "expected": {
                    "steps": 15,
                    "software": ["PLM系统", "MES系统", "Excel"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "工艺参数优化与效率提升",
            },
            {
                "id": "MFG011",
                "category": "能耗管理",
                "difficulty": "高",
                "steps_count": 14,
                "instruction": """
                能耗监控与分析：
                
                1. 登录能耗监测系统
                2. 导出本月用电数据
                3. 导出本月用水数据
                4. 导出本月用气数据
                5. 退出能耗系统
                
                6. 登录MES系统
                7. 导出本月产量数据
                8. 退出MES系统
                
                9. 打开Excel能耗分析表
                10. 计算单位产品能耗
                11. 与历史数据对比
                12. 识别能耗异常
                13. 生成节能建议报告
                14. 发送报告给生产经理
                """,
                "expected": {
                    "steps": 14,
                    "software": ["能耗监测系统", "MES系统", "Excel"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "能耗监控与节能优化",
            },
            {
                "id": "MFG012",
                "category": "生产报表编制",
                "difficulty": "高",
                "steps_count": 12,
                "instruction": """
                日报编制与汇报：
                
                1. 登录MES系统
                2. 导出当日产量数据
                3. 导出当日质量数据
                4. 退出MES系统
                
                5. 登录ERP系统
                6. 导出当日销售数据
                7. 退出ERP系统
                
                8. 打开Excel日报模板
                9. 填写生产日报表
                10. 生成数据图表
                
                11. 保存日报文件
                12. 通过企业微信发送给管理层
                """,
                "expected": {
                    "steps": 12,
                    "software": ["MES系统", "ERP系统", "Excel", "企业微信"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "生产日报编制与汇报",
            },
            {
                "id": "MFG013",
                "category": "设备故障处理",
                "difficulty": "高",
                "steps_count": 13,
                "instruction": """
                设备故障响应流程：
                
                1. 登录设备监控系统
                2. 接收故障报警
                3. 查看故障详情
                4. 退出监控系统
                
                5. 登录维修管理系统
                6. 创建维修工单
                7. 分配维修人员
                8. 退出维修系统
                
                9. 通过企业微信通知维修人员
                
                10. 登录维修系统
                11. 录入维修结果
                12. 更新设备状态
                13. 生成故障分析报告
                """,
                "expected": {
                    "steps": 13,
                    "software": ["设备监控系统", "维修管理系统", "企业微信"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "设备故障快速响应与处理",
            },
            {
                "id": "MFG014",
                "category": "安全生产管理",
                "difficulty": "高",
                "steps_count": 11,
                "instruction": """
                安全生产检查流程：
                
                1. 登录安全管理系统
                2. 导出安全隐患清单
                3. 导出整改记录
                4. 退出安全系统
                
                5. 打开Excel检查表
                6. 准备现场检查清单
                7. 录入检查结果
                8. 标记不合格项
                
                9. 登录安全管理系统
                10. 录入新的隐患
                11. 发送整改通知给相关部门
                """,
                "expected": {
                    "steps": 11,
                    "software": ["安全管理系统", "Excel"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "安全生产检查与隐患整改",
            },
            {
                "id": "MFG015",
                "category": "新产品导入",
                "difficulty": "高",
                "steps_count": 18,
                "instruction": """
                新产品导入流程：
                
                1. 登录PLM系统
                2. 下载产品设计图纸
                3. 下载BOM清单
                4. 退出PLM系统
                
                5. 登录ERP系统
                6. 创建新物料编码
                7. 录入BOM结构
                8. 退出ERP系统
                
                9. 登录MES系统
                10. 创建产品工艺路线
                11. 设置工时定额
                12. 退出MES系统
                
                13. 登录WMS系统
                14. 设置物料库位
                15. 退出WMS系统
                
                16. 打开Excel试产计划表
                17. 编制试产计划
                18. 发送计划给生产部门
                """,
                "expected": {
                    "steps": 18,
                    "software": ["PLM系统", "ERP系统", "MES系统", "WMS系统", "Excel"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "新产品导入与试产准备",
            },
        ],
    },
    
    # ═══════════════════════════════════════════════════════════
    # 电商行业（15个复杂任务）
    # 5个用例：20+步骤
    # 10个用例：10-19步骤
    # ═══════════════════════════════════════════════════════════
    "ecommerce": {
        "name": "电商行业",
        "icon": "🛒",
        "test_cases": [
            # ═════════════════════════════════════════════════
            # 超复杂任务（20+步骤）- 5个
            # ═════════════════════════════════════════════════
            {
                "id": "ECM001",
                "category": "大促活动全流程",
                "difficulty": "极高",
                "steps_count": 28,
                "instruction": """
                双十一大促活动全流程管理：
                
                1. 登录淘宝卖家中心
                2. 创建双十一活动页面
                3. 设置活动商品
                4. 设置促销价格
                5. 设置优惠券
                6. 退出淘宝
                
                7. 登录京东商家后台
                8. 创建京东双十一活动
                9. 设置活动商品
                10. 设置促销价格
                11. 退出京东
                
                12. 登录拼多多商家后台
                13. 创建拼多多活动
                14. 设置活动商品
                15. 退出拼多多
                
                16. 登录ERP系统
                17. 导出商品库存
                18. 计算活动备货量
                19. 生成采购计划
                20. 退出ERP系统
                
                21. 登录CRM系统
                22. 筛选目标客户
                23. 设置营销短信
                24. 退出CRM系统
                
                25. 登录BI系统
                26. 创建活动监控看板
                27. 设置实时预警
                28. 发送活动准备完成通知
                """,
                "expected": {
                    "steps": 28,
                    "software": ["淘宝", "京东", "拼多多", "ERP系统", "CRM系统", "BI系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "多平台大促活动策划与执行",
            },
            {
                "id": "ECM002",
                "category": "订单处理全流程",
                "difficulty": "极高",
                "steps_count": 25,
                "instruction": """
                日订单处理全流程：
                
                1. 登录淘宝卖家中心
                2. 导出今日订单
                3. 退出淘宝
                
                4. 登录京东商家后台
                5. 导出今日订单
                6. 退出京东
                
                7. 登录拼多多商家后台
                8. 导出今日订单
                9. 退出拼多多
                
                10. 登录ERP系统
                11. 导入淘宝订单
                12. 导入京东订单
                13. 导入拼多多订单
                14. 自动合并订单
                15. 退出ERP系统
                
                16. 登录WMS系统
                17. 查询库存
                18. 生成发货计划
                19. 打印快递单
                20. 打印拣货单
                21. 退出WMS系统
                
                22. 登录ERP系统
                23. 扣减库存
                24. 生成出库单
                25. 发送发货通知给客户
                """,
                "expected": {
                    "steps": 25,
                    "software": ["淘宝", "京东", "拼多多", "ERP系统", "WMS系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                    "loop_required": True,
                },
                "business_context": "多平台订单整合与发货处理",
            },
            {
                "id": "ECM003",
                "category": "商品管理全流程",
                "difficulty": "极高",
                "steps_count": 22,
                "instruction": """
                新品上架全流程：
                
                1. 登录ERP系统
                2. 查询新商品资料
                3. 导出商品图片
                4. 导出商品详情
                5. 退出ERP系统
                
                6. 使用Photoshop处理商品图片
                7. 保存处理后的图片
                
                8. 登录淘宝卖家中心
                9. 发布新商品
                10. 上传商品图片
                11. 填写商品详情
                12. 设置价格库存
                13. 退出淘宝
                
                14. 登录京东商家后台
                15. 发布新商品
                16. 上传商品图片
                17. 填写商品详情
                18. 退出京东
                
                19. 登录ERP系统
                20. 更新商品状态为已上架
                21. 退出ERP系统
                22. 发送上架完成通知
                """,
                "expected": {
                    "steps": 22,
                    "software": ["ERP系统", "Photoshop", "淘宝", "京东"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "多平台商品上架管理",
            },
            {
                "id": "ECM004",
                "category": "数据分析全流程",
                "difficulty": "极高",
                "steps_count": 23,
                "instruction": """
                月度经营数据分析：
                
                1. 登录淘宝卖家中心
                2. 导出销售数据
                3. 导出流量数据
                4. 导出转化数据
                5. 退出淘宝
                
                6. 登录京东商家后台
                7. 导出销售数据
                8. 导出流量数据
                9. 退出京东
                
                10. 登录拼多多商家后台
                11. 导出销售数据
                12. 退出拼多多
                
                13. 登录ERP系统
                14. 导出成本数据
                15. 导出利润数据
                16. 退出ERP系统
                
                17. 打开Excel分析模板
                18. 合并各平台数据
                19. 计算总销售额
                20. 计算总利润
                21. 生成趋势图表
                22. 保存分析报告
                23. 通过邮件发送给管理层
                """,
                "expected": {
                    "steps": 23,
                    "software": ["淘宝", "京东", "拼多多", "ERP系统", "Excel", "邮件"],
                    "data_flow": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "多平台经营数据分析与报告",
            },
            {
                "id": "ECM005",
                "category": "客户服务全流程",
                "difficulty": "极高",
                "steps_count": 21,
                "instruction": """
                客户服务质量管理：
                
                1. 登录淘宝千牛
                2. 导出客服聊天记录
                3. 导出客户评价
                4. 退出千牛
                
                5. 登录京东客服系统
                6. 导出客服记录
                7. 导出客户评价
                8. 退出京东客服
                
                9. 登录售后系统
                10. 导出退货申请
                11. 导出换货申请
                12. 导出退款记录
                13. 退出售后系统
                
                14. 打开Excel客服分析表
                15. 统计响应时间
                16. 统计满意度
                17. 分析退货原因
                18. 生成客服质量报告
                
                19. 登录CRM系统
                20. 标记问题客户
                21. 发送改进建议给客服团队
                """,
                "expected": {
                    "steps": 21,
                    "software": ["淘宝千牛", "京东客服系统", "售后系统", "Excel", "CRM系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.7,
                    "cross_system": True,
                },
                "business_context": "多平台客服质量监控与改进",
            },
            
            # ═════════════════════════════════════════════════
            # 高复杂度任务（10-19步骤）- 10个
            # ═════════════════════════════════════════════════
            {
                "id": "ECM006",
                "category": "价格管理",
                "difficulty": "高",
                "steps_count": 14,
                "instruction": """
                竞品价格监控与调价：
                
                1. 登录竞品监控系统
                2. 导出竞品价格数据
                3. 退出监控系统
                
                4. 登录ERP系统
                5. 导出本店商品价格
                6. 导出成本数据
                7. 退出ERP系统
                
                8. 打开Excel价格分析表
                9. 对比竞品价格
                10. 计算调价空间
                11. 生成调价建议
                
                12. 登录淘宝卖家中心
                13. 批量调整价格
                14. 退出淘宝
                """,
                "expected": {
                    "steps": 14,
                    "software": ["竞品监控系统", "ERP系统", "Excel", "淘宝"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "竞品价格监控与动态定价",
            },
            {
                "id": "ECM007",
                "category": "库存管理",
                "difficulty": "高",
                "steps_count": 15,
                "instruction": """
                智能补货管理：
                
                1. 登录WMS系统
                2. 导出库存清单
                3. 导出库存预警商品
                4. 退出WMS系统
                
                5. 登录ERP系统
                6. 导出销售历史数据
                7. 导出采购周期
                8. 退出ERP系统
                
                9. 打开Excel补货计算表
                10. 计算安全库存
                11. 计算补货量
                12. 生成补货计划
                
                13. 登录采购系统
                14. 创建采购订单
                15. 发送给供应商
                """,
                "expected": {
                    "steps": 15,
                    "software": ["WMS系统", "ERP系统", "Excel", "采购系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "智能补货与采购管理",
            },
            {
                "id": "ECM008",
                "category": "营销活动",
                "difficulty": "高",
                "steps_count": 13,
                "instruction": """
                优惠券活动管理：
                
                1. 登录CRM系统
                2. 筛选目标客户群
                3. 导出客户清单
                4. 退出CRM系统
                
                5. 登录营销系统
                6. 创建优惠券活动
                7. 设置优惠券面额
                8. 设置使用条件
                9. 批量发放优惠券
                10. 退出营销系统
                
                11. 登录CRM系统
                12. 记录发放记录
                13. 发送活动通知短信
                """,
                "expected": {
                    "steps": 13,
                    "software": ["CRM系统", "营销系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "精准营销与优惠券管理",
            },
            {
                "id": "ECM009",
                "category": "退货处理",
                "difficulty": "高",
                "steps_count": 12,
                "instruction": """
                退货处理流程：
                
                1. 登录售后系统
                2. 导出待处理退货申请
                3. 审核退货原因
                4. 批准退货
                5. 退出售后系统
                
                6. 登录WMS系统
                7. 接收退货入库
                8. 质检入库商品
                9. 更新库存
                10. 退出WMS系统
                
                11. 登录财务系统
                12. 处理退款
                """,
                "expected": {
                    "steps": 12,
                    "software": ["售后系统", "WMS系统", "财务系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "退货处理与退款管理",
            },
            {
                "id": "ECM010",
                "category": "评价管理",
                "difficulty": "高",
                "steps_count": 11,
                "instruction": """
                客户评价分析：
                
                1. 登录淘宝卖家中心
                2. 导出商品评价
                3. 退出淘宝
                
                4. 登录京东商家后台
                5. 导出商品评价
                6. 退出京东
                
                7. 打开Excel评价分析表
                8. 统计好评率
                9. 分析差评原因
                10. 生成评价分析报告
                11. 发送报告给运营团队
                """,
                "expected": {
                    "steps": 11,
                    "software": ["淘宝", "京东", "Excel"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "多平台评价监控与分析",
            },
            {
                "id": "ECM011",
                "category": "物流跟踪",
                "difficulty": "高",
                "steps_count": 13,
                "instruction": """
                物流异常处理：
                
                1. 登录物流系统
                2. 导出在途订单
                3. 查询超时未签收订单
                4. 退出物流系统
                
                5. 登录快递公司系统
                6. 查询物流详情
                7. 联系快递网点
                8. 退出快递系统
                
                9. 登录售后系统
                10. 记录异常订单
                11. 处理客户投诉
                
                12. 登录物流系统
                13. 更新物流状态
                """,
                "expected": {
                    "steps": 13,
                    "software": ["物流系统", "快递公司系统", "售后系统"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "物流异常监控与处理",
            },
            {
                "id": "ECM012",
                "category": "直播带货",
                "difficulty": "高",
                "steps_count": 14,
                "instruction": """
                直播带货管理：
                
                1. 登录淘宝直播后台
                2. 创建直播间
                3. 设置直播商品
                4. 设置直播优惠券
                5. 退出淘宝直播
                
                6. 登录ERP系统
                7. 查询直播商品库存
                8. 锁定库存
                9. 退出ERP系统
                
                10. 登录CRM系统
                11. 筛选直播目标客户
                12. 发送直播预告
                
                13. 登录淘宝直播后台
                14. 开始直播
                """,
                "expected": {
                    "steps": 14,
                    "software": ["淘宝直播", "ERP系统", "CRM系统"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "直播带货活动管理",
            },
            {
                "id": "ECM013",
                "category": "会员管理",
                "difficulty": "高",
                "steps_count": 12,
                "instruction": """
                会员积分管理：
                
                1. 登录CRM系统
                2. 导出会员清单
                3. 导出积分明细
                4. 退出CRM系统
                
                5. 打开Excel积分分析表
                6. 统计积分分布
                7. 计算即将过期积分
                8. 生成积分提醒清单
                
                9. 登录CRM系统
                10. 批量发送积分提醒
                11. 设置积分兑换活动
                12. 退出CRM系统
                """,
                "expected": {
                    "steps": 12,
                    "software": ["CRM系统", "Excel"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "会员积分管理与运营",
            },
            {
                "id": "ECM014",
                "category": "财务对账",
                "difficulty": "高",
                "steps_count": 16,
                "instruction": """
                电商平台财务对账：
                
                1. 登录淘宝卖家中心
                2. 导出结算单
                3. 导出交易明细
                4. 退出淘宝
                
                5. 登录京东商家后台
                6. 导出结算单
                7. 导出交易明细
                8. 退出京东
                
                9. 登录ERP系统
                10. 导出销售记录
                11. 退出ERP系统
                
                12. 打开Excel对账表
                13. 匹配平台结算与ERP记录
                14. 标记差异项
                15. 生成对账报告
                16. 发送给财务部门
                """,
                "expected": {
                    "steps": 16,
                    "software": ["淘宝", "京东", "ERP系统", "Excel"],
                    "data_flow": True,
                    "risks": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "多平台财务对账",
            },
            {
                "id": "ECM015",
                "category": "数据备份",
                "difficulty": "高",
                "steps_count": 11,
                "instruction": """
                业务数据备份：
                
                1. 登录淘宝卖家中心
                2. 导出商品数据
                3. 导出订单数据
                4. 退出淘宝
                
                5. 登录ERP系统
                6. 导出客户数据
                7. 导出库存数据
                8. 退出ERP系统
                
                9. 打开文件管理器
                10. 整理备份文件
                11. 上传到云盘
                """,
                "expected": {
                    "steps": 11,
                    "software": ["淘宝", "ERP系统", "云盘"],
                    "data_flow": True,
                    "confidence": 0.75,
                    "cross_system": True,
                },
                "business_context": "业务数据备份与归档",
            },
        ],
    },
}


# ═══════════════════════════════════════════════════════════════
# 统计信息
# ═══════════════════════════════════════════════════════════════

def print_statistics():
    """打印测试用例统计"""
    print("\n" + "="*70)
    print("  复杂测试用例统计")
    print("="*70 + "\n")
    
    total_cases = 0
    total_20plus = 0
    total_10plus = 0
    
    for industry_key, industry_data in COMPLEX_INDUSTRY_TEST_CASES.items():
        cases = industry_data['test_cases']
        count_20plus = sum(1 for c in cases if c['steps_count'] >= 20)
        count_10plus = sum(1 for c in cases if 10 <= c['steps_count'] < 20)
        
        print(f"{industry_data['icon']} {industry_data['name']}:")
        print(f"  总用例数: {len(cases)}")
        print(f"  20+步骤: {count_20plus} 个")
        print(f"  10-19步骤: {count_10plus} 个")
        print(f"  平均步骤数: {sum(c['steps_count'] for c in cases) / len(cases):.1f}")
        print()
        
        total_cases += len(cases)
        total_20plus += count_20plus
        total_10plus += count_10plus
    
    print("="*70)
    print(f"总计: {total_cases} 个用例")
    print(f"  20+步骤: {total_20plus} 个 ({total_20plus/total_cases*100:.1f}%)")
    print(f"  10-19步骤: {total_10plus} 个 ({total_10plus/total_cases*100:.1f}%)")
    print("="*70)


# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print_statistics()
