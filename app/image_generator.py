import io
import random
import re
from PIL import Image, ImageDraw, ImageFont

# 备用字体
fallback_font = "app/AlibabaPuHuiTi-3-55-Regular.ttf"

# --- 1. 根据店铺类型推荐颜色 ---
def get_recommended_colors_for_store_type(store_type: str) -> dict:
    """
    根据店铺类型返回推荐的背景颜色和字体颜色。
    Parameters:
        store_type (str): The type of store, such as "coffee", "crayfish", etc.

    Return:
        dict: a dictionary containing the "background_color" and "text_color" keys.
    """
    color_schemes = {
        "warm": [{"background_color": "#f5eecb", "text_color": "#8b4513"}, {"background_color": "#f4e6d4", "text_color": "#654321"}],
        "fresh": [{"background_color": "#e3f2fd", "text_color": "#006064"}, {"background_color": "#f0fff0", "text_color": "#3cb371"}],
        "vibrant": [{"background_color": "#ff6f61", "text_color": "#ffffff"}, {"background_color": "#ffc107", "text_color": "#212529"}],
        "elegant": [{"background_color": "#36454f", "text_color": "#f5f5dc"}, {"background_color": "#2c3e50", "text_color": "#ecf0f1"}],
        "sweet": [{"background_color": "#fcf5e5", "text_color": "#a0522d"}, {"background_color": "#ffb6c1", "text_color": "#8b0000"}],
        "spicy": [{"background_color": "#a52a2a", "text_color": "#ffc107"}, {"background_color": "#800000", "text_color": "#ffffff"}],
        "roasted": [{"background_color": "#444444", "text_color": "#e0c4a4"}, {"background_color": "#302824", "text_color": "#f0fff0"}],
        "traditional": [{"background_color": "#b0c4de", "text_color": "#4a2c11"}, {"background_color": "#d2b48c", "text_color": "#36454f"}],
        "general": [{"background_color": "#f5f5f5", "text_color": "#333333"}, {"background_color": "#ffffff", "text_color": "#2c3e50"}]
    }

    if store_type in ["小吃快餐", "家常菜", "地方菜系", "面馆", "东北菜", "农家菜", "新疆菜"]:
        colors = color_schemes["warm"]
    elif store_type in ["鱼鲜海鲜", "水果生鲜", "日式料理", "江浙菜", "私房菜"]:
        colors = color_schemes["fresh"]
    elif store_type in ["小龙虾", "饮品", "螺蛳粉", "韩式料理"]:
        colors = color_schemes["vibrant"]
    elif store_type in ["西餐", "粤菜", "酒吧", "创意菜", "北京菜", "东南亚菜", "中东菜"]:
        colors = color_schemes["elegant"]
    elif store_type in ["面包蛋糕甜品", "咖啡", "自助餐", "食品滋补"]:
        colors = color_schemes["sweet"]
    elif store_type in ["火锅", "川菜", "湘菜"]:
        colors = color_schemes["spicy"]
    elif store_type in ["烧烤烤串", "烤肉"]:
        colors = color_schemes["roasted"]
    elif store_type in ["茶馆", "早茶"]:
        colors = color_schemes["traditional"]
    else:
        colors = color_schemes["general"]
    return random.choice(colors)

# --- 2. 自动换行并绘制文字的工具函数 ---
def draw_autowrapped_text(draw, text, font, text_color, image_size, padding=20):
    """
    在图片上绘制支持自动换行和居中对齐的文字。

    Parameters:
    draw (ImageDraw.Draw): ImageDraw object.
    text (str): The text to be drawn.
    font (ImageFont): ImageFont object.
    text_color (str): Text color.
    image_size (tuple): Image size (width, height).
    padding (int): The inner margin between the text and the edge of the image.

    """
    max_width = image_size[0] - 2 * padding
    tokens = re.findall(r'[a-zA-Z0-9]+|\s|[^\s]', text)
    lines, current_line = [], ""
    for token in tokens:
        if not current_line:
            current_line = token
        else:
            test_line = current_line + token
            if font.getlength(test_line) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = token
    lines.append(current_line)
    line_height = font.getbbox("一")[3] + 5
    total_text_height = len(lines) * line_height
    y_start = (image_size[1] - total_text_height) / 2
    y = y_start
    for line in lines:
        line_width = font.getlength(line)
        x = (image_size[0] - line_width) / 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

# --- 3. 主程序：生成图片 ---
def generate_store_image(store_name: str, store_type: str, image_size=(400, 400), font_path='app/SweiMeatballCJKtc-Medium.ttf'):
    """
    生成一张带有店铺名称和自动换行文字的图片。
    Parameters:
    store_name (str): The name of the store.
    store_type (str): The type of store, used to recommend colors.
    image_size (tuple): The size of the image (width, height).
    font_path (str): The path to the font file.

    """
    try:
        colors = get_recommended_colors_for_store_type(store_type)
        background_color, text_color = colors['background_color'], colors['text_color']
        img = Image.new('RGB', image_size, background_color)
        draw = ImageDraw.Draw(img)
        font_size = 65
        font = ImageFont.truetype(font_path, font_size)
        max_text_width = image_size[0] - 40
        while font.getlength(store_name) > max_text_width and font_size > 45:
            font_size -= 2
            font = ImageFont.truetype(font_path, font_size)
        draw_autowrapped_text(draw, store_name, font, text_color, image_size)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr
    except IOError:
        print(f"警告：字体文件 '{font_path}' 未找到。请确保文件路径在容器内是正确的。")
        return None
    except Exception as e:
        print(f"生成图片时发生错误: {e}")
        return None

