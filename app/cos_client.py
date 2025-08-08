import os
import random
import string
import sys
import logging
from qcloud_cos import CosConfig, CosS3Client

# 日志配置
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# --- 从环境变量中读取COS配置 ---
# 这种方式更安全，避免将密钥硬编码在代码中
# 在运行Docker容器时，我们会通过环境变量将这些值传入
secret_id = os.environ.get('COS_SECRET_ID')
secret_key = os.environ.get('COS_SECRET_KEY')
region = os.environ.get('COS_REGION')
bucket = os.environ.get('COS_BUCKET')
token = None
scheme = 'https'

# --- 检查环境变量是否存在 ---
if not all([secret_id, secret_key, region, bucket]):
    raise ValueError("关键的COS环境变量缺失 (COS_SECRET_ID, COS_SECRET_KEY, COS_REGION, COS_BUCKET)，请检查。")

# --- 初始化COS客户端 ---
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


def upload(file_bytes: bytes) -> str:
    """
    上传二进制文件内容到腾讯云COS。

    参数:
        file_bytes (bytes): 文件的二进制内容。

    返回:
        str: 在COS中的文件名 (对象键)。
    """
    # 生成一个16位的随机文件名
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".png"

    response = client.put_object(
        Bucket=bucket,
        Body=file_bytes,
        Key=file_name
    )

    # 打印ETag以供调试
    print(f"文件上传成功, ETag: {response['ETag']}")

    return file_name
