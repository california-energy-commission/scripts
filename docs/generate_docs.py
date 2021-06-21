"""
Generate documentation for schema and stylesheet
python3 generate_docs.py "/opt/Oxygen XML Editor 22"
"""

import glob
import sys
import os
from multiprocessing import Pool

print("Script file for generating XML Schema documentation for all HERS Documents files\n")

oxygen_home = sys.argv[1]

# If OXYGEN_HOME is not supplied
if not oxygen_home:
  print("No arguments supplied.")
  print("You have to pass your Oxygen XML installation folder as the first argument.")
  sys.exit(1)

# Try to open Oxygen schemaDocumentation.sh script
script_path = "{}/schemaDocumentation.sh".format(oxygen_home)

try:
    _ = open(script_path)
except IOError:
    print("Cannot generate documentation because of one of the following reasons:")
    print("1. File {} does not exist".format(script_path))
    print("2. Path {} is not your Oxygen XML installation folder".format(oxygen_home))
    sys.exit(1)

# Generate documentation for each file given
def schema_documentation(document):
    oxygen_home = sys.argv[1]
    script_path = "{}/schemaDocumentation.sh".format(oxygen_home)
    os.system("sh '{}' {} -cfg:xsd-settings.xml".format(script_path, document))

def stylesheet_documentation(document):
    oxygen_home = sys.argv[1]
    script_path = "{}/stylesheetDocumentation.sh".format(oxygen_home)
    os.system("sh '{}' {} -cfg:xslt-settings.xml".format(script_path, document))

# Run for all documents
schemas = [schema for schema in glob.glob('../schema/**/*.xsd', recursive=True)]
stylesheets = [stylesheet for stylesheet in glob.glob('../stylesheet/**/*.xsl', recursive=True)]

print("Generating schema documentation...")
pool = Pool(processes=3)
pool.map(schema_documentation, schemas)

print("Generating stylesheet documentation...")
pool = Pool(processes=3)
pool.map(stylesheet_documentation, stylesheets)
