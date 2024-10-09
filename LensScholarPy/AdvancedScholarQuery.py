'''
Advanced Scholar Query Module for The Lens Scholar API.

This module serves to simplify the process of creating Elasticsearch queries tailored for The Lens Database.
It provides an intuitive SDK for constructing complex queries with ease and efficiency.
Ideal for researchers and developers, this module allows for constructing sophisticated search queries without needing in-depth knowledge of Elasticsearch syntax.

Classes
-------
- GeneralQuery: General query terms for Lens Scholar Request.
- RetractionQuery: Retraction query terms for Lens Scholar Request.
- AuthorQuery: Author query terms for Lens Scholar Request.
- CitationQuery: Citation query terms for Lens Scholar Request.
- ExternalIdQuery: External ID query terms for Lens Scholar Request.
- SourceQuery: Source query terms for Lens Scholar Request.
- SubjectMatterQuery: Subject matter query terms for Lens Scholar Request.
- InstitutionQuery: Institution query terms for Lens Scholar Request.
- FundingQuery: Funding query terms for Lens Scholar Request.
- ConferencesQuery: Conferences query terms for Lens Scholar Request.
- ClinicalTrialsQuery: Clinical trials query terms for Lens Scholar Request.
- OpenAccessQuery: Open access query terms for Lens Scholar Request.
- BasicFilterQuery: Basic filter query terms for Lens Scholar Request.
- DateQuery: Date query terms for Lens Scholar Request.
- QueryBuilder: Query builder class to build queries using the above classes.

Notes for Users
---------------
If the argument for any query object (GeneralQuery, AuthorQuery, etc.) can take many options like title, author_display_name, etc., argument can be either single list like *[bool_clause, query_clause, value]* or list of list like *[[bool_clause, query_clause, value], [bool_clause, query_clause, value], ...]*. For example;
- *title=["should", "match_phrase", "Recent advances"]* or *title=[["should", "match_phrase", "Recent advances"], ["should", "match_phrase", "Machine learning"]]*.

**bool_clause**: The condition to be applied. It can be *"must"*, *"should"*, *"must_not"*, or *"filter"*.

**query_clause**: The type of the field. It can be *"term"*, *"terms"*, *"match"*, or *"match_phrase"*.
- Avoid using the Term and Terms queries for text fields. To search text field values, using the Match and Match Phrase queries are recommended instead.
- Use the Term and Terms queries for fields like author_count, publication_year, identifiers, etc.

**value**: The parameter to be searched for. If the query_clause is *"terms"* use a list for the values. For example;
- *author_count=["must", "terms", [1, 2, 3]]*. This will search for all the documents which have 1, 2, or 3 authors.
- *author_display_name=["should", "terms", ["John Doe", "Jane Doe"]]*. This will search for all the documents which have either John Doe or Jane Doe as authors.

RangeQuery and BasicFilterQuery classes are different from other query classes. They can take only list of two elements *[bool_clause, value]*. For example;
- *year_published=["should", 2020]*.
- *is_referenced_by_scholarly=["must", True]*.

For more information, refer to the documentation at https://docs.api.lens.org/request-scholar.html#searchable-fields.

TODO
----
- Check if any arguments have special formatting requirements like ISSN.
'''

from .QueryUtilities import QueryManager
import logging
import re
from typing import Union
from .validator import validate_date_format

class GeneralQuery(QueryManager):
    '''
    Constructs general query parameters for Lens Scholar API requests.

    The GeneralQuery class allows users to create queries for various publication attributes within The Lens Database.

    Parameters
    ----------
    title : list or list of lists, optional
        Conditions for the publication's title as a string.

    abstract : list or list of lists, optional
        Conditions for the publication's abstract content as a string.

    full_text : list or list of lists, optional
        Conditions for the full text of the publication as a string.

    publication_type : list or list of lists, optional
        Type of the publication as a string. Refer to external documentation for accepted values. (Note: case sensitive)

    publication_supplementary_type : list or list of lists, optional
        Supplementary type of the publication as a string. Refer to external documentation for accepted values. (Note: case sensitive)

    external_id_type : list or list of lists, optional
        External identifier type for the publication as a string. Refer to external documentation for accepted values.

    Notes
    -----
    - Ensure proper data formats and refer to the Lens API documentation for detailed guidelines and examples.

    For further guidance and examples, see the API documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    '''

    def __init__(self, 
                 title: Union[list, list[list]] = None, 
                 abstract: Union[list, list[list]] = None, 
                 full_text: Union[list, list[list]] = None,
                 publication_type: Union[list, list[list]] = None,
                 publication_supplementary_type: Union[list, list[list]] = None, 
                 external_id_type: Union[list, list[list]] = None):
        
        super().__init__("GENERAL")
        self.add_arguments(
            title=title,
            abstract=abstract,
            full_text=full_text,
            publication_type=publication_type,
            publication_supplementary_type=publication_supplementary_type,
            external_id_type=external_id_type
        )

