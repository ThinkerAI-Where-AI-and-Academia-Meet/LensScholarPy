'''
Module to define the search fields in different categories for the Lens API.
For more information, refer to the documentation at https://docs.api.lens.org/request-scholar.html#searchable-fields

The parameters are defined as dictionaries with the following keys
- query_name: the name of the parameter in the API
- accepted_type: the accepted type for the parameter
- restrictions: the accepted values for the parameter

CATEGORIES
---------
- GENERAL
- RETRACTION
- AUTHOR
- CITATION
- EXTERNAL_ID
- SOURCE
- SUBJECT_MATTER
- INSTITUTIONS
- FUNDING
- CONFERENCES
- CLINICAL_TRIALS
- OPEN_ACCESS
- DATE
- BOOLEAN_FILTERS
- RANGE

GENERAL
-------
- title (str): The title of the publication. No restricted values.
- abstract (str): The abstract of the publication. No restricted values.
- full_text (str): The full text of the publication. No restricted values.
- publication_type (str): The type of publication. Accepted values:
    - conference proceedings
    - book chapter
    - journal article
    - component
    - conference proceedings article
    - dataset
    - libguide
    - reference entry
    - book
- publication_supplementary_type (str): The supplementary type of publication. Accepted values:
    - review
    - comparative study
    - research support
- external_id_type (str): The type of external ID. Accepted values:
    - doi
    - magid
    - pmid
    - pmcid
    - coreid
    - openalex

RETRACTION
----------
- retraction_update_date (str): The date of the retraction update. Format: YYYY-MM-DD.
- retraction_update_nature (str): The nature of the retraction update. Accepted values:
    - Retraction
    - Expression of Concern
    - Correction
    - Reinstatement
- retraction_update_reason (str): The reason for the retraction update. Accepted values:
    - Author Unresponsive
    - Bias Issues or Lack of Balance
    - Breach of Policy by Author
    - Check for below for more values...

AUTHOR
------
- author_display_name (str): The display name of the author. No restricted values.
- author_first_name (str): The first name of the author. No restricted values.
- author_last_name (str): The last name of the author. No restricted values.
- author_orcid (str): The ORCID of the author. No restricted values.
- author_maqid (str): The MAQID of the author. No restricted values.
- author_affiliation_name (str): The affiliation name of the author. No restricted values.
- author_count (int): The number of authors. No restricted values.

CITATION
--------
- reference_lens_id (str): The Lens ID of the reference. No restricted values.
- referenced_by_count (int): The number of references. No restricted values.
- reference_count (int): The number of references. No restricted values.
- referenced_by_patent_lens_id (str): The Lens ID of the patent reference. No restricted values.
- referenced_by_patent_count (int): The number of patent references. No restricted values.

EXTERNAL_ID
-----------
- doi (str): The DOI of the publication. No restricted values.
- magid (str): The MAG ID of the publication. No restricted values.
- pmid (str): The PMID of the publication. No restricted values.
- pmcid (str): The PMCID of the publication. No restricted values.
- coreid (str): The CORE ID of the publication. No restricted values.
- openalex (str): The OpenAlex ID of the publication. No restricted values.

SOURCE
------
- source_title (str): The title of the source. No restricted values.
- source_title_exact (str): The exact title of the source. No restricted values.
- source_publisher (str): The publisher of the source. No restricted values.
- source_country (str): The country of the source. No restricted values.
- source_asjc_code (str): The ASJC code of the source. No restricted values.
- source_issn (str): The ISSN of the source. No restricted values.

SUBJECT_MATTER
--------------
- field_of_study (str): The field of study. No restricted values.
- source_asjc_subject (str): The ASJC subject of the source. No restricted values.
- keyword (str): The keyword of the publication. No restricted values.
- chemical_mesh_ui (str): The Mesh UI of the chemical. No restricted values.
- chemical_registry_number (str): The registry number of the chemical. No restricted values.
- chemical_substance_name (str): The name of the chemical. No restricted values.
- mesh_term_mesh_heading (str): The Mesh heading of the term. No restricted values.
- mesh_term_mesh_ui (str): The Mesh UI of the term. No restricted values.

INSTITUTIONS
------------
- author_affiliation_name_exact (str): The exact name of the affiliation. No restricted values.
- author_affiliation_name_original (str): The original name of the affiliation. No restricted values.
- author_affiliation_ror_id (str): The ROR ID of the affiliation. No restricted values.
- author_affiliation_ror_id_lineage (str): The ROR ID lineage of the affiliation. No restricted values.
- author_affiliation_address_city (str): The city of the affiliation. No restricted values.
- author_affiliation_address_state_code (str): The state code of the affiliation. No restricted values.
- author_affiliation_address_country_code (str): The country code of the affiliation. No restricted values.
- author_affiliation_type (str): The type of affiliation. No restricted values.

FUNDING
-------
- funding_country (str): The country of the funding. No restricted values.
- funding_funding_id (str): The funding ID. No restricted values.
- funding_organisation (str): The organisation of the funding. No restricted values.
- funding_organisation_exact (str): The exact organisation of the funding. No restricted values.

CONFERENCES
-----------
- conference_name (str): The name of the conference. No restricted values.
- conference_instance (str): The instance of the conference. No restricted values.
- conference_location (str): The location of the conference. No restricted values.

CLINICAL_TRIALS
---------------
- clinical_trial_registry (str): The registry of the clinical trial. No restricted values.
- clinical_trial_trial_id (str): The trial ID of the clinical trial. No restricted values.

OPEN_ACCESS
-----------
- open_access_colour (str): The colour of the open access. No restricted values.
- open_access_license (str): The license of the open access. No restricted values.

DATE
-----
- date_published (str): The date of publication. Format: YYYY-MM-DD.
- year_published (int): The year of publication. Format: YYYY.
- created (str): The date of creation. Format: YYYY-MM-DD.

BOOLEAN_FILTERS
---------------
- is_referenced_by_scholarly (bool): Filter by whether the document is referenced by scholarly. No restricted values.
- has_patent_citations (bool): Filter by whether the document has patent citations. No restricted values.
- has_affiliation (bool): Filter by whether the document has an affiliation. No restricted values.
- has_affiliation_grid (bool): Filter by whether the document has an affiliation with a GRID ID. No restricted values.
- has_affiliation_ror (bool): Filter by whether the document has an affiliation with a ROR ID. No restricted values.
- has_orcid (bool): Filter by whether the document has an ORCID. No restricted values.
- has_mesh_term (bool): Filter by whether the document has a MeSH term. No restricted values.
- has_chemical (bool): Filter by whether the document has a chemical. No restricted values.
- has_keyword (bool): Filter by whether the document has a keyword. No restricted values.
- has_clinical_trial (bool): Filter by whether the document has a clinical trial. No restricted values.
- has_field_of_study (bool): Filter by whether the document has a field of study. No restricted values.
- has_abstract (bool): Filter by whether the document has an abstract. No restricted values.
- has_full_text (bool): Filter by whether the document has full text. No restricted values.
- has_funding (bool): Filter by whether the document has funding. No restricted values.
- is_open_access (bool): Filter by whether the document is open access. No restricted values.
- in_analytics_set (bool): Filter by whether the document is in an analytics set. No restricted values.
- source.is_diamond (bool): Filter by whether the source is a diamond source. No restricted values.
- is_retracted (bool): Filter by whether the document is retracted. No restricted values.

RANGE
-----
- date_published (str): The date of publication. Format: YYYY-MM-DD.
- year_published (int): The year of publication. Format: YYYY.
- created (str): The date of creation. Format: YYYY-MM-DD.
- retraction_update_date (str): The date of the retraction update. Format: YYYY-MM-DD.
- author_count (int): The number of authors. No restricted values.
- referenced_by_count (int): The number of references. No restricted values.
- reference_count (int): The number of references. No restricted values.
- referenced_by_patent_count (int): The number of patent references. No restricted values.

TODO
----
- Check if the parameter are case-sensitive and update the documentation accordingly.
- Add Regex for the accepted values which are case-sensitive or have specific formats, like ISSN should be in format XXXXXXXX.
- Turn these dictionaries into json files for easier access and modification.
'''

