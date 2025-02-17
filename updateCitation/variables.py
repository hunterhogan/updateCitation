from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
import attrs
import inspect
import pathlib
import warnings

"""
Long term:
	`fieldsSSOT` will be something more like, the SSOT for this field is: ____
	`Z0Z_addGitHubRelease` will be unnecessary. The flow will cycle through the SSOTs for each field. If the SSOT for a field is GitHub, then the flow will add the GitHub release.
"""

# TODO think of a clever way to dynamically set the default version
cffDASHversionDefaultHARDCODED: str = '1.2.0'
# TODO change this to dynamically load the schema default message
messageDefaultHARDCODED: str = "Cite this software with the metadata in this file."
# TODO dynamically load through the following:
CitationNexusFieldsRequiredHARDCODED: Set[str] = {"authors", "cffDASHversion", "message", "title"}
"""
from cffconvert.citation import Citation # from cffconvert.lib.citation import Citation # upcoming version 3.0.0
cffstr = "cff-version: 1.2.0"; citationObject = Citation(cffstr); schemaDOTjson = citationObject._get_schema()
# get "required": list of fields; # Convert '-' to 'DASH' in field names """

filename_pyprojectDOTtomlDEFAULT: str = 'pyproject.toml' # used by other processes before `SettingsPackage` is instantiated to help instantiate `SettingsPackage`
formatDateCFF: str = "%Y-%m-%d"
gitUserEmailFALLBACK: str = 'action@github.com'
mapNexusCitation2pyprojectDOTtoml: List[Tuple[str, str]] = [("authors", "authors"), ("contact", "maintainers")]
Z0Z_mappingFieldsURLFromPyPAMetadataToCFF: Dict[str, str] = {
	"homepage": "url",
	"license": "licenseDASHurl",
	"repository": "repository",
}

class FREAKOUT(Exception):
	pass

@attrs.define(slots=False)
class SettingsPackage:
	pathRepository: pathlib.Path = pathlib.Path.cwd()
	filename_pyprojectDOTtoml: str = filename_pyprojectDOTtomlDEFAULT
	pathFilenamePackageSSOT: pathlib.Path = pathlib.Path(pathRepository, filename_pyprojectDOTtoml)

	filenameCitationDOTcff: str = 'CITATION.cff'
	pathFilenameCitationDOTcffRepository: pathlib.Path = pathlib.Path(pathRepository, filenameCitationDOTcff)
	pathFilenameCitationSSOT: pathlib.Path = pathlib.Path(pathFilenameCitationDOTcffRepository)

	Z0Z_addGitHubRelease: bool = True
	Z0Z_addPyPIrelease: bool = True

	pathReferences: pathlib.Path = pathlib.Path(pathRepository, 'citations')
	projectURLTargets: Set[str] = {"homepage", "license", "repository"}

	gitCommitMessage: str = "Update citations [skip ci]"
	gitUserName: str = "updateCitation"
	gitUserEmail: str = ""
	gitPushFromGitHubAction: bool = True
	# gitPushFromOtherEnvironments_why_where_NotImplemented: bool = False
	tomlPackageData: Dict[str, Any] = attrs.field(factory=dict)

	GITHUB_TOKEN: str | None = None

CitationNexusFieldsRequired: Set[str] = CitationNexusFieldsRequiredHARDCODED
CitationNexusFieldsProtected: Set[str] = set()

@attrs.define()
class CitationNexus:
	"""one-to-one correlation with `cffconvert.lib.cff_1_2_x.citation` class Citation_1_2_x.cffobj"""
	abstract: str | None = None
	authors: List[Dict[str, str]] = attrs.field(factory=list)
	cffDASHversion: str = cffDASHversionDefaultHARDCODED
	commit: str | None = None
	contact: List[Dict[str, str]] = attrs.field(factory=list)
	dateDASHreleased: str | None = None
	doi: str | None = None
	identifiers: List[str] = attrs.field(factory=list)
	keywords: List[str] = attrs.field(factory=list)
	license: str | None = None
	licenseDASHurl: str | None = None
	message: str = messageDefaultHARDCODED
	preferredDASHcitation: str | None = None
	# TODO `cffconvert` doesn't convert this field yet either
	references: List[Dict] = attrs.field(factory=list)
	repository: str | None = None
	repositoryDASHartifact: str | None = None
	repositoryDASHcode: str | None = None
	title: str | None = None
	type: str | None = None
	url: str | None = None
	version: str | None = None

		# NOTE the names of the existing parameters for `__setattr__` are fixed
	def __setattr__(self, name: str, value: Any, warn: Optional[bool] = True) -> None:
		"""Prevent modification of protected fields."""
		if name in CitationNexusFieldsProtected:
			if warn:
				# Get the line of code that called this method
				context = inspect.stack()[1].code_context[0].strip() # type: ignore
				# TODO Improve this warning message and the context information.
				warnings.warn(f"A process tried to change the field '{name}' after the authoritative source set the field's value.\n{context=}", UserWarning)
			return
		super().__setattr__(name, value)

	# TODO re-enable this method in all of the modules
	# It works too well: pytest "freezes" fields from other tests and then those tests fail
	# Learn how to prevent the tests from interfering with each other
	def setInStone(self, prophet: str) -> None:
		"""
		Confirm that required fields are not None, and freeze fields specified by the context.
		Parameters:
			prophet: The power to protect a field.
		Returns:
			None:
		Raises:
			ValueError: A required field does not have a value.
		"""
		match prophet:
			case "Citation":
				fieldsSSOT = {"abstract", "cffDASHversion", "doi", "message", "preferredDASHcitation", "type"}
			case "GitHub":
				fieldsSSOT = {"commit", "dateDASHreleased", "identifiers", "repositoryDASHcode"}
			case "PyPA":
				fieldsSSOT = {"keywords", "license", "licenseDASHurl", "repository", "url", "version"}
			case "PyPI":
				fieldsSSOT = {"repositoryDASHartifact"}
			case "pyprojectDOTtoml":
				fieldsSSOT = {"authors", "contact", "title"}
			case _:
				fieldsSSOT = set()

		for fieldName in fieldsSSOT:
			if fieldName in CitationNexusFieldsRequired and not getattr(self, fieldName, None):
				# TODO work out the semiotics of SSOT, power, authority, then improve this message (and identifiers and your life and the world)
				raise ValueError(f"I have not yet received a value for the field '{fieldName}', but the Citation Field Format requires the field and {prophet} should have provided it.")

		CitationNexusFieldsProtected.update(fieldsSSOT)
