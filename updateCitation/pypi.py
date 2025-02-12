from updateCitation import CitationNexus
from typing import Any, Dict
import packaging.utils

def getPyPIrelease(nexusCitation: CitationNexus) -> Dict[str, Any]:
	"""
		Retrieves the PyPI release information for a given Nexus citation.
		Parameters:
			nexusCitation (CitationNexus): A CitationNexus object containing the package title (name) and version.
		Returns:
			Dict[str, Any]: A dictionary containing the repository artifact URL for the PyPI release.
		Raises:
			ValueError: If the package name (title) or version is missing in the Nexus citation.
	"""
	if not nexusCitation.title:
		raise ValueError("Package name (title) is required to get PyPI release info.")
	if not nexusCitation.version:
		raise ValueError("Package version is required to get PyPI release info.")

	packageName = packaging.utils.canonicalize_name(nexusCitation.title)
	version = str(nexusCitation.version)
	return {
		"repositoryDASHartifact": f"https://pypi.org/project/{packageName}/{version}/"
	}

def addPyPIrelease(nexusCitation: CitationNexus) -> CitationNexus:
	"""Adds PyPI release information to a CitationNexus object.

		Parameters:
			nexusCitation (CitationNexus): The CitationNexus object to update.

		Returns:
			CitationNexus: The updated CitationNexus object with PyPI release information.
		"""
	pypiReleaseData = getPyPIrelease(nexusCitation)
	nexusCitation.repositoryDASHartifact = pypiReleaseData.get("repositoryDASHartifact")

	# nexusCitation.setInStone("PyPI")
	return nexusCitation
