"""
Check for duplicate elements in each schema section
python3 duplicate_elements.py
"""

import glob
import os
import sys

from xml.etree import ElementTree
from collections import Counter

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob('{}/**[!base]/*.xsd'.format(target_folder), recursive=True) # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

'''
Check for duplicate elements on each node tree
'''
def check_duplicates(root, base_path):
    result = list()
    name = ''

    for node in root.iterfind('xsd:complexType/xsd:sequence/xsd:element', namespaces=namespace):
        name = node.attrib.get('name')
        result.append(name)
        check_duplicates(node, base_path)

    duplicates = [x for x, y in Counter(result).items() if y > 1]

    if len(duplicates) > 0:
        has_error = True
        print("[{}] Multiple elements with different types appear in the model group.".format(base_path, name))
        print("Multiple elements are {}.\n".format(duplicates))


for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
        check_duplicates(root, base_path)

    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
