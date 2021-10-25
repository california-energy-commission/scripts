"""
Check for missing base elements
python3 empty_sections.py
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

isRes = glob.glob('{}/base/ResCompliance.xsd'.format(target_folder))
tag = "NrPres" if len(isRes) == 0 else "Res"

map = dict({
    'dtyp': {
        'root': ElementTree.parse('{}/base/DataTypes.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/DataTypes.xsd'
    },
    'bld': {
        'root': ElementTree.parse('{}/base/{}Building.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Building.xsd'
    },
    'com': {
        'root': ElementTree.parse('{}/base/{}Common.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Common.xsd'
    },
    'comp': {
        'root': ElementTree.parse('{}/base/{}Compliance.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Compliance.xsd'
    },
    'env': {
        'root': ElementTree.parse('{}/base/{}Envelope.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Envelope.xsd'
    },
    'hvac': {
        'root': ElementTree.parse('{}/base/{}Hvac.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Hvac.xsd'
    },
    'lit': {
        'root': ElementTree.parse('{}/base/{}Lighting.xsd'.format(target_folder, tag)).getroot(),
        'path': 'base/{}Lighting.xsd'
    },
})


for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        tags = root.findall('.//*[@type]', namespace)

        for tag in tags:
            type = tag.attrib.get('type')
            base, name = type.split(':')

            if base in map.keys():
                query = map[base].get('root').findall(
                    './/*[@name="{}"]'.format(name), namespace)

                if len(query) == 0:
                    has_error = True
                    base_path = os.path.join(
                        *(filename.split(os.path.sep)[2:]))
                    basedoc = map[base].get('path')
                    print("[{}]: Element type '{}' does not exist in '{}'".format(
                        base_path, type, basedoc))
    except ElementTree.ParseError as err:
        raise err
    except ValueError:
        # type value from tag does not have a base type, e.g. comp:NotApplicableMessage
        continue

if has_error == True:
    sys.exit(1)
