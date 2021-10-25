import lxml.etree as ET
import sys

xsl_filename = sys.argv[1]
xml_filename = sys.argv[2]

dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)

try:
  ET.tostring(newdom, pretty_print=True)
except:
  print("XSLT transformation has failed.")
  exit(1)