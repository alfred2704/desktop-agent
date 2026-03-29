"""
Desktop Agent - 性能优化模块
缓存、并行处理、延迟加载
"""

from typing import Dict, Any, Optional, List
from functools import lru_cache
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
from loguru import logger


# ═══════════════════════════════════════════════════════════════
# 缓存管理器
# ═══════════════════════════════════════════════════════════════

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: str = "cache", default_ttl: int = 300):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录
            default_ttl: 默认过期时间（秒）
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.default_ttl = default_ttl
        
        # 内存缓存
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        
        # 缓存统计
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值（如果存在且未过期）
        """
        # 1. 检查内存缓存
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            
            # 检查是否过期
            if time.time() < entry["expires_at"]:
                self.stats["hits"] += 1
                logger.debug(f"✅ 缓存命中（内存）: {key}")
                return entry["value"]
            else:
                # 已过期，删除
                del self.memory_cache[key]
        
        # 2. 检查文件缓存
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                
                if time.time() < entry["expires_at"]:
                    self.stats["hits"] += 1
                    logger.debug(f"✅ 缓存命中（文件）: {key}")
                    
                    # 加载到内存
                    self.memory_cache[key] = entry
                    return entry["value"]
                else:
                    # 已过期，删除文件
                    cache_file.unlink()
            
            except Exception as e:
                logger.warning(f"读取缓存文件失败: {e}")
        
        self.stats["misses"] += 1
        logger.debug(f"❌ 缓存未命中: {key}")
        return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒）
        """
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        
        entry = {
            "value": value,
            "expires_at": expires_at,
            "created_at": time.time()
        }
        
        # 1. 保存到内存
        self.memory_cache[key] = entry
        
        # 2. 保存到文件
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(entry, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存缓存文件失败: {e}")
        
        self.stats["sets"] += 1
        logger.debug(f"✅ 缓存已设置: {key} (TTL={ttl}秒)")
    
    def delete(self, key: str):
        """删除缓存"""
        # 从内存删除
        if key in self.memory_cache:
            del self.memory_cache[key]
        
        # 从文件删除
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            cache_file.unlink()
        
        logger.debug(f"🗑️  缓存已删除: {key}")
    
    def clear(self):
        """清空所有缓存"""
        self.memory_cache.clear()
        
        # 删除所有缓存文件
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        
        logger.info("🗑️  所有缓存已清空")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            "hit_rate": f"{hit_rate:.1f}%",
            "memory_cache_size": len(self.memory_cache),
            "file_cache_size": len(list(self.cache_dir.glob("*.json")))
        }


# ═══════════════════════════════════════════════════════════════
# 元素定位缓存装饰器
# ═══════════════════════════════════════════════════════════════

class ElementLocatorCache:
    """元素定位结果缓存"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager
    
    def get_or_compute(
        self,
        element_description: str,
        compute_func,
        ttl: int = 300
    ) -> Any:
        """
        获取或计算元素位置
        
        Args:
            element_description: 元素描述
            compute_func: 计算函数
            ttl: 缓存过期时间
        
        Returns:
            元素位置
        """
        cache_key = f"element_{hash(element_description)}"
        
        # 尝试从缓存获取
        cached = self.cache_manager.get(cache_key)
        if cached is not None:
            logger.info(f"✅ 使用缓存的元素位置: {element_description}")
            return cached
        
        # 计算并缓存
        result = compute_func()
        self.cache_manager.set(cache_key, result, ttl)
        
        return result


# ═══════════════════════════════════════════════════════════════
# 并行处理
# ═══════════════════════════════════════════════════════════════

class ParallelExecutor:
    """并行执行器"""
    
    def __init__(self, max_workers: int = 4):
        """
        初始化并行执行器
        
        Args:
            max_workers: 最大工作线程数
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def execute_parallel(
        self,
        tasks: List[Dict[str, Any]],
        execute_func
    ) -> List[Any]:
        """
        并行执行多个任务
        
        Args:
            tasks: 任务列表
            execute_func: 执行函数
        
        Returns:
            执行结果列表
        """
        logger.info(f"🚀 并行执行 {len(tasks)} 个任务")
        
        futures = []
        for task in tasks:
            future = self.executor.submit(execute_func, task)
            futures.append(future)
        
        # 等待所有任务完成
        results = []
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"任务执行失败: {e}")
                results.append({
                    "success": False,
                    "error": str(e)
                })
        
        logger.info(f"✅ 并行执行完成: {len(results)}/{len(tasks)}")
        return results
    
    def shutdown(self):
        """关闭执行器"""
        self.executor.shutdown()
        logger.info("🛑 并行执行器已关闭")


