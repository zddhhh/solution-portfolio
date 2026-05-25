"""Remove company logos from PPT slide masters and slides, then export to PNG."""
from pathlib import Path
from copy import deepcopy
from pptx import Presentation
from pptx.util import Emu
import comtypes.client
import shutil
import time

BASE = Path(r"D:\workspace\22-solution-engineering\projects\27-solution-asset-library")
OUT = Path(r"D:\workspace\22-solution-engineering\projects\29-portfolio-site\assets")
TEMP = Path(r"D:\workspace\22-solution-engineering\projects\29-portfolio-site\_temp_pptx")

TASKS = [
    {"search_dir": BASE / "智慧会议室", "pattern": "智慧会议室标准方案", "output": OUT / "meeting-room"},
    {"search_dir": BASE / "智慧公园", "pattern": "智慧公园标准方案V3", "output": OUT / "smart-park"},
]


def find_pptx(search_dir, pattern):
    for f in search_dir.rglob("*.pptx"):
        if pattern in f.stem and "~$" not in f.name:
            return f
    return None


def is_logo_shape(shape, slide_width, slide_height):
    """Identify logo shapes by position: top-left corner or bottom-right corner."""
    if not hasattr(shape, 'left') or shape.left is None:
        return False
    
    left = shape.left
    top = shape.top
    width = shape.width or 0
    height = shape.height or 0
    right = left + width
    bottom = top + height
    
    sw = slide_width
    sh = slide_height

    # Top-left logo: small icon in top-left corner
    if left < sw * 0.06 and top < sh * 0.08 and width < sw * 0.06:
        return True

    # Bottom-right area: anything small in the bottom-right corner
    # "kaihong 开鸿" text or logo image
    if left > sw * 0.70 and top > sh * 0.90:
        return True

    return False


def remove_logos_from_pptx(pptx_path, output_path):
    """Remove logo shapes from all slides and slide layouts."""
    prs = Presentation(str(pptx_path))
    sw = prs.slide_width
    sh = prs.slide_height
    
    removed = 0
    
    # Remove from slide layouts
    for layout in prs.slide_layouts:
        shapes_to_remove = []
        for shape in layout.placeholders:
            pass  # Don't touch placeholders
        for shape in layout.shapes:
            if is_logo_shape(shape, sw, sh):
                shapes_to_remove.append(shape)
        for shape in shapes_to_remove:
            sp = shape._element
            sp.getparent().remove(sp)
            removed += 1

    # Remove from slide masters
    for master in prs.slide_masters:
        shapes_to_remove = []
        for shape in master.shapes:
            if is_logo_shape(shape, sw, sh):
                shapes_to_remove.append(shape)
        for shape in shapes_to_remove:
            sp = shape._element
            sp.getparent().remove(sp)
            removed += 1
    
    # Remove from individual slides
    for slide in prs.slides:
        shapes_to_remove = []
        for shape in slide.shapes:
            if is_logo_shape(shape, sw, sh):
                shapes_to_remove.append(shape)
        for shape in shapes_to_remove:
            sp = shape._element
            sp.getparent().remove(sp)
            removed += 1
    
    prs.save(str(output_path))
    print(f"  Removed {removed} logo shapes -> {output_path.name}")
    return removed


def export_slides(pptx_path, output_dir):
    """Export slides using PowerPoint COM."""
    output_dir.mkdir(parents=True, exist_ok=True)
    # Clear existing
    for f in output_dir.glob("slide_*.png"):
        f.unlink()

    ppt_app = comtypes.client.CreateObject("PowerPoint.Application")
    ppt_app.Visible = 1
    presentation = ppt_app.Presentations.Open(str(pptx_path), WithWindow=False)
    total = presentation.Slides.Count

    for i in range(1, total + 1):
        out_path = output_dir / f"slide_{i:02d}.png"
        presentation.Slides(i).Export(str(out_path), "PNG", 1280, 720)

    presentation.Close()
    ppt_app.Quit()
    time.sleep(1)
    print(f"  Exported {total} slides -> {output_dir}")


if __name__ == "__main__":
    TEMP.mkdir(parents=True, exist_ok=True)
    
    for task in TASKS:
        pptx = find_pptx(task["search_dir"], task["pattern"])
        if not pptx:
            print(f"  [WARN] Not found: {task['pattern']}")
            continue
        
        print(f"\nProcessing: {pptx.name}")
        temp_pptx = TEMP / f"cleaned_{pptx.stem}.pptx"
        
        remove_logos_from_pptx(pptx, temp_pptx)
        export_slides(temp_pptx, task["output"])
    
    # Cleanup temp
    shutil.rmtree(TEMP, ignore_errors=True)
    print("\nAll done!")
