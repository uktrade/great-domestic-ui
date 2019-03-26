from core import serializers


def test_parse_results():
    content = {
        'took': 17,
        'timed_out': False,
        '_shards': {
            'total': 4,
            'successful': 4,
            'skipped': 0,
            'failed': 0
        },
        'hits': {
            'total': 100,
            'max_score': 0.2876821,
            'hits': [{
                '_index': 'objects__feed_id_first_feed__date_2019',
                '_type': '_doc',
                '_id': 'dit:exportOpportunities:Opportunity:2',
                '_score': 0.2876821,
                '_source': {
                    'type': 'Opportunities',
                    'title': 'France - Data analysis services',
                    'content':
                    'The purpose of this contract is to analyze Python\
 For Loops. A for loop is used for iterating over a sequence (that is\
  either a list, a tuple, a dictionary, a set, or a string). This is \
  less like the for keyword in other programming language, and works \
  more like an iterator method as found in other object-orientated \
  programming languages.',
                    'url': 'www.great.gov.uk/opportunities/1'
                }
            }, {
                '_index': 'objects__feed_id_first_feed__date_2019',
                '_type': '_doc',
                '_id': 'dit:exportOpportunities:Opportunity:2',
                '_score': 0.18232156,
                '_source': {
                    'type': 'Opportunities',
                    'title': 'Germany - snow clearing',
                    'content':
                    'Winter services for the properties1) Former...',
                    'url': 'www.great.gov.uk/opportunities/2'
                }
            }, {
                '_index': 'objects__feed_id_first_feed__date_2019',
                '_type': '_doc',
                '_id': 'dit:exportOpportunities:Opportunity:3',
                '_score': 0.18232156,
                '_source': {
                    'type': 'Article',
                    'title': 'UK - notice of report',
                    'content':
                    "The UK and the EU have agreed a draft agreement\
 on withdrawing from the EU. Read the [Prime Minister's statement](ht\
tps://www.gov.k/government/speeches/pms-statement-on-brexit-14-novembe\
r-2018) and the full",
                    'url': 'www.great.gov.uk/opportunities/3'
                }
            }]
        }
    }

    assert serializers.parse_search_results(content) == [{
        "type": "Opportunities",
        "title": "France - Data analysis services",
        "content": "The purpose of this contract is to analyze Python\
 For Loops. A for loop is used for iterating over a sequence (that is\
  either a list, a tuple, a dictionary, a ...",
        "url": "www.great.gov.uk/opportunities/1"
    }, {
        "type": "Opportunities",
        "title": "Germany - snow clearing",
        "content": "Winter services for the properties1) Former...",
        "url": "www.great.gov.uk/opportunities/2"
    }, {
        "type": "Article",
        "title": "UK - notice of report",
        "content": "The UK and the EU have agreed a draft agreement\
 on withdrawing from the EU. Read the Prime Minister's statement and\
 the full",
        "url": "www.great.gov.uk/opportunities/3"
    }]
