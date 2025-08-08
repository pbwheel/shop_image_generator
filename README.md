# 餐厅图片生成器 API

本项目提供一个Web API，能够根据指定的店铺名称和类型，动态生成一张设计精美的推广图，并将其自动上传到腾讯云对象存储（COS），最后返回图片的公开访问URL。

## ✨ 功能特性

- **智能配色**: 根据店铺类型（如“火锅”、“咖啡厅”）自动选择和谐的背景与字体颜色。
- **自动布局**: 文本自动换行并垂直居中，确保长店名也能美观展示。
- **API驱动**: 通过简单的POST请求即可完成所有操作。
- **Docker化部署**: 提供Dockerfile，一键构建和部署，轻便快捷。
- **安全配置**: 通过环境变量管理敏感的云服务密钥，而非硬编码在代码中。

## 🚀 如何部署和运行

### 1. 准备工作

- **安装 Docker**: 确保你的服务器或本地机器已经安装了 [Docker](https://www.docker.com/)。
- **腾讯云COS**:
    - 拥有一个腾讯云账户并开通了对象存储服务。
    - 创建一个存储桶（Bucket）。
    - 获取你的 `SecretId`, `SecretKey`, `Region` (地域) 和 `Bucket` 名称。
- **下载字体文件**: 从 [这里](https://ziyouziti.com/mianfeiziti-103.html) 下载字体文件，并将其重命名为 `SweiMeatballCJKtc-Medium.ttf`，然后放到 `app/` 目录下。

### 2. 构建 Docker 镜像

在项目根目录下（即`Dockerfile`所在的目录），执行以下命令来构建镜像：

```bash
docker build -t shop-image-generator .