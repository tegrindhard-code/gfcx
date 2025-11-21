# Custom Icon Preparation Guide

Complete guide for using `prepare_custom_icon.py` to prepare Pokemon icons for Roblox upload.

## Installation

This tool requires Python 3.6+ and Pillow (PIL):

```bash
# Install required package
pip install Pillow

# Or install all tool requirements
pip install -r tools/requirements.txt
```

## What This Tool Does

**Automatic Preparations:**
- ✅ Validates PNG format
- ✅ Converts to RGBA color mode
- ✅ Ensures transparency/alpha channel
- ✅ Resizes to optimal dimensions (80×60px default)
- ✅ Centers sprites with padding
- ✅ Optimizes file size
- ✅ Checks Roblox size limits (1024×1024)
- ✅ Batch processes multiple icons
- ✅ Creates preview sheet
- ✅ Generates tracking spreadsheet

**What You Still Need to Do:**
- Upload to Roblox manually
- Note down asset IDs
- Add to Pokemon.lua using `add_custom_icon.py`

## Quick Start

### Single Icon
```bash
# Prepare one icon
python3 tools/prepare_custom_icon.py single pikachu.png

# With custom output name
python3 tools/prepare_custom_icon.py single pikachu.png pikachu_ready.png
```

### Batch Processing (Recommended)
```bash
# Prepare all icons in a directory
python3 tools/prepare_custom_icon.py batch ./my_pokemon_icons

# With custom output directory
python3 tools/prepare_custom_icon.py batch ./my_pokemon_icons ./ready_for_upload
```

### Interactive Mode
```bash
python3 tools/prepare_custom_icon.py interactive
```

## Example Output

### Single Icon
```
============================================================
Preparing: pikachu_normal.png
============================================================
✓ Format: PNG
✓ Mode: RGBA
✓ Transparency: Yes (alpha range: 0-255)
📏 Dimensions: 64×48px
   ⚠️  Smaller than recommended 80×60

🔧 Applying automatic fixes...
   • Centered on 80×60 canvas
   • Added 2px padding

⚙️  Optimizing file size...

✅ Saved to: pikachu_normal_prepared.png
   Original: 3,456 bytes
   Prepared: 3,102 bytes (↓ 10.2%)

============================================================
PREPARATION SUMMARY
============================================================

✅ FIXES APPLIED (2):
   • Centered on 80×60 canvas
   • Added padding

✅ No critical issues. Ready for upload.
============================================================
```

### Batch Processing
```
Found 6 PNG files
============================================================

[... processes each file ...]

✅ Created preview sheet: prepared/preview_sheet.png
✅ Created tracking CSV: prepared/upload_tracking.csv

============================================================
BATCH PREPARATION COMPLETE
============================================================
✅ Prepared: 6 / 6 icons
📁 Output directory: prepared
📋 Tracking CSV: prepared/upload_tracking.csv
🖼️  Preview sheet: prepared/preview_sheet.png

📝 NEXT STEPS:
   1. Review preview_sheet.png
   2. Upload prepared icons to Roblox
   3. Update upload_tracking.csv with asset IDs
   4. Use add_custom_icon.py to add to Pokemon.lua
============================================================
```

## Configuration

Default settings (can be customized in code):
```python
config = {
    'target_width': 80,      # Target width in pixels
    'target_height': 60,     # Target height in pixels
    'min_padding': 2,        # Minimum padding around sprite
    'output_format': 'PNG',  # Output format
    'optimize': True         # Enable file size optimization
}
```

## File Naming Conventions

For best results, name your files clearly:

**Recommended naming:**
```
pikachu_normal.png
pikachu_shiny.png
celebi_normal.png
celebi_shiny.png
mewtwo_mega_normal.png
mewtwo_mega_shiny.png
```

**The tool will:**
- Detect "normal" vs "shiny" in filename
- Extract Pokemon name automatically
- Group pairs in tracking CSV

## Output Files

