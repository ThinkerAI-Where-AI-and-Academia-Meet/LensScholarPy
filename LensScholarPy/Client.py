"""
Client module for interacting with the Lens Scholar API.

This module provides an interface for sending requests to the Lens Scholar API, allowing users to perform
complex searches, check API usage limits, and retrieve information based on Lens IDs. It leverages classes
from other modules to structure queries and handle API configurations efficiently.

Classes
-------
- LensScholarConfig:
    A class that handles API configuration details, ensuring necessary credentials and endpoints are set up
    using environment variables for secure and flexible management.

- LensScholarClient:
    Inherits from LensScholarConfig, enabling seamless interaction with the Lens Scholar API. It offers
    methods to:
    - Check API usage limits (check_api_limit)
    - Send search queries (scholar_request)
    - Retrieve information using Lens IDs (lensid_request)
    - Send search queries with scrolling support (scholar_request_scroll)

Methods
-------
- check_api_limit():
    Retrieves the current API usage statistics, helping users manage their API consumption effectively.

- scholar_request(query, size=10, sort=[{"relevance": "desc"}], include=["title"]):
    Posts a search query to the Lens Scholar API, structured either as a raw string or through advanced
    query objects, and returns relevant document results.

- lensid_request(lens_id):
    Retrieves document details using a specific Lens ID from the API.

- scholar_request_scroll(query, size=1000, sort=[{"relevance": "desc"}], include=["title"], sleep_time=5):
    Posts a search query to the Lens Scholar API with scrolling support, allowing users to retrieve large
    result sets efficiently. The method can store data in memory or save it to files based on user preference.

Usage Example
-------------
After setting the necessary environment variables in a .env file, you can create a client instance:
>>> from AdvancedScholarQuery import QueryBuilder, AuthorQuery
>>> client = LensScholarClient()
>>> gq = AuthorQuery(author_count=["must", "terms", [1, 2, 3]])
>>> query = QueryBuilder(gq).query_string
>>> data = client.scholar_request(query=query, size=100, include=["lens_id", "authors"])
>>> with open("data.json", "w") as f:
>>>     json.dump(data, f, indent=4)

Notes
-----
- Ensure that the .env file contains valid entries for the required API credentials and endpoints.

This module provides a structured way to interact with the Lens scholar API, abstracting away the complexity
of direct HTTP requests and error handling, promoting ease of use and reliability for application developers.

TODO
----
- Add scrolling support for large result sets by creating scroll_request method.
- Add either method or class for handling sorting, projections (include, exclude), and other query parameters.
- Add range queries for other fields which accept integer values like citation counts.
"""

import os
import requests
import dotenv
import logging
import json
from typing import Union, List
from .AdvancedScholarQuery import QueryManager
import time
import uuid

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

class ScholarConfig:
    '''
    TheLensConfig superclass is used to store the configuration for the Lens API.

    Attributes
    ----------
    - api_key : str
        The API key for the Lens API.
    - search_url : str
        The URL for the search endpoint of the Lens API.
    - usage_url : str
        The URL for the usage endpoint of the Lens API.
    - content_type : str
        The content type for the API request.
    - accept : str
        The accept type for the API response.

    Methods
    -------
    check_config()
        Checks if the configuration is set properly.

    Raises
    ------
    ValueError
        If a configuration is not set.
    '''
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.api_key = os.getenv("LENS_SCHOLAR_API_KEY")
        self.search_url = "https://api.lens.org/scholarly"
        self.usage_url = "https://api.lens.org/subscriptions/scholarly_api/usage"
        self.content_type = 'application/json'
        self.accept = 'application/json'

        self.check_config()

    def check_config(self) -> None:
        """
        Checks if the configuration is set properly.

        Raises
        ------
        ValueError
            If a configuration is not set.
        """
        for key, value in self.__dict__.items():
            if value is None:
                raise ValueError(f"{key} is not set. Please set it in the .env file.")

