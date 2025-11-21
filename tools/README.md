# Pokemon Icon Sheet Tools

Tools for creating, managing, and validating Pokemon icon sprite sheets.

## Quick Start

```bash
# 1. Generate template images
python generate_template.py all

# 2. Calculate where to place a Pokemon icon
python icon_calculator.py 151 Mew

# 3. Validate your sprite sheet
python validate_sheet.py my_pokemon_sheet.png regular

# 4. Add custom icon to Pokemon.lua
python add_custom_icon.py add
```

## Tools Overview

### 1. `icon_calculator.py` - Position Calculator

Calculates the exact pixel position for any icon number.

**Interactive Mode:**
```bash
python icon_calculator.py
# Then enter icon numbers interactively
```

**Command Line:**
```bash
python icon_calculator.py 151 Mew
python icon_calculator.py 1451  # Egg icon
```

**Batch Mode:**
```bash
python icon_calculator.py
> batch
> 1,25,151,251
```

**Output Example:**
```
============================================================
Pokemon: Mew
Icon Number: 151
============================================================
Type: Regular Pokemon Icon

Grid Position:
  Column: 4 (of 0-20)
  Row: 7

Sprite Sheet:
  Sheet Index: 1
  Asset ID: rbxassetid://17134745575
  Sheet Column: 4
  Sheet Row: 7

Pixel Coordinates:
  Normal Sprite: (320px, 210px)
  Shiny Sprite: (360px, 210px)
  Size: 40px × 30px
```

### 2. `validate_sheet.py` - Sprite Sheet Validator

Validates sprite sheets before uploading to Roblox.

**Usage:**
```bash
# Validate regular Pokemon sheet
python validate_sheet.py my_sheet.png regular

# Validate egg sheet
python validate_sheet.py eggs.png egg
```

**Checks:**
- ✓ Correct dimensions (1680×n or 880×n for regular, 540×n for eggs)
- ✓ Proper transparency (alpha channel)
- ✓ Color mode (RGBA recommended)
- ✓ Empty sprite cells
- ✓ Grid alignment

**Output Example:**
```
Validating: my_sheet.png
Sheet Type: regular
------------------------------------------------------------
✓ Width: 1680px (full sheet with 21 columns)
✓ Height: 750px (25 rows)
✓ Has transparency (alpha channel)
✓ Color mode: RGBA

Checking 21×25 grid = 1050 sprites...
⚠ Found 5 empty sprite cells:
  - Normal 150 at (720, 210)
  - Shiny 150 at (760, 210)
  - Normal 151 at (320, 240)

============================================================
VALIDATION RESULTS
============================================================

⚠️  WARNINGS (1):
  - Found 5 empty sprite cells

✅ No errors found. Warnings are non-critical.
============================================================
```

### 3. `add_custom_icon.py` - Custom Icon Manager

Adds custom Pokemon icons to Pokemon.lua automatically.

**Interactive Mode:**
```bash
python add_custom_icon.py add
```

**List Existing Icons:**
```bash
python add_custom_icon.py list
```

**Command Line:**
```bash
python add_custom_icon.py add 1186 12345678 12345679 Celebi
#                             key  normal   shiny    name

# Without shiny:
python add_custom_icon.py add 1186 12345678 '' Celebi
```

**Output Example:**
```
Current Custom Icons:
================================================================================
Key    Icon #   Pokemon                  Has Shiny  Asset ID
--------------------------------------------------------------------------------
1145   1144     xmas sceptile            No         11226762910
1146   1145     santa lax                No         15491372937
1147   1146     walking wake             Yes        13917084621
...
--------------------------------------------------------------------------------
Total: 35 custom icons

Available slots (gaps): 1151-1153
Next sequential slot: 1186
```

### 4. `generate_template.py` - Template Generator

Creates blank template images with grid guides.

**Usage:**
```bash
# Generate all templates
python generate_template.py all

# Regular Pokemon sheet (default 25 rows)
python generate_template.py regular

# Custom number of rows
python generate_template.py regular 50 my_template.png

# Egg sheet
python generate_template.py egg 30

# Reference guide
python generate_template.py reference
```

**Outputs:**
- `pokemon_sheet_template.png` - Grid template for regular Pokemon
- `egg_sheet_template.png` - Grid template for eggs
- `sprite_reference.png` - Visual guide showing sprite dimensions

## Workflow Examples

### Example 1: Add New Pokemon to Sprite Sheet

