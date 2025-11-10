from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

def add_text_watermark(image, text, position, opacity=0.5, font_size=40):
    watermark = image.copy()
    drawable = ImageDraw.Draw(watermark)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    bbox = drawable.textbbox((0, 0), text, font=font)
    textwidth = bbox[2] - bbox[0]
    textheight = bbox[3] - bbox[1]

    width, height = image.size
    margin = 10
    positions = {
        "Top-Left": (margin, margin),
        "Top-Right": (width - textwidth - margin, margin),
        "Bottom-Left": (margin, height - textheight - margin),
        "Bottom-Right": (width - textwidth - margin, height - textheight - margin),
        "Center": ((width - textwidth) // 2, (height - textheight) // 2)
    }
    pos = positions.get(position, positions["Bottom-Right"])

    # Draw text with opacity
    drawable.text(pos, text, fill=(255, 255, 255, int(255 * opacity)), font=font)
    return watermark



def add_logo_watermark(image, logo_path, position, opacity=0.5, scale=0.2):
    """
    Add a logo watermark to the given image.
    """
    base = image.convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    logo_width = int(base.width * scale)
    aspect_ratio = logo.height / logo.width
    logo_height = int(logo_width * aspect_ratio)
    logo = logo.resize((logo_width, logo_height))


    alpha = logo.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    logo.putalpha(alpha)

    margin = 10
    positions = {
        "Top-Left": (margin, margin),
        "Top-Right": (base.width - logo_width - margin, margin),
        "Bottom-Left": (margin, base.height - logo_height - margin),
        "Bottom-Right": (base.width - logo_width - margin, base.height - logo_height - margin),
        "Center": ((base.width - logo_width) // 2, (base.height - logo_height) // 2)
    }
    pos = positions.get(position, positions["Bottom-Right"])

    base.paste(logo, pos, logo)
    return base.convert("RGB")
