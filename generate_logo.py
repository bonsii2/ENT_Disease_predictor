import os
from PIL import Image, ImageDraw, ImageFont

def generate_medical_logo():
    img_dir = os.path.join(os.path.dirname(__file__), "static", "images")
    os.makedirs(img_dir, exist_ok=True)
    logo_path = os.path.join(img_dir, "logo.png")

    width, height = 300, 80
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw rounded shield / icon background
    icon_box = [10, 10, 70, 70]
    draw.rounded_rectangle(icon_box, radius=16, fill=(13, 148, 136, 255)) # Teal color

    # Draw medical cross
    # Vertical bar
    draw.rounded_rectangle([34, 22, 46, 58], radius=3, fill=(255, 255, 255, 255))
    # Horizontal bar
    draw.rounded_rectangle([22, 34, 58, 46], radius=3, fill=(255, 255, 255, 255))

    # Text rendering fallback using default font
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        sub_font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    draw.text((85, 18), "MediScan AI", fill=(15, 23, 42, 255), font=font)
    draw.text((85, 48), "Medical Image Predictor", fill=(100, 116, 139, 255), font=sub_font)

    image.save(logo_path, "PNG")
    print(f"Generated logo at: {logo_path}")

if __name__ == "__main__":
    generate_medical_logo()
