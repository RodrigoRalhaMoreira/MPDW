import pprint as pp
from opensearchpy import OpenSearch

host = 'api.novasearch.org'
port = 443

index_name = "farfetch_images"

user = 'ifetch'  # Add your username here.
password = 'S48YdnMQ'  # Add your user password here. For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True,
    http_auth = (user, password),
    url_prefix = 'opensearch',
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

if client.indices.exists(index = index_name):
    print("Index found")
    """
    print('\n----------------------------------------------------------------------------------- INDEX SETTINGS')
    settings = client.indices.get_settings(index = index_name)
    pp.pprint(settings)

    print('\n----------------------------------------------------------------------------------- INDEX MAPPINGS')
    mappings = client.indices.get_mapping(index = index_name)
    pp.pprint(mappings)

    print('\n----------------------------------------------------------------------------------- INDEX #DOCs')
    print(client.count(index = index_name))"""
else:
    print("Index not found")


def searchRawInfo(qtxt: str):
    qcolor, qtype = qtxt.split(" ")
    query_denc = {
        'size': 3,  # how many products we want
        '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender',
                    'product_main_colour', 'product_second_color', 'product_brand', 'product_materials',
                    'product_short_description', 'product_attributes', 'product_image_path',
                    'product_highlights', 'outfits_ids', 'outfits_products'],
        'query': {
            'bool': {
              'must': [
                {
                  'match': {
                    'product_main_colour': qcolor
                  }
                },
                {
                  'multi_match': {
                    'query': qtype,
                    'fields': ['product_category', 'product_sub_category']
                  }
                }
              ]
            }
        }
    }

    response = client.search(
      body = query_denc,
      index = index_name
    )
    """
    results = [r['_source'] for r in response['hits']['hits']]
    print('\nSearch results:')
    pp.pprint(results)
    """
    return response