class RetractionQuery(QueryManager):
    '''
    Constructs retraction-related query parameters for Lens Scholar API requests.

    The RetractionQuery class provides a structured way to create queries focusing on retraction details of publications within The Lens Database.

    Parameters
    ----------
    retraction_update_date : list or list of lists, optional
        Conditions for the date of the retraction update in *YYYY-MM-DD* format.

    retraction_update_nature : list or list of lists, optional
        Conditions for the nature of the retraction update as a string. Includes options like 'Retraction', 'Expression of Concern', etc.

    retraction_update_reason : list or list of lists, optional
        Conditions for the reason for the retraction update as a string. For a complete list of reasons, refer to the external documentation.

    Methods
    -------
    _update_date_format_check(date: str) -> None
        Internal method to validate the date format for retraction update date. Date must be in *YYYY-MM-DD* format.

    Raises
    ------
    ValueError
        If the date format is invalid.
        
    Notes
    -----
    - Ensure date values follow the required format for accurate query results.
    - Refer to external documentation for exhaustive lists of valid query terms for nature and reasons.

    For further guidance and examples, see the API documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    '''

    def __init__(self, 
                 retraction_update_date: Union[list, list[list]] = None,
                 retraction_update_nature: Union[list, list[list]] = None,
                 retraction_update_reason: Union[list, list[list]] = None):
        
        super().__init__("RETRACTION")
        
        for field, date in locals().items():
            if field != "self" and not field.startswith("__") and date:
                date_format = self.field_details[field]["date_format"]
                validate_date_format(field, date[2], date_format)
        self.add_arguments(
            retraction_update_date = retraction_update_date,
            retraction_update_nature = retraction_update_nature,
            retraction_update_reason = retraction_update_reason
        )

