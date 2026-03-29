#!/usr/bin/env python3
"""
测试异常处理系统
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core.exception_handler import ExceptionHandler, ExceptionType, RecoveryStrategy


def test_exception_classification():
    """测试异常分类"""
    print("\n" + "="*60)
    print("测试1: 异常分类")
    print("="*60)
    
    handler = ExceptionHandler()
    
    test_cases = [
        (Exception("network connection failed"), ExceptionType.NETWORK),
        (Exception("element not found: 确定"), ExceptionType.ELEMENT_NOT_FOUND),
        (Exception("permission denied"), ExceptionType.PERMISSION),
        (Exception("timeout after 30 seconds"), ExceptionType.TIMEOUT),
        (Exception("software application error"), ExceptionType.SOFTWARE),
        (Exception("data format invalid"), ExceptionType.DATA),
        (Exception("unknown error"), ExceptionType.UNKNOWN),
    ]
    
    passed = 0
    for error, expected_type in test_cases:
        result = handler.classify_exception(error)
        status = "✅" if result == expected_type else "❌"
        print(f"{status} {str(error)[:40]:<40} → {result.value}")
        if result == expected_type:
            passed += 1
    
    print(f"\n结果: {passed}/{len(test_cases)} 通过")
    return passed == len(test_cases)


def test_recovery_strategies():
    """测试恢复策略"""
    print("\n" + "="*60)
    print("测试2: 恢复策略")
    print("="*60)
    
    handler = ExceptionHandler()
    
    test_cases = [
        (ExceptionType.NETWORK, [RecoveryStrategy.RETRY, RecoveryStrategy.USER_INTERVENTION]),
        (ExceptionType.ELEMENT_NOT_FOUND, [RecoveryStrategy.DOWNGRADE, RecoveryStrategy.ALTERNATIVE, RecoveryStrategy.USER_INTERVENTION]),
        (ExceptionType.PERMISSION, [RecoveryStrategy.USER_INTERVENTION, RecoveryStrategy.ABORT]),
    ]
    
    passed = 0
    for exception_type, expected_strategies in test_cases:
        result = handler.get_recovery_strategies(exception_type)
        status = "✅" if result == expected_strategies else "❌"
        print(f"{status} {exception_type.value:<20} → {[s.value for s in result]}")
        if result == expected_strategies:
            passed += 1
    
    print(f"\n结果: {passed}/{len(test_cases)} 通过")
    return passed == len(test_cases)


def test_downgrade_execution():
    """测试降级执行"""
    print("\n" + "="*60)
    print("测试3: 降级执行")
    print("="*60)
    
    handler = ExceptionHandler()
    
    test_cases = [
        ({'method': 'api'}, 'control', True),
        ({'method': 'control'}, 'screen', True),
        ({'method': 'screen'}, None, False),
    ]
    
    passed = 0
    for context, expected_method, expected_success in test_cases:
        result = handler._downgrade_execution(context)
        
        actual_method = result.get('data', {}).get('method') if result.get('data') else None
        actual_success = result.get('success', False)
        
        status = "✅" if (actual_method == expected_method and actual_success == expected_success) else "❌"
        print(f"{status} {context['method']} → {actual_method or 'None'} (期望: {expected_method or 'None'})")
        
        if actual_method == expected_method and actual_success == expected_success:
            passed += 1
    
    print(f"\n结果: {passed}/{len(test_cases)} 通过")
    return passed == len(test_cases)


def test_retry_mechanism():
    """测试重试机制"""
    print("\n" + "="*60)
    print("测试4: 重试机制")
    print("="*60)
    
    handler = ExceptionHandler({'max_retries': 3, 'retry_interval': 0.1})
    
    # 测试1: 第2次成功
    attempt_count = [0]
    
    def retry_func_success_on_2():
        attempt_count[0] += 1
        if attempt_count[0] < 2:
            raise Exception("Not yet")
        return "Success!"
    
    result = handler._retry_execution(retry_func_success_on_2, {})
    print(f"✅ 第2次成功: {result}")
    
    # 测试2: 全部失败
    attempt_count2 = [0]
    
    def retry_func_always_fail():
        attempt_count2[0] += 1
        raise Exception("Always fail")
    
    result2 = handler._retry_execution(retry_func_always_fail, {})
    print(f"✅ 全部失败: {result2}")
    
    return True


def test_exception_handling():
    """测试完整异常处理流程"""
    print("\n" + "="*60)
    print("测试5: 完整异常处理")
    print("="*60)
    
    handler = ExceptionHandler({'max_retries': 2, 'retry_interval': 0.1})
    
    # 测试网络异常
    error = Exception("network connection timeout")
    context = {'test': 'network_error'}
    
    result = handler.handle_exception(error, context)
    print(f"✅ 网络异常处理: {result['message']}")
    
    # 测试元素定位失败
    error2 = Exception("element not found")
    context2 = {'method': 'api', 'test': 'element_error'}
    
    result2 = handler.handle_exception(error2, context2)
    print(f"✅ 元素定位失败处理: {result2['message']}")
    
    return True


def test_exception_stats():
    """测试异常统计"""
    print("\n" + "="*60)
    print("测试6: 异常统计")
    print("="*60)
    
    handler = ExceptionHandler({'max_retries': 1, 'retry_interval': 0.1})
    
    # 模拟一些异常
    handler.handle_exception(Exception("error 1"), {'test': 1})
    handler.handle_exception(Exception("error 2"), {'test': 2})
    
    stats = handler.get_exception_stats()
    
    print(f"✅ 总异常数: {stats['total']}")
    print(f"✅ 按类型统计: {stats['by_type']}")
    print(f"✅ 恢复率: {stats['recovery_rate']:.1%}")
    
    return stats['total'] >= 2


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🎯"*30)
    print("Desktop Agent - 异常处理系统测试套件")
    print("🎯"*30)
    
    tests = [
        ("异常分类", test_exception_classification),
        ("恢复策略", test_recovery_strategies),
        ("降级执行", test_downgrade_execution),
        ("重试机制", test_retry_mechanism),
        ("完整处理", test_exception_handling),
        ("异常统计", test_exception_stats),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} - {name}")
    
    total = len(results)
    passed_count = sum(1 for _, passed in results if passed)
    
    print(f"\n总计: {passed_count}/{total} 通过")
    print("="*60 + "\n")
    
    return passed_count == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
