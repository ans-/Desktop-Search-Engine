import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from subprocess import check_output
from docx import *
from dounicode import decode_heuristically
from whoosh.analysis import *


filename = ['doc','ppt','pdf','txt','docx','csv','odt','odp','py','rb','java','c','h','html','htm']

def make_index(indexdirname, analyzername):
    if not os.path.exists(indexdirname):
        return False

    if analyzername == 'Stemming':
        analyzer_method = StemmingAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer = analyzer_method))
    elif analyzername == '4-gram':
        analyzer_method = NgramAnalyzer(4)
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(spelling = True, stored=True, analyzer = analyzer_method))
    else:
        analyzer_method = StandardAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(spelling = True, stored=True, analyzer = analyzer_method))

    homename = os.environ['HOME']
    if not os.path.exists(homename + "/indexdir"):
        os.mkdir( homename +"/indexdir")
    ix = create_in( homename + "/indexdir", schema)
    writer = ix.writer()

    rootdir = indexdirname
    for root, dirs, files in os.walk(rootdir):

        for f in files:
            if len(f.split('.')) > 1 and f.split('.')[-1] in filename:
                if f.split('.')[-1] == 'doc':
                    ff = f[:f.rfind('.')]
                    doc = check_output(['catdoc']+ [os.path.join(root,f)])
                    writer.add_document(title= unicode(ff), path= unicode(os.path.join(root,f)), content= unicode(decode_heuristically(doc)[0]))
                elif f.split('.')[-1] == 'pdf':
                    ff = f[:f.rfind('.')]
                    doc = check_output(['pdf2txt.py'] + [os.path.join(root,f)])
                    writer.add_document(title= unicode(ff), path= unicode(os.path.join(root,f)), content= unicode(decode_heuristically(doc)[0]))
                elif f.split('.')[-1] == 'ppt':
                    ff = f[:f.rfind('.')]
                    doc = check_output(['catppt']+ [os.path.join(root,f)])
                    doc = ''
                    writer.add_document(title= unicode(ff), path= unicode(os.path.join(root,f)), content= unicode(decode_heuristically(doc)[0]))
                elif f.split('.')[-1] in ['odt','odp']:
                    ff = f[:f.rfind('.')]
                    doc = check_output(['odt2txt']+[os.path.join(root, f)])
                    writer.add_document(title= unicode(ff), path= unicode(os.path.join(root,f)), content= unicode(decode_heuristically(doc)[0]))
                elif f.split('.')[-1] == 'docx':
                    ff = f[:f.rfind('.')]
                    doc1 = opendocx(os.path.join(root,f))
                    doc1 = getdocumenttext(doc1)
                    doc = ''
                    for j in range(len(doc1)):
                        doc = doc + doc1[j] + '\n'
                    writer.add_document(title= unicode(ff), path= unicode(os.path.join(root,f)), content= unicode(decode_heuristically(doc)[0]))
                else:
                    ff = f[:f.rfind('.')]
                    doc = open(os.path.join(root, f))
                    writer.add_document(title= unicode(ff), path= unicode(os.path.join(root,f)), content= unicode(decode_heuristically(doc.read())[0]))
                    doc.close()
            if len(f.split('.')) == 1:
                doc = open(os.path.join(root, f))
                writer.add_document(title= unicode(f), path= unicode(os.path.join(root,f)), content= unicode(decode_heuristically(doc.read())[0]))
                doc.close()
    writer.commit()
    return True
