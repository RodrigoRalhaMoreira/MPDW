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


def parse_search_string(search_string):
    search_terms = search_string.split()
    attributes = {}
    weights = {'color_weight': 1, 'gender_weight': 1, 'category_weight': 1, 'brand_weight': 1}
    valid_genders = {'men', 'women'}
    valid_keys = {'color', 'gender', 'category', 'brand'}

    for term in search_terms:
        if ':' not in term:
            raise ValueError(f"Invalid syntax: {term}. Expected format: key:value")

        key, value = term.split(':', 1)

        if key not in valid_keys and not key.endswith('_weight'):
            raise ValueError(f"Invalid attribute key: {key}. Allowed keys: {', '.join(valid_keys)}")

        if key.endswith('_weight'):
            try:
                weight = float(value)
                if not 1 <= weight <= 10:
                    raise ValueError(f"Invalid weight value: {value}. Weight should be between 1 and 10.")
                weights[key] = weight
            except ValueError as e:
                raise ValueError(f"Invalid weight value: {value}. Weight should be a number between 1 and 10.") from e
        elif key == 'gender':
            if value.lower() not in valid_genders:
                raise ValueError(f"Invalid gender value: {value}. Allowed values: {', '.join(valid_genders)}")
            attributes[key] = value.lower()
        else:
            attributes[key] = value

    return attributes, weights



def search_raw_info(search_string):
    try:
      kwargs, weights = parse_search_string(search_string)
    except ValueError:
        raise
    must_clauses = []

    if 'color' in kwargs:
        must_clauses.append({
            'match': {
                'product_main_colour': kwargs['color']
            }
        })

    if 'gender' in kwargs:
        must_clauses.append({
            'match': {
                'product_gender': kwargs['gender']
            }
        })

    if 'category' in kwargs:
        must_clauses.append({
            'multi_match': {
                'query': kwargs['category'],
                'fields': ['product_category', 'product_sub_category']
            }
        })

    if 'brand' in kwargs:
        must_clauses.append({
            'match': {
                'product_brand': kwargs['brand']
            }
        })

    # Add more filter parameters if needed

    query_denc = {
            'size': 3,  # how many products we want
            '_source': ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender',
                        'product_main_colour', 'product_second_color', 'product_brand', 'product_materials',
                        'product_short_description', 'product_attributes', 'product_image_path',
                        'product_highlights', 'outfits_ids', 'outfits_products'],
            'query': {
                'function_score': {
                    'query': {
                        'bool': {
                            'must': must_clauses
                        }
                    },
                    'functions': [
                        {
                            'filter': {'match': {'product_main_colour': kwargs.get('color', '')}},
                            'weight': weights['color_weight']
                        },
                        {
                            'filter': {'match': {'product_gender': kwargs.get('gender', '')}},
                            'weight': weights['gender_weight']
                        },
                        {
                            'filter': {'multi_match': {
                                'query': kwargs.get('category', ''),
                                'fields': ['product_category', 'product_sub_category']
                            }},
                            'weight': weights['category_weight']
                        },
                        {
                            'filter': {'match': {'product_brand': kwargs.get('brand', '')}},
                            'weight': weights['brand_weight']
                        }
                    ],
                    'score_mode': 'sum'
                }
            }
        }

    response = client.search(
        body=query_denc,
        index=index_name
    )

    return response

# Example usage:
search_string = "color:black gender:men brand:Nike color_weight:3 gender_weight:1 brand_weight:9"
results = search_raw_info(search_string)
pp.pprint(results)
