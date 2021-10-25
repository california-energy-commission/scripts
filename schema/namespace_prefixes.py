"""
Check for missing namespaces prefixes
python3 namespace_prefixes.py
"""

import glob
import os
import sys
import re

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
schema_files = glob.glob('{}/**[!base]/*.xsd'.format(target_folder), recursive=True) # exclude base schemas
namespace = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

for filename in schema_files:
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        tags = root.findall('.//*', namespace)

        # Get all namespaces
        namespaces = dict([node for _, node in ElementTree.iterparse(filename,
                                                        events=['start-ns'])])

        tree_string = ElementTree.tostring(root).decode('utf-8')
        regex = re.search('\[d:.*?\]', tree_string)

        in_namespace = 'd' in namespaces.keys() and 'http://www.lmonte.com/besm/d' in namespaces.values()

        if regex and not in_namespace:
            base_path = os.path.join(*(filename.split(os.path.sep)[2:]))
            print("[{}]: Square brackets markup was found but namespace declaration is missing.".format(base_path))
            print('Correct namespace is xmlns:d="http://www.lmonte.com/besm/d"')

    except ElementTree.ParseError as err:
        raise err

if has_error == True:
    sys.exit(1)
