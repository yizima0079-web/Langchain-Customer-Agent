# AGENTS.md

> 本文件是给 AI 编程代理（Claude Code / Cursor / Copilot 等）的工作守则，与给人看的 `README.md` 互补。
> 目标是：**高复用型**（改动不破坏既有模式）与**高执行效率**（单例复用、连接池、一次到位）。

## 1. 项目结构（三端）

```text
server/   FastAPI + SQLAlchemy 2.0 + MySQL 8 + LangChain 1.4 + Chroma 后端
client/   Vue3 + Vite + Element Plus 管理后台
weixin/   微信原生小程序（商城 + AI 客服）
docs/     架构设计、客服知识库手册
```

版本实测基线：Python 3.14 / FastAPI 0.141 / LangChain **1.4** / SQLAlchemy 2.0.5 / Chroma 1.5 / Vue3 / Vite 8。

## 2. 运行与校验命令（先跑通再改）

```bash
# 后端（在 server/ 目录下）
python -m compileall -q app          # 语法校验
python -c "import app.main"          # 导入校验（暴露循环导入/缺依赖）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 前端（在 client/ 目录下）
npm install
npm run dev                          # 开发，端口 5173
npm run build                        # 构建校验

# 数据库初始化（先 schema 后 data）
mysql -h localhost -P3306 -uroot -p < server/sql/schema.sql
mysql -h localhost -P3306 -uroot -p < server/sql/data.sql

# 健康检查
curl http://127.0.0.1:8000/api/v1/health
```

改动后端后**至少跑** `compileall` + `import app.main` 两项；改动前端页面后**至少跑** `npm run build`。

## 3. 后端硬约束（禁止破坏）

### 3.1 分层
- `api/routes/`：只做参数校验、调 service、返回结果，**不写业务逻辑**。
- `services/`：业务逻辑与外部调用（LLM、向量库、文件解析）。
- `models/`（ORM）+ `schemas/`（Pydantic）分离，出参一律用 `*Out` 模型。

### 3.2 路由注册（易漏，必做）
新增路由文件 `app/api/routes/xxx.py` 后，必须在 `app/main.py` 的 `create_app()` 里
`application.include_router(xxx.router, prefix=settings.API_PREFIX)`，否则不生效。

### 3.3 ORM 序列化（历史 500 根因，最高优先级）
返回数据**必须** `XxxOut.model_validate(obj)`，**禁止**把裸 SQLAlchemy 对象直接放进
`Response(data=...)`，否则 Pydantic v2 抛 `PydanticSerializationError`。

```python
# 正确
return Response(data={"total": total, "items": [ProductOut.model_validate(p) for p in items]})
# 错误（会 500）
return Response(data={"items": items})
```

### 3.4 统一响应
- 成功：`Response(code=0, message="ok", data=...)`；列表 `{"total":…,"items":[…]}`。
- 失败：`raise HTTPException(status_code=4xx/5xx, detail="中文提示")`，**不**用 `Response(code!=0)` 表示业务错误。

### 3.5 依赖注入
- 会话：`db: Session = Depends(get_db)`
- 登录态：`Depends(get_current_user)`
- 管理员：`Depends(get_current_admin)`（`user.role == 1`）

### 3.6 模型注册
新 ORM 模型继承 `app.core.database.Base`，并在 `models/__init__.py` 集中 import + `__all__` 导出。

### 3.7 单例懒加载（高执行效率，照此模式）
LLM / 嵌入 / 向量库均为「模块级缓存 + 懒加载单例」：
`get_llm()`、`get_embeddings()`、`get_vectorstore()`。新增外部资源连接**必须**沿用该模式，避免每请求重复建连。

### 3.8 下单库存并发（防超卖）
扣库存前**必须** `with_for_update()` 行锁，且按商品 id 排序锁定顺序（避免死锁）。见 `order.py::create_order`。

## 4. 数据库硬约束

- **host 一律 `localhost`**，不用 `127.0.0.1`（MySQL 8 在 Windows 常仅监听 IPv6 `::1`）。
- 连接串密码用 `quote_plus` 转义 + `charset=utf8mb4`（见 `core/config.py::database_url`）。
- 连接池 `pool_pre_ping=True`、`pool_recycle=3600` 保持不动。
- 用户密码 **bcrypt** 存储（`core/security.py`）；历史 MD5 密码登录成功后自动升级为 bcrypt，勿改回 MD5。测试账号 `admin/123456`、`zhangsan/123456` 等。
- 字段语义：`user.role` 0=普通/1=管理；`user.status` 0=禁用/1=正常；`product.status` 0=下架/1=上架。
- 数据库密码以 `server/.env` 为准（当前 `MySQL@123456`）。

