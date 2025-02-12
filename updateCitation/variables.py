from typing import Any, Dict, List, Set, Tuple
import attrs
import inspect
import pathlib
import warnings

cffDASHversionDEFAULT: str = '1.2.0'
filename_pyprojectDOTtomlDEFAULT: str = 'pyproject.toml'
formatDateCFF: str = "%Y-%m-%d"
gitUserEmailFALLBACK: str = 'gitUserEmail'
mapNexusCitation2pyprojectDOTtoml: List[Tuple[str, str]] = [("authors", "authors"), ("contact", "maintainers")]
messageDEFAULT: str = "Cite this software with the metadata in this file."
projectURLTargets: Set[str] = {"homepage", "license", "repository"}

class FREAKOUT(Exception):
	pass

@attrs.define(slots=False)
class SettingsPackage:
	pathFilenamePackageSSOT: pathlib.Path
	pathRepository: pathlib.Path = pathlib.Path.cwd()
	filenameCitationDOTcff: str = 'CITATION.cff'
	tomlPackageData: Dict[str, Any] = attrs.field(factory=dict)

	pathReferences: pathlib.Path = pathRepository / 'citations'
	pathCitationSSOT: pathlib.Path = pathRepository / "citations"
	pathFilenameCitationDOTcffRepository: pathlib.Path = pathRepository / filenameCitationDOTcff

	pathFilenameCitationSSOT: pathlib.Path = pathCitationSSOT / filenameCitationDOTcff

	gitCommitMessage: str = "Update citations [skip ci]"
	gitUserName: str = "updateCitation"
	gitUserEmail: str = ""
	gitPushFromGitHubAction: bool = True
	# gitPushFromOtherEnvironments_why_where_NotImplemented: bool = False

	GITHUB_TOKEN: str | None = None

CitationNexusFieldsRequired: Set[str] = {"authors", "cffDASHversion", "message", "title"}
""" `fieldsRequired` could be dynamically loaded through the following:
from cffconvert.citation import Citation # from cffconvert.lib.citation import Citation # upcoming version 3.0.0
cffstr = "cff-version: 1.2.0"; citationObject = Citation(cffstr); schemaDOTjson = citationObject._get_schema()
# get "required": list of fields; # Convert '-' to 'DASH' in field names """

CitationNexusFieldsFrozen: Set[str] = set()

@attrs.define()
class CitationNexus:
	"""one-to-one correlation with `cffconvert.lib.cff_1_2_x.citation` class Citation_1_2_x.cffobj"""
	abstract: str | None = None
	authors: List[Dict[str, str]] = attrs.field(factory=list)
	cffDASHversion: str = cffDASHversionDEFAULT
	commit: str | None = None
	contact: List[Dict[str, str]] = attrs.field(factory=list)
	dateDASHreleased: str | None = None
	doi: str | None = None
	identifiers: List[str] = attrs.field(factory=list)
	keywords: List[str] = attrs.field(factory=list)
	license: str | None = None
	licenseDASHurl: str | None = None
	message: str = messageDEFAULT
	preferredDASHcitation: str | None = None
	# TODO
	references: List[Dict] = attrs.field(factory=list)
	repository: str | None = None
	repositoryDASHartifact: str | None = None
	repositoryDASHcode: str | None = None
	title: str | None = None
	type: str | None = None
	url: str | None = None
	version: str | None = None

	def __setattr__(self, name: str, value: Any) -> None:
		"""Prevent modification of frozen fields."""
		if name in CitationNexusFieldsFrozen:
			context = inspect.stack()[1].code_context[0].strip() # type: ignore
			warnings.warn(f"Field {name} is frozen and cannot be changed.\n{context}", UserWarning)
			return
		super().__setattr__(name, value)

	def setInStone(self, prophet: str) -> None:
		"""
		Confirm that required fields are not None and freeze fields specified by the context.
		Parameters:
			prophet (str): The context for freezing fields.
		Returns:
			CitationNexus: The same object with specified fields frozen.
		Raises:
			ValueError: If any required field is None.
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
			if fieldName in CitationNexusFieldsRequired and getattr(self, fieldName) is None:
				raise ValueError(f"Field {fieldName} is required but not provided.")

		CitationNexusFieldsFrozen.update(fieldsSSOT)
