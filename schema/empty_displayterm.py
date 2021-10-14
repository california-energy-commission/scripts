"""
Check for empty displayterm tags
python3 empty_displayterm.py
"""

import glob
import os
import sys
from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob('{}/schema/**/*.xsd'.format(target_folder), recursive=True)
namespace = {'dtyp': 'http://www.lmonte.com/besm/dtyp'}

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        tags = root.findall('.//dtyp:displayterm', namespace)
        map = dict()

        for tag in tags:
            if tag.text is None or tag.text.isspace():
                has_error = True
                base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
                print('[{}]: {} displayterm value is empty'.format(base_path, tag.attrib.get('value')))

    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
