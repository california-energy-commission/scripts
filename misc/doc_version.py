"""
Generate document versions
python3 doc_version.py
"""

import glob
import os
import sys
import csv

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob('{}/schema/**[!base]/*.xsd'.format(target_folder), recursive=True) # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
stats = list()

def get_attrib(doc):
    return doc.attrib.get('fixed') if doc is not None else "N/A"

for filename in schema_files:
    base_path = os.path.join(*(filename.split(os.path.sep)[2:]))

    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        version = root.find('[@version]', namespace)
        version = root.attrib.get('version')

        doc = root.find('.//xsd:element[@name="ComplianceDocumentPackage"].//xsd:attribute[@name="doc"]', namespace)
        doc_type = root.find('.//xsd:element[@name="ComplianceDocumentPackage"].//xsd:attribute[@name="docType"]', namespace)
        doc_title = root.find('.//xsd:element[@name="ComplianceDocumentPackage"].//xsd:attribute[@name="docTitle"]', namespace)
        doc_variant_subtitle = root.find('.//xsd:element[@name="ComplianceDocumentPackage"].//xsd:attribute[@name="docVariantSubtitle"]', namespace)
        doc_variant_letter = root.find('.//xsd:element[@name="ComplianceDocumentPackage"].//xsd:attribute[@name="docVariantLetter"]', namespace)

        doc = get_attrib(doc)
        doc_type = get_attrib(doc_type)
        doc_title = get_attrib(doc_title)
        doc_variant_subtitle = get_attrib(doc_variant_subtitle)
        doc_variant_letter = get_attrib(doc_variant_letter)

        revision = root.find('.//xsd:element[@name="ComplianceDocumentPackage"].//xsd:attribute[@name]', namespace)
        revision = revision.attrib.get('fixed')

        stats.append({
            'File Path': base_path,
            'Version': version,
            'Revision': revision,
            'doc': doc,
            'docType': doc_type,
            'docTitle': doc_title,
            'docVariantSubtitle': doc_variant_subtitle,
            'docVariantLetter': doc_variant_letter
        })

    except ElementTree.ParseError as err:
        raise err

fieldnames = list(['File Path', 'Version', 'Revision', 'doc', 'docType', 'docTitle', 'docVariantSubtitle', 'docVariantLetter'])

with open('doc_version.csv', 'w+', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in stats:
        writer.writerow(row)

if has_error == True:
    sys.exit(1)