class AuthorQuery(QueryManager):
    """
    Constructs author-related query parameters for Lens Scholar API requests.

    The AuthorQuery class facilitates creating complex queries targeting specific authors or author attributes within The Lens Database.

    Parameters
    ----------
    author_display_name : list or list of lists, optional
        Conditions for the author's display name as a string.

    author_first_name : list or list of lists, optional
        Conditions for the author's first name as a string.

    author_last_name : list or list of lists, optional
        Conditions for the author's last name as a string.

    author_orcid : list or list of lists, optional
        ORCID identifiers for the author as strings.

    author_maqid : list or list of lists, optional
        MAQID of the author as strings.

    author_affiliation_name : list or list of lists, optional
        Conditions for the author's affiliation names as strings.

    author_count : list, optional
        Conditions for the number of authors, with the value type being an integer.

    Notes
    -----
    - Ensure correct data formats for effective query execution.
    - For comprehensive examples and guidance, refer to the API documentation.

    For further guidance and examples, see the API documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, author_display_name: Union[list, list[list]] = None,
                 author_first_name: Union[list, list[list]] = None,
                 author_last_name: Union[list, list[list]] = None,
                 author_orcid: Union[list, list[list]] = None,
                 author_maqid: Union[list, list[list]] = None,
                 author_affiliation_name: Union[list, list[list]] = None,
                 author_count: list = None):
        
        super().__init__("AUTHOR")
        self.add_arguments(
            author_display_name = author_display_name,
            author_first_name = author_first_name,
            author_last_name = author_last_name,
            author_orcid = author_orcid,
            author_maqid = author_maqid,
            author_affiliation_name = author_affiliation_name,
            author_count = author_count
        )

class CitationQuery(QueryManager):
    """
    Constructs citation-related query parameters for Lens Scholar API requests.

    The CitationQuery class allows users to set conditions for citation metrics related to documents within The Lens Database.

    Parameters
    ----------
    reference_lens_id : list or list of lists, optional
        Conditions for the ID of the reference lens, with the value type as str.

    referenced_by_count : list or list of lists, optional
        Conditions for the count of references that cite the document, with the value type as int.

    reference_count : list or list of lists, optional
        Conditions for the count of references cited by the document, with the value type as int.

    referenced_by_patent_lens_id : list or list of lists, optional
        Conditions for the ID of the patent lens that cites the document, with the value type as str.
        (In replace of patent_citation.lens_id)

    referenced_by_patent_count : list or list of lists, optional
        Conditions for the count of patents that cite the document, with the value type as int.
        (In replace of patent_citation_count)

    Notes
    -----
    - Ensure correct data formats to facilitate accurate queries.
    - Refer to the API documentation for full details on field usage and additional examples.
    """

    def __init__(self, 
                 reference_lens_id: Union[list, list[list]] = None,
                 referenced_by_count: Union[list, list[list]] = None,
                 reference_count: Union[list, list[list]] = None,
                 referenced_by_patent_lens_id: Union[list, list[list]] = None, 
                 referenced_by_patent_count: Union[list, list[list]] = None):

        super().__init__("CITATION")
        self.add_arguments(
            reference_lens_id=reference_lens_id,
            referenced_by_count=referenced_by_count,
            reference_count=reference_count,
            referenced_by_patent_lens_id=referenced_by_patent_lens_id,
            referenced_by_patent_count=referenced_by_patent_count
        )

class ExternalIdQuery(QueryManager):
    """
    Constructs external ID query parameters for Lens Scholar API requests.

    The ExternalIdQuery class allows users to set conditions based on various external identifiers for documents within The Lens Database.

    Parameters
    ----------
    doi : list or list of lists, optional
        Conditions for the Digital Object Identifier (DOI) as a string.

    magid : list or list of lists, optional
        Conditions for the Microsoft Academic Graph ID (MAGID) as a string.

    pmid : list or list of lists, optional
        Conditions for the PubMed Identifier (PMID) as a string.

    pmcid : list or list of lists, optional
        Conditions for the PubMed Central Identifier (PMCID) as a string.

    coreid : list or list of lists, optional
        Conditions for the CORE ID as a string.

    openalex : list or list of lists, optional
        Conditions for the OpenAlex ID as a string.

    Notes
    -----
    - Ensure correct data formats for accurate query results.
    - For a comprehensive guide on field usage, see the API documentation.

    For further guidance and examples, see the API documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, 
                 doi: Union[list, list[list]] = None,
                 magid: Union[list, list[list]] = None,
                 pmid: Union[list, list[list]] = None,
                 pmcid: Union[list, list[list]] = None,
                 coreid: Union[list, list[list]] = None,
                 openalex: Union[list, list[list]] = None):
        
        super().__init__("EXTERNAL_ID")
        self.add_arguments(
            doi=doi,
            magid=magid,
            pmid=pmid,
            pmcid=pmcid,
            coreid=coreid,
            openalex=openalex
        )

