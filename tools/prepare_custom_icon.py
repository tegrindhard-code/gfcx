#!/usr/bin/env python3
"""
Prepare Custom Pokemon Icons for Upload

Automates all pre-upload preparations for individual custom Pokemon icons:
- Validates image format and properties
- Ensures transparency
- Optimizes file size
- Resizes to optimal dimensions
- Centers sprites with padding
- Creates tracking spreadsheet
- Generates preview
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import csv
from pathlib import Path
import json

class IconPreparer:
    def __init__(self, config=None):
        self.config = config or {
            'target_width': 80,
            'target_height': 60,
            'min_padding': 2,  # pixels of padding around sprite
            'output_format': 'PNG',
            'optimize': True,
            'bg_tolerance': 10  # color tolerance for background detection (0-255)
        }
        self.issues = []
        self.warnings = []
        self.fixes_applied = []

    def prepare_icon(self, input_path, output_path=None, auto_fix=True):
        """Prepare a single icon for upload"""
        print(f"\n{'='*60}")
        print(f"Preparing: {input_path}")
        print(f"{'='*60}")

        if not os.path.exists(input_path):
            print(f"❌ Error: File not found: {input_path}")
            return False

        # Load image
        try:
            img = Image.open(input_path)
            original_img = img.copy()
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return False

        # Run checks
        self._check_format(img, input_path)
        self._check_mode(img)
        self._check_transparency(img)
        self._check_dimensions(img)

        # Apply fixes if requested
        if auto_fix and (self.issues or self.warnings):
            print(f"\n🔧 Applying automatic fixes...")
            img = self._apply_fixes(img, original_img)

        # Optimize
        if self.config['optimize']:
            print(f"⚙️  Optimizing file size...")

        # Determine output path
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_prepared{ext}"

        # Save
        try:
            save_kwargs = {
                'format': 'PNG',
                'optimize': self.config['optimize']
            }
            img.save(output_path, **save_kwargs)

            # Show file size comparison
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            reduction = ((original_size - new_size) / original_size * 100) if original_size > new_size else 0

            print(f"\n✅ Saved to: {output_path}")
            print(f"   Original: {original_size:,} bytes")
            print(f"   Prepared: {new_size:,} bytes", end="")
            if reduction > 0:
                print(f" (↓ {reduction:.1f}%)")
            else:
                print()

        except Exception as e:
            print(f"❌ Error saving: {e}")
            return False

        # Summary
        self._print_summary()

        return True

    def _check_format(self, img, path):
        """Check file format"""
        if not path.lower().endswith('.png'):
            self.issues.append("File is not PNG format")
            print("❌ Format: Not PNG (JPG/other)")
        else:
            print("✓ Format: PNG")

    def _check_mode(self, img):
        """Check color mode"""
        if img.mode != 'RGBA':
            if img.mode in ['RGB', 'P', 'L']:
                self.warnings.append(f"Color mode is {img.mode}, should be RGBA")
                print(f"⚠️  Mode: {img.mode} (will convert to RGBA)")
            else:
                print(f"✓ Mode: {img.mode}")
        else:
            print("✓ Mode: RGBA")

    def _check_transparency(self, img):
        """Check if image has transparency"""
        if img.mode not in ['RGBA', 'LA', 'PA']:
            self.warnings.append(f"No alpha channel (mode: {img.mode}) - will auto-detect and remove background")
            print(f"⚠️  Transparency: No alpha channel (will be fixed automatically)")
        else:
            # Check if any pixels are actually transparent
            if img.mode == 'RGBA':
                alpha = img.getchannel('A')
                extrema = alpha.getextrema()
                if extrema[0] == 255 and extrema[1] == 255:
                    self.warnings.append("Has alpha channel but no transparent pixels - will remove background")
                    print("⚠️  Transparency: No transparent pixels (will auto-detect background)")
                else:
                    print(f"✓ Transparency: Yes (alpha range: {extrema[0]}-{extrema[1]})")
            else:
                print("✓ Transparency: Yes")

    def _check_dimensions(self, img):
        """Check image dimensions"""
        width, height = img.size
        target_w = self.config['target_width']
        target_h = self.config['target_height']

        print(f"📏 Dimensions: {width}×{height}px")

        if width < 40 or height < 30:
            self.warnings.append(f"Size {width}×{height} is smaller than minimum 40×30")
            print(f"   ⚠️  Smaller than minimum 40×30px")
        elif width == target_w and height == target_h:
            print(f"   ✓ Perfect size ({target_w}×{target_h})")
        elif width < target_w or height < target_h:
            self.warnings.append(f"Size {width}×{height} is smaller than recommended {target_w}×{target_h}")
            print(f"   ⚠️  Smaller than recommended {target_w}×{target_h}")
        elif width > 1024 or height > 1024:
            self.issues.append(f"Size {width}×{height} exceeds Roblox limit of 1024×1024")
            print(f"   ❌ Exceeds Roblox limit (1024×1024)")
        else:
            print(f"   ✓ Good size (target: {target_w}×{target_h})")

        # Check aspect ratio
        aspect = width / height if height > 0 else 0
        target_aspect = target_w / target_h
        if abs(aspect - target_aspect) > 0.2:
            self.warnings.append(f"Aspect ratio {aspect:.2f} differs from target {target_aspect:.2f}")
            print(f"   ⚠️  Aspect ratio {aspect:.2f} (target: {target_aspect:.2f})")

    def _detect_background_color(self, img):
        """Detect the background color (most likely from corners)"""
        width, height = img.size

        # Sample corner pixels
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((width - 1, 0)),
            img.getpixel((0, height - 1)),
            img.getpixel((width - 1, height - 1))
        ]

        # Also sample edges
        edge_samples = []
        for x in range(0, width, max(1, width // 10)):
            edge_samples.append(img.getpixel((x, 0)))
            edge_samples.append(img.getpixel((x, height - 1)))
        for y in range(0, height, max(1, height // 10)):
            edge_samples.append(img.getpixel((0, y)))
            edge_samples.append(img.getpixel((width - 1, y)))

        # Find most common color in corners and edges
        all_samples = corners + edge_samples
        color_counts = {}
        for color in all_samples:
            # Normalize to RGB tuple (handle different modes)
            if isinstance(color, int):
                color = (color, color, color)
            elif len(color) > 3:
                color = color[:3]  # Drop alpha if present

            color_counts[color] = color_counts.get(color, 0) + 1

        # Return most common color
        if color_counts:
            bg_color = max(color_counts, key=color_counts.get)
            return bg_color

        # Default to white if detection fails
        return (255, 255, 255)

    def _make_background_transparent(self, img, bg_color, tolerance=10):
        """Convert image to RGBA and make background color transparent"""
        # Convert to RGBA
        img = img.convert('RGBA')

        # Get image data
        datas = img.getdata()
        new_data = []

        pixels_changed = 0
        for item in datas:
            # Check if pixel is close to background color (within tolerance)
            if len(item) >= 3:
                r_diff = abs(item[0] - bg_color[0])
                g_diff = abs(item[1] - bg_color[1])
                b_diff = abs(item[2] - bg_color[2])

                if r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance:
                    # Make transparent
                    new_data.append((item[0], item[1], item[2], 0))
                    pixels_changed += 1
                else:
                    # Keep original (but ensure full opacity if it wasn't transparent)
                    new_data.append((item[0], item[1], item[2], 255))
            else:
                new_data.append(item)

        img.putdata(new_data)
        return img, pixels_changed

    def _apply_fixes(self, img, original):
        """Apply automatic fixes"""
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            print(f"   • Converting {img.mode} → RGBA")

            # Special handling for palette mode with transparency
            if img.mode == 'P' and 'transparency' in img.info:
                img = img.convert('RGBA')
                self.fixes_applied.append("Converted to RGBA (preserved palette transparency)")
            else:
                # Detect background color from original image
                bg_color = self._detect_background_color(original if original.mode in ['RGB', 'P', 'L'] else img)
                print(f"   • Detected background color: RGB{bg_color}")

                # Convert and make background transparent
                img, pixels_changed = self._make_background_transparent(
                    original if original.mode in ['RGB', 'P', 'L'] else img,
                    bg_color,
                    tolerance=self.config['bg_tolerance']
                )

                if pixels_changed > 0:
                    total_pixels = img.size[0] * img.size[1]
                    percent = (pixels_changed / total_pixels) * 100
                    print(f"   • Made {pixels_changed:,} pixels transparent ({percent:.1f}%)")
                    self.fixes_applied.append(f"Converted to RGBA with transparency (removed background)")
                else:
                    print(f"   • No background pixels detected")
                    self.fixes_applied.append("Converted to RGBA")
        else:
            # Already RGBA, check if it needs transparency added
            alpha = img.getchannel('A')
            extrema = alpha.getextrema()
            if extrema[0] == 255 and extrema[1] == 255:
                # Has alpha channel but no transparent pixels
                print(f"   • Detecting and removing background from RGBA image")
                bg_color = self._detect_background_color(img)
                print(f"   • Detected background color: RGB{bg_color}")
                img, pixels_changed = self._make_background_transparent(img, bg_color, tolerance=self.config['bg_tolerance'])
                if pixels_changed > 0:
                    total_pixels = img.size[0] * img.size[1]
                    percent = (pixels_changed / total_pixels) * 100
                    print(f"   • Made {pixels_changed:,} pixels transparent ({percent:.1f}%)")
                    self.fixes_applied.append(f"Removed background color")


        # Resize if needed
        width, height = img.size
        target_w = self.config['target_width']
        target_h = self.config['target_height']

        if width > 1024 or height > 1024:
            # Scale down to fit within Roblox limits
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            print(f"   • Resized from {width}×{height} to {img.size[0]}×{img.size[1]} (Roblox limit)")
            self.fixes_applied.append(f"Resized to fit Roblox limit")
            width, height = img.size

        if width < target_w or height < target_h:
            # Create canvas with target size and center the sprite
            canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))

            # Calculate centered position
            x = (target_w - width) // 2
            y = (target_h - height) // 2

            # Paste sprite onto canvas
            canvas.paste(img, (x, y), img if img.mode == 'RGBA' else None)
            img = canvas
            print(f"   • Centered sprite on {target_w}×{target_h} canvas")
            self.fixes_applied.append(f"Centered on {target_w}×{target_h} canvas")

        elif width > target_w or height > target_h:
            # Scale down to target size while preserving aspect ratio
            img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)

            # Center on canvas
            canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
            x = (target_w - img.size[0]) // 2
            y = (target_h - img.size[1]) // 2
            canvas.paste(img, (x, y), img)
            img = canvas
            print(f"   • Scaled and centered to {target_w}×{target_h}")
            self.fixes_applied.append(f"Scaled to {target_w}×{target_h}")

        # Add slight padding if sprite goes to edges
        bbox = img.getbbox()
        if bbox:
            min_pad = self.config['min_padding']
            if bbox[0] < min_pad or bbox[1] < min_pad or \
               bbox[2] > width - min_pad or bbox[3] > height - min_pad:
                # Shrink sprite slightly to add padding
                pad_size = (width - min_pad * 2, height - min_pad * 2)
                temp = img.crop(bbox)
                temp.thumbnail(pad_size, Image.Resampling.LANCZOS)

                canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                x = (width - temp.size[0]) // 2
                y = (height - temp.size[1]) // 2
                canvas.paste(temp, (x, y), temp)
                img = canvas
                print(f"   • Added {min_pad}px padding")
                self.fixes_applied.append("Added padding")

        return img

    def _print_summary(self):
        """Print preparation summary"""
        print(f"\n{'='*60}")
        print("PREPARATION SUMMARY")
        print(f"{'='*60}")

        if self.fixes_applied:
            print(f"\n✅ FIXES APPLIED ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"   • {fix}")

        if self.issues:
            print(f"\n❌ REMAINING ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   • {issue}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")

        if not self.issues and not self.warnings:
            print("\n✅ All checks passed! Ready for upload to Roblox.")
        elif not self.issues:
            print("\n✅ No critical issues. Ready for upload.")
        else:
            print("\n⚠️  Please review issues before uploading.")

        print(f"{'='*60}\n")

def create_preview_sheet(icon_files, output_path='preview_sheet.png'):
    """Create a preview sheet showing all icons"""
    if not icon_files:
        return

    # Calculate grid size
    icons_per_row = min(8, len(icon_files))
    num_rows = (len(icon_files) + icons_per_row - 1) // icons_per_row

    # Cell size
    cell_width = 100
    cell_height = 100
    padding = 10

    # Create canvas
    width = icons_per_row * (cell_width + padding) + padding
    height = num_rows * (cell_height + padding) + padding + 30  # +30 for labels

    canvas = Image.new('RGBA', (width, height), (40, 40, 40, 255))
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.load_default()
    except:
        font = None

    # Place icons
    for idx, icon_path in enumerate(icon_files):
        if not os.path.exists(icon_path):
            continue

        row = idx // icons_per_row
        col = idx % icons_per_row

        x = padding + col * (cell_width + padding)
        y = padding + row * (cell_height + padding)

        # Draw cell background
        draw.rectangle([x, y, x + cell_width, y + cell_height],
                      fill=(60, 60, 60, 255),
                      outline=(100, 100, 100, 255))

        try:
            # Load and resize icon
            icon = Image.open(icon_path)
            icon.thumbnail((cell_width - 10, cell_height - 30), Image.Resampling.LANCZOS)

            # Center icon in cell
            icon_x = x + (cell_width - icon.size[0]) // 2
            icon_y = y + (cell_height - 30 - icon.size[1]) // 2

            canvas.paste(icon, (icon_x, icon_y), icon if icon.mode == 'RGBA' else None)

            # Draw filename
            filename = os.path.basename(icon_path)
            if len(filename) > 15:
                filename = filename[:12] + '...'
            if font:
                draw.text((x + 5, y + cell_height - 20), filename,
                         fill=(200, 200, 200, 255), font=font)

        except Exception as e:
            # Draw error
            if font:
                draw.text((x + 10, y + 40), "Error loading",
                         fill=(255, 100, 100, 255), font=font)

    canvas.save(output_path)
    print(f"✅ Created preview sheet: {output_path}")

def create_tracking_csv(icon_info, output_path='icon_tracking.csv'):
    """Create a tracking spreadsheet for upload management"""

    fieldnames = ['Pokemon', 'Type', 'File', 'Size', 'Dimensions',
                  'Ready', 'Normal Asset ID', 'Shiny Asset ID', 'Status', 'Notes']

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(icon_info)

    print(f"✅ Created tracking CSV: {output_path}")

def batch_prepare(input_dir, output_dir=None, config=None):
    """Batch prepare all images in a directory"""

    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Error: Directory not found: {input_dir}")
        return

    # Find all PNG files
    png_files = list(input_path.glob('*.png'))

    if not png_files:
        print(f"❌ No PNG files found in {input_dir}")
        return

    print(f"\nFound {len(png_files)} PNG files")
    print(f"{'='*60}")

    # Create output directory
    if output_dir is None:
        output_dir = input_path / 'prepared'
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Prepare each icon
    preparer = IconPreparer(config)
    prepared_files = []
    icon_info = []

    for png_file in png_files:
        output_file = output_dir / png_file.name

        success = preparer.prepare_icon(str(png_file), str(output_file), auto_fix=True)

        if success:
            prepared_files.append(str(output_file))

            # Gather info for tracking
            img = Image.open(output_file)
            file_size = os.path.getsize(output_file)

            # Determine if this is normal or shiny
            name = png_file.stem.lower()
            icon_type = 'Shiny' if 'shiny' in name else 'Normal'
            pokemon_name = name.replace('_normal', '').replace('_shiny', '').replace('_', ' ').title()

            icon_info.append({
                'Pokemon': pokemon_name,
                'Type': icon_type,
                'File': png_file.name,
                'Size': f"{file_size:,} bytes",
                'Dimensions': f"{img.size[0]}×{img.size[1]}",
                'Ready': '✓' if not preparer.issues else '⚠',
                'Normal Asset ID': '',
                'Shiny Asset ID': '',
                'Status': 'Pending Upload',
                'Notes': '; '.join(preparer.issues[:2]) if preparer.issues else ''
            })

        # Reset for next file
        preparer.issues = []
        preparer.warnings = []
        preparer.fixes_applied = []

    # Create preview sheet
    if prepared_files:
        preview_path = output_dir / 'preview_sheet.png'
        create_preview_sheet(prepared_files, str(preview_path))

        # Create tracking CSV
        csv_path = output_dir / 'upload_tracking.csv'
        create_tracking_csv(icon_info, str(csv_path))

    # Final summary
    print(f"\n{'='*60}")
    print(f"BATCH PREPARATION COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Prepared: {len(prepared_files)} / {len(png_files)} icons")
    print(f"📁 Output directory: {output_dir}")
    print(f"📋 Tracking CSV: {output_dir / 'upload_tracking.csv'}")
    print(f"🖼️  Preview sheet: {output_dir / 'preview_sheet.png'}")
    print(f"\n📝 NEXT STEPS:")
    print(f"   1. Review preview_sheet.png")
    print(f"   2. Upload prepared icons to Roblox")
    print(f"   3. Update upload_tracking.csv with asset IDs")
    print(f"   4. Use add_custom_icon.py to add to Pokemon.lua")
    print(f"{'='*60}\n")

def interactive_mode():
    """Interactive mode for preparing icons"""
    print("Pokemon Custom Icon Preparer")
    print("="*60)
    print("\nThis tool will prepare your custom Pokemon icons for upload:")
    print("  • Validates format and properties")
    print("  • Ensures transparency")
    print("  • Optimizes file size")
    print("  • Resizes to optimal dimensions (80×60px)")
    print("  • Centers sprites with padding")
    print()

    mode = input("Prepare (s)ingle file or (b)atch directory? [s/b]: ").strip().lower()

    if mode == 'b':
        input_dir = input("Input directory path: ").strip()
        output_dir = input("Output directory (press Enter for 'prepared'): ").strip()
        output_dir = output_dir if output_dir else None

        batch_prepare(input_dir, output_dir)

    else:
        input_file = input("Input file path: ").strip()
        output_file = input("Output file path (press Enter for auto): ").strip()
        output_file = output_file if output_file else None

        preparer = IconPreparer()
        preparer.prepare_icon(input_file, output_file, auto_fix=True)

def main():
    if len(sys.argv) < 2:
        print("Pokemon Custom Icon Preparer")
        print("-"*60)
        print("\nUsage:")
        print("  python prepare_custom_icon.py single <input_file> [output_file]")
        print("  python prepare_custom_icon.py batch <input_dir> [output_dir]")
        print("  python prepare_custom_icon.py interactive")
        print("\nExamples:")
        print("  python prepare_custom_icon.py single pikachu.png")
        print("  python prepare_custom_icon.py batch ./my_icons")
        print("  python prepare_custom_icon.py interactive")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'single':
        if len(sys.argv) < 3:
            print("Error: Missing input file")
            print("Usage: python prepare_custom_icon.py single <input_file> [output_file]")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None

        preparer = IconPreparer()
        preparer.prepare_icon(input_file, output_file, auto_fix=True)

    elif command == 'batch':
        if len(sys.argv) < 3:
            print("Error: Missing input directory")
            print("Usage: python prepare_custom_icon.py batch <input_dir> [output_dir]")
            sys.exit(1)

        input_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None

        batch_prepare(input_dir, output_dir)

    elif command in ['interactive', 'i']:
        interactive_mode()

    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
