# Desktop-Search-Engine
DSE (Desktop Search Engine) is based on [Whoosh][Whoosh]. It is 
implemented by python and can retrieve internet and local PC 
information in the same time.

## Feathers

DSE will give users choices to 
choose different algorithms for indexing, scoring files and 
clustering the search results, and it also provide different 
keywords operators and many types of files for user to search. 

DSE provides TF-IDF, BM25F and Frequency algorithm for 
scoring files, Standard, stemming and 4-gram for indexing files, 
MajorClust for clustering results.

## Requirements
This tool is developed under Ubuntn 12.04.You have to install some thing to run DSE. 
Here is what you need: python 2.7, wxpython 2.8, whoosh, open-docx, odt2txt, catdoc, pdfminer.

To run it, just type:

`python gui.py &`

[Whoosh]:(https://bitbucket.org/mchaput/whoosh/wiki/Home)


