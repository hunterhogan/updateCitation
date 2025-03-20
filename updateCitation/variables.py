from typing import Any, Literal, TypedDict
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
CitationNexusFieldsRequiredHARDCODED: set[str] = {"authors", "cffDASHversion", "message", "title"}
"""
from cffconvert.citation import Citation # from cffconvert.lib.citation import Citation # upcoming version 3.0.0
cffstr = "cff-version: 1.2.0"; citationObject = Citation(cffstr); schemaDOTjson = citationObject._get_schema()
# get "required": list of fields; # Convert '-' to 'DASH' in field names """

filename_pyprojectDOTtomlDEFAULT: str = 'pyproject.toml' # used by other processes before `SettingsPackage` is instantiated to help instantiate `SettingsPackage`
formatDateCFF: str = "%Y-%m-%d"
gitUserEmailFALLBACK: str = 'action@github.com'
mapNexusCitation2pyprojectDOTtoml: list[tuple[str, str]] = [("authors", "authors"), ("contact", "maintainers")]
Z0Z_mappingFieldsURLFromPyPAMetadataToCFF: dict[str, str] = {
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
	projectURLTargets: set[str] = {"homepage", "license", "repository"}

	gitCommitMessage: str = "Update citations [skip ci]"
	gitUserName: str = "updateCitation"
	gitUserEmail: str = ""
	gitAmendFromGitHubAction: bool = True
	# gitPushFromOtherEnvironments_why_where_NotImplemented: bool = False
	tomlPackageData: dict[str, Any] = attrs.field(factory=dict)

	GITHUB_TOKEN: str | None = None

CitationNexusFieldsRequired: set[str] = CitationNexusFieldsRequiredHARDCODED
CitationNexusFieldsProtected: set[str] = set()

# Define type definitions for schema structures
class Person(TypedDict, total=False):
	address: str
	affiliation: str
	alias: str
	city: str
	country: str
	email: str
	family_names: str
	fax: str
	given_names: str
	name_particle: str
	name_suffix: str
	orcid: str
	post_code: str | int
	region: str
	tel: str
	website: str

class Entity(TypedDict, total=False):
	address: str
	alias: str
	city: str
	country: str
	date_end: str
	date_start: str
	email: str
	fax: str
	location: str
	name: str
	orcid: str
	post_code: str | int
	region: str
	tel: str
	website: str

class Identifier(TypedDict, total=False):
	description: str
	type: Literal["doi", "url", "swh", "other"]
	value: str

class ReferenceDictionary(TypedDict, total=False):
	abbreviation: str
	abstract: str
	authors: list[Person | Entity]
	collection_doi: str
	collection_title: str
	collection_type: str
	commit: str
	conference: Entity
	contact: list[Person | Entity]
	copyright: str
	data_type: str
	database: str
	database_provider: Entity
	date_accessed: str
	date_downloaded: str
	date_published: str
	date_released: str
	department: str
	doi: str
	edition: str
	editors: list[Person | Entity]
	editors_series: list[Person | Entity]
	end: int | str
	entry: str
	filename: str
	format: str
	identifiers: list[Identifier]
	institution: Entity
	isbn: str
	issn: str
	issue: str | int
	issue_date: str
	issue_title: str
	journal: str
	keywords: list[str]
	languages: list[str]
	license: str | list[str]
	license_url: str
	loc_end: int | str
	loc_start: int | str
	location: Entity
	medium: str
	month: int | str
	nihmsid: str
	notes: str
	number: str | int
	number_volumes: int | str
	pages: int | str
	patent_states: list[str]
	pmcid: str
	publisher: Entity
	recipients: list[Entity | Person]
	repository: str
	repository_artifact: str
	repository_code: str
	scope: str
	section: str | int
	senders: list[Entity | Person]
	start: int | str
	status: Literal["abstract", "advance-online", "in-preparation", "in-press", "preprint", "submitted"]
	term: str
	thesis_type: str
	title: str
	translators: list[Entity | Person]
	type: str
	url: str
	version: str | int
	volume: int | str
	volume_title: str
	year: int | str
	year_original: int | str

@attrs.define()
class CitationNexus:
	"""one-to-one correlation with `cffconvert.lib.cff_1_2_x.citation` class Citation_1_2_x.cffobj"""
	abstract: str | None = None
	authors: list[dict[str, str]] = attrs.field(factory=list)
	cffDASHversion: str = cffDASHversionDefaultHARDCODED
	commit: str | None = None
	contact: list[dict[str, str]] = attrs.field(factory=list)
	dateDASHreleased: str | None = None
	doi: str | None = None
	identifiers: list[str] = attrs.field(factory=list)
	keywords: list[str] = attrs.field(factory=list)
	license: str | None = None
	licenseDASHurl: str | None = None
	message: str = messageDefaultHARDCODED
	preferredDASHcitation: ReferenceDictionary | None = None
	# TODO `cffconvert` also doesn't convert references yet
	references: list[ReferenceDictionary] = attrs.field(factory=list)
	repository: str | None = None
	repositoryDASHartifact: str | None = None
	repositoryDASHcode: str | None = None
	title: str | None = None
	type: str | None = None
	url: str | None = None
	version: str | None = None

	# NOTE the names of the existing parameters for `__setattr__` are fixed
	def __setattr__(self, name: str, value: Any, warn: bool | None = True) -> None:
		"""Prevent modification of protected fields."""
		if name in CitationNexusFieldsProtected:
			if warn:
				# Get the line of code that called this method
				context = inspect.stack()[1].code_context[0].strip() # type: ignore
				# TODO Improve this warning message and the context information.
				warnings.warn(f"A process tried to change the field '{name}' after the authoritative source set the field's value.\n{context=}", UserWarning)
			return
		super().__setattr__(name, value)

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
				fieldsSSOT: set[str] = {"abstract", "cffDASHversion", "doi", "message", "preferredDASHcitation", "type"}
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
