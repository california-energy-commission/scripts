"""
Check for missing schema sections.
python3 missing_sections.py
"""

import glob
import os
import sys
import string

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob('{}/**[!base]/*.xsd'.format(target_folder), recursive=True) # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        sections = root.findall('./xsd:complexType/xsd:sequence/xsd:element[@name]', namespace)

        for index, section in enumerate(sections):
            name = section.attrib.get('name')

            # check if any section is missing, e.g. Section_C or Section_3
            # transform ASCII character to number and check if it's equal to loop index
            ascii = ord(name[-1:])
            number = ascii - 65 if ascii > 64 else ascii - 49
            expected = chr(index + 65) if ascii > 64 else number

            if number != index:
                has_error = True
                base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
                print('{} - Expected: Section_{}, instead got: {}\n'.format(base_path, expected, name))
    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
