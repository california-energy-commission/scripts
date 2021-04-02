"""
Check if stylesheet is well formed
python3 lint_stylesheet.py
"""

import glob
import os
import sys

from xml.etree import ElementTree

has_error = False
target_folder = sys.argv[1]
stylesheet_files = glob.glob(
    '{}/stylesheet/**/*.xsl'.format(target_folder), recursive=True)

for filename in stylesheet_files:
    try:
        stylsheeet = ElementTree.parse(filename)
    except ElementTree.ParseError:
        has_error = True
        print('{} is not a valid XSL document!\n'.format(
            os.path.basename(filename)))
        pass

if has_error == True:
    sys.exit(1)
