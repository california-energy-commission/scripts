"""
Format, lint and process schema files
python3 deploy-schema.py -s <source_folder> -d <destination_folder>
"""

import glob
import os
import sys
import argparse
import subprocess

from xml.etree import ElementTree

text = 'This tool is used to format, lint and process schema files.'

parser = argparse.ArgumentParser(description=text, allow_abbrev=True)
parser.add_argument("-s", "--source", type=str, help="Set source schema file", required=True)
parser.add_argument("-d", "--destination", type=str, help="Set deployed schema file", required=True)

args = parser.parse_args()

print("Source schema file set to %s" % os.path.abspath(args.source))
print("Deployed schema file set to %s" % os.path.abspath(args.destination))

has_error = False
target_folder = args.source
schema_files = glob.glob('{}/**/*.xsd'.format(target_folder), recursive=True) 
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
dtyp = {'dtyp': 'http://www.lmonte.com/besm/dtyp'}

for baseName in glob.glob('{}/base/*Compliance.xsd'.format(target_folder)):
  base = ElementTree.parse(baseName).getroot()

tag_dict = {
  'doc': 'ComplianceDocumentTag',
  'docTitle': 'ComplianceDocumentTitleRes',
  'docType': 'ComplianceDocumentType',
  'docVariantSubtitle': 'ComplianceDocumentVariantSubtitle',
  'docVariantLetter': 'ComplianceDocumentVariant'
}

# List all files changed in the current PR
# git ls-files -dmo
stdout = subprocess.run(["git", "ls-files", "-dmo", "--full-name"], check=True, capture_output=True, text=True).stdout
print(stdout)

for filename in schema_files:
  try:
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    # elements = root.findall('.//xsd:annotation/..', namespace)
    # base_path = os.path.join(*(filename.split(os.path.sep)[2:]))

    # for element in elements:
    #   name = element.attrib.get('name')
    #   documentation = element.find('xsd:annotation/xsd:documentation', namespace)

    #   if documentation.findall('.//d:l/d:l', { 'd': 'http://www.lmonte.com/besm/d' }):
    #     has_error = True
    #     base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
    #     print('List inside list found in {} in embedded markup in element {}\n'.format(base_path, name))

  except ElementTree.ParseError as err:
    raise err

if has_error == True:
  sys.exit(1)