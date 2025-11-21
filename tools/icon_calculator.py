#!/usr/bin/env python3
"""
Pokemon Icon Position Calculator

Calculates the exact position and sprite sheet for any icon number.
"""

def calculate_regular_icon(icon_number):
    """Calculate position for regular Pokemon icons (0-1450)"""
    column = icon_number % 21
    row = icon_number // 21

    # Determine which sprite sheet
    image_index = 1
    adjusted_column = column
    adjusted_row = row

    if column > 10:
        image_index += 1
        adjusted_column = column - 11

    if row > 24:
        image_index += 2
        adjusted_row = row - 25

    if adjusted_row > 32:
        image_index += 2
        adjusted_row = adjusted_row - 33

    # Calculate pixel positions
    x_normal = column * 80
    x_shiny = column * 80 + 40
    y = row * 30

    sprite_sheets = {
        1: '17134745575',
        2: '17134749969',
        3: '17134753859',
        4: '17134757872',
        5: '17134761227',
        6: '0'
    }

    return {
        'type': 'regular',
        'column': column,
        'row': row,
        'sheet_index': image_index,
        'sheet_asset_id': sprite_sheets.get(image_index, 'Unknown'),
        'x_normal': x_normal,
        'x_shiny': x_shiny,
        'y': y,
        'adjusted_column': adjusted_column,
        'adjusted_row': adjusted_row
    }

def calculate_egg_icon(icon_number):
    """Calculate position for egg icons (1451+)"""
    # Determine egg sprite index
    if icon_number > 1872:
        egg_index = icon_number - 1442
    else:
        egg_index = icon_number - 1451

    column = egg_index % 18
    row = egg_index // 18

    x = column * 30
    y = row * 32

    return {
        'type': 'egg',
        'egg_index': egg_index,
        'column': column,
        'row': row,
        'sheet_asset_id': '13039987315',
        'x': x,
        'y': y,
        'sprite_size': (30, 32)
    }

def calculate_position(icon_number):
    """Main function to calculate icon position"""
    if icon_number <= 1450:
        return calculate_regular_icon(icon_number)
    else:
        return calculate_egg_icon(icon_number)

def print_icon_info(icon_number, pokemon_name=None):
    """Print formatted information about an icon"""
    info = calculate_position(icon_number)

    print("=" * 60)
    if pokemon_name:
        print(f"Pokemon: {pokemon_name}")
    print(f"Icon Number: {icon_number}")
    print("=" * 60)

    if info['type'] == 'regular':
        print(f"Type: Regular Pokemon Icon")
        print(f"\nGrid Position:")
        print(f"  Column: {info['column']} (of 0-20)")
        print(f"  Row: {info['row']}")
        print(f"\nSprite Sheet:")
        print(f"  Sheet Index: {info['sheet_index']}")
        print(f"  Asset ID: rbxassetid://{info['sheet_asset_id']}")
        print(f"  Sheet Column: {info['adjusted_column']}")
        print(f"  Sheet Row: {info['adjusted_row']}")
        print(f"\nPixel Coordinates:")
        print(f"  Normal Sprite: ({info['x_normal']}px, {info['y']}px)")
        print(f"  Shiny Sprite: ({info['x_shiny']}px, {info['y']}px)")
        print(f"  Size: 40px × 30px")
        print(f"\nAseprite/GIMP Instructions:")
        print(f"  1. Open sprite sheet {info['sheet_index']}")
        print(f"  2. Navigate to position ({info['x_normal']}, {info['y']})")
        print(f"  3. Place NORMAL sprite at X={info['x_normal']}")
        print(f"  4. Place SHINY sprite at X={info['x_shiny']}")

    else:  # egg
        print(f"Type: Egg Icon")
        print(f"\nGrid Position:")
        print(f"  Egg Index: {info['egg_index']}")
        print(f"  Column: {info['column']} (of 0-17)")
        print(f"  Row: {info['row']}")
        print(f"\nSprite Sheet:")
        print(f"  Asset ID: rbxassetid://{info['sheet_asset_id']}")
        print(f"\nPixel Coordinates:")
        print(f"  Position: ({info['x']}px, {info['y']}px)")
        print(f"  Size: {info['sprite_size'][0]}px × {info['sprite_size'][1]}px")

    print("=" * 60)

