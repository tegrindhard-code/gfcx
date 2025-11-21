#!/usr/bin/env python3
"""
Generate Template Image

Creates blank template images for sprite sheets with guides.
"""

from PIL import Image, ImageDraw, ImageFont
import sys

def create_regular_template(rows=25, output_path="pokemon_sheet_template.png"):
    """Create a template for regular Pokemon sprite sheet"""

    width = 1680  # 21 columns × 80px
    height = rows * 30

    # Create image with transparency
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    grid_color = (100, 100, 100, 128)  # Semi-transparent gray
    divider_color = (200, 50, 50, 180)  # Red for normal/shiny divider
    text_color = (150, 150, 150, 200)

    # Draw vertical grid lines (80px apart for cells)
    for x in range(0, width + 1, 80):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)

    # Draw normal/shiny dividers (40px apart)
    for x in range(40, width, 80):
        draw.line([(x, 0), (x, height)], fill=divider_color, width=1)

    # Draw horizontal grid lines (30px apart for rows)
    for y in range(0, height + 1, 30):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Add labels
    try:
        # Try to use a small font
        font = ImageFont.load_default()
    except:
        font = None

    # Column numbers
    for col in range(21):
        x = col * 80 + 40
        y = 5
        text = str(col)
        if font:
            draw.text((x, y), text, fill=text_color, font=font)

    # Row numbers and icon numbers
    for row in range(rows):
        y = row * 30 + 10
        x = 5
        text = f"R{row}"
        if font:
            draw.text((x, y), text, fill=text_color, font=font)

        # Icon number at start of row
        icon_num = row * 21
        text2 = f"#{icon_num}"
        if font:
            draw.text((x, y + 10), text2, fill=(100, 150, 255, 200), font=font)

    # Save
    img.save(output_path)
    print(f"✅ Created template: {output_path}")
    print(f"   Size: {width}×{height}px")
    print(f"   Grid: 21 columns × {rows} rows")
    print(f"   Capacity: {rows * 21 * 2} sprites (normal + shiny)")
    print(f"\nGuidelines:")
    print(f"   - Each cell is 80px wide × 30px tall")
    print(f"   - Left 40px = Normal sprite")
    print(f"   - Right 40px = Shiny sprite (divided by red line)")
    print(f"   - Gray lines = cell boundaries")

def create_egg_template(rows=25, output_path="egg_sheet_template.png"):
    """Create a template for egg sprite sheet"""

    width = 540  # 18 columns × 30px
    height = rows * 32

    # Create image with transparency
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    grid_color = (100, 100, 100, 128)
    text_color = (150, 150, 150, 200)

    # Draw vertical grid lines (30px apart)
    for x in range(0, width + 1, 30):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)

    # Draw horizontal grid lines (32px apart)
    for y in range(0, height + 1, 32):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Add labels
    try:
        font = ImageFont.load_default()
    except:
        font = None

    # Column numbers
    for col in range(18):
        x = col * 30 + 10
        y = 5
        text = str(col)
        if font:
            draw.text((x, y), text, fill=text_color, font=font)

    # Row numbers and egg numbers
    for row in range(rows):
        y = row * 32 + 10
        x = 2
        text = f"R{row}"
        if font:
            draw.text((x, y), text, fill=text_color, font=font)

        # Egg number
        egg_num = row * 18 + 1451
        text2 = f"#{egg_num}"
        if font:
            draw.text((x, y + 10), text2, fill=(255, 200, 100, 200), font=font)

    # Save
    img.save(output_path)
    print(f"✅ Created template: {output_path}")
    print(f"   Size: {width}×{height}px")
    print(f"   Grid: 18 columns × {rows} rows")
    print(f"   Capacity: {rows * 18} eggs")
    print(f"\nGuidelines:")
    print(f"   - Each cell is 30px wide × 32px tall")
    print(f"   - Gray lines = cell boundaries")

def create_reference_sheet(output_path="sprite_reference.png"):
    """Create a reference sheet showing sprite dimensions"""

    img = Image.new('RGBA', (400, 300), (40, 40, 40, 255))
    draw = ImageDraw.Draw(img)

    # Regular Pokemon sprite box
    x1, y1 = 50, 50
    w, h = 40, 30
    draw.rectangle([x1, y1, x1 + w, y1 + h], outline=(0, 255, 0, 255), width=2)
    draw.text((x1 + 5, y1 - 20), "Regular Pokemon", fill=(255, 255, 255))
    draw.text((x1 + 5, y1 + 5), "40×30px", fill=(255, 255, 255))

    # Shiny sprite box
    x2, y2 = x1 + w + 10, y1
    draw.rectangle([x2, y2, x2 + w, y2 + h], outline=(255, 100, 255, 255), width=2)
    draw.text((x2 + 5, y2 - 20), "Shiny", fill=(255, 255, 255))

    # Full cell
    x3, y3 = 50, 150
    cw = 80
    draw.rectangle([x3, y3, x3 + cw, y3 + h], outline=(100, 150, 255, 255), width=2)
    draw.line([(x3 + cw/2, y3), (x3 + cw/2, y3 + h)], fill=(255, 50, 50), width=2)
    draw.text((x3 + 5, y3 - 20), "Full Cell = 80×30px", fill=(255, 255, 255))
    draw.text((x3 + 5, y3 + 5), "Normal", fill=(255, 255, 255))
    draw.text((x3 + 45, y3 + 5), "Shiny", fill=(255, 255, 255))

    # Egg sprite
    x4, y4 = 250, 50
    ew, eh = 30, 32
    draw.rectangle([x4, y4, x4 + ew, y4 + eh], outline=(255, 200, 100, 255), width=2)
    draw.text((x4 - 20, y4 - 20), "Egg", fill=(255, 255, 255))
    draw.text((x4 + 5, y4 + 10), "30×32px", fill=(255, 255, 255))

    img.save(output_path)
    print(f"✅ Created reference: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Template Generator for Pokemon Icon Sheets")
        print("-" * 60)
        print("\nUsage:")
        print("  python generate_template.py regular [rows] [output]")
        print("  python generate_template.py egg [rows] [output]")
        print("  python generate_template.py reference [output]")
        print("  python generate_template.py all")
        print("\nExamples:")
        print("  python generate_template.py regular")
        print("  python generate_template.py regular 50 my_sheet.png")
        print("  python generate_template.py egg 30")
        print("  python generate_template.py all")
        sys.exit(1)

    template_type = sys.argv[1].lower()

    if template_type == 'regular':
        rows = int(sys.argv[2]) if len(sys.argv) > 2 else 25
        output = sys.argv[3] if len(sys.argv) > 3 else "pokemon_sheet_template.png"
        create_regular_template(rows, output)

    elif template_type == 'egg':
        rows = int(sys.argv[2]) if len(sys.argv) > 2 else 25
        output = sys.argv[3] if len(sys.argv) > 3 else "egg_sheet_template.png"
        create_egg_template(rows, output)

    elif template_type == 'reference':
        output = sys.argv[2] if len(sys.argv) > 2 else "sprite_reference.png"
        create_reference_sheet(output)

    elif template_type == 'all':
        create_regular_template()
        create_egg_template()
        create_reference_sheet()
        print("\n✅ All templates created!")

    else:
        print(f"Error: Unknown template type '{template_type}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
