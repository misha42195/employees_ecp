import xml.etree.ElementTree as ET


tree = ET.parse('simple.xml')
root = tree.getroot()

print(root.find('country').find('rank'))

