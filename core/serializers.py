def parse_search_results(content):
    # import pdb; pdb.set_trace()
    results = [hit['_source'] for hit in content['hits']['hits']]
    for result in results:
        if ('content' in result) and (len(result['content']) > 160):
            result['content'] = result['content'][0:160] + '...'
    return results
