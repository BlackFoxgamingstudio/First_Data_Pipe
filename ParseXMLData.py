
import xml.etree.ElementTree as ET
import pandas as pd

def parse_root(root):
    for child in root.getchildren():
    # print(child)
    # passed test 1 block 1
        return parse_element(child) 

def parse_element(element, parsed=None):
    if parsed is None:
        parsed = dict()
    # print(element.keys())
    # passed test 2 block 2
    for key in element.keys():
        if key not in parsed:
            parsed[key] = element.attrib.get(key)
         # print(parsed[key])
         # passed test 3 block 3
        if element.text:
            parsed[element.tag] = element.text
    for child in list(element):
        parse_element(child, parsed)
    return parsed
def process_data(root):
        """ Initiate the root XML, parse it, and return a dataframe"""
        structure_data = parse_root(root)
         # print(structure_data)
         # passed test 4 block 4
        all = []
        for data in structure_data:
            all.append(data)    
            
        return pd.DataFrame(structure_data)
xml_data = open('Learning.xml').read()
root = ET.XML(xml_data)
parsed_df = process_data(root)
print(parsed_df)