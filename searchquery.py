from whoosh.index import create_in, open_dir
from whoosh.fields import *

from whoosh.qparser import QueryParser, MultifieldParser, OrGroup, AndGroup
from whoosh.scoring import *
from whoosh.sorting import ScoreFacet, FieldFacet, MultiFacet

from whoosh.analysis import StandardAnalyzer
import googleanswer
import os

global_string = ''
corrector_string = ''

def all_stop_words( lst):
    analyzer = StandardAnalyzer()
    for t in analyzer( unicode(lst)):
        if not t.stopped:
            return False
    return True

def check_all_stop_words(yourQuery):
    if all_stop_words(yourQuery):
        return False
    else:
        return True

def remove_stop(lst):
    l = []
    analyzer = StandardAnalyzer()
    for i in range( len(lst)):
        for t in analyzer( unicode(lst[i])):
            if not t.stopped:
                l.append(lst[i])
    return l

def searchfile(yourQuery, score_method, and_or, filetypelist, clustering_not):
    global global_string, corrector_string
    global_string = ''
    corrector_string = ''
    local_string = ''

    global_string += googleanswer.findgoogle(yourQuery)

    homename = os.environ['HOME']
    ix = open_dir(homename + "/indexdir")

    if score_method == 'Frequency':
        scores_method = Frequency()
    elif score_method == 'BM25F':
        scores_method = BM25F()
    else:
        scores_method = TF_IDF()

    with ix.searcher(weighting=scores_method) as searcher:
        if and_or == 'AND':
            group_method = AndGroup
        else:
            group_method = OrGroup
        parser = MultifieldParser(["title","content"], ix.schema, group = group_method)
        user_q = parser.parse( unicode(yourQuery))
        scores = ScoreFacet()
        from whoosh.spelling import Corrector
        corrector = searcher.corrector("content")
        corrected = searcher.correct_query(user_q, unicode(yourQuery))
        if corrected.query != user_q:
            corrector_string = corrector_string + corrected.string
        else:
            corrector_string += ''
        results = searcher.search(user_q, sortedby = scores)
        abstract_word = remove_stop(yourQuery.split())
        abstract_word = abstract_word[0]
        if clustering_not == 'majorclust' and len(results) > 1:
            import clust
            text_a = []
            for i in range( len(results)):
                cx = results[i]['content']
                cx = cx.encode('ascii', 'ignore')
                cx.lower()
                cx += ' '+ str(i)
                text_a.append(cx)
            text_aa = []
            for i in text_a:
                if len(i) > 0:
                    text_aa.append(i)
            if len(text_aa) > 1:
                cl_documents, cl_majorclust = clust.main(text_aa)
            number_of_cluster = 1
            for cluster in cl_majorclust:
                local_string += 'Clustering '+ str(number_of_cluster) +':<br><br>'
                number_of_cluster += 1
                for j in cluster:
                    i = cl_documents[j]['text'].split()[-1]
                    i = int(i)
                    x = results[i]['path']
                    x = x.encode('ascii', 'ignore')
                    x = x.lower()
                    x = x.split('/')[-1]
                    x = x.split('.')
                    if x[-1] in filetypelist and len(x) > 1:
                        local_string += add_string(results[i]['title'],results[i]['path'],results[i]['content'],abstract_word)
                    if '@_@' in filetypelist:
                        notfiletypelist = ['pdf','doc','txt']
                        if x[-1] not in notfiletypelist or len(x) == 1:
                            local_string += add_string(results[i]['title'],results[i]['path'],results[i]['content'],abstract_word)

                    if len(filetypelist) == 0:
                        local_string += add_string(results[i]['title'],results[i]['path'],results[i]['content'],abstract_word)
        else:
            for i in results:
                x = i['path']
                x = x.encode('ascii', 'ignore')
                x = x.lower()
                x = x.split('/')[-1]
                x = x.split('.')
                if x[-1] in filetypelist and len(x) > 1:
                    local_string += add_string(i['title'],i['path'],i['content'],abstract_word)
                if '@_@' in filetypelist:
                    notfiletypelist = ['pdf','doc','txt']
                    if x[-1] not in notfiletypelist or len(x) == 1:
                        local_string += add_string(i['title'],i['path'],i['content'],abstract_word)
                if len(filetypelist) == 0:
                    local_string += add_string(i['title'],i['path'],i['content'],abstract_word)
    if len(local_string)==0:
        global_string += '<font color=\"red\">There is no file which can be found in your dir!</font>'
    else:
        global_string += local_string
    return global_string, corrector_string

def add_string(i1, i2, i3, abstract_word):
    local_string = ''
    x = i2
    x = x.encode('ascii','ignore')
    filename = x.split('/')
    filename = filename[-1]
    x = x.split()
    xx = ''
    for i in range(len(x)-1):
        xx += x[i] + '%20'
    xx += x[-1]
    local_string += '<a href="file://'+xx+'">'+filename+'</a><br>'
    a = i3
    a = a.encode('ascii','ignore')
    a = a.lower()
    a = a.split()
    if abstract_word in a:
        if a.index(abstract_word)-10 > 0 and a.index(abstract_word) + 10 < len(a):
            local_string = local_string + '<font color=\"gray\">...'+' '.join(a[ a.index(abstract_word)-10 : a.index(abstract_word)])+'<font color=\"black\">'+' '+a[a.index(abstract_word)]+' '+'</font>'+' '.join(a[ a.index(abstract_word)+1: a.index(abstract_word) +10])+'...</font>'
        elif a.index(abstract_word) - 10> 0:
            local_string = local_string + '<font color=\"gray\">...'+' '.join(a[ a.index(abstract_word)-10  : a.index(abstract_word)])+'<font color=\"black\">'+' '+a[a.index(abstract_word)]+' '+'</font>'+' '.join(a[ a.index(abstract_word)+1:])+'</font>'
        elif a.index(abstract_word) + 10 <len(a):
            local_string = local_string +'<font color=\"gray\">'+ ' '.join(a[ : a.index(abstract_word)])+'<font color=\"black\">'+' '+a[a.index(abstract_word)]+' '+'</font>'+' '.join(a[ a.index(abstract_word)+1: a.index(abstract_word)+10])+'...</font>'
        else:
            local_string = local_string + '<font color=\"gray\">'+' '.join(a[ : a.index(abstract_word)])+'<font color=\"black\">'+' '+a[a.index(abstract_word)]+' '+'</font>'+' '.join(a[ a.index(abstract_word)+1:])+'</font>'
    local_string += '<hr />'
    return local_string
