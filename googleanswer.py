import json
import urllib

def findgoogle(searchfor):
    query = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    try:
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']

        local_string = "Google's answer:<br>"

        for h in hits:
            local_string += '<a href="'+h['url']+'">'+h['url']+'</a><br>'
        local_string +=  'For more results: '+ '<a href="' + data['cursor']['moreResultsUrl'] +'">'+data['cursor']['moreResultsUrl']+'</a><hr />'
        return local_string
    except:
        return '<font color=\"gray\">Your computer does not connect to network!</font><hr />'
