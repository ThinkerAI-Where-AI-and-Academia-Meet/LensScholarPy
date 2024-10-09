"""
QueryUtilities module offers a set of management tools and validators for designing queries compatible
with the Lens Scholar API. It facilitates the construction of Elasticsearch queries by providing
interfaces to handle different groups of searchable fields, validate query parameters, and organize them
into structured queries.

Classes
-------
- FieldTypeManager:
    Manages field types specific to query groups, enabling the retrieval of field data for query construction.
- QueryManager:
    Constructs and organizes query components, integrating validations to streamline query building.

Global Variables
----------------
- SEARCHABLE_FIELDS_SOURCE (str):
    The module name containing definitions for searchable fields, segmented by query categories like "GENERAL", "AUTHOR".
- SEARCHABLE_FIELDS (module):
    Dynamically imports the module specified in SEARCHABLE_FIELDS_SOURCE, granting access to field data.
- AVAILABLE_GROUPS (List[str]):
    Lists the query categories available for construction, including "AUTHOR", "GENERAL", "CITATION", etc.
- AVAILABLE_BOOL_CLAUSES (List[str]):
    Enumerates Boolean clauses accepted in query construction: "must", "should", "must_not", "filter".
- AVAILABLE_QUERY_CLAUSES (List[str]):
    Enumerates query clauses permissible in query construction: "term", "terms", "match", "match_phrase".

Notes
-----
This module integrates stringent validation and dynamic field management to simplify and secure the process
of building query requests for the Lens Scholar API. It is designed to be used as a backend utility for more
complex query orchestration modules.
"""

import importlib
import logging
from typing import List, Dict, Any
from .validator import *

### Global Variables ###
SEARCHABLE_FIELDS_SOURCE = ".SearchableFields"
SEARCHABLE_FIELDS = importlib.import_module(SEARCHABLE_FIELDS_SOURCE, package="LensScholarPy")

AVAILABLE_GROUPS = ['AUTHOR','CITATION', 'CLINICAL_TRIALS', 'CONFERENCES',
                    'EXTERNAL_ID', 'FUNDING', 'GENERAL', 'INSTITUTIONS',
                    'OPEN_ACCESS', 'RETRACTION', 'SOURCE', 'SUBJECT_MATTER',
                    'BOOLEAN_FILTERS', 'DATE']
### End of Global Variables ###

class FieldTypeManager:
    '''
    Manages the field types for classes responsible for constructing queries for Lens Scholar Request.

    Parameters
    ----------
    group_type : str
        The group type to manage field types such as "GENERAL", "AUTHOR", "CITATION", etc.
        More information can be found in the documentation at https://docs.api.lens.org/request-scholar.html#searchable-fields.

    Attributes
    ----------
    _field_data : dict
        The field data for the group type. Dictionary contains parent keys and 3 nested keys with values in parent key.
        - parameter_name (also the parent key): str
        
        The name of the parameter used in classes like GeneralSearch, AuthorSearch, etc.
        - query_name (nested key): str
        
        The name of the parameter which is used in formating the query. Some fields can have special characters like **dot ('.')**.
        - accepted_type (nested key): Union[type, List[type]]
        
        The accepted type for the field. It can be a single type or a list of types.
        - restrictions (nested key): List[str], None
        
        The list of restricted values for the field. If None, any value is accepted.

    Raises
    ------
    ValueError
        If the group type is not available.

    Examples
    --------
    >>> field_manager = FieldTypeManager("GENERAL")
    >>> print(field_manager._field_data)
    '''
    def __init__(self, group_type: str):
        self.field_data = self._get_field_data(group_type)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.field_data})"

    def __str__(self):
        return f"{self.field_data}"

    def _get_field_data(self, group_name: str) -> Dict[str, Any]:
        '''
        Get the field data for the group type.

        Parameters
        ----------
        group_name : str
            The group type to get the field data for.

        Returns
        -------
        Dict[str, Any]
            The field data for the group type.

        Raises
        ------
        ValueError
            If the group type is not available.

        TODO
        ----
        - Create function for getting field data from various sources like DB, JSON, etc. rather than python file.
        Additional data sources needs specific encoder/decoder for the data due to accepted_type.
        accepted_type in source file contains type objects like str, int, etc.
        '''
        try:
            selected_group = getattr(SEARCHABLE_FIELDS, group_name)
            logging.debug(f"Field type {group_name} is available.")
            return selected_group
        except AttributeError:
            logging.error(
                f"Field type {group_name} is not available.",
                f"Available groups are {AVAILABLE_GROUPS}.")
            raise ValueError(
                f"Field type {group_name} is not available."
                f"Available groups are {AVAILABLE_GROUPS}.")
            
