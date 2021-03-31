"""
Check for missing base elements
python3 empty_sections.py
"""

import glob
import os
import sys

from xml.etree import ElementTree

has_error = False
schema_files = glob.glob('../schema/**[!base]/*.xsd', recursive=True) # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

map = dict({
    'dtyp': {
        'root': ElementTree.parse('../schema/base/DataTypes.xsd').getroot(),
        'path': 'base/DataTypes.xsd'
    },
    'bld': {
        'root': ElementTree.parse('../schema/base/ResBuilding.xsd').getroot(),
        'path': 'base/ResBuilding.xsd'
    },
    'com': {
        'root': ElementTree.parse('../schema/base/ResCommon.xsd').getroot(),
        'path': 'base/ResCommon.xsd'
    },
    'comp': {
        'root': ElementTree.parse('../schema/base/ResCompliance.xsd').getroot(),
        'path': 'base/ResCompliance.xsd'
    },
    'env': {
        'root': ElementTree.parse('../schema/base/ResEnvelope.xsd').getroot(),
        'path': 'base/ResEnvelope.xsd'
    },
    'hvac': {
        'root': ElementTree.parse('../schema/base/ResHvac.xsd').getroot(),
        'path': 'base/ResHvac.xsd'
    },
    'lit': {
        'root': ElementTree.parse('../schema/base/ResLighting.xsd').getroot(),
        'path': 'base/ResLighting.xsd'
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
                query = map[base].get('root').findall('.//*[@name="{}"]'.format(name), namespace)

                if len(query) == 0:
                    has_error = True
                    base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
                    basedoc = map[base].get('path')
                    print("[{}]: Element type '{}' does not exist in '{}'".format(base_path, type, basedoc))
    except ElementTree.ParseError as err:
        raise err
    except ValueError:
        # type value from tag does not have a base type, e.g. comp:NotApplicableMessage
        continue

if has_error == True:
    sys.exit(1)
