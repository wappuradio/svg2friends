import xml.etree.ElementTree as ET

class BoundingRect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def calculate_bounds(paths):
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')

    for path in paths:
        if 'd' in path.attrib:
            # Basic parsing of path data to find coordinates
            d = path.get('d')
            coords = []
            for cmd in d.split():
                try:
                    x, y = map(float, cmd.split(','))
                    coords.append((x, y))
                except:
                    continue

            if coords:
                path_min_x = min(x for x, y in coords)
                path_min_y = min(y for x, y in coords)
                path_max_x = max(x for x, y in coords)
                path_max_y = max(y for x, y in coords)

                min_x = min(min_x, path_min_x)
                min_y = min(min_y, path_min_y)
                max_x = max(max_x, path_max_x)
                max_y = max(max_y, path_max_y)

    return BoundingRect(min_x, min_y, max_x, max_y)

def extract_paths():
    # Parse the SVG file
    tree = ET.parse('example.svg')
    root = tree.getroot()

    # Dictionary to store fill colors and their class names
    fill_classes = {}
    class_counter = 1

    new_paths = []

    # Find all path elements and copy them
    for old_path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        new_path = ET.Element('path')
        if 'd' in old_path.attrib:
            new_path.set('d', old_path.get('d'))
        if 'fill' in old_path.attrib:
            fill_color = old_path.get('fill')
            if fill_color not in fill_classes:
                class_name = f'f{class_counter}'
                fill_classes[fill_color] = class_name
                class_counter += 1
            new_path.set('className', fill_classes[fill_color])
        new_paths.append(new_path)

    print('colors: [' + ','.join([f'{color}' for color, class_name in fill_classes.items()]) + ']')
    return new_paths


if __name__ == '__main__':
    # Create new root element for output
    new_root = ET.Element('svg')
    new_root.set('xmlns', 'http://www.w3.org/2000/svg')

    paths = extract_paths()
    bounds = calculate_bounds(paths)
    print(f"Bounding rectangle: (x1={bounds.x1}, y1={bounds.y1}, x2={bounds.x2}, y2={bounds.y2})")

    for path in paths:
        new_root.append(path)

    # Create new tree and write to file
    new_tree = ET.ElementTree(new_root)
    ET.indent(new_tree, space='  ')
    new_tree.write('paths_only.svg', encoding='utf-8', xml_declaration=True)