class SourceQuery(QueryManager):
    """
    Constructs source-related query parameters for Lens Scholar API requests.

    The SourceQuery class allows users to specify conditions for various attributes of a publication's source within The Lens Database.

    Parameters
    ----------
    source_title : list or list of lists, optional
        Conditions for the title of the source as a string.

    source_title_exact : list or list of lists, optional
        Conditions for the exact title of the source as a string. (Note: case sensitive)

    source_publisher : list or list of lists, optional
        Conditions for the publisher of the source as a string.

    source_country : list or list of lists, optional
        Conditions for the country of the source as a string. (Note: case sensitive)

    source_asjc_code : list or list of lists, optional
        Conditions for the ASJC code of the source as a string.

    source_issn : list or list of lists, optional
        Conditions for the ISSN of the source as a string. Accepts both hyphenated and non-hyphenated formats. (Note: case sensitive)

    Notes
    -----
    - Pay attention to case sensitivity where indicated to ensure accurate queries.
    - For further details on field usage, see the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, 
                 source_title: Union[list, list[list]] = None, 
                 source_title_exact: Union[list, list[list]] = None,
                 source_publisher: Union[list, list[list]] = None,
                 source_country: Union[list, list[list]] = None,
                 source_asjc_code: Union[list, list[list]] = None,
                 source_issn: Union[list, list[list]] = None):
        
        super().__init__("SOURCE")

        # Normalize ISSN given in list using an internal method
        try:
            if source_issn and isinstance(source_issn, list) and len(source_issn) == 3:
                source_issn[2] = self._normalize_issn(source_issn[2])
        except:
            pass

        self.add_arguments(
            source_title=source_title,
            source_title_exact=source_title_exact,
            source_publisher=source_publisher,
            source_country=source_country,
            source_asjc_code=source_asjc_code,
            source_issn=source_issn
        )

    def _normalize_issn(self, issn: str) -> str:
        """
        Internal method to normalize the ISSN to XXXXXXXx format by removing hyphens and validating.
        
        Parameters
        ----------
        issn : str
            The ISSN input by the user.
        
        Returns
        -------
        str
            A normalized ISSN in XXXXXXXx format.
        
        Raises
        ------
        ValueError
            If the ISSN is not valid.
        """
        # Remove hyphens
        normalized_issn = issn.replace('-', '')
        
        # Validate ISSN format (7 digits followed by a digit or 'x'). For example, 1234-567x will turn into 1234567x
        if re.match(r'^\d{7}[0-9Xx]$', normalized_issn):
            return normalized_issn.lower()  # Return normalized ISSN in lowercase
        else:
            raise ValueError(f"Invalid ISSN format: {issn}")

class SubjectMatterQuery(QueryManager):
    '''
    Constructs query parameters related to subject matter for Lens Scholar API requests.

    The SubjectMatterQuery class allows users to define search criteria based on various attributes of a publication's subject matter within The Lens Database.

    Parameters
    ----------
    field_of_study : list or list of lists, optional
        Conditions for the field of study as a string.

    source_asjc_subject : list or list of lists, optional
        Conditions for the ASJC subject of the source as a string.

    keyword : list or list of lists, optional
        Conditions for keywords as a string. (Note: case sensitive)

    chemical_mesh_ui : list or list of lists, optional
        Conditions for the MeSH UI of the chemical as a string. (Note: case sensitive)

    chemical_registry_number : list or list of lists, optional
        Conditions for the registry number of the chemical as a string.

    chemical_substance_name : list or list of lists, optional
        Conditions for the name of the chemical substance as a string.

    mesh_term_mesh_heading : list or list of lists, optional
        Conditions for the MeSH heading of the term as a string. (Note: case sensitive)

    mesh_term_mesh_ui : list or list of lists, optional
        Conditions for the MeSH UI of the term as a string. (Note: case sensitive)

    Notes
    -----
    - Pay attention to case sensitivity where indicated to ensure accurate queries.
    - For further details on field usage and comprehensive examples, refer to the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    '''

    def __init__(self, 
                 field_of_study: Union[list, list[list]] = None,
                 source_asjc_subject: Union[list, list[list]] = None,
                 keyword: Union[list, list[list]] = None,
                 chemical_mesh_ui: Union[list, list[list]] = None,
                 chemical_registry_number: Union[list, list[list]] = None,
                 chemical_substance_name: Union[list, list[list]] = None,
                 mesh_term_mesh_heading: Union[list, list[list]] = None,
                 mesh_term_mesh_ui: Union[list, list[list]] = None):
        
        super().__init__("SUBJECT_MATTER")
        self.add_arguments(
            field_of_study=field_of_study,
            source_asjc_subject=source_asjc_subject,
            keyword=keyword,
            chemical_mesh_ui=chemical_mesh_ui,
            chemical_registry_number=chemical_registry_number,
            chemical_substance_name=chemical_substance_name,
            mesh_term_mesh_heading=mesh_term_mesh_heading,
            mesh_term_mesh_ui=mesh_term_mesh_ui
        )

class InstitutionQuery(QueryManager):
    """
    Constructs institution-related query parameters for Lens Scholar API requests.

    The InstitutionQuery class enables users to define search criteria based on various attributes of author affiliations within The Lens Database.

    Parameters
    ----------
    author_affiliation_name_exact : list or list of lists, optional
        Conditions for the exact name of the author's affiliation as a string. (Note: case sensitive)

    author_affiliation_name_original : list or list of lists, optional
        Conditions for the original name of the author's affiliation as a string.

    author_affiliation_ror_id : list or list of lists, optional
        Conditions for the ROR ID of the author's affiliation as a string. (Note: case sensitive)

    author_affiliation_ror_id_lineage : list or list of lists, optional
        Conditions for the lineage of the ROR ID of the author's affiliation as a string. (Note: case sensitive)

    author_affiliation_address_city : list or list of lists, optional
        Conditions for the city of the author's affiliation as a string. (Note: case sensitive)

    author_affiliation_address_state_code : list or list of lists, optional
        Conditions for the state code of the author's affiliation as a string. (Note: case sensitive)

    author_affiliation_address_country_code : list or list of lists, optional
        Conditions for the country code of the author's affiliation as a string. (Note: case sensitive)

    author_affiliation_type : list or list of lists, optional
        Conditions for the type of the author's affiliation as a string. (Note: case sensitive)

    Notes
    -----
    - Pay attention to case sensitivity where indicated to ensure accurate queries.
    - For more detailed guidelines and examples, refer to the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, 
                 author_affiliation_name_exact: Union[list, list[list]] = None,
                 author_affiliation_name_original: Union[list, list[list]] = None,
                 author_affiliation_ror_id: Union[list, list[list]] = None,
                 author_affiliation_ror_id_lineage: Union[list, list[list]] = None,
                 author_affiliation_address_city: Union[list, list[list]] = None,
                 author_affiliation_address_state_code: Union[list, list[list]] = None,
                 author_affiliation_address_country_code: Union[list, list[list]] = None,
                 author_affiliation_type: Union[list, list[list]] = None):
        
        super().__init__("INSTITUTIONS")
        self.add_arguments(
            author_affiliation_name_exact=author_affiliation_name_exact,
            author_affiliation_name_original=author_affiliation_name_original,
            author_affiliation_ror_id=author_affiliation_ror_id,
            author_affiliation_ror_id_lineage=author_affiliation_ror_id_lineage,
            author_affiliation_address_city=author_affiliation_address_city,
            author_affiliation_address_state_code=author_affiliation_address_state_code,
            author_affiliation_address_country_code=author_affiliation_address_country_code,
            author_affiliation_type=author_affiliation_type
        )

