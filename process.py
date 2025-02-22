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

    from svgpathtools import parse_path

    for path in paths:
        if 'd' in path.attrib:
            # Parse path and get bounding box
            parsed_path = parse_path(path.get('d'))
            bbox = parsed_path.bbox()

            min_x = min(min_x, bbox[0])
            min_y = min(min_y, bbox[2])
            max_x = max(max_x, bbox[1])
            max_y = max(max_y, bbox[3])

    return BoundingRect(min_x, min_y, max_x, max_y)
def extract_paths(input):
    # Parse the SVG file
    tree = ET.parse(input)
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
    input_file = "example.svg"
    output_file = "paths_only.svg"

    paths = extract_paths(input_file)
    bounds = calculate_bounds(paths)

    # Calculate scale factors to fit in 480x150 while preserving aspect ratio
    width = bounds.x2 - bounds.x1
    height = bounds.y2 - bounds.y1
    scale_x = 480 / width
    scale_y = 150 / height
    scale = min(scale_x, scale_y)

    room_x = 480 - width*scale
    room_y = 150 - height*scale

    # Create group element with transform
    group = ET.Element('g')
    group.set('transform', f'translate({-bounds.x1 + room_x / 2},{-bounds.y1 + room_y / 2}) scale({scale})')

    for path in paths:
        group.append(path)

    # Create new tree and write to file
    new_tree = ET.ElementTree(group)
    ET.indent(new_tree, space='  ')
    new_tree.write(output_file, encoding='utf-8', xml_declaration=False)

    print(f"Processed {input_file} into {output_file}")