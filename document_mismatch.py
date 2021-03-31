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
schema_files = glob.glob('{}/schema/**[!base]/*[!CF3RNoTestH].xsd'.format(target_folder), recursive=True) # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        # Get all namespaces
        namespaces = dict([node for _, node in ElementTree.iterparse(filename, events=['start-ns'])])

        target_namespace = root.attrib.get('targetNamespace').rsplit('/', 1)[1]
        compliance = root.find('.//xsd:element[@name="DocID"].//xsd:attribute[@type="comp:ComplianceDocumentTag"]', namespace).attrib.get('fixed')
        required = root.find('./xsd:element/xsd:complexType/xsd:attribute[@type="comp:ComplianceDocumentTag"]', namespace).attrib.get('fixed')
        complex = root.find('xsd:complexType', namespace).attrib.get('name')

        ref = root.find('.//xsd:element[@name="DocumentData"].//xsd:element[@ref]', namespace).attrib.get('ref')

        name = root.find('xsd:element[last()]', namespace).attrib.get('name')
        type = root.find('xsd:element[last()]', namespace).attrib.get('type')

        names = [name.lower() for name in [target_namespace, compliance, required, complex, ref, name, type] if name is not None]

        if len(set(names)) > 1:
            has_error = True
            base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
            print("[{}]: Inconsistent target namespaces found '{}'".format(base_path, names))

    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