## 5. 配置与密钥硬约束

- `server/.env` 只存在于本地，**永不提交**；`.gitignore` 已忽略。
- 大模型密钥环境变量名固定为 `OPENAL_APLKEY`（OS 环境变量优先于 `.env`），兼容回退 `OPENAI_API_KEY`。
- `.env.example` 中 `OPENAL_APLKEY=` **必须留空**；提交前 `grep OPENAL_APLKEY server/.env.example` 确认。
- 目录默认：`UPLOAD_DIR=F:/uploads14`、`CHROMA_DIR=F:/uploads14/chroma`；静态挂载 `/uploads14`。
- `EMBEDDING_DIM=1024`（qwen3.7-text-embedding-flash 实测上限，**勿设 2048**）。

## 6. LLM / RAG 硬约束

- **只用 LCEL**：`prompt | llm | StrOutputParser()`。LangChain 1.4 已删除 `langchain.chains`，不要写 `from langchain.chains import …`。
- 嵌入**必须用**自定义 `DashScopeEmbeddings`（`services/embeddings.py`，openai client 直连）；`langchain_openai.OpenAIEmbeddings` 有传参 bug（input 被包成对象→网关 400）。
- 检索参数：`RETRIEVE_TOP_K=4`、`COLLECTION_NAME="knowledge_base"`。
- 客服提示词 `SYSTEM_PROMPT` 限定「不编造知识库外内容，无答案转人工」，改动需同步评估效果。
- AI 客服双通道：`POST /chat/stream`（SSE）+ `POST /chat`（同步兜底），两路都要可用。

## 7. 前端硬约束

- 统一 axios 封装 `client/src/api/request.js`：baseURL `/api/v1`、注入 Bearer、拦截器解包 `code==0`、401 清 token 跳登录。
- 业务接口**只加到** `client/src/api/index.js`；页面**不**直接 `axios.get`，走 `@/api` 导出函数。
- 新增页面三同步：`router/index.js` 路由 + `layout/index.vue` 菜单项 + `meta.title`。
- Element Plus 图标需在 `main.js` 全局注册后才能在模板 `<el-icon>` 使用。

## 8. 小程序硬约束

- 统一请求封装 `weixin/utils/api.js`：`get/post/put/del/fullUrl/streamChat`，页面**不**裸写 `wx.request`。
- SSE 用 `streamChat`（已含 `enableChunked` + `onChunkReceived` 解析 + 同步 fallback），**不要绕过**。
- token 存 `wx.getStorageSync('token')`，401 自动清除并提示。
- 图片地址一律 `api.fullUrl(path)` 拼完整 URL。
- `BASE_URL`/`STATIC_URL` 现为 `127.0.0.1:8000`，真机调试需改局域网 IP。

## 9. Git 与安全硬约束

- 忽略清单：`.env`/`.env.*`(除 `.env.example`)、`project.private.config.json`、`__pycache__`/`.venv`/`node_modules`/`dist`/`.vite`、`uploads14`/`chroma`/`*.db`、`release/`。
- 提交前检查：`git status --short` 确认无上述文件；`git show :server/.env.example | grep OPENAL_APLKEY` 确认留空。
- 默认分支 `master`；作者 `yizima0079-web <yizima0079@gmail.com>`。

## 10. 代码风格

- 全代码**中文注释 + docstring**，风格与现有文件一致（每个模块顶部有模块 docstring）。
- Python 函数签名带类型注解 + 返回类型。
- 路由函数命名 `list_xxx / get_xxx / create_xxx / update_xxx / delete_xxx`；service 单例 `get_xxx()`。

## 11. 已知待办

1. 补最小冒烟测试到 `server/tests/`（当前无入库 pytest；日常改动用「curl 健康检查 + 登录 + 列表接口」做端到端冒烟代替）。
2. 前端构建产物 `dashboard`/`index` chunk 超过 500 kB，若在意首屏性能可做 `dynamic import()` 路由级拆包（当前不影响运行）。