class QueryManager:
    '''
    Manages the query construction for Lens Scholar Request.

    Parameters
    ----------
    _group_type : str
        The group type to manage field types such as "GENERAL", "AUTHOR", "CITATION", etc.
        More information can be found in the documentation at https://docs.api.lens.org/request-scholar.html#searchable-fields.
    
    Attributes
    ----------
    field_details : dict
        The field details for the group type. Dictionary contains parent keys and 3 nested keys with values in parent key.
        - parameter_name (also the parent key): str
        
        The name of the parameter used in classes like GeneralSearch, AuthorSearch, etc.
        - query_name (nested key): str
        
        The name of the parameter which is used in formating the query. Some fields can have special characters like **dot ('.')**.
        - accepted_type (nested key): Union[type, List[type]]
        
        The accepted type for the field. It can be a single type or a list of types.
        - restrictions (nested key): List[str], None
        
        The list of restricted values for the field. If None, any value is accepted.

    output : dict
        Contains the constructed query for the Lens Scholar Request.
        - must : List[Dict[str, Dict[str, Any]]]
        
        The list of must clauses for the query.
        - should : List[Dict[str, Dict[str, Any]]]
        
        The list of should clauses for the query.
        - must_not : List[Dict[str, Dict[str, Any]]]
        
        The list of must_not clauses for the query.
        - filter : List[Dict[str, Dict[str, Any]]]
        
        The list of filter clauses for the query.

    Methods
    -------
    _add_single_value(field: str, bool_clause: str, query_clause: str, value: Any) -> None
        Add a single value to the self.output.

    _add_multiple_value(field: str, value: List[List]) -> None
        Add multiple values to the self.output.

    add_arguments(**kwargs) -> None
        Add multiple arguments to the self.output. This methods intended to be used other classes like GeneralQuery, AuthorQuery, etc.
    '''

    def __init__(self, _group_type: str):
        self.field_details = FieldTypeManager(_group_type).field_data
        self.output = {
            "must"      : [],
            "should"    : [],
            "must_not"  : [],
            "filter"    : []
        }

    # For single arguments which has only one value as ["must", "match", "COVID-19"], etc.
    def _add_single_value(self,field: str, bool_clause: str, query_clause: str, value: Any) -> None:
        '''
        Add a single value to the self.output.

        Parameters
        ----------
        field : str
            The field to add to the output.
        bool_clause : str
            The boolean clause for the field. Must be one of "must", "should", "must_not", or "filter".
        query_clause : str
            The query clause for the field. Must be one of "term", "terms", "match", "match_phrase", or "range".
        value : Any
            The value for the field.
        '''

        # Validate the boolean clause
        validate_bool_clause(field, bool_clause)

        # Validate the query clause
        validate_query_clause(field, query_clause)

        # Validate the list value for "terms" query clause
        validate_term_list_value(field, query_clause, value)

        # Validate the value type
        accepted_type = self.field_details[field]["accepted_type"]
        validate_value_type(field, value, accepted_type)

        # Validate the value restriction
        restrictions = self.field_details[field]["restrictions"]
        validate_value_restriction(field, value, restrictions)

        # Add the field to the output
        self.output[bool_clause].append({query_clause: {self.field_details[field]["query_name"]: value}})
        logging.debug(f"Added {field} with value as {value}, {bool_clause}, and {query_clause}.")

    # For single argument which has multiple list of lists as [["must", "match", "COVID-19"], ["should", "term", "vaccine"], etc.]
    def _add_multiple_value(self, field: str, value: List[List]) -> None:
        '''
        Add multiple values to the self.output.

        Parameters
        ----------
        field : str
            The field to add to the output.
        value : List[List]
            The list of values for the field.
        '''
        for item in value:
            # Validate the value length
            validate_argument_list_length(field, item, 3)

            self._add_single_value(field, *item)

    # For adding multiple arguments to the self.output
    def add_arguments(self, **kwargs) -> None:
        '''
        Add multiple arguments to the self.output.
        This methods intended to be used other classes like GeneralQuery, AuthorQuery, etc.

        Parameters
        ----------
        **kwargs : Dict[str, List]
            The keyword arguments to add to the output.
            The key is the field name and the value is a list of lists.
        '''
        for field, value in kwargs.items():
            if value is None or not value:
                continue

            if not isinstance(value, list):
                raise ValueError(f"Invalid value for {field}: {value}. Must be a list.")

            # Validate the field
            validate_field(field, list(self.field_details.keys()))

            logging.debug(f"Processing {field} with value {value}.")

            # Check if the first item is a list, implying multiple values
            if isinstance(value[0], list):
                self._add_multiple_value(field, value)
                logging.debug(f"Added {field} as multiple values.")
            else:
                self._add_single_value(field, *value)
                logging.debug(f"Added {field} as single values.")

    # Range query construction is different from match, term, etc. queries. So, it is handled separately.
    def add_range_arguments(self, **kwargs) -> None:
        '''
        Add multiple range arguments to the self.output.

        Parameters
        ----------
        **kwargs : Dict[str, Dict]
            The keyword arguments to add to the output.
            The key is the field name and the value is a dictionary with keys 'gte', 'gt', 'lte', 'lt'.
        '''
        for field, value in kwargs.items():
            logging.debug(f"Processing {field} with value {value}.")
            if value is None or not value:
                logging.debug(f"Skipping {field}")
                continue

            if not isinstance(value, list):
                raise ValueError(f"Invalid value for {field}: {value}. Must be a list.")
            
            # Validate the field
            validate_field(field, list(self.field_details.keys()))

            # Check if the value is list with 2 elements
            validate_argument_list_length(field, value, 2)

            bool_clause, range_dict = value

            # Validate the range value is a dictionary
            validate_range_dict_type_value(field, range_dict)

            # Validate the only gte or gt
            validate_gte_gt(field, range_dict.get("gte"), range_dict.get("gt"))

            # Validate the only lte or lt
            validate_lte_lt(field, range_dict.get("lte"), range_dict.get("lt"))

            less_than = range_dict.get("lte", range_dict.get("lt", None))
            greater_than = range_dict.get("gte", range_dict.get("gt", None))

            # Validate the date format if the fields are date related
            if self.field_details[field].get("date_format"):
                accept_date_format = self.field_details[field]["date_format"]
                if less_than:
                    validate_date_format(field, less_than, accept_date_format)
                if greater_than:
                    validate_date_format(field, greater_than, accept_date_format)
            
            # Compare the greater_than and less_than
            if less_than and greater_than:
                validate_g_and_l(field, greater_than, less_than)

            # Add the field to the output
            self.output[bool_clause].append({"range": {self.field_details[field]["query_name"]: range_dict}})

    def add_bool_arguments(self, **kwargs) -> None:
        # Boolean filters aka BasicFilterQuery arguments can only take field = ["bool_clause", "value"]
        for field, value in kwargs.items():
            logging.debug(f"Processing {field} with value {value}.")
            if value is None or not value:
                logging.debug(f"Skipping {field}")
                continue

            if not isinstance(value, list):
                raise ValueError(f"Invalid value for {field}: {value}. Must be a list.")

            # Validate the field
            validate_field(field, list(self.field_details.keys()))

            # Check if the value is list with 2 elements
            validate_argument_list_length(field, value, 2)

            bool_clause, bool_value = value

            # Validate the boolean clause
            validate_bool_clause(field, bool_clause)

            # Validate the value type
            accepted_type = self.field_details[field]["accepted_type"]
            validate_value_type(field, bool_value, accepted_type)

            # Add values to the output. If bool_clause is "filter", then add with query clause "term". Else, add with query clause "match".
            if bool_clause == "filter":
                self.output[bool_clause].append({"term": {self.field_details[field]["query_name"]: bool_value}})
            else:
                self.output[bool_clause].append({"match": {self.field_details[field]["query_name"]: bool_value}})