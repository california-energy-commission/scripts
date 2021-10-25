"""
Check for mismatched Header
python3 header.py
"""

import glob
import os
import sys

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob(
    '{}/**[!base]/*.xsd'.format(target_folder), recursive=True)  # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

path = glob.glob('{}/base/**esCompliance.xsd'.format(target_folder))[0]
tree = ElementTree.parse(path)
base = tree.getroot()

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        tags = root.findall(
            './/xsd:element[@name="ComplianceDocumentPackage"]/.//xsd:element[@name="DocumentData"]/.//xsd:element[@name="Header"]', namespace)

        for tag in tags:
            type = tag.attrib.get('type')
            name = type.split(':')[1]
            query = base.find(
                './xsd:complexType[@name="{}"]'.format(name), namespace)
            header = None if not query else query.attrib.get('name')

            if not header and header != name:
                has_error = True
                base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
                print("[{}] Cannot resolve the name '{}' to a 'type definition' component\n".format(
                    base_path, type))

    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
