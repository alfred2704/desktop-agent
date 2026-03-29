"""
搜索豆包进程
"""

import subprocess
import sys

print("="*70)
print("  搜索豆包进程")
print("="*70)
print()

try:
    # 使用tasklist查找进程
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq Doubao.exe'],
        capture_output=True,
        text=True,
        encoding='gbk'
    )
    
    print("搜索 Doubao.exe:")
    print(result.stdout)
    
    # 也搜索包含"豆包"的进程
    result2 = subprocess.run(
        ['tasklist', '/FI', 'WINDOWTITLE eq 豆包*'],
        capture_output=True,
        text=True,
        encoding='gbk'
    )
    
    print("搜索窗口标题包含'豆包'的进程:")
    print(result2.stdout)
    
except Exception as e:
    print(f"搜索失败: {e}")

print("="*70)
