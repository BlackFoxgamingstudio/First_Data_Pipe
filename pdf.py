# extracting_text.py
 
from PyPDF2 import PdfFileReader
 
 
def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
 
        # get the first page
        page = pdf.getPage(66)
        print(page)
        
 
        text = page.extractText()
        print(text)
 
 
if __name__ == '__main__':
    path = 'Flask Web Development_ Developing Web Applications with Python [Grinberg 2014-05-18].pdf'
    text_extractor(path)