# ═══════════════════════════════════════════════════════════════
# 延迟加载
# ═══════════════════════════════════════════════════════════════

class LazyLoader:
    """延迟加载器"""
    
    def __init__(self):
        """初始化延迟加载器"""
        self.loaded_modules: Dict[str, Any] = {}
        self.load_lock = threading.Lock()
    
    def load_module(
        self,
        module_name: str,
        import_func,
        force_reload: bool = False
    ) -> Any:
        """
        延迟加载模块
        
        Args:
            module_name: 模块名称
            import_func: 导入函数
            force_reload: 是否强制重新加载
        
        Returns:
            模块对象
        """
        # 检查是否已加载
        if not force_reload and module_name in self.loaded_modules:
            logger.debug(f"✅ 使用已加载模块: {module_name}")
            return self.loaded_modules[module_name]
        
        # 加载模块
        with self.load_lock:
            # 双重检查
            if not force_reload and module_name in self.loaded_modules:
                return self.loaded_modules[module_name]
            
            logger.info(f"🔄 延迟加载模块: {module_name}")
            module = import_func()
            self.loaded_modules[module_name] = module
            
            return module
    
    def preload_modules(self, module_names: List[str], import_func):
        """
        预加载多个模块（并行）
        
        Args:
            module_names: 模块名称列表
            import_func: 导入函数
        """
        logger.info(f"🚀 预加载 {len(module_names)} 个模块")
        
        def load_one(name):
            self.load_module(name, import_func)
        
        threads = []
        for name in module_names:
            thread = threading.Thread(target=load_one, args=(name,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        logger.info(f"✅ 预加载完成")


# ═══════════════════════════════════════════════════════════════
# 性能监控
# ═══════════════════════════════════════════════════════════════

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        """初始化性能监控器"""
        self.metrics: Dict[str, List[float]] = {}
    
    def record(self, operation: str, duration: float):
        """
        记录操作耗时
        
        Args:
            operation: 操作名称
            duration: 耗时（秒）
        """
        if operation not in self.metrics:
            self.metrics[operation] = []
        
        self.metrics[operation].append(duration)
    
    def get_stats(self, operation: str) -> Dict[str, float]:
        """
        获取操作统计
        
        Args:
            operation: 操作名称
        
        Returns:
            统计数据
        """
        if operation not in self.metrics:
            return {}
        
        durations = self.metrics[operation]
        
        return {
            "count": len(durations),
            "avg": sum(durations) / len(durations),
            "min": min(durations),
            "max": max(durations),
            "total": sum(durations)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """获取所有操作统计"""
        return {
            operation: self.get_stats(operation)
            for operation in self.metrics
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n=== 性能优化模块测试 ===\n")
    
    # 1. 缓存测试
    print("1. 测试缓存管理器...")
    cache = CacheManager()
    
    # 设置缓存
    cache.set("test_key", {"data": "test"}, ttl=60)
    
    # 获取缓存
    value = cache.get("test_key")
    print(f"缓存值: {value}")
    
    # 统计
    stats = cache.get_stats()
    print(f"缓存统计: {stats}")
    
    # 2. 并行执行测试
    print("\n2. 测试并行执行...")
    executor = ParallelExecutor(max_workers=2)
    
    def task_func(task):
        time.sleep(0.5)
        return {"task_id": task["id"], "result": "done"}
    
    tasks = [{"id": 1}, {"id": 2}, {"id": 3}]
    results = executor.execute_parallel(tasks, task_func)
    print(f"并行执行结果: {results}")
    
    executor.shutdown()
    
    # 3. 延迟加载测试
    print("\n3. 测试延迟加载...")
    loader = LazyLoader()
    
    # 延迟加载模块
    def import_os():
        import os
        return os
    
    os_module = loader.load_module("os", import_os)
    print(f"已加载模块: {os_module}")
    
    print("\n✅ 所有测试完成")
