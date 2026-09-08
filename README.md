# Langchain Customer Agent

基于 LangChain 的 AI 智能客服微信小程序商城系统，包含 FastAPI 后端、Vue 3 管理后台和微信原生小程序。

## 项目组成

```text
client/   Vue 3 + Vite + Element Plus 管理后台
server/   FastAPI + SQLAlchemy + MySQL + LangChain 后端
weixin/   微信原生小程序商城与 AI 客服
docs/     架构设计与客服知识库文档
```

## 功能

- 商品、分类、轮播图、用户、订单、购物车和地址管理。
- 微信小程序商品浏览、购物车、下单、预设地址、新地址、支付方式选择和待付款订单取消。
- LangChain + Chroma RAG 知识库问答。
- 微信小程序 AI 客服 SSE 流式输出，并兼容同步接口降级。
- Web 管理后台数据统计、知识库维护和 AI 客服调试。

## 数据库初始化

仓库只提交初始化 SQL，不提交真实数据库、运行时数据库或向量库：

```bash
mysql -h localhost -P3306 -uroot -p < server/sql/schema.sql
mysql -h localhost -P3306 -uroot -p < server/sql/data.sql
```

`data.sql` 仅包含演示用户、商品、分类、订单和地址数据。测试账号：`admin / 123456`，普通用户：`zhangsan / 123456`、`lisi / 123456`、`wangwu / 123456`。

## 启动后端

```bash
cd server
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动前在 `server/.env` 中配置 MySQL 和大模型参数。密钥只放在本地 `.env` 或系统环境变量中，仓库不会提交 `.env`。

后端文档：`http://127.0.0.1:8000/docs`  
健康检查：`http://127.0.0.1:8000/api/v1/health`

## 启动管理后台

```bash
cd client
npm install
npm run dev
```

管理后台默认地址：`http://localhost:5173`。

## 启动微信小程序

使用微信开发者工具导入 `weixin/` 目录，并在 `weixin/utils/api.js` 中配置后端地址。开发环境下需确保小程序可以访问后端主机和端口。

商品演示图片位于 `server/assets/product/`，与 `server/sql/data.sql` 的路径一致。初始化数据库后，如需使用演示图：

```powershell
Copy-Item server/assets/product F:/uploads14/product -Recurse -Force
```

## 注意事项

- 不要提交 `.env`、API 密钥、数据库备份、真实用户数据、Chroma 数据、上传目录、`node_modules`、`dist`、`.venv` 或 Python 缓存。
- `weixin/project.private.config.json` 是微信开发者工具本机私有配置，已加入忽略规则；提交前确认它未进入暂存区。
- 当前支付页用于选择支付方式并推进订单状态，没有接入真实第三方支付和支付回调。
- `server/assets/product/` 是开发演示素材，正式环境应替换为已获授权的商品图片。
- 后端默认上传目录为 `F:/uploads14`，可通过 `UPLOAD_DIR` 修改；Chroma 目录通过 `CHROMA_DIR` 修改。

## 文档

- [架构设计](docs/架构设计.md)
- [客服知识库手册](docs/客服知识库手册.md)
- [后端说明](server/README.md)
