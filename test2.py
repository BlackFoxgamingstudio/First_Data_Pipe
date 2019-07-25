import pandas as pd
import PyPDF2
import re
from flask import Flask
from flask import request
from flask import render_template
import argparse
import datetime
import pprint
# [START storage_upload_file]
from google.cloud import storage

# [END storage_upload_file]

app = Flask(__name__)


def get_bucket_labels(bucket_name):
    """Prints out a bucket's labels."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    labels = bucket.labels
    pprint.pprint(labels)

def add_bucket_label(bucket_name):
    """Add a label to a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    labels = bucket.labels
    labels['example'] = 'label'
    bucket.labels = labels
    bucket.patch()

    print('Updated labels on {}.'.format(bucket.name))
    pprint.pprint(bucket.labels)

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


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

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()
    lists = []
    for blob in blobs:
        lists.append(blob)
    return lists

@app.route('/')
def index():
    # add_bucket_label("oneforallstorage")
    list_blobs("parsher")
    get_bucket_labels("parsher")
    hi = list_blobs("parsher")
    bucket = 'parsher'
    file = 'api2.pdf'
    gcs_url = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':bucket, 'file':file}
    print gcs_url
    return render_template("index.html",gcs_url=gcs_url, hi=hi)

@app.route('/<book>/<keyword>')
def Hell_ya(keyword, book): 
   
    download_blob("parsher", book, "api.pdf")
    text = pdf_reader("api.pdf")
    text = {'Pages': text}
    df = pd.DataFrame(text)
    keyword = keyword
    chap1 = df[:4]
    chap2  = df[4:8]
    df1 = df.set_index('Pages').filter(like='Table of Content', axis=0)
   
    df2 = df.set_index('Pages').filter(like=keyword, axis=0)
 
    return render_template("view.html",keyword = keyword,table4=[df1.to_html(classes="df")],table2=[df2.to_html(classes="df")],table3=[chap2.to_html(classes="df")],tables=[df.to_html(classes="df")], titles = ['name'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)