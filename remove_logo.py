"""Remove company logos from slide images by covering with background color."""
from pathlib import Path
from PIL import Image, ImageDraw

ASSETS = Path(r"D:\workspace\22-solution-engineering\projects\29-portfolio-site\assets")

DIRS = [ASSETS / "meeting-room", ASSETS / "smart-park"]

# Logo regions (relative to 1280x720)
# Top-left: circular logo icon ~(15,15) to (55,55)
TOP_LEFT = (0, 0, 60, 60)
# Bottom-right: "kaihong 开鸿" text ~(1080,680) to (1280,720)
BOTTOM_RIGHT = (1060, 680, 1280, 720)


def get_bg_color(img, region):
    """Sample background color from the edge of the region."""
    x, y = region[0], region[1]
    # Sample a few pixels near the region to detect background
    colors = []
    for dx in range(3):
        for dy in range(3):
            px = max(0, x + dx)
            py = max(0, y + dy)
            colors.append(img.getpixel((px, py)))
    # Use most common or just the corner pixel
    return img.getpixel((region[2] - 5, region[1] + 5))


def process_slide(path):
    img = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Cover top-left logo with sampled background
    bg1 = img.getpixel((5, 5))
    draw.rectangle(TOP_LEFT, fill=bg1)

    # Cover bottom-right text with sampled background
    bg2 = img.getpixel((1275, 715))
    draw.rectangle(BOTTOM_RIGHT, fill=bg2)

    img.save(path)


if __name__ == "__main__":
    for d in DIRS:
        for f in sorted(d.glob("slide_*.png")):
            process_slide(f)
            print(f"  Processed: {f.name}")
        print(f"Done: {d.name}")
