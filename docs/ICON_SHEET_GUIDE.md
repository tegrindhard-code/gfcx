# Pokemon Icon Sheet Guide

## Table of Contents
1. [Icon Numbering System](#icon-numbering-system)
2. [Creating Templates](#creating-templates)
3. [Adding New Pokemon](#adding-new-pokemon)

---

## Icon Numbering System

### How Icon Numbers Work

The icon system maps icon numbers to positions in sprite sheets:

```
Icon Number → Position Calculation → Sprite Sheet Location
```

### Regular Pokemon Icons (0-1450)

**Grid Layout:**
- 21 columns per sprite sheet (split into two sheets of 11 columns each)
- Multiple rows across 5 sprite sheets

**Calculation:**
```lua
column = iconNumber % 21        -- Which column (0-20)
row = floor(iconNumber / 21)    -- Which row

-- Which sprite sheet?
imageIndex = 1
if column > 10 then
    imageIndex = imageIndex + 1
    column = column - 11
end
if row > 24 then
    imageIndex = imageIndex + 2
    row = row - 25
end
if row > 32 then
    imageIndex = imageIndex + 2
    row = row - 33
end
```

**Sprite Sheet Distribution:**

| Sheet | Columns | Rows | Icon Range (approx) |
|-------|---------|------|---------------------|
| 1 | 0-10 | 0-24 | 0-274 |
| 2 | 11-20 | 0-24 | 11-284 (odd columns) |
| 3 | 0-10 | 25-57 | 525-647 |
| 4 | 11-20 | 25-57 | 536-657 (odd columns) |
| 5 | 0-10 | 58+ | 1218+ |

**Examples:**
```
Icon 0:   Column 0, Row 0, Sheet 1, Position (0, 0)
Icon 21:  Column 0, Row 1, Sheet 1, Position (0, 30)
Icon 11:  Column 11, Row 0, Sheet 2, Position (0, 0)
Icon 150: Column 3, Row 7, Sheet 1, Position (240, 210)
```

### Egg Icons (1451-1872 and 1873+)

**Grid Layout:**
- 18 columns per sheet
- Single sprite sheet

**Calculation:**
```lua
if iconNumber > 1872 then
    eggSpriteIndex = iconNumber - 1442
else
    eggSpriteIndex = iconNumber - 1451
end

spriteColumn = eggSpriteIndex % 18
spriteRow = floor(eggSpriteIndex / 18)
```

**Examples:**
```
Icon 1451: Egg 0, Position (0, 0)
Icon 1469: Egg 18, Position (0, 32)
Icon 1873: Egg 431, Position (11*30px, 23*32px)
```

### Custom Icons (1145+)

Custom icons use `icon + 1` as the lookup key:
```lua
Icon 1144 → customNormalIcons[1145]
Icon 1149 → customNormalIcons[1150]
```

**Currently Used Custom Slots:**
- 1145-1150 (Event Pokemon)
- 1154-1185 (Regional forms, Paradox Pokemon)
- 2008 (Mega Arceus)

---

## Creating Templates

### Aseprite Template

**Setup:**
1. New File → Width: 1680px, Height: 750px (for 25 rows)
2. Mode: RGBA
3. Grid Setup:
   - Grid → Grid Settings
   - Width: 80px, Height: 30px
   - Show Grid: Enabled

**Layer Structure:**
```
├─ Reference (for alignment)
├─ Row Labels
├─ Column Labels
├─ Sprites
│  ├─ Shiny Layer
│  └─ Normal Layer
└─ Background (transparent)
```

**Workflow:**
1. Draw normal sprite in left 40px of cell
2. Draw shiny variant in right 40px
3. Keep sprites centered vertically (15px from top/bottom)
4. Export as PNG with transparency

**Aseprite Script Template:**
```lua
-- Save as: scripts/export_icon_sheet.lua
local sprite = app.activeSprite
if not sprite then
  app.alert("No sprite open")
  return
end

app.command.ExportSpriteSheet {
  ui=false,
  type=SpriteSheetType.HORIZONTAL,
  textureFilename="pokemon_icons.png",
  borderPadding=0,
  shapePadding=0,
  innerPadding=0
}
```

### GIMP Template

**Setup:**
1. File → New
   - Width: 1680px
   - Height: 750px (adjust for rows needed)
   - Advanced Options → Fill with: Transparency
2. View → Show Grid
3. Image → Configure Grid:
   - Width: 80px
   - Height: 30px
   - Line style: Solid line

**Guide Setup:**
```python
# GIMP Python-Fu script
# Filters → Python-Fu → Console

import gimpfu

def create_icon_guides():
    img = gimp.image_list()[0]

    # Vertical guides every 40px (normal/shiny split)
    for x in range(40, 1680, 40):
        pdb.gimp_image_add_vguide(img, x)

    # Horizontal guides every 30px (rows)
    for y in range(30, img.height, 30):
        pdb.gimp_image_add_hguide(img, y)

    gimp.displays_flush()

create_icon_guides()
```

### Photoshop Template

**Actions to create:**
1. New Icon Sheet (Action):
   - New document: 1680×750px, 72dpi, RGB, transparent
   - Create grid guides (Edit → Preferences → Guides & Grid)
   - Grid every 80px

2. Add Icon Guides (Action):
   - View → New Guide → Vertical → Every 40px
   - View → New Guide → Horizontal → Every 30px

**Layer Structure Template:**
```
📁 Pokemon Icons
├─ 📁 Row 0
│  ├─ 🖼️ Icon 0 Shiny
│  ├─ 🖼️ Icon 0 Normal
│  ├─ 🖼️ Icon 1 Shiny
│  └─ 🖼️ Icon 1 Normal
├─ 📁 Row 1
│  └─ ...
└─ 📁 Labels
```

---

## Adding New Pokemon

### Quick Reference Calculator

Use this to find where to place your icon:

```
Icon Number: [YOUR_NUMBER]

Regular Pokemon (0-1450):
  Column: [NUMBER] % 21 = [RESULT]
  Row: floor([NUMBER] / 21) = [RESULT]
  X Position: [COLUMN] * 80px (normal at +0, shiny at +40)
  Y Position: [ROW] * 30px

Egg (1451+):
  Adjusted: [NUMBER] - 1451 = [RESULT]
  Column: [ADJUSTED] % 18 = [RESULT]
  Row: floor([ADJUSTED] / 18) = [RESULT]
  X Position: [COLUMN] * 30px
  Y Position: [ROW] * 32px
```

### Method 1: Add to Sprite Sheet

**Steps:**
1. **Calculate position:**
   ```python
   # Python calculator
   icon_num = 151  # Mew example
   column = icon_num % 21  # Result: 4
   row = icon_num // 21     # Result: 7

   x_normal = column * 80   # Result: 320px
   x_shiny = column * 80 + 40  # Result: 360px
   y = row * 30             # Result: 210px
   ```

2. **Determine sprite sheet:**
   - Column 0-10, Row 0-24 → Sheet 1
   - Column 11-20, Row 0-24 → Sheet 2
   - etc.

3. **Add sprite:**
   - Open sprite sheet in editor
   - Navigate to calculated position
   - Paste normal sprite at (x_normal, y)
   - Paste shiny sprite at (x_shiny, y)

4. **Export and upload:**
   - Export as PNG (no compression)
   - Upload to Roblox Creator Hub
   - Note the new asset ID
   - Update Pokemon.lua with new ID

### Method 2: Add as Custom Icon

**When to use:**
- Icon number > 1144
- Special event Pokemon
- Don't want to modify existing sheets
- Need higher resolution

**Steps:**

1. **Create standalone icon:**
   - 40px × 30px (or larger if needed)
   - PNG with transparency
   - Upload both normal and shiny versions

2. **Add to Pokemon.lua:**

```lua
-- In Pokemon:getIcon() function around line 154

local customNormalIcons = {
    -- ... existing entries ...
    [1186] = 'rbxassetid://YOUR_NORMAL_ID', --Celebi
}

local customShinyIcons = {
    -- ... existing entries ...
    [1186] = 'rbxassetid://YOUR_SHINY_ID', --Celebi
}
```

3. **Use in game:**
   ```lua
   -- Icon number 1185 will look up customNormalIcons[1186]
   local icon = Pokemon:getIcon(1185, false)  -- Normal
   local shiny = Pokemon:getIcon(1185, true)  -- Shiny
   ```

### Method 3: Batch Add Multiple Pokemon

**Excel/Google Sheets Template:**

| Icon # | Pokemon Name | Sheet | Column | Row | X (Normal) | X (Shiny) | Y | Status |
|--------|-------------|-------|--------|-----|------------|-----------|---|--------|
| 151 | Mew | 1 | 4 | 7 | 320 | 360 | 210 | ✓ |
| 152 | Chikorita | 1 | 5 | 7 | 400 | 440 | 210 | ✗ |

**Formulas:**
```
Column: =MOD(A2, 21)
Row: =FLOOR(A2/21, 1)
X (Normal): =C2*80
X (Shiny): =C2*80+40
Y: =D2*30
```

---

## Export Settings

### Optimal Settings for Roblox

**PNG Export:**
- Color Mode: RGBA (with transparency)
- Bit Depth: 8-bit per channel
- Compression: None or minimal
- Filter: None
- Interlacing: None

**Aseprite:**
```
File → Export → Export Sprite Sheet
- Sheet Type: By Rows
- Trim: None
- Padding: 0
- Format: PNG
```

**GIMP:**
```
File → Export As → PNG
- Interlacing: OFF
- Compression level: 0-1
```

**Photoshop:**
```
File → Export → Export As
- Format: PNG
- Transparency: ON
- Convert to sRGB: OFF
- Metadata: None
```

---

## Testing Your Icons

### In-Game Testing

```lua
-- Test in Roblox Studio console:
local icon = Pokemon:getIcon(YOUR_ICON_NUMBER, false)
icon.Parent = game.Players.LocalPlayer.PlayerGui.ScreenGui

-- Test shiny version:
local shiny = Pokemon:getIcon(YOUR_ICON_NUMBER, true)
shiny.Parent = game.Players.LocalPlayer.PlayerGui.ScreenGui
```

### Verify Positioning

```lua
-- Check if icon loads from correct sheet and position:
local icon = Pokemon:getIcon(151, false)
print(icon.Image)  -- Should show correct rbxassetid
print(icon.ImageRectOffset)  -- Should show calculated position
print(icon.ImageRectSize)  -- Should be (40, 30)
```

---

## Troubleshooting

### Common Issues

1. **Icon appears blank:**
   - Check asset ID is correct
   - Verify asset is public in Roblox
   - Check ImageRectOffset calculation

2. **Wrong Pokemon appears:**
   - Recheck icon number calculation
   - Verify sprite sheet structure
   - Check for off-by-one errors

3. **Icon is cut off:**
   - Ensure ImageRectSize is (40, 30)
   - Check sprite fits within cell bounds
   - Verify no padding issues

4. **Shiny not working:**
   - Check customShinyIcons table has entry
   - Verify shiny parameter is true
   - Check if custom icon needs separate shiny asset

---

## Tools & Resources

### Useful Scripts

See `/tools/` directory for:
- `icon_calculator.py` - Calculate positions
- `validate_sheet.py` - Verify sprite sheet structure
- `batch_export.py` - Export multiple icons
- `aseprite_template.aseprite` - Ready-to-use template

### Reference Images

Example sprite sheets are in `/reference/`:
- `sheet_layout.png` - Visual guide to grid system
- `icon_examples.png` - Properly formatted icons
- `size_reference.png` - Exact dimensions overlay
