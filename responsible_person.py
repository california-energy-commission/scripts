"""
Check for existence of responsible person
python3 responsible_person.py
"""

import glob
import os
import sys

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob('{}/schema/**/*.xsd'.format(target_folder), recursive=True)
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

for filename in schema_files:
    try:
        rootTree = ElementTree.parse(filename)
        mainRoot = rootTree.getroot()
        respPersonList = mainRoot.findall('./xsd:element[@name="ComplianceDocumentPackage"]/.//xsd:element[@name="RespPerson"]', namespace)

        for respPerson in respPersonList:
            resCompTree = ElementTree.parse('{}/schema/base/ResCompliance.xsd'.format(target_folder))
            resCompRoot = resCompTree.getroot()

            name = respPerson.attrib.get('type').split(':')[1]
            query = resCompRoot.findall('./xsd:complexType[@name="{}"]'.format(name), namespace)

            if len(query) == 0:
                has_error = True
                base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
                print('{} header {} mismatch with ResCompliance.xsd\n'.format(base_path, name))
    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