class ScholarClient(ScholarConfig):
    '''
    The LensScholarClient class is used to interact with the Lens Scholar API.    
    '''
    def __init__(self):
        super().__init__()
        pass
        
    def check_api_limit(self):
        """
        Checks the remaining API limit.

        Returns
        -------
        dict
            The response from the API.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(self.usage_url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def scholar_request(self,
                        query: Union[str, QueryManager],
                        sort: list = [{"relevance": "desc"}],
                        include: list = ['title', 'abstract', 'authors', 'lens_id'],
                        exclude: list = None,
                        size: int = 10,
                        _from: int = 0,
                        stemming: bool = True,
                        regex: bool = False,
                        min_score: float = 0.0) -> dict:
        """
        Sends a POST request to the Lens API for scholarly searches.

        Args
        ----
        query : Union[dict, QueryManager]
            The query to search for.
        sort : list
            The sort order of the returned documents.
        include : list
            The fields to include in the response.
        exclude : list
            The fields to exclude from the response.
        size : int
            The number of results to return.
        _from : int
            The offset from the start of results for pagination.
        stemming : bool
            Enable or disable stemming in text search.
        regex : bool
            Allow queries using regular expressions.
        min_score : float
            The minimum relevance score for filtering results.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        requests.exceptions.HTTPError
            If the request fails, logging error details.
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': self.content_type,
            'accept': self.accept
        }
        
        data = {
            "query": query,
            "sort": sort,
            "include": include,
            "exclude": exclude,
            "size": size,
            "from": _from,
            "stemming": stemming,
            "regex": regex,
            "min_score": min_score
        }

        response = requests.post(f"{self.search_url}/search", headers=headers, json=data)
        if response.status_code != 200:
            logging.error(f"Error: {response.json()}")
            response.raise_for_status()
        return response.json()
    
    def lensid_request(self, lens_id: str) -> dict:
        """
        Sends a GET request to the Lens API with a Lens ID.

        Args
        ----
        lens_id : str
            The Lens ID to search for.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        requests.exceptions.HTTPError
            If the request fails.
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': self.content_type,
            'accept': self.accept
        }

        response = requests.get(f"{self.search_url}/{lens_id}", headers=headers)
        return response.json()
    
    def scholar_request_scroll(self,
                           query: Union[str, 'QueryManager'],
                           sort: List[dict] = [{"relevance": "desc"}],
                           include: List[str] = ['title', 'authors', 'lens_id'],
                           exclude: List[str] = None,
                           size: int = 1000,
                           stemming: bool = True,
                           regex: bool = False,
                           min_score: float = 0.0,
                           scroll: str = "1m",
                           sleep_time: int = 5,
                           data_folder: str = None) -> List[dict]:
        """
        Sends a POST request to the Lens API for scholarly searches with scrolling support.
        This method has two modes of operation: saving data to files or storing data in memory.
        In this method, the data is saved in files if the data_folder parameter is provided, otherwise, it is stored in memory.

        Args
        ----
        query : Union[str, QueryManager]
            The query to search for.
        sort : List[dict]
            The sort order of the returned documents.
        include : List[str]
            The fields to include in the response.
        exclude : List[str]
            The fields to exclude from the response.
        size : int
            The number of results to return in each scroll request. Maximum accepted value is 1000.
        stemming : bool
            Enable or disable stemming in text search.
        regex : bool
            Allow queries using regular expressions.
        min_score : float
            The minimum relevance score for filtering results.
        scroll : str
            The scroll time for the request.
        sleep_time : int
            The time to sleep between requests.
        data_folder : str
            The folder to save the data in.

        Returns
        -------
        List[dict]
            - If data_folder is None, the data is stored in memory and returned as a list of dictionaries for further processing.
            - If data_folder is provided, the data is saved in files and a list of file names is returned for reference.

        Raises
        ------
        requests.exceptions.RequestException
            If the request fails.
        json.JSONDecodeError
            If the JSON decoding fails.

        Notes
        -----
        - The data is saved in files with the name "scroll_data_{timestamp}.json", if the data_folder is provided.
        """

        # Set headers for the request
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': self.content_type,
            'accept': self.accept
        }
        # Set the request query
        request_query = {
            "query": query,
            "sort": sort,
            "include": include,
            "exclude": exclude,
            "size": size,
            "stemming": stemming,
            "regex": regex,
            "min_score": min_score,
            "scroll": scroll
        }

        # Prepare for data storage
        if data_folder:
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            file_name_list = []
        else:
            all_data = []

        scroll_id = None

        while True:
            try:
                if scroll_id:
                    request_query["scroll_id"] = scroll_id
                    logging.debug(f"Scroll ID: {scroll_id[:10]}...{scroll_id[-10:]}")

                response = requests.post(url=f"{self.search_url}/search", headers=headers, json=request_query)
                logging.debug(f"Request status: {response.status_code}")

                if response.status_code == 429:
                    logging.warning(f"Too many requests. Sleeping for {sleep_time} seconds.")
                    time.sleep(sleep_time)
                    continue

                response.raise_for_status()
                data = response.json()

                # Handle the scroll data based on the data_folder parameter
                if data_folder:
                    # Save the data in a file
                    file_name = os.path.join(data_folder, f"scroll_data_{int(time.time())}_{str(uuid.uuid4())[:4]}.json")
                    with open(file_name, "w") as f:
                        json.dump(data, f, indent=4)
                    file_name_list.append(file_name)
                    logging.debug(f"Scrol data saved in {file_name}")
                else:
                    # Save the data in memory
                    all_data.append(data.get('data', []))
                    logging.debug(f"Scroll data saved in memory.")

                scroll_id = data.get('scroll_id')
                # Check if there is one more set of data to retrieve
                if len(data.get('data', [])) < size:
                    logging.info("No more data to retrieve.")
                    break

            except requests.exceptions.RequestException as e:
                logging.error(f"Request error: {e}", exc_info=True)
                break
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {e}", exc_info=True)
                break

        if data_folder:
            # Return the list of file names
            logging.info(f"Data saved in {len(file_name_list)} files.")
            return file_name_list
        else:
            # Return the list of dictionaries which includes all the scroll data
            logging.info(f"Data saved in memory.")
            return all_data
    
    
if __name__ == "__main__":
    pass