```bash
# Step 1: Calculate position
python icon_calculator.py 152 Chikorita
# Output: Column 5, Row 7, Position (400, 210)

# Step 2: Generate template if needed
python generate_template.py regular 25

# Step 3: Open template in Aseprite/GIMP/Photoshop
# Navigate to position (400, 210)
# Place normal sprite at x=400
# Place shiny sprite at x=440

# Step 4: Validate before uploading
python validate_sheet.py my_sheet.png regular

# Step 5: Upload to Roblox and update Pokemon.lua with asset ID
```

### Example 2: Add Custom Event Pokemon

```bash
# Step 1: Create your custom icon (any size, with transparency)
# Upload normal and shiny versions to Roblox
# Note the asset IDs

# Step 2: Add to Pokemon.lua
python add_custom_icon.py add
# Enter: Pokemon name, asset IDs

# Step 3: Test in game
# Use: Pokemon:getIcon(ICON_NUMBER, shiny)
```

### Example 3: Batch Process Multiple Pokemon

```bash
# Step 1: Calculate positions for range
python icon_calculator.py
> range 1 151
> y  # Export to CSV

# Step 2: Open CSV in Excel/Google Sheets
# Use as reference while placing sprites

# Step 3: Validate completed sheet
python validate_sheet.py pokedex_gen1.png regular
```

## Requirements

All tools require Python 3.6+

**Additional requirements for some tools:**
```bash
pip install Pillow  # For generate_template.py and validate_sheet.py
```

## Icon Numbering Quick Reference

| Range | Type | Layout | Cell Size |
|-------|------|--------|-----------|
| 0-1450 | Regular Pokemon | 21 cols, 80×30px cells | 40×30px each sprite |
| 1451-1872 | Eggs (Type 1) | 18 cols, 30×32px cells | 30×32px |
| 1873+ | Eggs (Type 2) | 18 cols, 30×32px cells | 30×32px |
| Custom | Event/Special | Individual assets | Any size |

**Regular Pokemon Calculation:**
```
column = icon_number % 21
row = floor(icon_number / 21)
x_position = column * 80 + (0 for normal, 40 for shiny)
y_position = row * 30
```

**Egg Calculation:**
```
egg_index = icon_number - 1451  (or - 1442 if > 1872)
column = egg_index % 18
row = floor(egg_index / 18)
x_position = column * 30
y_position = row * 32
```

## Sprite Sheet Structure

### Regular Pokemon Sheet

```
Total Width: 1680px (21 columns × 80px)
Row Height: 30px

Each Cell (80×30px):
├─ Normal (40×30px) - Left side
└─ Shiny (40×30px) - Right side

Layout:
[0N][0S][1N][1S][2N][2S]...[20N][20S]  Row 0 (Icons 0-20)
[21N][21S][22N][22S]...[41N][41S]      Row 1 (Icons 21-41)
...
```

### Egg Sheet

```
Total Width: 540px (18 columns × 30px)
Row Height: 32px

Each Cell: 30×32px (single egg sprite)

Layout:
[0][1][2]...[17]        Row 0 (Icons 1451-1468)
[18][19][20]...[35]     Row 1 (Icons 1469-1486)
...
```

## Tips & Best Practices

1. **Always validate** before uploading to Roblox
2. **Keep backups** of original sprite sheets
3. **Use templates** to ensure proper alignment
4. **Test in-game** before finalizing
5. **Document** custom icon numbers in a separate file
6. **Export with minimal compression** for best quality
7. **Maintain transparency** - use RGBA mode
8. **Center sprites** vertically within cells

## Troubleshooting

**"Icon appears blank in game"**
- Check asset ID is correct
- Verify asset is public in Roblox
- Confirm ImageRectOffset calculation

**"Wrong Pokemon appears"**
- Recheck icon number calculation
- Verify sprite is in correct cell
- Check for off-by-one errors (icon vs key)

**"Sprite is cut off"**
- Ensure sprite fits within cell bounds
- Check ImageRectSize is correct
- Verify no extra padding in export

**"Validation fails with dimension error"**
- Regular sheets: Must be 1680px or 880px wide
- Egg sheets: Must be 540px wide
- Height must be multiple of row height (30px or 32px)

## Contributing

Found a bug or want to add a feature? Feel free to modify these tools!

## See Also

- [ICON_SHEET_GUIDE.md](../docs/ICON_SHEET_GUIDE.md) - Comprehensive guide
- [Pokemon.lua](../Pokemon.lua) - Main implementation
