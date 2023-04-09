import os

CONFIG = {
    "host": "api.novasearch.org",
    "port": 443,
    "index_name": "farfetch_images",
    "user": os.environ["OPENSEARCH_USER"],
    "password": os.environ["OPENSEARCH_PASSWORD"],
}
