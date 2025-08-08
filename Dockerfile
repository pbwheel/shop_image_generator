# 步骤 1: 使用官方轻量级Python 3.12镜像作为基础
FROM python:3.12-slim

# 步骤 2: 设置容器内的工作目录
WORKDIR /app

# 步骤 3: 设置环境变量，避免Python将.pyc文件写入磁盘
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 步骤 4: 复制依赖文件并安装依赖
# 仅复制requirements.txt可以利用Docker的层缓存机制
# 只有当requirements.txt改变时，这一层才会重新执行
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 步骤 5: 将整个app目录复制到容器的工作目录中
COPY ./app /app/app

# 步骤 6: 暴露应用运行的端口
EXPOSE 8000

# 步骤 7: 容器启动时执行的命令
# 使用uvicorn启动FastAPI应用，并监听所有网络接口
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]