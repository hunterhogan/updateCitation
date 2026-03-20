"""Integrate PyPA metadata with Citation File Format.

(AI generated docstring)

You can use this module to extract metadata from Python Package Authority
(PyPA) compliant package dictionaries and merge that metadata into `CitationNexus` [1]
objects. The module supports version comparison using `packaging.version.Version` [2]
and handles metadata normalization including package name canonicalization, license
expression parsing, and project URL mapping.

Contents
--------
Functions
	addPyPAMetadata
		Populate a `CitationNexus` object with PyPA metadata field.
	compareVersions
		Compare two version strings using PyPA version semantics.
	getPyPAMetadata
		Extract and normalize PyPA metadata from a package dictionary.

References
----------
[1] updateCitation.variables.CitationNexus
	Internal package reference
[2] packaging.version.Version - PyPA
	https://packaging.pypa.io/en/stable/version.html

"""
from hunterMakesPy import raiseIfNone
from packaging.metadata import Metadata as PyPAMetadata
from typing import Any, cast
from updateCitation import CitationNexus, Z0Z_mappingFieldsURLFromPyPAMetadataToCFF
import packaging
import packaging.metadata
import packaging.utils
import packaging.version

def compareVersions(comparand: str, comparator: str) -> int:
	"""Compare two version strings using PyPA version semantics.

	This function uses `packaging.version.Version` [1] to parse and compare version
	strings according to PEP 440 [2] version specification. The function returns
	an integer indicating the relationship between `comparand` and `comparator`.

	Parameters
	----------
	comparand : str
		The version string to compare.
	comparator : str
		The version string to compare against.

	Returns
	-------
	relationship : int
		`-1` if `comparand` is less than `comparator`, `0` if `comparand` equals
		`comparator`, `1` if `comparand` is greater than `comparator`, or `3153`
		if the comparison produces an unexpected result (should never occur with
		valid `packaging.version.Version` comparisons).

	Examples
	--------
	Real usage from updateCitation.github module:

		if compareVersions(latestRelease.tag_name, nexusCitation.version) == -1:
			# Handle case where release tag is older than current version
			...

	References
	----------
	[1] packaging.version.Version - PyPA
		https://packaging.pypa.io/en/stable/version.html
	[2] PEP 440 - Version Identification and Dependency Specification
		https://peps.python.org/pep-0440/

	"""
	versionComparand: packaging.version.Version = packaging.version.Version(comparand)
	versionComparator: packaging.version.Version = packaging.version.Version(comparator)
	if versionComparand < versionComparator:
		return -1
	elif versionComparator < versionComparand:
		return 1
	elif versionComparand == versionComparator:
		return 0
	else:
		return 3153

def getPyPAMetadata(packageData: dict[str, Any]) -> PyPAMetadata:
	"""Extract and normalize PyPA metadata from a package dictionary.

	This function converts a dictionary containing package information into a
	`packaging.metadata.Metadata` [1] object. The function handles polymorphic
	license fields per PEP 621 [2] and PEP 639 [3], normalizes URL names to
	lowercase, and canonicalizes package names using `packaging.utils.canonicalize_name` [4].
	The function validates the package name and raises `packaging.metadata.InvalidMetadata` [1]
	if the name field is missing.

	Parameters
	----------
	packageData : dict[str, Any]
		A dictionary containing package information, typically from `pyproject.toml` [5]
		project table. Expected keys include `name`, `version`, `keywords`, `license`,
		and `urls`.

	Returns
	-------
	metadataNormalized : PyPAMetadata
		A `PyPAMetadata` object containing the extracted and formatted metadata. The
		package name is canonicalized and validated.

	Examples
	--------
	Real usage from updateCitation.pypa module:

		pypaMetadata: PyPAMetadata = getPyPAMetadata(tomlPackageData)

	Real usage from test suite:

		dictionaryPackageData = {
			"version": "17.19.23",
		}
		with pytest.raises(Exception):
			getPyPAMetadata(dictionaryPackageData)

	References
	----------
	[1] packaging.metadata.Metadata - PyPA
		https://packaging.pypa.io/en/stable/metadata.html
	[2] PEP 621 - Storing project metadata in pyproject.toml
		https://peps.python.org/pep-0621/
	[3] PEP 639 - Improving License Clarity with Better Package Metadata
		https://peps.python.org/pep-0639/
	[4] packaging.utils.canonicalize_name - PyPA
		https://packaging.pypa.io/en/stable/utils.html#packaging.utils.canonicalize_name
	[5] pyproject.toml specification - Python Packaging User Guide
		https://packaging.python.org/en/latest/specifications/pyproject-toml/

	"""
	dictionaryPackageDataURLs: dict[str, str] = packageData.get("urls", {})
	dictionaryProjectURLs: dict[str, str] = {}
	for urlName, url in dictionaryPackageDataURLs.items():
		urlName = urlName.lower()
		dictionaryProjectURLs[urlName] = url

