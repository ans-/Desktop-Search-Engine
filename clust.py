import sys
import math
import itertools

def cosd(a, b):
    cos = 0.0
    a_ti = a["ti"]
    for tt, ti in b["ti"].iteritems():
        if tt in a_ti:
            cos += ti * a_ti[tt]
    return cos

def norm(features):
    normalization = 1.0 / math.sqrt(sum(i**2 for i in features.itervalues()))
    for k, v in features.iteritems():
        features[k] = v * normalization
    return features

def addti(documents):
    tokens = {}
    for i, d in enumerate(documents):
        tf = {}
        d["ti"] = {}
        doc_tokens = d.get("tokens", [])
        for token in doc_tokens:
            tf[token] = tf.get(token, 0) + 1
        num_tokens = len(doc_tokens)
        if num_tokens > 0:
            for token, freq in tf.iteritems():
                tokens.setdefault(token, []).append((i, float(freq) / num_tokens))

    doc_count = float(len(documents))
    for token, docs in tokens.iteritems():
        idf = math.log(doc_count / len(docs))
        for id, tf in docs:
            ti = tf * idf
            if ti > 0:
                documents[id]["ti"][token] = ti

    for d in documents:
        d["ti"] = norm(d["ti"])

def findcl(node, lookup, edges):
    new = lookup[node]
    if node in edges:
        seen, num_seen = {}, {}
        for target, weight in edges.get(node, []):
            seen[lookup[target]] = seen.get(lookup[target], 0.0) + weight
        for k, v in seen.iteritems():
            num_seen.setdefault(v, []).append(k)
        new = num_seen[max(num_seen)][0]
    return new

def majorclust(graph):
    lookup = dict((node, i) for i, node in enumerate(graph.nodes))

    count = 0
    movements = set()
    finished = False
    while not finished:
        finished = True
        for node in graph.nodes:
            new = findcl(node, lookup, graph.edges)
            move = (node, lookup[node], new)
            if new != lookup[node] and move not in movements:
                movements.add(move)
                lookup[node] = new
                finished = False

    clusters = {}
    for k, v in lookup.iteritems():
        clusters.setdefault(v, []).append(k)

    return clusters.values()

def get_dis(documents):
    class Graph(object):
        def __init__(self):
            self.edges = {}

        def add_edge(self, n1, n2, w):
            self.edges.setdefault(n1, []).append((n2, w))
            self.edges.setdefault(n2, []).append((n1, w))

    graph = Graph()
    doc_ids = range(len(documents))
    graph.nodes = set(doc_ids)
    for a, b in itertools.combinations(doc_ids, 2):
        graph.add_edge(a, b, cosd(documents[a], documents[b]))
    return graph

def get_documents(texts):
    return [{"text": text, "tokens": text.split()}
             for i, text in enumerate(texts)]

def main(texts):
    documents = get_documents(texts)
    addti(documents)
    dist_graph = get_dis(documents)

    return documents, majorclust(dist_graph)