### Prepared Icons
- Saved to `prepared/` directory (or custom location)
- Same filenames as input
- Optimized and ready for Roblox upload

### Preview Sheet (`preview_sheet.png`)
- Visual grid showing all prepared icons
- 8 icons per row
- Includes filenames
- Quick visual check before uploading

Example:
```
┌─────────┬─────────┬─────────┬─────────┐
│Pikachu  │Pikachu  │Celebi   │Celebi   │
│ Normal  │ Shiny   │ Normal  │ Shiny   │
├─────────┼─────────┼─────────┼─────────┤
│Mewtwo   │Mewtwo   │         │         │
│ Normal  │ Shiny   │         │         │
└─────────┴─────────┴─────────┴─────────┘
```

### Tracking CSV (`upload_tracking.csv`)
Spreadsheet to manage upload process:

| Pokemon | Type | File | Size | Dimensions | Ready | Normal Asset ID | Shiny Asset ID | Status | Notes |
|---------|------|------|------|------------|-------|-----------------|----------------|--------|-------|
| Pikachu | Normal | pikachu_normal.png | 3,102 bytes | 80×60 | ✓ | | | Pending Upload | |
| Pikachu | Shiny | pikachu_shiny.png | 3,215 bytes | 80×60 | ✓ | | | Pending Upload | |

**Workflow:**
1. Open in Excel/Google Sheets
2. Upload icons to Roblox
3. Fill in Asset IDs as you upload
4. Update Status column
5. Use as reference when adding to Pokemon.lua

## Common Scenarios

### Scenario 1: Starting from scratch
```bash
# 1. Put all your source icons in a folder
mkdir my_pokemon_icons
# (add your .png files)

# 2. Prepare all icons
python3 tools/prepare_custom_icon.py batch my_pokemon_icons

# 3. Review the preview
open prepared/preview_sheet.png

# 4. Upload to Roblox
# (manual step)

# 5. Track uploads in CSV
# Edit prepared/upload_tracking.csv

# 6. Add to Pokemon.lua
python3 tools/add_custom_icon.py add
```

### Scenario 2: Icons are various sizes
```bash
# Tool automatically resizes and centers!
# Small icons: Centered on 80×60 canvas with padding
# Large icons: Scaled down to fit 80×60
# Perfect size: Validated and optimized

python3 tools/prepare_custom_icon.py batch ./mixed_sizes
```

### Scenario 3: Icons don't have transparency
```bash
# Tool automatically converts to RGBA
# Note: It treats white (255,255,255) as transparent
# For other backgrounds, pre-process in GIMP/Photoshop

python3 tools/prepare_custom_icon.py single icon_no_alpha.png
```

### Scenario 4: One icon needs special attention
```bash
# Prepare individually with custom output
python3 tools/prepare_custom_icon.py single special.png special_ready.png

# Then include in batch CSV manually
```

## Validation Checks

### Format Checks
- ✅ PNG format
- ⚠️ Non-PNG formats will fail

### Color Mode Checks
- ✅ RGBA (best)
- ⚠️ RGB, P, L (auto-converted)
- ⚠️ Other modes (may have issues)

### Transparency Checks
- ✅ Has alpha channel with transparent pixels
- ⚠️ Has alpha but no transparent pixels
- ❌ No alpha channel

### Dimension Checks
- ✅ Exactly 80×60 (target size)
- ✅ 60×45 to 100×75 (good range, will be centered)
- ⚠️ Below 40×30 (too small, may look pixelated)
- ⚠️ Above 200×150 (will be scaled down)
- ❌ Above 1024×1024 (exceeds Roblox limit)

### File Size Checks
- ✅ Under 1MB (optimal)
- ⚠️ 1-5MB (may be slow to load)
- Tool optimizes to reduce size

## Troubleshooting

### "Image has no alpha channel"
**Solution:** Tool will auto-convert to RGBA. White pixels become transparent.

