from packaging.metadata import Metadata as PyPAMetadata
from typing import Any
from updateCitation import CitationNexus, Z0Z_mappingFieldsURLFromPyPAMetadataToCFF
import packaging
import packaging.metadata
import packaging.utils
import packaging.version

def compareVersions(comparand: str, comparator: str) -> int:
	"""
	Compares two version strings using packaging.version.Version.
	Parameters:
		comparand: The version string to compare.
		comparator: The version string to compare against.
	Returns:
		relationship: '-1' if `comparand` is less than `comparator`, '0' if they are equal, '1' if `comparand` is greater than `comparator`, or 'else'.
	"""
	versionComparand = packaging.version.Version(comparand)
	versionComparator = packaging.version.Version(comparator)
	if versionComparand < versionComparator:
		return -1
	elif versionComparand > versionComparator:
		return 1
	elif versionComparand == versionComparator:
		return 0
	else:
		return 3153

def getPyPAMetadata(packageData: dict[str, Any]) -> PyPAMetadata:
	"""
	Retrieves and formats package metadata from a dictionary into a PyPAMetadata object.
	Parameters:
		packageData: A dictionary containing package information.
	Returns:
		PyPAMetadata: A PyPAMetadata object containing the extracted and formatted
			metadata. The package name is canonicalized using `packaging.utils.canonicalize_name` and validated.
	"""
	dictionaryPackageDataURLs: dict[str, str] = packageData.get("urls", {})
	dictionaryProjectURLs: dict[str, str] = {}
	for urlName, url in dictionaryPackageDataURLs.items():
		urlName = urlName.lower()
		dictionaryProjectURLs[urlName] = url

	dictionaryPackageDataLicense: dict[str, str] = packageData.get("license", {})
	metadataRaw = packaging.metadata.RawMetadata(
		keywords=packageData.get("keywords", []),
		license_expression=dictionaryPackageDataLicense.get("text", ""),
		metadata_version="2.4",
		# NOTE packaging.metadata.InvalidMetadata: 'name' is a required field
		name=packaging.utils.canonicalize_name(packageData.get("name", None), validate=True),
		project_urls=dictionaryProjectURLs,
		version=packageData.get("version", None),
	)

	metadata = PyPAMetadata().from_raw(metadataRaw)
	return metadata

def addPyPAMetadata(nexusCitation: CitationNexus, tomlPackageData: dict[str, Any], projectURLTargets: set[str]) -> CitationNexus:
	pypaMetadata: PyPAMetadata = getPyPAMetadata(tomlPackageData)

	if pypaMetadata.version: nexusCitation.version = str(pypaMetadata.version)
	if pypaMetadata.keywords: nexusCitation.keywords = pypaMetadata.keywords
	if pypaMetadata.license_expression: nexusCitation.license = pypaMetadata.license_expression

	if pypaMetadata.project_urls:
		for urlTarget in projectURLTargets:
			url = pypaMetadata.project_urls.get(urlTarget, None)
			if url:
				setattr(nexusCitation, Z0Z_mappingFieldsURLFromPyPAMetadataToCFF[urlTarget], url)

	nexusCitation.setInStone("PyPA")
	return nexusCitation
