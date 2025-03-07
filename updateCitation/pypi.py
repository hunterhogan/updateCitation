from updateCitation import CitationNexus
from typing import Any
import packaging.utils

def getPyPIrelease(nexusCitation: CitationNexus) -> dict[str, Any]:
	if not nexusCitation.title:
		raise ValueError("Package name (title) is required to get PyPI release info.")
	if not nexusCitation.version:
		raise ValueError("Package version is required to get PyPI release info.")

	packageName = packaging.utils.canonicalize_name(nexusCitation.title)
	version = str(nexusCitation.version)
	return {"repositoryDASHartifact": f"https://pypi.org/project/{packageName}/{version}/"}

def addPyPIrelease(nexusCitation: CitationNexus) -> CitationNexus:
	pypiReleaseData = getPyPIrelease(nexusCitation)
	nexusCitation.repositoryDASHartifact = pypiReleaseData.get("repositoryDASHartifact")

	nexusCitation.setInStone("PyPI")
	return nexusCitation
