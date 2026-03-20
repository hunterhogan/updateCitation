"""Define core types and configuration for citation metadata aggregation.

(AI generated docstring)

You can use this module to access the data structures and configuration values that
govern the citation update workflow. The module defines `CitationNexus` [1], the
central data container for citation fields, and `SettingsPackage` [2], the
configuration container for repository paths, git settings, and feature flags.
The module also defines `TypedDict` [3] types that model the Citation File Format
(CFF) [4] schema structures.

Contents
--------
Variables
	cffDASHversionDefaultHARDCODED
		The default CFF specification version string.
	CitationNexusFieldsProtected
		The set of field name string that are frozen after their authoritative source populates them.
	CitationNexusFieldsRequired
		The set of field name string required by the CFF specification.
	CitationNexusFieldsRequiredHARDCODED
		The hardcoded set of required CFF field name string.
	filename_pyprojectDOTtomlDEFAULT
		The default filename for `pyproject.toml`.
	formatDateCFF
		The `strftime` format string for CFF date field.
	gitUserEmailFALLBACK
		The fallback email address for git commit authorship.
	mapNexusCitation2pyprojectDOTtoml
		The mapping of `CitationNexus` field name to `pyproject.toml` key name.
	messageDefaultHARDCODED
		The default CFF message string.
	Z0Z_mappingFieldsURLFromPyPAMetadataToCFF
		The mapping of PyPA URL key name to CFF field name.

Classes
	CitationNexus
		Store and manage all citation metadata field for a CFF file.
	Entity
		Represent an organization or entity in CFF schema.
	FREAKOUT
		Signal an unrecoverable error in the citation workflow.
	Identifier
		Represent a persistent identifier (DOI, URL, SWH, other) in CFF schema.
	Person
		Represent a person in CFF schema.
	ReferenceDictionary
		Represent a bibliographic reference entry in CFF schema.
	SettingsPackage
		Store repository path, git configuration, and feature flag for the workflow.

References
----------
[1] updateCitation.variables.CitationNexus
	Internal package reference
[2] updateCitation.variables.SettingsPackage
	Internal package reference
[3] typing.TypedDict - Python standard library
	https://docs.python.org/3/library/typing.html#typing.TypedDict
[4] Citation File Format (CFF) specification
	https://citation-file-format.github.io/

"""
from typing import Any, cast, Literal, TypedDict
import attrs
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
	"""Signal an unrecoverable error in the citation workflow.

	(AI generated docstring)

	You can raise `FREAKOUT` when a required precondition is missing and no
	recovery is possible. For example, `GitHubRepository` [1] raises `FREAKOUT`
	when `nexusCitation.repository` is `None`.

	References
	----------
	[1] updateCitation.github.GitHubRepository
		Internal package reference

	"""

@attrs.define(slots=False)
class SettingsPackage:
	"""Store repository path, git configuration, and feature flag for the workflow.

	(AI generated docstring)

	You can use `SettingsPackage` to configure the citation update workflow.
	`SettingsPackage` holds filesystem path for the repository and citation file,
	git commit settings, GitHub authentication token, and boolean flag that
	control which metadata source to include. `getSettingsPackage` [1]
	instantiates `SettingsPackage` from `pyproject.toml` [2] `[tool.updateCitation]`
	table values.

	Attributes
	----------
	pathRepository : pathlib.Path = Path.cwd()
		The root directory of the repository.
	filename_pyprojectDOTtoml : str = 'pyproject.toml'
		The filename of the `pyproject.toml` configuration file.
	pathFilenamePackageSSOT : pathlib.Path
		The full path to the `pyproject.toml` file.
	filenameCitationDOTcff : str = 'CITATION.cff'
		The filename of the CITATION.cff file.
	pathFilenameCitationDOTcffRepository : pathlib.Path
		The full path to the CITATION.cff file in the repository root.
	pathFilenameCitationSSOT : pathlib.Path
		The full path to the authoritative CITATION.cff file.
	Z0Z_addGitHubRelease : bool = True
		Whether to include GitHub release metadata.
	Z0Z_addPyPIrelease : bool = True
		Whether to include PyPI release metadata.
	pathReferences : pathlib.Path
		The directory path for reference citation file.
	projectURLTargets : set[str] = {'homepage', 'license', 'repository'}
		The set of PyPA project URL key name to extract.
	gitCommitMessage : str = 'Update citations [skip ci]'
		The default git commit message.
	gitUserName : str = 'updateCitation'
		The git user name for commit authorship.
	gitUserEmail : str = ''
		The git user email for commit authorship.
	gitAmendFromGitHubAction : bool = True
		Whether to amend and push from a GitHub Actions environment.
	tomlPackageData : dict[str, Any]
		The parsed `[project]` table from `pyproject.toml`.
	GITHUB_TOKEN : str | None = None
		The GitHub authentication token.

	Examples
	--------
	Real usage from updateCitation.pyprojectDOTtoml module:

		truth = SettingsPackage(**Z0Z_SettingsPackage, pathFilenamePackageSSOT=pathFilename)

	References
	----------
	[1] updateCitation.pyprojectDOTtoml.getSettingsPackage
		Internal package reference
	[2] pyproject.toml specification - Python Packaging User Guide
		https://packaging.python.org/en/latest/specifications/pyproject-toml/

	"""
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
	tomlPackageData: dict[str, Any] = cast(dict[str, Any], attrs.field(factory=dict))

	GITHUB_TOKEN: str | None = None

