-- 初始化数据库脚本
-- 这个脚本会在 MySQL 容器首次启动时自动执行

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 使用数据库
USE shop_db;

-- 注意:表结构由 Flask-SQLAlchemy 和 Flask-Migrate 管理
-- 这里只用于初始化数据,表结构请使用 flask db upgrade 命令创建
