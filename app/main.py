from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .image_generator import generate_store_image
from . import cos_client
import io

app = FastAPI(
    title="Shop Image Generator API",
    description="一个根据店铺名称和类型生成推广图并上传到腾讯云COS的API服务。",
    version="1.0.0",
)


# 定义请求体的数据模型，确保传入参数的类型正确
class StoreInfo(BaseModel):
    name: str
    store_type: str


@app.post("/generate-image/", summary="生成并上传店铺图片")
async def create_image(store: StoreInfo):
    """
    接收店铺名称和类型，生成图片并上传，最终返回可访问的图片URL。

    - **name**: 店铺的完整名称。
    - **store_type**: 店铺的类型 (例如: "火锅", "咖啡", "日式料理" 等)，用于智能配色。
    """
    try:
        # 1. 调用图片生成函数，返回一个内存中的二进制对象
        image_bytes_io = generate_store_image(store.name, store.store_type)

        if image_bytes_io is None:
            raise HTTPException(status_code=500, detail="图片生成失败。")

        # 2. 调用COS上传函数，传入图片的二进制数据
        # .getvalue() 从BytesIO对象中获取完整的bytes
        file_name = cos_client.upload(image_bytes_io.getvalue())

        # 3. 构造图片的公开访问URL
        # URL格式: https://<Bucket名>-<APPID>.cos.<地域>.myqcloud.com/<对象键>
        # 我们从cos_client模块中获取bucket和region信息
        image_url = f"https://{cos_client.bucket}.cos.{cos_client.region}.myqcloud.com/{file_name}"

        return {"image_url": image_url, "file_name": file_name}

    except Exception as e:
        # 捕获任何可能的异常，并返回一个详细的错误信息
        raise HTTPException(status_code=500, detail=f"处理请求时发生未知错误: {str(e)}")