def find_empty_slots(start=0, end=1450):
    """Find gaps in icon numbering (useful for adding new Pokemon)"""
    # This would need to be updated with actual used slots
    print(f"Scanning icon slots {start} to {end}...")
    print("Note: This shows calculated positions, not actual usage.")
    print("Check your sprite sheets to see which slots are actually empty.")

def batch_calculate(icon_list):
    """Calculate positions for multiple icons"""
    results = []
    for item in icon_list:
        if isinstance(item, tuple):
            icon_num, name = item
        else:
            icon_num = item
            name = f"Pokemon {icon_num}"

        info = calculate_position(icon_num)
        info['icon_number'] = icon_num
        info['name'] = name
        results.append(info)

    return results

def export_to_csv(results, filename='icon_positions.csv'):
    """Export results to CSV for use in spreadsheets"""
    import csv

    with open(filename, 'w', newline='') as f:
        if not results:
            return

        if results[0]['type'] == 'regular':
            fieldnames = ['icon_number', 'name', 'column', 'row', 'sheet_index',
                         'sheet_asset_id', 'x_normal', 'x_shiny', 'y']
        else:
            fieldnames = ['icon_number', 'name', 'egg_index', 'column', 'row',
                         'sheet_asset_id', 'x', 'y']

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Exported {len(results)} entries to {filename}")

# Interactive mode
if __name__ == "__main__":
    import sys

    print("Pokemon Icon Position Calculator")
    print("-" * 60)

    if len(sys.argv) > 1:
        # Command line mode
        icon_num = int(sys.argv[1])
        name = sys.argv[2] if len(sys.argv) > 2 else None
        print_icon_info(icon_num, name)
    else:
        # Interactive mode
        print("\nCommands:")
        print("  [number] - Calculate position for icon number")
        print("  [number] [name] - Calculate with Pokemon name")
        print("  batch - Calculate multiple icons")
        print("  range [start] [end] - Calculate range of icons")
        print("  quit - Exit")
        print()

        while True:
            try:
                cmd = input("Enter command: ").strip()

                if cmd.lower() in ['quit', 'exit', 'q']:
                    break

                elif cmd.lower() == 'batch':
                    print("Enter icon numbers (comma separated):")
                    nums = input().strip().split(',')
                    results = []
                    for num in nums:
                        num = num.strip()
                        if num:
                            icon_num = int(num)
                            print()
                            print_icon_info(icon_num)
                            results.append(calculate_position(icon_num))

                    export = input("\nExport to CSV? (y/n): ").strip().lower()
                    if export == 'y':
                        export_to_csv(results)

                elif cmd.lower().startswith('range'):
                    parts = cmd.split()
                    if len(parts) == 3:
                        start = int(parts[1])
                        end = int(parts[2])
                        results = batch_calculate(range(start, end + 1))

                        print(f"\nCalculated {len(results)} positions")
                        export = input("Export to CSV? (y/n): ").strip().lower()
                        if export == 'y':
                            export_to_csv(results)
                    else:
                        print("Usage: range [start] [end]")

                else:
                    parts = cmd.split(maxsplit=1)
                    icon_num = int(parts[0])
                    name = parts[1] if len(parts) > 1 else None
                    print()
                    print_icon_info(icon_num, name)
                    print()

            except ValueError as e:
                print(f"Error: Invalid number - {e}")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

# Example usage in code:
"""
# Single icon
info = calculate_position(151)
print(f"Mew is at position ({info['x_normal']}, {info['y']})")

# Batch processing
pokemon_list = [
    (1, "Bulbasaur"),
    (25, "Pikachu"),
    (151, "Mew"),
]
results = batch_calculate(pokemon_list)
export_to_csv(results, "my_pokemon.csv")
"""
