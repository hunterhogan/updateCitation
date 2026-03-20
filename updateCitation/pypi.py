"""Construct PyPI release URL for citation metadata.

(AI generated docstring)

You can use this module to generate the PyPI release URL for a package and
populate the `repositoryDASHartifact` field of a `CitationNexus` [1] object.
The module uses `packaging.utils.canonicalize_name` [2] to normalize the
package name.

Contents
--------
Functions
	addPyPIrelease
		Populate a `CitationNexus` with the PyPI release URL.
	getPyPIrelease
		Construct the PyPI release URL dictionary from `CitationNexus` metadata.

References
----------
[1] updateCitation.variables.CitationNexus
	Internal package reference
[2] packaging.utils.canonicalize_name - PyPA
	https://packaging.pypa.io/en/stable/utils.html#packaging.utils.canonicalize_name

"""
from typing import Any
from updateCitation import CitationNexus
import packaging.utils

def getPyPIrelease(nexusCitation: CitationNexus) -> dict[str, Any]:
	"""Construct the PyPI release URL dictionary from `CitationNexus` metadata.

	(AI generated docstring)

	You can use `getPyPIrelease` to build a dictionary containing the
	`repositoryDASHartifact` key with a PyPI release URL constructed from
	`nexusCitation.title` and `nexusCitation.version`. The function
	canonicalize the package name using `packaging.utils.canonicalize_name` [1].

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object containing `title` and `version`.

	Returns
	-------
	dictionaryPyPIRelease : dict[str, Any]
		A dictionary with key `"repositoryDASHartifact"` mapped to the PyPI
		release URL string.

	Raises
	------
	ValueError
		If `nexusCitation.title` or `nexusCitation.version` is falsy.

	Examples
	--------
	Real usage from test suite:

		standardizedEqualTo(expected, getPyPIrelease, nexusCitationTesting)

	References
	----------
	[1] packaging.utils.canonicalize_name - PyPA
		https://packaging.pypa.io/en/stable/utils.html#packaging.utils.canonicalize_name

	"""
	if not nexusCitation.title:
		message = "Package name (title) is required to get PyPI release info."
		raise ValueError(message)
	if not nexusCitation.version:
		message = "Package version is required to get PyPI release info."
		raise ValueError(message)

	packageName: str = packaging.utils.canonicalize_name(nexusCitation.title)
	version = str(nexusCitation.version)
	return {"repositoryDASHartifact": f"https://pypi.org/project/{packageName}/{version}/"}

def addPyPIrelease(nexusCitation: CitationNexus) -> CitationNexus:
	"""Populate a `CitationNexus` with the PyPI release URL.

	(AI generated docstring)

	You can use `addPyPIrelease` to set the `repositoryDASHartifact` field on
	`nexusCitation` using the URL returned by `getPyPIrelease` [1]. After
	populating, the function calls `nexusCitation.setInStone("PyPI")` [2]
	to freeze the PyPI-owned field.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object to populate.

	Returns
	-------
	nexusCitationPopulated : CitationNexus
		The `nexusCitation` object with `repositoryDASHartifact` populated.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		nexusCitation = addPyPIrelease(nexusCitation)

	References
	----------
	[1] updateCitation.pypi.getPyPIrelease
		Internal package reference
	[2] updateCitation.variables.CitationNexus.setInStone
		Internal package reference

	"""
	pypiReleaseData: dict[str, Any] = getPyPIrelease(nexusCitation)
	nexusCitation.repositoryDASHartifact = pypiReleaseData.get("repositoryDASHartifact")

	nexusCitation.setInStone("PyPI")
	return nexusCitation