class FundingQuery(QueryManager):
    """
    Constructs funding-related query parameters for Lens Scholar API requests.

    The FundingQuery class enables users to define search criteria based on various attributes of funding information within The Lens Database.

    Parameters
    ----------
    funding_country : list or list of lists, optional
        Conditions for the country of the funding as a string.

    funding_funding_id : list or list of lists, optional
        Conditions for the ID of the funding as a string. (Note: case sensitive)

    funding_organisation : list or list of lists, optional
        Conditions for the organisation providing the funding as a string.

    funding_organisation_exact : list or list of lists, optional
        Conditions for the exact name of the funding organisation as a string. (Note: case sensitive)

    Notes
    -----
    - Pay attention to case sensitivity where indicated to ensure accurate queries.
    - For further details and examples, refer to the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, 
                 funding_country: Union[list, list[list]] = None,
                 funding_funding_id: Union[list, list[list]] = None,
                 funding_organisation: Union[list, list[list]] = None,
                 funding_organisation_exact: Union[list, list[list]] = None):
        
        super().__init__("FUNDING")
        self.add_arguments(
            funding_country=funding_country,
            funding_funding_id=funding_funding_id,
            funding_organisation=funding_organisation,
            funding_organisation_exact=funding_organisation_exact
        )

class ConferencesQuery(QueryManager):
    """
    Constructs conference-related query parameters for Lens Scholar API requests.

    The ConferencesQuery class enables users to define search criteria based on various attributes of conferences within The Lens Database.

    Parameters
    ----------
    conference_name : list or list of lists, optional
        Conditions for the name of the conference as a string.

    conference_instance : list or list of lists, optional
        Conditions for the instance of the conference as a string. (Note: case sensitive)

    conference_location : list or list of lists, optional
        Conditions for the location of the conference as a string. (Note: case sensitive)

    Notes
    -----
    - Pay attention to case sensitivity where indicated to ensure accurate queries.
    - For further details and examples, refer to the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, 
                 conference_name: Union[list, list[list]] = None, 
                 conference_instance: Union[list, list[list]] = None,
                 conference_location: Union[list, list[list]] = None):
        
        super().__init__("CONFERENCES")
        self.add_arguments(
            conference_name=conference_name,
            conference_instance=conference_instance,
            conference_location=conference_location
        )

