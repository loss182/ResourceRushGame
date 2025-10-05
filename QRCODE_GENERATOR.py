import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import re

output_folder = r"output_folder_path"

def sanitize_filename(name):
    """Remove invalid filename characters for Windows."""
    return re.sub(r'[<>:"/\\|?*]+', '_', name).strip()

def generate_qrcodes(data, output_dir=None, size=300, margin=4, max_font=36, min_font=8):
    """
    Generate QR codes with a title that always fits in width, shrinking if necessary.

    Parameters:
        data (dict): {"Title": "Link"}
        output_dir (str): Folder to save QR codes
        size (int): QR code size in pixels
        margin (int): Margin around the QR image
        max_font (int): Maximum font size to start from
        min_font (int): Minimum font size allowed
    """
    if output_dir is None:
        output_dir = globals().get("output_folder", "qrcodes")
    os.makedirs(output_dir, exist_ok=True)

    font_path = "arial.ttf"
    has_truetype = True
    try:
        ImageFont.truetype(font_path, max_font)
    except:
        has_truetype = False

    for title, link in data.items():
        # --- Generate QR code ---
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_img = qr_img.resize((size, size), Image.LANCZOS)

        # --- Create final image ---
        final_img = Image.new("RGB", (size + 2 * margin, size + 2 * margin), "white")
        final_img.paste(qr_img, (margin, margin))

        draw = ImageDraw.Draw(final_img)

        # --- Determine font size that fits ---
        if has_truetype:
            font_size = max_font
            while font_size >= min_font:
                font = ImageFont.truetype(font_path, font_size)
                try:
                    bbox = draw.textbbox((0, 0), title, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except AttributeError:
                    text_width, text_height = draw.textsize(title, font=font)
                if text_width <= size - (2 * margin):
                    break
                font_size -= 1
        else:
            font = ImageFont.load_default()
            try:
                bbox = draw.textbbox((0, 0), title, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                text_width, text_height = draw.textsize(title, font=font)

        # --- Draw the title centered on top ---
        x_text = (final_img.width - text_width) // 2
        y_text = margin

        # Background box behind text
        text_bg = Image.new("RGB", (text_width + 6, text_height + 6), "white")
        final_img.paste(text_bg, (x_text - 3, y_text - 3))
        draw.text((x_text, y_text), title, font=font, fill="black")

        # --- Save the file ---
        safe_name = sanitize_filename(title)
        path = os.path.join(output_dir, f"{safe_name}.png")
        final_img.save(path)
        print(f"✅ Saved: {path}")

# Example usage
if __name__ == "__main__":
    data = {
    "NASA SMAP Mission":"https://smap.jpl.nasa.gov/",
    "NASA Landsat Program":"https://landsat.gsfc.nasa.gov/",
    "NASA Spinoff: Drones for Agriculture":"https://spinoff.nasa.gov/Spinoff2019/ee_1.html",
    "NASA Technology Transfer: Soil Sensors":"https://technology.nasa.gov/patent/LEW-TOPS-39",
    "NASA Aqua Mission":"https://aqua.nasa.gov/",
    "NASA Spinoff: Water Recycling":"https://spinoff.nasa.gov/Spinoff2017/cg_7.html",
    "NASA GRACE-FO Mission":"https://gracefo.jpl.nasa.gov/",
    "NASA Research: Microbes in Space":"https://www.nasa.gov/mission_pages/station/research/news/microbes-in-space",
    "NASA ECOSTRESS Mission":"https://ecostress.jpl.nasa.gov/",
    "NASA Harvest Program":"https://www.nasaharvest.org/",
    "NASA ICESat-2 Mission":"https://icesat-2.gsfc.nasa.gov/",
    "NASA Spinoff: Plant Monitoring":"https://spinoff.nasa.gov/Spinoff2020/ee_2.html",
    "Earthdata":"https://www.earthdata.nasa.gov/",
    "Worldview":"https://www.earthdata.nasa.gov/data/tools/worldview",
    "AppEEARS":"https://appeears.earthdatacloud.nasa.gov/",
    "Giovanni":"https://giovanni.gsfc.nasa.gov/giovanni/",
    "VEDA":"https://www.earthdata.nasa.gov/data/tools/veda",
    "Pathfinder":"https://appliedsciences.nasa.gov/what-we-do/food-security-agriculture/practitioner-resources",
    "GFSAD":"https://www.earthdata.nasa.gov/data/catalog/lpcloud-gfsad1kcd-001",
    }

    generate_qrcodes(data, output_dir=output_folder, size=400, margin=10)

