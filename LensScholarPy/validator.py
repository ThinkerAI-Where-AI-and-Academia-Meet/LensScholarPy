"""
validator module contains functions to validate the arguments. The functions are used to validate
the arguments of the query classes and RangeQuery class in AdvancedScholarQuery module.

Global Constants
----------------
- AVAILABLE_BOOL_CLAUSES: List[str]
    List of available boolean clauses for the query.
- AVAILABLE_QUERY_CLAUSES: List[str]
    List of available query clauses for the query.

Functions
---------
- validate_field(field: str, accepted_field: List) -> None:
    Validate that a field is within an accepted list of fields.
- validate_argument_list_length(field: str, argument_list: List, length: int) -> None:
    Validate that a list of arguments is of a certain length.
- validate_bool_clause(field: str, condition_clause: str) -> None:
    Validate that a boolean clause is one of the accepted strings in AVAILABLE_BOOL_CLAUSES.
- validate_query_clause(field: str, query_clause: str) -> None:
    Validate that a query clause is one of the accepted strings in AVAILABLE_QUERY_CLAUSES.
- validate_term_list_value(field: str, query_clause, value: List[str]) -> None:
    Validate that a value is a list, if query_clause is 'terms'.
- validate_value_type(field: str, value: Any, accepted_type: type) -> None:
    Validate that a value is of an accepted type or validate every item in list of values is of an accepted type.
- validate_value_restriction(field: str, value: Any, restrictions: Union[List[str], None]) -> None:
    Validate that a value is within an restricted list of values. If None, any value is accepted.
- validate_date_format(field: str, value: str, format: str) -> None:
    Validate that a value is in the correct format.
- validate_range_dict_type_value(field: str, value: Dict) -> None:
    Validate that a value is a dictionary.
- validate_gte_gt(field: str, gte: str, gt: str) -> None:
    Validate that only one of 'gte' or 'gt' is provided.
- validate_lte_lt(field: str, lte: str, lt: str) -> None:
    Validate that only one of 'lte' or 'lt' is provided.
- validate_g_and_l(field: str, g: str, l: str) -> None:
    Validate that gte or gt is less than lte or lt.

Exceptions
----------
- ValueError
    Raised when the value of the argument is not valid.
"""
from typing import Any, List, Union, Dict
from datetime import datetime

AVAILABLE_BOOL_CLAUSES = ["must", "should", "must_not", "filter"]
AVAILABLE_QUERY_CLAUSES = ["term", "terms", "match", "match_phrase"]

### Scholar Query Validators ###

def validate_field(field: str, accepted_field: List) -> None:
    """Validate that a field is within an accepted list of fields."""
    if field not in accepted_field:
        raise ValueError(f"Invalid field: {field}. Must be one of {accepted_field}.")

def validate_argument_list_length(field: str, argument_list: List, length: int) -> None:
    """Validate that a list of arguments is of a certain length."""
    if len(argument_list) != length:
        raise ValueError(f"Invalid number of arguments for {field}. Must have {length} arguments.")

def validate_bool_clause(field: str, condition_clause: str) -> None:
    """Validate that a boolean clause is one of the accepted strings in AVAILABLE_BOOL_CLAUSES."""
    if condition_clause not in AVAILABLE_BOOL_CLAUSES:
        raise ValueError(f"Invalid condition type for {field}: {condition_clause}. Must be {AVAILABLE_BOOL_CLAUSES}.")

def validate_query_clause(field: str, query_clause: str) -> None:
    """Validate that a query clause is one of the accepted strings in AVAILABLE_QUERY_CLAUSES."""
    if query_clause not in AVAILABLE_QUERY_CLAUSES:
        raise ValueError(f"Invalid query type for {field}: {query_clause}. Must be {AVAILABLE_QUERY_CLAUSES}.")

def validate_term_list_value(field: str, query_clause, value: List[str]) -> None:
    """Validate that a value is a list, if query_clause is 'terms'."""
    if query_clause == "terms" and not isinstance(value, list):
        raise ValueError(f"Invalid value for {field}: {value}. Must be a list.")
    elif query_clause == "term" and isinstance(value, list):
        raise ValueError(f"Invalid value for {field}: {value}. Must be a single value.")

def validate_value_type(field: str, value: Any, accepted_type: type) -> None:
    """Validate that a value is of an accepted type or validate every item in list of values is of an accepted type."""
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, accepted_type):
                raise ValueError(f"Invalid value for {field}: {item}. Must be of type {accepted_type}.")
    elif not isinstance(value, accepted_type):
        raise ValueError(f"Invalid value for {field}: {value}. Must be of type {accepted_type}.")
    
def validate_value_restriction(field: str, value: Any, restrictions: Union[List[str], None]) -> None:
    """Validate that a value is within an restricted list of values. If None, any value is accepted."""

    if restrictions is not None and value not in restrictions:
        raise ValueError(f"Invalid value for {field}: {value}. Must be one of {restrictions}.")

def validate_date_format(field: str, value: str, format: str) -> None:
    """Validate that a value is in the correct format."""
    try:
        datetime.strptime(value, format)
    except ValueError:
        raise ValueError(f"Invalid value for {field}: {value}. Must be in the format {format}.")

### End Scholar Query Validators ###

### Scholar Range Validators ###
def validate_range_dict_type_value(field: str, value: Dict) -> None:
    """Validate that a value is a dictionary."""
    if not isinstance(value, dict):
        raise ValueError(f"Invalid value for {field}: {value}. For range queries, value must be a dictionary.")
            
def validate_gte_gt(field: str, gte: str, gt: str) -> None:
    """Validate that only one of 'gte' or 'gt' is provided."""
    if gte is not None and gt is not None:
        raise ValueError(f"Invalid value for {field}: {gte}, {gt}. Must have only one of 'gte' or 'gt'.")
    
def validate_lte_lt(field: str, lte: str, lt: str) -> None:
    """Validate that only one of 'lte' or 'lt' is provided."""
    if lte is not None and lt is not None:
        raise ValueError(f"Invalid value for {field}: {lte}, {lt}. Must have only one of 'lte' or 'lt.")

def validate_g_and_l(field: str, g: str, l: str) -> None:
    """Validate that gte or gt is less than lte or lt."""
    if g > l:
        raise ValueError(f"Invalid value for {field}: gt/e -> {g}, lt/e -> {l}. gt/e must be less than lt/e.")

### End Scholar Range Validators ###