CitationNexusFieldsRequired: set[str] = CitationNexusFieldsRequiredHARDCODED
CitationNexusFieldsProtected: set[str] = set()

# Define type definitions for schema structures
class Person(TypedDict, total=False):
	"""Represent a person in CFF schema.

	(AI generated docstring)

	You can use `Person` to type-check dictionary value that represent
	a person author, contact, editor, or other role in Citation File
	Format [1]. The key name match the CFF schema field name.

	References
	----------
	[1] Citation File Format (CFF) specification
		https://citation-file-format.github.io/

	"""
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
	"""Represent an organization or entity in CFF schema.

	(AI generated docstring)

	You can use `Entity` to type-check dictionary value that represent
	an organization, institution, or other entity in Citation File
	Format [1]. The key name match the CFF schema field name.

	References
	----------
	[1] Citation File Format (CFF) specification
		https://citation-file-format.github.io/

	"""
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
	"""Represent a persistent identifier (DOI, URL, SWH, other) in CFF schema.

	(AI generated docstring)

	You can use `Identifier` to type-check dictionary value that represent
	a persistent identifier entry in Citation File Format [1].

	References
	----------
	[1] Citation File Format (CFF) specification
		https://citation-file-format.github.io/

	"""
	description: str
	type: Literal["doi", "url", "swh", "other"]
	value: str

