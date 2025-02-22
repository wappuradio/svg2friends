import xml.etree.ElementTree as ET

def extract_paths():
    # Parse the SVG file
    tree = ET.parse('example.svg')
    root = tree.getroot()

    # Create new root element for output
    new_root = ET.Element('svg')
    new_root.set('xmlns', 'http://www.w3.org/2000/svg')

    # Dictionary to store fill colors and their class names
    fill_classes = {}
    class_counter = 1

    # Find all path elements and copy them
    for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        new_path = ET.Element('path')
        if 'd' in path.attrib:
            new_path.set('d', path.get('d'))
        if 'fill' in path.attrib:
            fill_color = path.get('fill')
            if fill_color not in fill_classes:
                class_name = f'f{class_counter}'
                fill_classes[fill_color] = class_name
                class_counter += 1
            new_path.set('className', fill_classes[fill_color])
        new_root.append(new_path)

    print('colors: [' + ','.join([f'{color}' for color, class_name in fill_classes.items()]) + ']')

    # Create new tree and write to file
    new_tree = ET.ElementTree(new_root)
    ET.indent(new_tree, space='  ')
    new_tree.write('paths_only.svg', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    extract_paths()