# NOTE Handle polymorphic license field (str or dict) per PEP 621 / PEP 639
	packageDataLicense: str | dict[str, str] = packageData.get("license", {})
	licenseExpression: str = ""

	if isinstance(packageDataLicense, str):
		licenseExpression = packageDataLicense
	elif isinstance(packageDataLicense, dict):
		licenseExpression = packageDataLicense.get("text", "")

	metadataRaw = packaging.metadata.RawMetadata(
		keywords=packageData.get("keywords", []),
		license_expression=licenseExpression,
		metadata_version="2.4",
# NOTE packaging.metadata.InvalidMetadata: 'name' is a required field
		name=packaging.utils.canonicalize_name(raiseIfNone(packageData.get("name")), validate=True),
		project_urls=dictionaryProjectURLs,
		version=cast(str, packageData.get("version")),  # pyright: ignore[reportArgumentType]
	)

	return PyPAMetadata().from_raw(metadataRaw)

def addPyPAMetadata(nexusCitation: CitationNexus, tomlPackageData: dict[str, Any], projectURLTargets: set[str]) -> CitationNexus:
	"""Populate a `CitationNexus` object with PyPA metadata field.

	(AI generated docstring)

	This function extracts PyPA metadata from `tomlPackageData` using `getPyPAMetadata` [1]
	and merges that metadata into `nexusCitation`. The function populates `version`,
	`keywords`, `license`, and project URL fields (`url`, `repository`, `licenseDASHurl`)
	based on the mapping defined in `Z0Z_mappingFieldsURLFromPyPAMetadataToCFF` [2].
	After populating fields, the function calls `nexusCitation.setInStone("PyPA")` [3]
	to protect the PyPA-sourced fields from modification by other metadata sources.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object to populate with PyPA metadata.
	tomlPackageData : dict[str, Any]
		A dictionary containing package information, typically from `pyproject.toml` [4]
		project table.
	projectURLTargets : set[str]
		A set of URL key names to extract from `pypaMetadata.project_urls`. Common
		values include `"homepage"`, `"repository"`, and `"license"`.

	Returns
	-------
	nexusCitationPopulated : CitationNexus
		The `nexusCitation` object with PyPA metadata fields populated.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		nexusCitation = addPyPAMetadata(nexusCitation, truth.tomlPackageData, truth.projectURLTargets)

	References
	----------
	[1] updateCitation.pypa.getPyPAMetadata
		Internal package reference
	[2] updateCitation.variables.Z0Z_mappingFieldsURLFromPyPAMetadataToCFF
		Internal package reference
	[3] updateCitation.variables.CitationNexus.setInStone
		Internal package reference
	[4] pyproject.toml specification - Python Packaging User Guide
		https://packaging.python.org/en/latest/specifications/pyproject-toml/

	"""
	pypaMetadata: PyPAMetadata = getPyPAMetadata(tomlPackageData)

	if pypaMetadata.version:
		nexusCitation.version = str(pypaMetadata.version)
	if pypaMetadata.keywords:
		nexusCitation.keywords = pypaMetadata.keywords
	if pypaMetadata.license_expression:
		nexusCitation.license = pypaMetadata.license_expression

	if pypaMetadata.project_urls:
		for urlTarget in projectURLTargets:
			url = pypaMetadata.project_urls.get(urlTarget, None)
			if url:
				setattr(nexusCitation, Z0Z_mappingFieldsURLFromPyPAMetadataToCFF[urlTarget], url)

	nexusCitation.setInStone("PyPA")
	return nexusCitation
