# Background Removal - How It Works

The `prepare_custom_icon.py` script now **automatically detects and removes background colors** from your Pokemon icons!

## What Changed

### Before (Old Behavior)
- ❌ Palette mode (P) images without transparency stayed opaque
- ❌ RGB images had solid backgrounds
- ❌ RGBA images with no transparent pixels stayed opaque
- ⚠️ You had to manually remove backgrounds in an image editor first

### After (New Behavior - Fixed!)
- ✅ Automatically detects background color from corners and edges
- ✅ Removes background with configurable tolerance
- ✅ Works with P, RGB, L, and RGBA modes
- ✅ Converts to RGBA with proper transparency
- ✅ No manual pre-processing needed!

## How It Works

### 1. Background Detection
The script intelligently samples:
- **Corner pixels** (all 4 corners)
- **Edge pixels** (top, bottom, left, right edges)
- Finds the **most common color** among samples
- This is almost always the background color

### 2. Color Removal
- Compares each pixel to detected background color
- Uses **tolerance** (default: 10) to catch similar shades
- Makes matching pixels fully transparent (alpha = 0)
- Keeps sprite pixels fully opaque (alpha = 255)

### 3. Tolerance Explained
```
Tolerance = 10 means:
  If pixel RGB is within ±10 of background RGB, make it transparent

Example:
  Background: RGB(255, 255, 255) - white
  Pixel: RGB(250, 252, 248)
  Difference: (5, 3, 7) - all within 10
  Result: Made transparent ✓
```

## Examples

### Example 1: Palette Mode Image (Your Case!)
```bash
# Input: 1025.png (P mode, white background, no alpha)
python3 tools/prepare_custom_icon.py single 1025.png

# Output:
# ⚠️  Transparency: No alpha channel (will be fixed automatically)
# 🔧 Applying automatic fixes...
#    • Converting P → RGBA
#    • Detected background color: RGB(255, 255, 255)
#    • Made 432 pixels transparent (53.3%)
# ✅ Ready for upload!
```

### Example 2: RGB Image
```bash
# Input: sprite.png (RGB mode, blue background)
python3 tools/prepare_custom_icon.py single sprite.png

# Output:
#    • Detected background color: RGB(135, 206, 250)  # Light blue
#    • Made 2,841 pixels transparent (62.4%)
```

### Example 3: RGBA with Solid Background
```bash
# Input: icon.png (RGBA but no transparent pixels)
python3 tools/prepare_custom_icon.py single icon.png

# Output:
#    • Detecting and removing background from RGBA image
#    • Detected background color: RGB(0, 0, 0)  # Black
#    • Made 1,523 pixels transparent (38.1%)
```

## Configuration

You can adjust the tolerance if needed:

```python
# In the script, modify the config:
config = {
    'target_width': 80,
    'target_height': 60,
    'min_padding': 2,
    'output_format': 'PNG',
    'optimize': True,
    'bg_tolerance': 10  # Adjust this (0-255)
}
```

**Tolerance Guide:**
- `0` = Exact match only (may miss some background)
- `10` = **Default** - Good for most cases
- `20` = More aggressive (may affect sprite edges)
- `30+` = Very aggressive (may affect sprite colors)

## When It Runs

Background removal happens automatically when:
1. ✅ Image has no alpha channel (P, RGB, L modes)
2. ✅ Image is RGBA but has no transparent pixels
3. ✅ Auto-fix is enabled (default)

It does **NOT** run when:
- ❌ Image already has proper transparency
- ❌ Auto-fix is disabled
- ❌ Image is already RGBA with transparent pixels

## Visual Comparison

**Before Fix:**
```
Input: 1025.png (27×30, P mode, white bg)
   ┌──────────────┐
   │░░░░░░░░░░░░░░│  ░ = white background (opaque)
   │░░░██████░░░░░│  █ = sprite pixels
   │░░██░░░░██░░░░│
   │░██░████░░██░░│
   │████████████░░│
   │░░░░░░░░░░░░░░│
   └──────────────┘
Background: Opaque white ❌
```

**After Fix:**
```
Output: 1025_prepared.png (80×60, RGBA, transparent)
   ┌──────────────┐
   │··············│  · = transparent (alpha = 0)
   │····██████····│  █ = sprite pixels (alpha = 255)
   │··██░░░░██····│
   │·██·████··██··│
   │████████████··│
   │··············│
   └──────────────┘
Background: Transparent ✓
```

## Troubleshooting

### Issue: Background not fully removed
**Solution:** Increase tolerance
```python
config['bg_tolerance'] = 20  # From 10 to 20
```

### Issue: Sprite edges look wrong
**Solution:** Decrease tolerance
```python
config['bg_tolerance'] = 5  # From 10 to 5
```

### Issue: Wrong color detected as background
**Reason:** Sprite touches edges or corners
**Solution:**
1. Add padding to source image in editor
2. Or manually set background color in script

### Issue: Sprite color similar to background
**Example:** White Pokemon on white background
**Solution:** Pre-process with different background color first

## Advanced: Manual Background Color

If auto-detection fails, you can specify the background color:

```python
# Edit _apply_fixes method:
bg_color = (255, 255, 255)  # Force white background
# Instead of:
# bg_color = self._detect_background_color(...)
```

## Testing Your Results

After preparing, verify transparency:

```bash
# Check file info
file 1025_prepared.png
# Should show: "PNG image data, ... with alpha channel"

# Or open in image editor and check:
# - GIMP: Should see checkered transparency pattern
# - Photoshop: Should see transparency grid
# - Preview/Mac: Transparent areas show as checkered
```

## Benefits

1. **No Manual Work** - Just run the script!
2. **Batch Processing** - Works on entire directories
3. **Consistent Results** - Same quality every time
4. **Smart Detection** - Handles various background colors
5. **Preserves Quality** - Only removes background, sprite unchanged

## Summary

The script now handles **everything** for you:
- ✅ Detects background color automatically
- ✅ Removes it with smart tolerance
- ✅ Converts to proper RGBA
- ✅ Resizes and centers
- ✅ Optimizes file size
- ✅ Ready for Roblox!

**Just run it and upload!** 🚀

---

**Try it now:**
```bash
python3 tools/prepare_custom_icon.py single 1025.png
# Check the output - should have proper transparency!
```
