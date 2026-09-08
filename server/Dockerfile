# 后端镜像：FastAPI + LangChain + Chroma + MySQL
# 基础镜像用 3.12（而非本地 3.14）：chromadb 依赖 onnxruntime 等原生库，
# 3.12 的预编译 wheel 最齐全，可保证 docker build 一次成功
FROM python:3.12-slim

WORKDIR /app

# 先单独拷贝依赖清单，利用 Docker 层缓存（改源码不触发重装）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝源码
COPY . .

# 上传文件 / 向量库目录（compose 中挂载卷持久化）
RUN mkdir -p /app/uploads

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