class ReferenceDictionary(TypedDict, total=False):
	"""Represent a bibliographic reference entry in CFF schema.

	(AI generated docstring)

	You can use `ReferenceDictionary` to type-check dictionary value that
	represent a bibliographic reference in Citation File Format [1].
	The key name match the CFF schema field for the `references` and
	`preferred-citation` section.

	References
	----------
	[1] Citation File Format (CFF) specification
		https://citation-file-format.github.io/

	"""
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
	"""Store and manage all citation metadata field for a CFF file.

	(AI generated docstring)

	You can use `CitationNexus` to aggregate citation metadata from multiple
	authoritative source into a single object. `CitationNexus` has a one-to-one
	correlation with `cffconvert.lib.cff_1_2_x.citation.Citation_1_2_x.cffobj` [1].
	Each metadata source populates its designated field, then calls
	`setInStone` [2] to freeze those field and prevent later source from
	overwriting authoritative value. The `__setattr__` override emits a
	warning when a process attempts to modify a frozen field.

	Attributes
	----------
	abstract : str | None = None
		The software abstract or description.
	authors : list[dict[str, str]]
		The list of author dictionary with CFF person field.
	cffDASHversion : str = '1.2.0'
		The CFF specification version.
	commit : str | None = None
		The git commit SHA of the release.
	contact : list[dict[str, str]]
		The list of contact dictionary with CFF person field.
	dateDASHreleased : str | None = None
		The release date in CFF date format.
	doi : str | None = None
		The Digital Object Identifier for the software.
	identifiers : list[Identifier]
		The list of persistent `Identifier` for the software.
	keywords : list[str]
		The list of keyword string.
	license : str | None = None
		The SPDX license expression.
	licenseDASHurl : str | None = None
		The URL to the license text.
	message : str
		The CFF message prompting citation.
	preferredDASHcitation : ReferenceDictionary | None = None
		The preferred citation `ReferenceDictionary` for academic use.
	references : list[ReferenceDictionary]
		The list of `ReferenceDictionary` for related work.
	repository : str | None = None
		The URL of the source code repository.
	repositoryDASHartifact : str | None = None
		The URL of the package artifact (for example, PyPI release).
	repositoryDASHcode : str | None = None
		The URL of the release on the code hosting platform.
	title : str | None = None
		The software title (package name).
	type : str | None = None
		The CFF type (for example, "software").
	url : str | None = None
		The project homepage URL.
	version : str | None = None
		The software version string.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		nexusCitation: CitationNexus = CitationNexus()
		nexusCitation = add_pyprojectDOTtoml(nexusCitation, truth)

	Real usage from test suite:

		nexusCitation = CitationNexus(**attributes)

	References
	----------
	[1] cffconvert - Citation File Format converter
		https://github.com/citation-file-format/cffconvert
	[2] updateCitation.variables.CitationNexus.setInStone
		Internal package reference

	"""
	abstract: str | None = None
	authors: list[dict[str, str]] = cast(list[dict[str, str]], attrs.field(factory=list))
	cffDASHversion: str = cffDASHversionDefaultHARDCODED
	commit: str | None = None
	contact: list[dict[str, str]] = cast(list[dict[str, str]], attrs.field(factory=list))
	dateDASHreleased: str | None = None
	doi: str | None = None
	identifiers: list[Identifier] = cast(list[Identifier], attrs.field(factory=list))
	keywords: list[str] = cast(list[str], attrs.field(factory=list))
	license: str | None = None
	licenseDASHurl: str | None = None
	message: str = messageDefaultHARDCODED
	preferredDASHcitation: ReferenceDictionary | None = None
	# TODO `cffconvert` also doesn't convert references yet
	references: list[ReferenceDictionary] = cast(list[ReferenceDictionary], attrs.field(factory=list))
	repository: str | None = None
	repositoryDASHartifact: str | None = None
	repositoryDASHcode: str | None = None
	title: str | None = None
	type: str | None = None
	url: str | None = None
	version: str | None = None

	# NOTE the names of the existing parameters for `__setattr__` are fixed
	def __setattr__(self, name: str, value: Any, warn: bool | None = True) -> None:
		"""Guard frozen field from modification by later metadata source.

		(AI generated docstring)

		You can rely on `__setattr__` to enforce field protection after
		`setInStone` [1] freezes a set of field name. When a process
		attempts to modify a field in `CitationNexusFieldsProtected`,
		`__setattr__` emits a `UserWarning` with the calling code context
		and silently discards the assignment.

		Parameters
		----------
		name : str
			The attribute name to set.
		value : Any
			The value to assign.
		warn : bool | None = True
			Whether to emit a `UserWarning` when the field is protected.

		References
		----------
		[1] updateCitation.variables.CitationNexus.setInStone
			Internal package reference

		"""
		if name in CitationNexusFieldsProtected:
			if warn:
				message: str = f"A process tried to change the field '{name}' after the authoritative source set the field's value.\n"
				warnings.warn(message, UserWarning, stacklevel=2)
			return
		super().__setattr__(name, value)

	def setInStone(self, prophet: str) -> None:
		"""Validate required field and freeze the field owned by `prophet`.

		(AI generated docstring)

		You can call `setInStone` after a metadata source finishes populating its
		field. The method verifies that every required field owned by `prophet`
		has a non-`None` value, then adds those field name to
		`CitationNexusFieldsProtected` so that `__setattr__` [1] prevents later
		modification.

		Parameters
		----------
		prophet : str
			The name of the metadata source whose field to freeze. Accepted
			value: `"Citation"`, `"GitHub"`, `"PyPA"`, `"PyPI"`,
			`"pyprojectDOTtoml"`.

		Raises
		------
		ValueError
			If a required field owned by `prophet` has no value.

		Examples
		--------
		Real usage from updateCitation.citationFileFormat module:

			nexusCitation.setInStone("Citation")

		References
		----------
		[1] updateCitation.variables.CitationNexus.__setattr__
			Internal package reference

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
				message = f"I have not yet received a value for the field '{fieldName}', but the Citation Field Format requires the field and {prophet} should have provided it."
				raise ValueError(message)

		CitationNexusFieldsProtected.update(fieldsSSOT)
