# server — 智能客服商城后端（FastAPI + LangChain + RAG）

「基于 LangChain 的带 AI 智能客服的微信小程序商城系统」后端服务。

## 技术栈

- FastAPI + Uvicorn + SQLAlchemy 2.0 + PyMySQL（MySQL 8，端口 3306）
- JWT 认证 + MD5 密码
- LangChain + langchain-openai（OpenAI 兼容接口，DashScope）
- Chroma 向量数据库（向量维度 1024）
- 文档解析：txt / doc / docx / pdf / markdown

## 目录结构

```
server/
├── app/
│   ├── main.py                # 应用入口 create_app()
│   ├── core/                  # 配置 / 安全 / 数据库 / 依赖
│   ├── models/                # SQLAlchemy ORM 模型
│   ├── schemas/               # Pydantic 模型
│   ├── services/              # LLM / 嵌入 / 向量库 / 文档解析 / RAG
│   └── api/routes/            # 业务路由
├── sql/
│   ├── schema.sql             # 建表语句
│   └── data.sql               # 测试数据（密码 123456）
├── requirements.txt
└── .env.example
```

## 启动

### 1. 初始化数据库（MySQL 8，端口 3306）

```bash
mysql -h localhost -P3306 -uroot -p < sql/schema.sql
mysql -h localhost -P3306 -uroot -p < sql/data.sql
```

### 2. 配置环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env        # Windows
cp .env.example .env          # Linux/macOS

# 设置大模型访问密钥（环境变量名 OPENAL_APLKEY）
set OPENAL_APLKEY=你的密钥     # Windows
export OPENAL_APLKEY=你的密钥  # Linux/macOS
```

### 3. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- 交互文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/api/v1/health
- 上传文件根目录：`F:/uploads14`

## 关键配置（.env）

| 配置项 | 说明 |
|--------|------|
| `MYSQL_PORT` | MySQL 端口（默认 3306） |
| `MYSQL_HOST` | MySQL 地址（默认 `localhost`，若仅能连 localhost 请勿改为 127.0.0.1） |
| `OPENAI_API_BASE` | LLM 接口地址（DashScope 兼容模式） |
| `LLM_MODEL` | 聊天模型（默认 `qwen3.8-flash`） |
| `EMBEDDING_MODEL` | 嵌入模型（默认 `qwen3.7-text-embedding-flash`） |
| `EMBEDDING_DIM` | 向量维度（默认 1024） |
| `UPLOAD_DIR` | 上传目录（默认 `F:/uploads14`） |
| `CHROMA_DIR` | 向量库持久化目录 |

> 访问密钥环境变量名：`OPENAL_APLKEY`（兼容回退 `OPENAI_API_KEY`）。

## 测试账号

- 管理员：`admin / 123456`
- 普通用户：`zhangsan / 123456`、`lisi / 123456`、`wangwu / 123456`
