"""
Check for incorrect end note naming
python3 end_notes.py
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
            section_name = section.attrib.get('name')
            section_letter = section_name.split('_')[1]
            last_element = section.find('./xsd:complexType/.//xsd:sequence/*[last()]', namespace)
            _, _, type = last_element.tag.rpartition('}')

            if type == 'element':
                elem_name = last_element.attrib.get('name')

                if len(last_element) > 0 and 'endnote' in elem_name.lower() and elem_name[:1] != section_letter:
                    has_error = True
                    base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
                    print('[{}]: {} end note name mismatch in {}\n'.format(base_path, section_name, elem_name))
    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
