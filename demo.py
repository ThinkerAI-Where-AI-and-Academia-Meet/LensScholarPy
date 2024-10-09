from LensScholarPy import ScholarClient, ScholarConfig
from LensScholarPy import GeneralQuery, RangeQuery, QueryBuilder
import json

"""
Create dotenv file with the following content:
```
LENS_SCHOLAR_API_KEY = "your_api_key"
```
"""

client = ScholarClient()

gq = GeneralQuery(title=["must", "match_phrase", "machine learning"],
                  abstract=["should", "terms", ["deep learning", "neural network"]])

rq = RangeQuery(year_published=["filter", {"gte": "2019", "lte": "2021"}])

query = QueryBuilder(gq, rq).query_string

response = client.scholar_request(query, size=10)

with open('response.json', 'w') as f:
    json.dump(response, f, indent=4)