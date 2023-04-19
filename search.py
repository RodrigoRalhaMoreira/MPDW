import pprint as pp
from config import CONFIG
from opensearchpy import OpenSearch
from utils import parse_search_string

import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")

# Use configuration variables from CONFIG.py
client = OpenSearch(
    hosts=[{"host": CONFIG["host"], "port": CONFIG["port"]}],
    http_compress=True,
    http_auth=(CONFIG["user"], CONFIG["password"]),
    url_prefix="opensearch",
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# Check if the index exists
if client.indices.exists(index=CONFIG["index_name"]):
    print("Index found")
else:
    print("Index not found")

"""
    Searches for products based on the provided search_string and returns the raw response from OpenSearch.

    :param search_string: A string containing search terms in the format "key:value".
    :return: A dictionary containing the raw response from the OpenSearch query.
"""


def search_raw_info(search_string: str):
    try:
        kwargs, weights = parse_search_string(search_string)
    except ValueError:
        raise
    must_clauses = []

    # Build must_clauses for the search query
    if "color" in kwargs:
        must_clauses.append({"match": {"product_main_colour": kwargs["color"]}})

    if "gender" in kwargs:
        must_clauses.append({"match": {"product_gender": kwargs["gender"]}})

    if "category" in kwargs:
        must_clauses.append(
            {"multi_match": {"query": kwargs["category"], "fields": ["product_category", "product_sub_category"]}}
        )

    if "brand" in kwargs:
        must_clauses.append({"match": {"product_brand": kwargs["brand"]}})

    # Construct the final search query
    query_denc = {
        "size": 3,
        "_source": [
            "product_id",
            "product_family",
            "product_category",
            "product_sub_category",
            "product_gender",
            "product_main_colour",
            "product_second_color",
            "product_brand",
            "product_materials",
            "product_short_description",
            "product_attributes",
            "product_image_path",
            "product_highlights",
            "outfits_ids",
            "outfits_products",
        ],
        "query": {
            "function_score": {
                "query": {"bool": {"must": must_clauses}},
                "functions": [
                    {
                        "filter": {"match": {"product_main_colour": kwargs.get("color", "")}},
                        "weight": weights["color_weight"],
                    },
                    {
                        "filter": {"match": {"product_gender": kwargs.get("gender", "")}},
                        "weight": weights["gender_weight"],
                    },
                    {
                        "filter": {
                            "multi_match": {
                                "query": kwargs.get("category", ""),
                                "fields": ["product_category", "product_sub_category"],
                            }
                        },
                        "weight": weights["category_weight"],
                    },
                    {
                        "filter": {"match": {"product_brand": kwargs.get("brand", "")}},
                        "weight": weights["brand_weight"],
                    },
                ],
                "score_mode": "sum",
            }
        },
    }

    # Perform the search query
    return client.search(body=query_denc, index=CONFIG["index_name"])

# Example usage:
search_string = "color:black gender:men brand:Nike color_weight:3 gender_weight:1 brand_weight:9"
results = search_raw_info(search_string)
pp.pprint(results)



def search_natural_text(search_string: str):
  inputs = tokenizer([search_string], padding=True, return_tensors="pt")

  text_features = F.normalize(model.get_text_features(**inputs))

	# inputs = processor(text=[search_query], images=[], return_tensors="pt", padding=True)

	#text_embeds = F.normalize(outputs["text_embeds"])

  query_denc = {
		'size': 3,
		'_source': ['product_id',
              	'product_family',
               	'product_category',
                'product_sub_category',
                'product_gender', 
								'product_main_colour',
     						'product_second_color',
           			'product_brand', 'product_materials', 
								'product_short_description',
								'product_attributes',
								'product_image_path', 
								'product_highlights',
								'outfits_ids',
								'outfits_products',
     						'image_embedding'],
		"query": {
							"knn": {
								"combined_embedding": {
								"vector": text_features[0].detach().numpy(),
								"k": 2
								}
							}
						}
	}

  return client.search(
		body = query_denc,
		index = CONFIG["index_name"]
  )

	# results = [r['_source'] for r in response['hits']['hits']]
	# print('\nSearch results:')
	# results
