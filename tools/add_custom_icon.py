#!/usr/bin/env python3
"""
Add Custom Icon Helper

Helps add new custom Pokemon icons to Pokemon.lua
"""

import re
import sys
from pathlib import Path

def find_pokemon_lua():
    """Find Pokemon.lua file"""
    possible_paths = [
        Path("Pokemon.lua"),
        Path("../Pokemon.lua"),
        Path("../gfcx/Pokemon.lua"),
        Path(__file__).parent.parent / "Pokemon.lua"
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None

def parse_existing_icons(content):
    """Parse existing custom icons from file"""
    # Find customNormalIcons table
    normal_pattern = r'local customNormalIcons = \{(.*?)\}'
    shiny_pattern = r'local customShinyIcons = \{(.*?)\}'

    normal_match = re.search(normal_pattern, content, re.DOTALL)
    shiny_match = re.search(shiny_pattern, content, re.DOTALL)

    normal_icons = {}
    shiny_icons = {}

    if normal_match:
        entries = re.findall(r'\[(\d+)\]\s*=\s*[\'"]([^\'"]+)[\'"].*?--(.*)', normal_match.group(1))
        for key, asset_id, comment in entries:
            normal_icons[int(key)] = (asset_id, comment.strip())

    if shiny_match:
        entries = re.findall(r'\[(\d+)\]\s*=\s*[\'"]([^\'"]+)[\'"].*?--(.*)', shiny_match.group(1))
        for key, asset_id, comment in entries:
            shiny_icons[int(key)] = (asset_id, comment.strip())

    return normal_icons, shiny_icons

def find_next_available_slot(normal_icons, preferred_start=1186):
    """Find next available icon slot"""
    used_slots = sorted(normal_icons.keys())

    # Check from preferred start
    slot = preferred_start
    while slot in used_slots:
        slot += 1

    return slot

def format_icon_entry(key, asset_id, comment):
    """Format a single icon entry"""
    return f"\t\t\t[{key}] = 'rbxassetid://{asset_id}', --{comment}"

def add_custom_icon(lua_path, icon_key, normal_asset_id, shiny_asset_id, pokemon_name):
    """Add a custom icon to Pokemon.lua"""

    # Read current file
    with open(lua_path, 'r') as f:
        content = f.read()

    # Parse existing icons
    normal_icons, shiny_icons = parse_existing_icons(content)

    # Check if slot is already used
    if icon_key in normal_icons:
        print(f"Warning: Slot {icon_key} is already used for: {normal_icons[icon_key][1]}")
        response = input("Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return False

    # Add new entries
    new_normal_entry = format_icon_entry(icon_key, normal_asset_id, pokemon_name)
    new_shiny_entry = format_icon_entry(icon_key, shiny_asset_id, pokemon_name) if shiny_asset_id else None

    # Find insertion point (before closing brace of customNormalIcons)
    normal_pattern = r'(local customNormalIcons = \{.*?)(\n\s*\})'
    shiny_pattern = r'(local customShinyIcons = \{.*?)(\n\s*\})'

    # Insert normal icon
    def insert_normal(match):
        return f"{match.group(1)}\n{new_normal_entry}{match.group(2)}"

    content = re.sub(normal_pattern, insert_normal, content, count=1, flags=re.DOTALL)

    # Insert shiny icon if provided
    if new_shiny_entry:
        def insert_shiny(match):
            return f"{match.group(1)}\n{new_shiny_entry}{match.group(2)}"

        content = re.sub(shiny_pattern, insert_shiny, content, count=1, flags=re.DOTALL)

    # Write back
    with open(lua_path, 'w') as f:
        f.write(content)

    print(f"\n✅ Successfully added {pokemon_name} to Pokemon.lua")
    print(f"   Icon key: {icon_key}")
    print(f"   Use in game: Pokemon:getIcon({icon_key - 1}, shiny)")
    print(f"   Normal asset: rbxassetid://{normal_asset_id}")
    if shiny_asset_id:
        print(f"   Shiny asset: rbxassetid://{shiny_asset_id}")

    return True

def list_custom_icons(lua_path):
    """List all custom icons"""
    with open(lua_path, 'r') as f:
        content = f.read()

    normal_icons, shiny_icons = parse_existing_icons(content)

    print("\nCurrent Custom Icons:")
    print("=" * 80)
    print(f"{'Key':<6} {'Icon #':<8} {'Pokemon':<25} {'Has Shiny':<10} {'Asset ID'}")
    print("-" * 80)

    for key in sorted(normal_icons.keys()):
        icon_num = key - 1
        asset_id, name = normal_icons[key]
        has_shiny = "Yes" if key in shiny_icons else "No"
        print(f"{key:<6} {icon_num:<8} {name:<25} {has_shiny:<10} {asset_id}")

    print("-" * 80)
    print(f"Total: {len(normal_icons)} custom icons")

    # Find gaps
    all_keys = sorted(normal_icons.keys())
    gaps = []
    for i in range(len(all_keys) - 1):
        if all_keys[i+1] - all_keys[i] > 1:
            gaps.append((all_keys[i] + 1, all_keys[i+1] - 1))

    if gaps:
        print(f"\nAvailable slots (gaps): ", end="")
        print(", ".join([f"{start}-{end}" if start != end else str(start) for start, end in gaps]))

    next_slot = find_next_available_slot(normal_icons)
    print(f"Next sequential slot: {next_slot}")

def interactive_add():
    """Interactive mode for adding icons"""
    lua_path = find_pokemon_lua()
    if not lua_path:
        print("Error: Could not find Pokemon.lua")
        print("Please run this script from the project root or tools directory")
        return

    print(f"Found Pokemon.lua at: {lua_path}")
    print()

    # Get existing icons
    with open(lua_path, 'r') as f:
        content = f.read()
    normal_icons, shiny_icons = parse_existing_icons(content)

    # Suggest next slot
    next_slot = find_next_available_slot(normal_icons)
    print(f"Next available slot: {next_slot}")
    print()

    # Get input
    pokemon_name = input("Pokemon name: ").strip()
    if not pokemon_name:
        print("Cancelled.")
        return

    icon_key_input = input(f"Icon key (press Enter for {next_slot}): ").strip()
    icon_key = int(icon_key_input) if icon_key_input else next_slot

    normal_asset_id = input("Normal asset ID (numbers only): ").strip()
    if not normal_asset_id:
        print("Error: Normal asset ID is required")
        return

    has_shiny = input("Has shiny variant? (y/n): ").strip().lower()
    shiny_asset_id = None
    if has_shiny == 'y':
        shiny_asset_id = input("Shiny asset ID (numbers only): ").strip()

    # Confirm
    print("\nPreview:")
    print(f"  {pokemon_name}")
    print(f"  Key: {icon_key} (use as icon #{icon_key - 1} in game)")
    print(f"  Normal: rbxassetid://{normal_asset_id}")
    if shiny_asset_id:
        print(f"  Shiny: rbxassetid://{shiny_asset_id}")
    print()

    confirm = input("Add this icon? (y/n): ").strip().lower()
    if confirm == 'y':
        add_custom_icon(lua_path, icon_key, normal_asset_id, shiny_asset_id, pokemon_name)
    else:
        print("Cancelled.")

def main():
    if len(sys.argv) < 2:
        print("Pokemon Custom Icon Helper")
        print("-" * 60)
        print("\nUsage:")
        print("  python add_custom_icon.py list")
        print("  python add_custom_icon.py add")
        print("  python add_custom_icon.py add <key> <normal_id> [shiny_id] <name>")
        print("\nExamples:")
        print("  python add_custom_icon.py list")
        print("  python add_custom_icon.py add")
        print("  python add_custom_icon.py add 1186 12345678 12345679 Celebi")
        print("  python add_custom_icon.py add 1186 12345678 '' Celebi  # No shiny")
        sys.exit(1)

    command = sys.argv[1].lower()
    lua_path = find_pokemon_lua()

    if not lua_path:
        print("Error: Could not find Pokemon.lua")
        sys.exit(1)

    if command == 'list':
        list_custom_icons(lua_path)

    elif command == 'add':
        if len(sys.argv) == 2:
            # Interactive mode
            interactive_add()
        elif len(sys.argv) >= 5:
            # Command line mode
            icon_key = int(sys.argv[2])
            normal_asset_id = sys.argv[3]
            shiny_asset_id = sys.argv[4] if len(sys.argv) > 5 and sys.argv[4] else None
            pokemon_name = sys.argv[5] if len(sys.argv) > 5 else sys.argv[4]

            add_custom_icon(lua_path, icon_key, normal_asset_id, shiny_asset_id, pokemon_name)
        else:
            print("Error: Invalid arguments for add command")
            print("Usage: python add_custom_icon.py add <key> <normal_id> [shiny_id] <name>")
            sys.exit(1)

    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
