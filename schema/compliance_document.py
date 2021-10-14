"""
Checking for mismatched ComplianceDocument tags
python3 compliance_document.py
"""

import glob
import os
import sys

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob(
    '{}/schema/**[!base]/*.xsd'.format(target_folder), recursive=True)  # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
dtyp = {'dtyp': 'http://www.lmonte.com/besm/dtyp'}

base = ElementTree.parse(
    '{}/schema/base/ResCompliance.xsd'.format(target_folder)).getroot()
tag_dict = {
    'doc': 'ComplianceDocumentTag',
    'docTitle': 'ComplianceDocumentTitleRes',
    'docType': 'ComplianceDocumentType',
    'docVariantSubtitle': 'ComplianceDocumentVariantSubtitle',
    'docVariantLetter': 'ComplianceDocumentVariant'
}

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        for key, value in tag_dict.items():
            tags = root.findall(
                './/xsd:element[@name="ComplianceDocumentPackage"]/xsd:complexType/xsd:attribute[@name="{}"]/[@fixed]'.format(key), namespace)

            for tag in tags:
                tag_value = tag.attrib.get('fixed')
                displayterm = base.find(
                    "./*[@name='ComplianceDocumentTag'].//dtyp:displayterm[@value='{}']".format(tag_value), dtyp)
                enum = base.find(
                    "./*[@name='ComplianceDocumentTag'].//xsd:enumeration[@value='{}']".format(tag_value), namespace)
                enum_value = enum.attrib.get('value')

                if enum_value != tag_value or enum_value != displayterm.text or tag_value != displayterm.text:
                    has_error = True
                    base_path = os.path.join(
                        *(filename.split(os.path.sep)[2:]))
                    print(
                        '{} mismatch for {} and base/ResCompliance.xsd\n'.format(value, base_path))

    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
