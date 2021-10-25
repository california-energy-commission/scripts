"""
Check for empty schema sections.
python3 empty_sections.py
"""

import glob
import os
import sys

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob('{}/**[!base]/*.xsd'.format(target_folder), recursive=True) # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        sections = root.findall('./xsd:complexType/xsd:sequence/xsd:element', namespace)

        for section in sections:
            name = section.attrib.get('name')
            query = section.find('./xsd:complexType/xsd:sequence', namespace)

            if query:
                _, _, type = query.tag.rpartition('}')

                if type == 'element':
                    has_error = True
                    base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
                    print('{} has an empty section: {}\n'.format(base_path, name))
    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
