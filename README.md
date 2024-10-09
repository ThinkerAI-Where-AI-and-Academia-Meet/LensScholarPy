# LensScholarPy

Welcome to LensScholarPy. This SDK provides a user-friendly interface for interacting with The Lens API using Python, making it easier to perform complex queries without deep knowledge of Elasticsearch syntax.

## About The Lens

[The Lens](https://www.lens.org/) provides open access to scholarly and patent literature accelerating innovation and facilitating global collaboration. Our SDK leverages their APIs for enhanced search capabilities in scholarly research.

## Usage

Here's a basic example of how to use:

First, create a dotenv file with the following content:
```
LENS_SCHOLAR_API_KEY = "your_api_key"
```

```python
from TheLensScholar import ScholarClient, ScholarConfig
from TheLensScholar import GeneralQuery, RangeQuery, QueryBuilder
import json

client = ScholarClient()

gq = GeneralQuery(title=["must", "match_phrase", "machine learning"],
                  abstract=["should", "terms", ["deep learning", "neural network"]])

rq = RangeQuery(year_published=["filter", {"gte": "2019", "lte": "2021"}])

query = QueryBuilder(gq, rq).query_string

response = client.scholar_request(query, size=10)

with open('response.json', 'w') as f:
    json.dump(response, f, indent=4)
```

## Features

- **Easy to use**: The SDK provides a simple and intuitive API to facilitate your work.
- **Comprehensive**: Access to all endpoints of The Lens API, empowering your projects with broad functionality.
- **Well-documented**: Thorough and clear documentation to guide you through setup and usage.

## Acknowledgments

This project leverages the capabilities of [The Lens Scholar API](https://www.lens.org/lens/user/subscriptions#scholar), providing essential tools for research and innovation. We extend our gratitude to [The Lens](https://www.lens.org/) for enabling such open and accessible resources.

## Authors

- **Murat Can Çetingörür** - *Main Developer* - [Caisenberg](https://github.com/Caisenberg)
- **Berkay Sungur** - *Contributor* - [BrkySungur](https://github.com/BrkySungur)