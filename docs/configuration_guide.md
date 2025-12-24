# 配置文件说明

## 文件说明

### .env.example（✅ 可提交到 Git）
- **作用**：环境变量文件的示例模板
- **内容**：展示需要配置哪些环境变量
- **安全性**：只包含示例，不包含真实值

### .env（❌ 不可提交到 Git）
- **作用**：实际的环境变量配置文件
- **内容**：包含真实的数据库密码等敏感信息
- **安全性**：已在 `.gitignore` 中，不会被提交

## 使用步骤

### 1. 创建 .env 文件

```bash
cp .env.example .env
```

### 2. 编辑 .env 文件，填入真实配置

```env
# Flask 安全密钥
SECRET_KEY=your-secret-key-here

# MySQL 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=shop_user
MYSQL_PASSWORD=your-database-password
MYSQL_DB=shop_db
MYSQL_CHARSET=utf8mb4

# 环境标识
FLASK_ENV=development
FLASK_DEBUG=1
```

### 3. 在代码中使用

```python
from flask import Flask
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
```

## 安全检查清单

### 提交代码前，务必确认：

- [ ] `.gitignore` 文件中已包含 `.env`
- [ ] `.env` 文件不存在于 Git 仓库中
- [ ] 代码中不要硬编码真实密码

### 检查命令：

```bash
# 检查哪些文件会被 Git 跟踪
git status

# 检查 .gitignore 是否生效
git check-ignore -v .env
```

## 常见问题

### Q: 如果不小心提交了 .env 怎么办？

1. **立即更改密码**
2. **从 Git 历史中移除**（如果是课程作业，重新创建数据库即可）
3. **将 .env 添加到 .gitignore**

### Q: 如何验证 .env 不会被提交？

```bash
# 测试 gitignore 规则
git check-ignore -v .env

# 应该输出类似：
# .gitignore:19:.env    .env

# 查看会被提交的文件
git ls-files
```
