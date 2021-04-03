"""
Check for missing xsd:enumeration in xsd:restriction
python3 missing_enumeration.py
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

isRes = glob.glob('{}/schema/base/ResBuilding.xsd'.format(target_folder))
tag = "NrPres" if len(isRes) == 0 else "Res"

dataTypes = ElementTree.parse(
    '{}/schema/base/DataTypes.xsd'.format(target_folder, tag)).getroot()
resBuilding = ElementTree.parse(
    '{}/schema/base/{}Building.xsd'.format(target_folder, tag)).getroot()
resCommon = ElementTree.parse(
    '{}/schema/base/{}Common.xsd'.format(target_folder, tag)).getroot()
resCompliance = ElementTree.parse(
    '{}/schema/base/{}Compliance.xsd'.format(target_folder, tag)).getroot()
resEnvelope = ElementTree.parse(
    '{}/schema/base/{}Envelope.xsd'.format(target_folder, tag)).getroot()
resHvac = ElementTree.parse(
    '{}/schema/base/{}Hvac.xsd'.format(target_folder, tag)).getroot()
resLighting = ElementTree.parse(
    '{}/schema/base/{}Lighting.xsd'.format(target_folder, tag)).getroot()

map = dict({
    'dtyp': {
        'root': ElementTree.parse('{}/schema/base/DataTypes.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/DataTypes.xsd'
    },
    'bld': {
        'root': ElementTree.parse('{}/schema/base/{}Building.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Building.xsd'
    },
    'com': {
        'root': ElementTree.parse('{}/schema/base/{}Common.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Common.xsd'
    },
    'comp': {
        'root': ElementTree.parse('{}/schema/base/{}Compliance.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Compliance.xsd'
    },
    'env': {
        'root': ElementTree.parse('{}/schema/base/{}Envelope.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Envelope.xsd'
    },
    'hvac': {
        'root': ElementTree.parse('{}/schema/base/{}Hvac.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Hvac.xsd'
    },
    'lit': {
        'root': ElementTree.parse('{}/schema/base/{}Lighting.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Lighting.xsd'
    },
})

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        restrictions = root.findall('.//xsd:restriction', namespace)
        base_path = os.path.join(*(filename.split(os.path.sep)[2:]))

        for restriction in restrictions:
            fullBase = restriction.attrib.get('base')
            base, type = fullBase.split(':')
            enumerations = restriction.findall('xsd:enumeration', namespace)

            for enumeration in enumerations:
                value = enumeration.attrib.get('value')

                if base in map.keys():
                    query = map[base].get('root').findall(
                        './/xsd:simpleType[@name="{}"]/.//xsd:enumeration[@value="{}"]'.format(type, value), namespace)

                    if len(query) == 0:
                        basedoc = map[base].get('base_path')
                        print("[{}]: Enumeration value '{}' is not in the value space of the base type '{}' in '{}'.".format(
                            base_path, value, type, basedoc))
                        has_error = True

    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
