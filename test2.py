import pandas as pd
import PyPDF2
import re
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

def pdf_reader(filename):
   pdf_file_obj = open(filename, 'rb')
   pdfReader = PyPDF2.PdfFileReader(pdf_file_obj)
   
   pdf_list = []
   for i in range(pdfReader.numPages):
       page_object = pdfReader.getPage(i)
       page = page_object.extractText()
       text_list = re.split('|', page)
       pdf_list.append(text_list)
   return(pdf_list)



@app.route('/')
def Hell_ya():
    text = pdf_reader("flask.pdf")
    
    df = pd.DataFrame(text)
    
    return render_template("view.html",tables=[df.to_html(classes="df")], titles = ['name'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)