### SEARCHABLE FIELDS ###
GENERAL = {
    'title': {
        'query_name'        : 'title',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'abstract': {
        'query_name'        : 'abstract',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'full_text': {
        'query_name'        : 'full_text',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'publication_type': {
        'query_name'        : 'publication_type',
        'accepted_type'     : str,
        'restrictions'      : ['journal article',
                               'book chapter',
                               'component',
                               'conference proceedings article',
                               'dataset',
                               'book',
                               'dissertation',
                               'preprint',
                               'libguide',
                               'journal issue',
                               'report',
                               'conference proceedings',
                               'reference entry',
                               'unknown',
                               'other'
                               ]
    },
    'publication_supplementary_type': {
        'query_name'        : 'publication_supplementary_type',
        'accepted_type'     : str,
        'restrictions'      : ['review',
                               'standart',
                               'editorial',
                               'letters',
                               'news',
                               'journal',
                               'clinical trial',
                               'journal volume',
                               'clinical stduy',
                               'working paper'
                               ]
    },
    'external_id_type': {
        'query_name'        : 'external_id_type',
        'accepted_type'     : str,
        'restrictions'      : ['doi',
                               'magid',
                               'pmid',
                               'pmcid',
                               'coreid',
                               'openalex'
                              ]
    }
}

RETRACTION = {
    'retraction_update_date' : {
        'query_name'        : 'retraction_update.date',
        'accepted_type'     : str,
        'restrictions'      : None,
        'date_format'       : '%Y-%m-%d'
    },
    'retraction_update_nature' : {
        'query_name'        : 'retraction_update.nature',
        'accepted_type'     : str,
        'restrictions'      : ['Retraction',
                               'Expression of Concern',
                               'Correction',
                               'Reinstatement'
                              ]
    },
    'retraction_update_reason' : {
        'query_name'        : 'retraction_update.reason',
        'accepted_type'     : str,
        'restrictions'      : ['Author Unresponsive',
                               'Bias Issues or Lack of Balance',
                               'Breach of Policy by Author',
                               'Cites Retracted Work',
                               'Civil Proceedings',
                               'Complaints about Author',
                               'Complaints about Company/Institution',
                               'Complaints about Third Party',
                               'Concerns/Issues about Animal Welfare',
                               'Concern/Issues about Article',
                               'Concerns/Issues About Authorship/Affiliation',
                               'Concerns/Issues About Data',
                               'Concerns/Issues about Human Subject Welfare',
                               'Concerns/Issues About Image',
                               'Concerns/Issues about Referencing/Attributions',
                               'Concerns/Issues About Results',
                               'Concerns/Issues about Third Party Involvement',
                               'Concerns/Issues with Peer Review',
                               'Conflict of Interest',
                               'Contamination of Cell Lines/Tissues',
                               'Contamination of Materials',
                               'Copyright Claims',
                               'Criminal Proceedings',
                               'Date of Retraction/Other Unknown',
                               'Doing the Right Thing',
                               'Duplication of Article',
                               'Duplication of Data',
                               'Duplication of Image',
                               'Duplication of Text',
                               'Duplicate Publication through Error by Journal/Publisher',
                               'EOC Lifted',
                               'Error by Journal/Publisher',
                               'Error by Third Party',
                               'Error in Analyses',
                               'Error in Cell Lines/Tissues',
                               'Error in Data',
                               'Error in Image',
                               'Error in Materials (General)',
                               'Error in Methods',
                               'Error in Results and/or Conclusions',
                               'Error in Text',
                               'Ethical Violations by Author',
                               'Ethical Violations by Third Party',
                               'Euphemisms for Duplication',
                               'Euphemisms for Misconduct',
                               'Euphemisms for Plagiarism',
                               'Fake Peer Review',
                               'Falsification/Fabrication of Data',
                               'Falsification/Fabrication of Image',
                               'Falsification/Fabrication of Results',
                               'Forged Authorship',
                               'Hoax Paper',
                               'Informed/Patient Consent – None/Withdrawn'
                               'Investigation by Company/Institution',
                               'Investigation by Journal/Publisher',
                               'Investigation by ORI',
                               'Investigation by Third Party',
                               'Lack of Approval from Author',
                               'Lack of Approval from Company/Institution',
                               'Lack of Approval from Third Party',
                               'Lack of IRB/IACUC Approval',
                               'Legal Reasons/Legal Threats',
                               'Manipulation of Images',
                               'Manipulation of Results',
                               'Miscommunication by Author',
                               'Miscommunication by Company/Institution',
                               'Miscommunication by Journal/Publisher',
                               'Miscommunication by Third Party',
                               'Misconduct – Official Investigation/Finding',
                               'Misconduct by Author',
                               'Misconduct by Company/Institution',
                               'Misconduct by Third Party',
                               'No Further Action',
                               'Nonpayment of Fees/Refusal to Pay',
                               'Notice – Lack of',
                               'Notice – Limited or No Information',
                               'Notice – Unable to Access via current resources',
                               'Objections by Author(s)',
                               'Objections by Company/Institution',
                               'Objections by Third Party',
                               'Original Data not Provided',
                               'Paper Mill',
                               'Plagiarism of Article',
                               'Plagiarism of Data',
                               'Plagiarism of Image',
                               'Plagiarism of Text',
                               'Publishing Ban',
                               'Randomly Generated Content',
                               'Results Not Reproducible',
                               'Retract and Replace',
                               'Rogue Editor',
                               'Sabotage of Materials',
                               'Sabotage of Methods',
                               'Salami Slicing',
                               'Taken from Dissertation/Thesis',
                               'Temporary Removal',
                               'Transfer of Copyright/Ownership',
                               'Unreliable Data',
                               'Unreliable Image',
                               'Unreliable Results',
                               'Updated to Correction',
                               'Updated to Retraction',
                               'Upgrade/Update of Prior Notice',
                               'Removed',
                               'Withdrawn (out of date)',
                               'Withdrawn to Publish in Different Journal'
                                ]
    }
}

AUTHOR = {
    'author_display_name': {
        'query_name'        : 'author.display_name',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_first_name': {
        'query_name'        : 'author.first_name',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_last_name': {
        'query_name'        : 'author.last_name',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_orcid': {
        'query_name'        : 'author.orcid',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_maqid': {
        'query_name'        : 'author.maqid',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_name': {
        'query_name'        : 'author.affiliation.name',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_count': {
        'query_name'        : 'author_count',
        'accepted_type'     : int,
        'restrictions'      : None
    }
}

CITATION = {
    'reference_lens_id': {
        'query_name'        : 'reference_lens_id',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'referenced_by_count': {
        'query_name'        : 'referenced_by_count',
        'accepted_type'     : int,
        'restrictions'      : None
    },
    'reference_count': {
        'query_name'        : 'reference_count',
        'accepted_type'     : int,
        'restrictions'      : None
    },
    'referenced_by_patent_lens_id': {
        'query_name'        : 'referenced_by_patent.lens_id',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'referenced_by_patent_count': {
        'query_name'        : 'referenced_by_patent_count',
        'accepted_type'     : int,
        'restrictions'      : None
    }
}

EXTERNAL_ID = {
    'doi': {
        'query_name'        : 'doi',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'magid': {
        'query_name'        : 'magid',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'pmid': {
        'query_name'        : 'pmid',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'pmcid': {
        'query_name'        : 'pmcid',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'coreid': {
        'query_name'        : 'coreid',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'openalex': {
        'query_name'        : 'openalex',
        'accepted_type'     : str,
        'restrictions'      : None
    }
}

SOURCE = {
    'source_title': {
        'query_name'        : 'source.title',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'source_title_exact': {
        'query_name'        : 'source.title.exact',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'source_publisher': {
        'query_name'        : 'source.publisher',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'source_country': {
        'query_name'        : 'source.country',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'source_asjc_code': {
        'query_name'        : 'source.asjc_code',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'source_issn': {
        'query_name'        : 'source.issn',
        'accepted_type'     : str,
        'restrictions'      : None
    },
}

SUBJECT_MATTER = {
    'field_of_study': {
        'query_name'        : 'field_of_study',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'source_asjc_subject': {
        'query_name'        : 'source.asjc_subject',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'keyword': {
        'query_name'        : 'keyword',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'chemical_mesh_ui': {
        'query_name'        : 'chemical.mesh_ui',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'chemical_registry_number': {
        'query_name'        : 'chemical.registry_number',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'chemical_substance_name': {
        'query_name'        : 'chemical.substance_name',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'mesh_term_mesh_heading': {
        'query_name'        : 'mesh_term.mesh_heading',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'mesh_term_mesh_ui': {
        'query_name'        : 'mesh_term.mesh_ui',
        'accepted_type'     : str,
        'restrictions'      : None
    }
}

INSTITUTIONS = {
    'author_affiliation_name_exact': {
        'query_name'        : 'author.affiliation.name.exact',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_name_original': {
        'query_name'        : 'author.affiliation.name.original',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_ror_id': {
        'query_name'        : 'author.affiliation.ror_id',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_ror_id_lineage': {
        'query_name'        : 'author.affiliation.ror_id_lineage',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_address_city': {
        'query_name'        : 'author.affiliation.address.city',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_address_state_code': {
        'query_name'        : 'author.affiliation.address.state_code',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_address_country_code': {
        'query_name'        : 'author.affiliation.address.country_code',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'author_affiliation_type': {
        'query_name'        : 'author.affiliation.type',
        'accepted_type'     : str,
        'restrictions'      : None
    }
}

FUNDING = {
    'funding_country': {
        'query_name'        : 'funding.country',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'funding_funding_id': {
        'query_name'        : 'funding.funding_id',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'funding_organisation': {
        'query_name'        : 'funding.organisation',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'funding_organisation_exact': {
        'query_name'        : 'funding.organisation.exact',
        'accepted_type'     : str,
        'restrictions'      : None
    }
}

CONFERENCES = {
    'conference_name': {
        'query_name'        : 'conference.name',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'conference_instance': {
        'query_name'        : 'conference.instance',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'conference_location': {
        'query_name'        : 'conference.location',
        'accepted_type'     : str,
        'restrictions'      : None
    }
}

CLINICAL_TRIALS = {
    'clinical_trial_registry': {
        'query_name'        : 'clinical_trial.registry',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'clinical_trial_trial_id': {
        'query_name'        : 'clinical_trial.trial_id',
        'accepted_type'     : str,
        'restrictions'      : None
    }
}

OPEN_ACCESS = {
    'open_access_colour': {
        'query_name'        : 'open_access.colour',
        'accepted_type'     : str,
        'restrictions'      : None
    },
    'open_access_license': {
        'query_name'        : 'open_access.license',
        'accepted_type'     : str,
        'restrictions'      : None
    }
}

DATE = {
    'date_published': {
        'query_name'        : 'date_published',
        'accepted_type'     : str,
        'restrictions'      : None,
        'date_format'       : '%Y-%m-%d'
    },
    'year_published': {
        'query_name'        : 'year_published',
        'accepted_type'     : int,
        'restrictions'      : None,
        'date_format'       : '%Y'
    },
    'created': {
        'query_name'        : 'created',
        'accepted_type'     : str,
        'restrictions'      : None,
        'date_format'       : '%Y-%m-%d'
    },
}
### END OF SEARCHABLE FIELDS ###

### BOOLEAN FILTERS ###
BOOLEAN_FILTERS = {
    "is_referenced_by_scholarly": {
        "query_name"        : "is_referenced_by_scholarly",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_patent_citations": {
        "query_name"        : "has_patent_citations",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_affiliation": {
        "query_name"        : "has_affiliation",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_affiliation_grid": {
        "query_name"        : "has_affiliation_grid",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_affiliation_ror": {
        "query_name"        : "has_affiliation_ror",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_orcid": {
        "query_name"        : "has_orcid",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_mesh_term": {
        "query_name"        : "has_mesh_term",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_chemical": {
        "query_name"        : "has_chemical",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_keyword": {
        "query_name"        : "has_keyword",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_clinical_trial": {
        "query_name"        : "has_clinical_trial",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_field_of_study": {
        "query_name"        : "has_field_of_study",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_abstract": {
        "query_name"        : "has_abstract",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_full_text": {
        "query_name"        : "has_full_text",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "has_funding": {
        "query_name"        : "has_funding",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "is_open_access": {
        "query_name"        : "is_open_access",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "in_analytics_set": {
        "query_name"        : "in_analytics_set",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "source.is_diamond": {
        "query_name"        : "source.is_diamond",
        "accepted_type"     : bool,
        "restrictions"      : None
    },
    "is_retracted": {
        "query_name"        : "is_retracted",
        "accepted_type"     : bool,
        "restrictions"      : None
    }
}
### END OF BOOLEAN FILTERS ###

### FIELDS FOR RANGE QUERIES ###
RANGE = {
    'date_published': {
        'query_name'        : 'date_published',
        'accepted_type'     : str,
        'restrictions'      : None,
        'date_format'       : '%Y-%m-%d'
    },
    'year_published': {
        'query_name'        : 'year_published',
        'accepted_type'     : int,
        'restrictions'      : None,
        'date_format'       : '%Y'
    },
    'created': {
        'query_name'        : 'created',
        'accepted_type'     : str,
        'restrictions'      : None,
        'date_format'       : '%Y-%m-%d'
    },
    'retraction_update_date': {
        'query_name'        : 'retraction_update.date',
        'accepted_type'     : str,
        'restrictions'      : None,
        'date_format'       : '%Y-%m-%d'
    },
    'author_count': {
        'query_name'        : 'author_count',
        'accepted_type'     : int,
        'restrictions'      : None
    },
    'referenced_by_count': {
        'query_name'        : 'referenced_by_count',
        'accepted_type'     : int,
        'restrictions'      : None
    },
    'reference_count': {
        'query_name'        : 'reference_count',
        'accepted_type'     : int,
        'restrictions'      : None
    },
    'referenced_by_patent_count': {
        'query_name'        : 'referenced_by_patent.count',
        'accepted_type'     : int,
        'restrictions'      : None
    }
}
### END OF RANGE QUERIES ###