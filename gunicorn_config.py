"""Gunicorn 配置文件"""
import multiprocessing
import os

# 服务器绑定地址
bind = "0.0.0.0:5000"

# 工作进程数 (建议设置为 CPU 核心数 * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# 工作进程类型
# - sync: 同步工作进程(默认)
# - gevent: 使用协程,适合 I/O 密集型应用
# - eventlet: 使用协程,适合 I/O 密集型应用
worker_class = "sync"

# 每个工作进程的线程数
threads = 2

# 工作进程最大请求数,超过后重启工作进程(防止内存泄漏)
max_requests = 1000
max_requests_jitter = 100

# 超时时间(秒)
timeout = 120
keepalive = 5

# 日志配置
accesslog = "/app/logs/access.log"
errorlog = "/app/logs/error.log"
loglevel = os.getenv("LOG_LEVEL", "info")

# 进程名称
proc_name = "flask_shop"

# 守护进程(在 Docker 中不要启用)
daemon = False

# PID 文件
pidfile = "/tmp/gunicorn.pid"

# 启动前的钩子函数
def on_starting(server):
    """服务器启动时调用"""
    # 确保日志目录存在
    os.makedirs("/app/logs", exist_ok=True)
    server.log.info("Gunicorn server starting...")

# 工作进程启动后的钩子函数
def post_worker_init(worker):
    """工作进程初始化后调用"""
    worker.log.info("Worker spawned (pid: %s)", worker.pid)

# 优雅关闭
def worker_int(worker):
    """工作进程收到 SIGINT 信号时调用"""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """工作进程 fork 前调用"""
    pass

def pre_exec(server):
    """在 master 进程中重新加载应用前调用"""
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    """服务器准备就绪时调用"""
    server.log.info("Gunicorn server is ready. Spawning workers")

def pre_fork(server, worker):
    """工作进程 fork 前调用"""
    pass

def post_fork(server, worker):
    """工作进程 fork 后调用"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_exec(server):
    """在 master 进程中重新加载应用前调用"""
    server.log.info("Forked child, re-executing.")

def worker_int(worker):
    """工作进程收到 SIGINT 信号时调用"""
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    """工作进程异常退出时调用"""
    worker.log.info("Worker received SIGABRT signal")
