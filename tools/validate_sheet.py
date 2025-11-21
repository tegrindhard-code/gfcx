#!/usr/bin/env python3
"""
Sprite Sheet Validator

Validates Pokemon icon sprite sheets to ensure they meet requirements.
"""

from PIL import Image
import sys
import os

class SpriteSheetValidator:
    def __init__(self, image_path, sheet_type='regular'):
        self.image_path = image_path
        self.sheet_type = sheet_type
        self.errors = []
        self.warnings = []

        try:
            self.image = Image.open(image_path)
        except Exception as e:
            raise Exception(f"Failed to open image: {e}")

    def validate(self):
        """Run all validation checks"""
        print(f"Validating: {self.image_path}")
        print(f"Sheet Type: {self.sheet_type}")
        print("-" * 60)

        self.check_dimensions()
        self.check_transparency()
        self.check_mode()
        self.check_sprites()

        self.print_results()

        return len(self.errors) == 0

    def check_dimensions(self):
        """Validate image dimensions"""
        width, height = self.image.size

        if self.sheet_type == 'regular':
            # Regular sheets should be 1680px wide (21 columns × 80px)
            # or 880px wide (11 columns × 80px) for split sheets
            if width not in [1680, 880]:
                self.errors.append(
                    f"Width {width}px is invalid. Should be 1680px (full) or 880px (split)"
                )
            elif width == 1680:
                print(f"✓ Width: {width}px (full sheet with 21 columns)")
            else:
                print(f"✓ Width: {width}px (split sheet with 11 columns)")

            # Height should be multiple of 30px
            if height % 30 != 0:
                self.errors.append(
                    f"Height {height}px is not a multiple of 30px"
                )
            else:
                rows = height // 30
                print(f"✓ Height: {height}px ({rows} rows)")

        elif self.sheet_type == 'egg':
            # Egg sheets should be 540px wide (18 columns × 30px)
            if width != 540:
                self.errors.append(
                    f"Width {width}px is invalid. Should be 540px (18 columns)"
                )
            else:
                print(f"✓ Width: {width}px")

            # Height should be multiple of 32px
            if height % 32 != 0:
                self.errors.append(
                    f"Height {height}px is not a multiple of 32px"
                )
            else:
                rows = height // 32
                print(f"✓ Height: {height}px ({rows} rows)")

    def check_transparency(self):
        """Check if image has transparency"""
        if self.image.mode not in ['RGBA', 'LA', 'PA']:
            self.warnings.append(
                "Image has no alpha channel - background won't be transparent"
            )
        else:
            print("✓ Has transparency (alpha channel)")

    def check_mode(self):
        """Check color mode"""
        if self.image.mode != 'RGBA':
            self.warnings.append(
                f"Image mode is {self.image.mode}, recommend RGBA for best compatibility"
            )
        else:
            print("✓ Color mode: RGBA")

    def check_sprites(self):
        """Check individual sprite cells"""
        width, height = self.image.size

        if self.sheet_type == 'regular':
            cell_width = 40  # Each sprite (normal or shiny)
            cell_height = 30
            columns = width // 80  # Each cell is 80px (normal + shiny)
            rows = height // 30

            print(f"\nChecking {columns}×{rows} grid = {columns * rows * 2} sprites...")

            empty_cells = []
            potentially_misaligned = []

            for row in range(rows):
                for col in range(columns):
                    # Check normal sprite (left side)
                    x = col * 80
                    y = row * 30
                    if self._is_sprite_empty(x, y, cell_width, cell_height):
                        icon_num = row * 21 + col  # Approximate
                        empty_cells.append(f"Normal {icon_num} at ({x}, {y})")

                    # Check shiny sprite (right side)
                    x_shiny = col * 80 + 40
                    if self._is_sprite_empty(x_shiny, y, cell_width, cell_height):
                        icon_num = row * 21 + col
                        empty_cells.append(f"Shiny {icon_num} at ({x_shiny}, {y})")

            if empty_cells:
                if len(empty_cells) <= 10:
                    print(f"\n⚠ Found {len(empty_cells)} empty sprite cells:")
                    for cell in empty_cells[:10]:
                        print(f"  - {cell}")
                else:
                    print(f"\n⚠ Found {len(empty_cells)} empty sprite cells (showing first 10):")
                    for cell in empty_cells[:10]:
                        print(f"  - {cell}")
                    print(f"  ... and {len(empty_cells) - 10} more")
            else:
                print("✓ No empty cells detected")

        elif self.sheet_type == 'egg':
            cell_width = 30
            cell_height = 32
            columns = width // 30
            rows = height // 32

            print(f"\nChecking {columns}×{rows} grid = {columns * rows} eggs...")

            empty_cells = []
            for row in range(rows):
                for col in range(columns):
                    x = col * 30
                    y = row * 32
                    if self._is_sprite_empty(x, y, cell_width, cell_height):
                        egg_num = row * 18 + col + 1451
                        empty_cells.append(f"Egg {egg_num} at ({x}, {y})")

            if empty_cells and len(empty_cells) < columns * rows * 0.5:
                print(f"⚠ Found {len(empty_cells)} empty egg cells")
            elif empty_cells:
                self.warnings.append(f"Many empty cells ({len(empty_cells)}) - is this correct?")

    def _is_sprite_empty(self, x, y, width, height):
        """Check if a sprite cell is empty (all transparent or all one color)"""
        try:
            # Crop the sprite region
            box = (x, y, x + width, y + height)
            sprite = self.image.crop(box)

            # Check if all pixels are transparent
            if sprite.mode == 'RGBA':
                pixels = list(sprite.getdata())
                # Check if all pixels have alpha = 0
                all_transparent = all(pixel[3] == 0 for pixel in pixels)
                if all_transparent:
                    return True

                # Check if all non-transparent pixels are the same color
                non_transparent = [p for p in pixels if p[3] > 0]
                if len(non_transparent) == 0:
                    return True

            return False

        except Exception:
            return False

    def print_results(self):
        """Print validation results"""
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All checks passed! Sheet is ready for upload.")
        elif not self.errors:
            print("\n✅ No errors found. Warnings are non-critical.")
        else:
            print("\n❌ Please fix errors before uploading.")

        print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_sheet.py <image_path> [sheet_type]")
        print("  sheet_type: 'regular' (default) or 'egg'")
        sys.exit(1)

    image_path = sys.argv[1]
    sheet_type = sys.argv[2] if len(sys.argv) > 2 else 'regular'

    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        sys.exit(1)

    if sheet_type not in ['regular', 'egg']:
        print(f"Error: Invalid sheet type '{sheet_type}'. Use 'regular' or 'egg'")
        sys.exit(1)

    try:
        validator = SpriteSheetValidator(image_path, sheet_type)
        success = validator.validate()
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