**Better Solution:** Pre-process in image editor:
```bash
# Using ImageMagick
magick input.png -background none -alpha set output.png

# Or open in GIMP and Layer → Transparency → Add Alpha Channel
```

### "Size exceeds Roblox limit"
**Solution:** Tool automatically scales down to 1024×1024 max.

### "Aspect ratio differs from target"
**Solution:** Tool centers sprite on canvas. If sprite looks stretched, adjust source image.

### "File is not PNG format"
**Convert first:**
```bash
# Using ImageMagick
magick input.jpg output.png

# Or use GIMP/Photoshop: Export As → PNG
```

### Preview sheet shows "Error loading"
**Cause:** File might be corrupted or unsupported format.
**Solution:** Re-export from source editor.

## Integration with Other Tools

### Complete Workflow
```bash
# 1. Prepare icons
python3 tools/prepare_custom_icon.py batch ./my_icons

# 2. Review output
cat prepared/upload_tracking.csv

# 3. Upload to Roblox and note asset IDs
# (manual step, update CSV)

# 4. Calculate next available icon slot
python3 tools/add_custom_icon.py list

# 5. Add to Pokemon.lua
python3 tools/add_custom_icon.py add 1186 12345678 12345679 Celebi

# 6. Test in game
# Pokemon:getIcon(1185, false)
```

### Using with External Tools

**Export from Aseprite:**
```bash
# Export at 2x scale
aseprite -b sprite.ase --scale 2 --save-as pikachu_normal.png

# Then prepare
python3 tools/prepare_custom_icon.py single pikachu_normal.png
```

**Batch from sprite sheet:**
```bash
# Extract individual sprites first (manual or scripted)
# Then prepare all
python3 tools/prepare_custom_icon.py batch ./extracted_sprites
```

## Advanced Usage

### Custom Configuration
Edit the script and modify config dictionary:
```python
config = {
    'target_width': 160,     # 4x size for extra quality
    'target_height': 120,
    'min_padding': 4,
    'optimize': True
}
```

### Programmatic Use
```python
from prepare_custom_icon import IconPreparer

preparer = IconPreparer({
    'target_width': 100,
    'target_height': 100
})

preparer.prepare_icon('input.png', 'output.png', auto_fix=True)
```

## Tips & Best Practices

1. **Always batch process** - Faster and creates tracking CSV
2. **Review preview sheet** - Catch issues before uploading
3. **Keep source files** - Don't delete originals
4. **Use clear naming** - Include "normal"/"shiny" in filename
5. **Update CSV immediately** - Fill in asset IDs right after upload
6. **Test one first** - Upload and test one icon before doing batch
7. **Backup everything** - Keep copies of prepared icons and CSVs

## File Size Guidelines

| Resolution | Good Size | Warning Size |
|------------|-----------|--------------|
| 40×30 | 1-3 KB | >5 KB |
| 80×60 | 2-5 KB | >10 KB |
| 160×120 | 5-15 KB | >30 KB |

Tool optimization typically achieves 10-30% size reduction.

## Quality Checklist

Before uploading prepared icons:
- [ ] Preview sheet looks good
- [ ] All icons have transparency
- [ ] Sprites are centered
- [ ] Consistent style across all icons
- [ ] Normal and shiny versions for each
- [ ] File sizes reasonable
- [ ] Tracking CSV is ready
- [ ] Backup of originals saved

## See Also

- [add_custom_icon.py](README.md#3-add_custom_iconpy) - Add icons to Pokemon.lua
- [icon_calculator.py](README.md#1-icon_calculatorpy) - Calculate icon positions
- [ICON_SHEET_GUIDE.md](../docs/ICON_SHEET_GUIDE.md) - Complete icon system guide
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Quick reference

## Support

If you encounter issues:
1. Check error messages in terminal
2. Review prepared icons manually
3. Try processing one file first
4. Check file format with `file image.png`
5. Verify source image isn't corrupted

---

**Ready to prepare your icons?**
```bash
python3 tools/prepare_custom_icon.py interactive
```
