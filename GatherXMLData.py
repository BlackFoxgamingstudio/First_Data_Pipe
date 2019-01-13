import pandas as pd
import xml.etree.ElementTree as ET

def iter_author(etree):
    for page in etree.iter('page'):
        for row in iter_docs(page):
            yield row

def iter_docs(page):
    page_attr = page.attrib
    for doc in page.iter('document'):
        doc_dict = page_attr.copy()
        doc_dict.update(page.attrib)
        doc_dict['data'] = doc.text
        yield doc_dict

xml_data = open('Learning.xml').read()

etree = ET.parse(xml_data) #create an ElementTree object 
doc_df = pd.DataFrame(list(iter_author(etree)))