class ClinicalTrialsQuery(QueryManager):
    """
    Constructs clinical trial query parameters for Lens Scholar API requests.

    The ClinicalTrialsQuery class enables users to define search criteria based on various attributes of clinical trials within The Lens Database.

    Parameters
    ----------
    clinical_trial_registry : list or list of lists, optional
        Conditions for the registry of the clinical trial as a string. (Note: case sensitive)

    clinical_trial_trial_id : list or list of lists, optional
        Conditions for the ID of the clinical trial as a string. (Note: case sensitive)

    Notes
    -----
    - Pay attention to case sensitivity where indicated to ensure accurate queries.
    - For further details and examples, refer to the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, 
                 clinical_trial_registry: Union[list, list[list]] = None, 
                 clinical_trial_trial_id: Union[list, list[list]] = None):
        
        super().__init__("CLINICAL_TRIALS")
        self.add_arguments(
            clinical_trial_registry=clinical_trial_registry,
            clinical_trial_trial_id=clinical_trial_trial_id
        )

class OpenAccessQuery(QueryManager):
    """
    Constructs open access query parameters for Lens Scholar API requests.

    The OpenAccessQuery class enables users to define search criteria based on various attributes of open access publications within The Lens Database.

    Parameters
    ----------
    open_access_colour : list or list of lists, optional
        Conditions for the colour of the open access as a string. (Note: case sensitive)

    open_access_license : list or list of lists, optional
        Conditions for the license of the open access as a string. (Note: case sensitive)

    Notes
    -----
    - Pay attention to case sensitivity where indicated to ensure accurate queries.
    - For further details and examples, refer to the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """

    def __init__(self, 
                 open_access_colour: Union[list, list[list]] = None,
                 open_access_license: Union[list, list[list]] = None):
        
        super().__init__("OPEN_ACCESS")
        self.add_arguments(
            open_access_colour=open_access_colour,
            open_access_license=open_access_license
        )

class DateQuery(QueryManager):
    """
    Constructs date-related query parameters for Lens Scholar API requests.

    The DateQuery class allows users to set conditions based on various date attributes of documents within The Lens Database.

    Parameters
    ----------
    year_published : list or list of lists, optional
        Conditions for the year of publication as an integer.
    
    date_published : list or list of lists, optional
        Conditions for the date of publication as a string in *YYYY-MM-DD* format.

    created : list or list of lists, optional
        Conditions for the creation date as a string in *YYYY-MM-DDTHH:MM:SS%z* format.

    Notes
    -----
    - Ensure correct data formats for accurate query results.
    - For further details and examples, refer to the API documentation.
    - **Do not use Elasticsearch range queries for date fields like gte, lte, etc.**
    - **For range queries, use the "RangeQuery" class instead.**

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#searchable-fields.
    """
    def __init__(self, 
                 year_published: Union[list, list[list]] = None,
                 date_published: Union[list, list[list]] = None,
                 created: Union[list, list[list]] = None):
        super().__init__("DATE")

        # Validate date formats for date fields
        for field, date in locals().items():
            if field != "self" and not field.startswith("__") and date:
                accepted_date_format = self.field_details[field]["date_format"]
                print(date[2])
                validate_date_format(field, date[2], self.field_details[field]["date_format"])

        self.add_arguments(
            year_published=year_published,
            date_published=date_published,
            created=created
        )

class BasicFilterQuery(QueryManager):
    """
    Constructs basic filter query parameters for Lens Scholar API requests.

    The BasicFilterQuery class provides filtering options based on boolean attributes of documents within The Lens Database.
    BasicFilterQeury class is different from other query classes. Argument can take a list of two elements ["bool_clause", "value"]

    Parameters
    ----------
    is_referenced_by_scholarly : list, optional
        Filter documents referenced by scholarly documents. Value type is bool.

    has_patent_citations : list, optional
        Filter documents with patent citations. Value type is bool.

    has_affiliation : list, optional
        Filter documents with an affiliation. Value type is bool.

    has_affiliation_grid : list, optional
        Filter documents with an affiliation grid. Value type is bool.

    has_affiliation_ror : list, optional
        Filter documents with an affiliation ROR. Value type is bool.

    has_orcid : list, optional
        Filter documents with an ORCID. Value type is bool.

    has_mesh_term : list, optional
        Filter documents with a MeSH term. Value type is bool.

    has_chemical : list, optional
        Filter documents with a chemical. Value type is bool.

    has_keyword : list, optional
        Filter documents with a keyword. Value type is bool.

    has_clinical_trial : list, optional
        Filter documents with a clinical trial. Value type is bool.

    has_field_of_study : list, optional
        Filter documents with a field of study. Value type is bool.

    has_abstract : list, optional
        Filter documents with an abstract. Value type is bool.

    has_full_text : list, optional
        Filter documents with full text. Value type is bool.

    has_funding : list, optional
        Filter documents with funding. Value type is bool.

    is_open_access : list, optional
        Filter documents that are open access. Value type is bool.

    in_analytics_set : list, optional
        Filter documents in the analytics set. Value type is bool.

    source_is_diamond : list, optional
        Filter documents where the source is diamond. Value type is bool.

    Notes
    -----
    - Ensure boolean values are used to facilitate accurate filtering.
    - For further details and examples, refer to the API documentation.

    For more information, refer to the documentation at:
    https://docs.api.lens.org/request-scholar.html#filtering.
    """

    def __init__(self,
                 is_referenced_by_scholarly: list = None,
                 has_patent_citations: list = None,
                 has_affiliation: list = None,
                 has_affiliation_grid: list = None,
                 has_affiliation_ror: list = None,
                 has_orcid: list = None,
                 has_mesh_term: list = None,
                 has_chemical: list = None,
                 has_keyword: list = None,
                 has_clinical_trial: list = None,
                 has_field_of_study: list = None,
                 has_abstract: list = None,
                 has_full_text: list = None,
                 has_funding: list = None,
                 is_open_access: list = None,
                 in_analytics_set: list = None,
                 source_is_diamond: list = None,
                 is_retracted: list = None):
        
        super().__init__("BOOLEAN_FILTERS")
        self.add_bool_arguments(
            is_referenced_by_scholarly=is_referenced_by_scholarly,
            has_patent_citations=has_patent_citations,
            has_affiliation=has_affiliation,
            has_affiliation_grid=has_affiliation_grid,
            has_affiliation_ror=has_affiliation_ror,
            has_orcid=has_orcid,
            has_mesh_term=has_mesh_term,
            has_chemical=has_chemical,
            has_keyword=has_keyword,
            has_clinical_trial=has_clinical_trial,
            has_field_of_study=has_field_of_study,
            has_abstract=has_abstract,
            has_full_text=has_full_text,
            has_funding=has_funding,
            is_open_access=is_open_access,
            in_analytics_set=in_analytics_set,
            source_is_diamond=source_is_diamond,
            is_retracted=is_retracted
        )

class RangeQuery(QueryManager):
    """
    Constructs range query parameters for Lens Scholar API requests.

    The RangeQuery class allows users to set Elasticsearch range queries for date and numeric fields within The Lens Database.
    RangeQuery class is different from other query classes. Argument can take a list of two elements ["bool_clause", "range_query"]:

    - range_query is a dictionary consisting of "gt/e" or "lt/e" keys or a combination of both.

    Parameters
    ----------
    date_published : list, optional
        Range query for the date of publication. Format: "YYYY-MM-DD".

    year_published : list, optional
        Range query for the year of publication. Format: YYYY.

    created : list, optional
        Range query for the creation date. Format: "YYYY-MM-DD".

    retraction_update_date : list, optional
        Range query for the date of the retraction update. Format: "YYYY-MM-DD".

    author_count : list, optional
        Range query for the number of authors. Value type is int.

    referenced_by_count : list, optional
        Range query for the count of references that cite the document. Value type is int.

    reference_count : list, optional
        Range query for the count of references cited by the document. Value type is int.

    referenced_by_patent_count : list, optional
        Range query for the count of patents that cite the document. Value type is int.

    Notes
    -----
    - Ensure correct data formats for accurate range queries.
    - Do not use same field in RangeQuery instance and other query instances. Results may not be as expected.
    - For further details and examples, refer to the API documentation.
    """
    def __init__(self,
                 date_published: list= None,
                 year_published: list = None,
                 created: list = None,
                 retraction_update_date: list = None,
                 author_count: list = None,
                 referenced_by_count: list = None,
                 reference_count: list = None,
                 referenced_by_patent_count: list = None):
        super().__init__("RANGE")

        self.add_range_arguments(
            date_published=date_published,
            year_published=year_published,
            created=created,
            retraction_update_date=retraction_update_date,
            author_count=author_count,
            referenced_by_count=referenced_by_count,
            reference_count=reference_count,
            referenced_by_patent_count=referenced_by_patent_count
        )

class QueryBuilder:
    '''
    Query builder to combine multiple query objects into a single query.

    Parameters
    ----------
    kwargs : QueryManager
        The query objects to be combined.

    Attributes
    ----------
    query_objects : QueryManager
        The query objects to be combined.
    query_string : dict
        The combined query object.

    Raises
    ------
    ValueError
        If the query object is not an instance of QueryManager.

    Returns
    -------
    dict
        The combined query object.

    Example
    -------
    >>> query1 = GeneralQuery(title=[["must", "term", "covid-19"]])
    >>> query2 = AuthorQuery(author_last_name=[["must", "term", "smith"]])
    >>> query_builder = QueryBuilder(query1, query2)
    >>> query_builder.query_string
    {'bool': {'must': [{'term': {'title': 'covid-19'}}, {'term': {'author_last_name': 'smith'}]}}    
    '''

    def __init__(self, *kwargs):
        self.query_objects = kwargs
        self.query_string = {
            "bool": {
                "must": [],
                "should": [],
                "must_not": [],
                "filter": []
            }
        }

        self._check_query_objects()
        self._build_query()
        self._clean_query()

    def _check_query_objects(self):
        '''
        Check if the query objects are instances of QueryManager.

        Raises
        ------
        ValueError
            If the query object is not an instance of QueryManager.

        Returns
        -------
        None
        '''

        for query_object in self.query_objects:
            if not isinstance(query_object, QueryManager):
                raise ValueError(f"Invalid query object: {query_object}")
    
    def _build_query(self):
        '''
        Build the query object by combining the query objects.
        
        Returns
        -------
        dict
            The combined query object.
        '''
        try:
            for query_object in self.query_objects:
                self.query_string["bool"]["must"] += query_object.output.get("must", [])
                self.query_string["bool"]["should"] += query_object.output.get("should", [])
                self.query_string["bool"]["must_not"] += query_object.output.get("must_not", [])
                self.query_string["bool"]["filter"] += query_object.output.get("filter", [])
        except Exception as e:
            logging.error(e)
        return self.query_string
    
    def _clean_query(self):
        '''
        Clean the query object by removing empty fields.

        Returns
        -------
        dict
            The cleaned query object.
        '''
        if not self.query_string["bool"]["must"]:
            self.query_string["bool"].pop("must")
        if not self.query_string["bool"]["should"]:
            self.query_string["bool"].pop("should")
        if not self.query_string["bool"]["must_not"]:
            self.query_string["bool"].pop("must_not")
        if not self.query_string["bool"]["filter"]:
            self.query_string["bool"].pop("filter")
        return self.query_string


class SortQuery(QueryManager):
    # TODO: Implement SortQuery class with Sort query for sorting results
    pass

class ProjectionQuery(QueryManager):
    # TODO: Implement ProjectionQuery class for include and exclude fields
    pass

if __name__ == "__main__":
    pass