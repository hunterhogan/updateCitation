"""Access citation metadata aggregation and CITATION.cff generation.

(AI generated docstring)

You can use this package to aggregate citation metadata from multiple sources and
generate valid Citation File Format (CFF) [1] files. The package reads metadata from
`pyproject.toml` [2], PyPA packaging metadata [3], GitHub releases [4], and PyPI [5],
then merges the metadata into a single `CitationNexus` object and writes a validated
CITATION.cff file.

Modules
-------
variables
	Core types, configuration, and data structures for citation metadata.
pyprojectDOTtoml
	Read `pyproject.toml` settings and extract author and contact data.
citationFileFormat
	Read, write, and validate CITATION.cff files using `cffconvert` and `ruamel.yaml`.
pypa
	Extract and normalize PyPA packaging metadata for citation fields.
github
	GitHub API integration for release data, authentication, and git operations.
pypi
	Construct PyPI release URL for the `repositoryDASHartifact` citation field.
flowControl
	Orchestrate the full citation update workflow.

References
----------
[1] Citation File Format (CFF) specification
	https://citation-file-format.github.io/
[2] pyproject.toml specification - Python Packaging User Guide
	https://packaging.python.org/en/latest/specifications/pyproject-toml/
[3] packaging - PyPA
	https://packaging.pypa.io/en/stable/
[4] PyGithub - GitHub API client
	https://pygithub.readthedocs.io/en/stable/
[5] PyPI - Python Package Index
	https://pypi.org/

"""

# isort: split
from updateCitation.variables import (
	CitationNexus, CitationNexusFieldsProtected, filename_pyprojectDOTtomlDEFAULT, formatDateCFF, FREAKOUT, gitUserEmailFALLBACK,
	mapNexusCitation2pyprojectDOTtoml, SettingsPackage, Z0Z_mappingFieldsURLFromPyPAMetadataToCFF)

# isort: split
from updateCitation.pyprojectDOTtoml import add_pyprojectDOTtoml, getSettingsPackage

# isort: split
from updateCitation.citationFileFormat import addCitation, writeCitation

# isort: split
from updateCitation.pypa import addPyPAMetadata, compareVersions

# isort: split
from updateCitation.github import addGitHubRelease, addGitHubSettings, gittyUpGitAmendGitHub

# isort: split
from updateCitation.pypi import addPyPIrelease

# isort: split
from updateCitation.flowControl import here as here
