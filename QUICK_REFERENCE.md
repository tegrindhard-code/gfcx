# Pokemon Icon Sheet - Quick Reference

## At a Glance

| Type | Width | Height | Cell Size | Sprite Size |
|------|-------|--------|-----------|-------------|
| **Regular** | 1680px | 30px × rows | 80×30px | 40×30px (N+S) |
| **Egg** | 540px | 32px × rows | 30×32px | 30×32px |
| **Custom** | Any | Any | N/A | Any |

## Position Formulas

### Regular Pokemon (Icons 0-1450)
```python
column = icon_number % 21          # 0-20
row = icon_number // 21            # 0, 1, 2...
x_normal = column * 80             # Left side
x_shiny = column * 80 + 40         # Right side
y = row * 30
```

### Eggs (Icons 1451+)
```python
egg_index = icon_number - 1451     # or -1442 if >1872
column = egg_index % 18            # 0-17
row = egg_index // 18
x = column * 30
y = row * 32
```

### Custom Icons
```lua
-- In Pokemon.lua, use icon+1 as key:
customNormalIcons[icon_number + 1] = 'rbxassetid://...'
```

## Quick Examples

| Icon # | Pokemon | Column | Row | X (Normal) | X (Shiny) | Y |
|--------|---------|--------|-----|------------|-----------|---|
| 0 | (First) | 0 | 0 | 0 | 40 | 0 |
| 1 | (Second) | 1 | 0 | 80 | 120 | 0 |
| 21 | (Row 2) | 0 | 1 | 0 | 40 | 30 |
| 25 | Pikachu | 4 | 1 | 320 | 360 | 30 |
| 151 | Mew | 4 | 7 | 320 | 360 | 210 |

## Tool Commands

```bash
# Calculate position
python tools/icon_calculator.py 151 Mew

# Generate templates
python tools/generate_template.py all

# Validate sheet
python tools/validate_sheet.py mysheet.png regular

# Add custom icon
python tools/add_custom_icon.py add

# List custom icons
python tools/add_custom_icon.py list
```

## Export Settings

**Format:** PNG with transparency (RGBA)
**Compression:** None or minimal
**Bit Depth:** 8-bit per channel
**Mode:** RGBA (not RGB!)

## In-Game Usage

```lua
-- Get icon (in Lua)
local icon = Pokemon:getIcon(icon_number, is_shiny)

-- Examples:
local pikachu = Pokemon:getIcon(25, false)  -- Normal Pikachu
local shiny_mew = Pokemon:getIcon(151, true)  -- Shiny Mew
local custom = Pokemon:getIcon(1185, false)   -- Custom (key 1186)
```

## Common Issues

| Problem | Solution |
|---------|----------|
| Icon blank | Check asset ID, make it public |
| Wrong Pokemon | Recheck icon number calculation |
| Cut off | Sprite must fit in cell bounds |
| No transparency | Use RGBA mode, not RGB |

## Sprite Sheet IDs

Current regular Pokemon sheets:
- Sheet 1: `17134745575`
- Sheet 2: `17134749969`
- Sheet 3: `17134753859`
- Sheet 4: `17134757872`
- Sheet 5: `17134761227`

Egg sheet:
- `13039987315`

## Directory Structure

```
gfcx/
├── Pokemon.lua              # Main icon system
├── docs/
│   └── ICON_SHEET_GUIDE.md  # Full documentation
├── tools/
│   ├── icon_calculator.py   # Calculate positions
│   ├── validate_sheet.py    # Validate sheets
│   ├── add_custom_icon.py   # Add custom icons
│   ├── generate_template.py # Create templates
│   └── README.md            # Tools documentation
└── QUICK_REFERENCE.md       # This file
```

## Visual Guide

### Regular Pokemon Cell
```
     80px total
   ┌─────────────┐
   │  N  │  S   │  30px
   └─────────────┘
    40px  40px
```

### Grid Layout (Regular)
```
Column: 0   1   2   3  ...  20
       ┌───┬───┬───┬───────┬───┐
Row 0  │ 0 │ 1 │ 2 │  ...  │20 │ Icons 0-20
       ├───┼───┼───┼───────┼───┤
Row 1  │21 │22 │23 │  ...  │41 │ Icons 21-41
       ├───┼───┼───┼───────┼───┤
       │...│...│...│  ...  │...│
       └───┴───┴───┴───────┴───┘
```

### Egg Layout
```
18 columns × 30px = 540px wide
       ┌──┬──┬──┬────┬──┐
Row 0  │0 │1 │2 │ ...│17│ 1451-1468
       ├──┼──┼──┼────┼──┤
Row 1  │18│19│20│ ...│35│ 1469-1486
       └──┴──┴──┴────┴──┘
```

## Remember

1. Regular icons: **Column × 80px** (N=+0, S=+40)
2. Regular icons: **Row × 30px**
3. Eggs: **Column × 30px, Row × 32px**
4. Custom: **icon_key = icon_number + 1**
5. Always validate before uploading!

---

**Pro Tip:** Keep this file open while working on sprite sheets!

For full details, see: [docs/ICON_SHEET_GUIDE.md](docs/ICON_SHEET_GUIDE.md)
