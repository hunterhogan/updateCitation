"""Read, write, and validate CITATION.cff file.

(AI generated docstring)

You can use this module to parse an existing CITATION.cff file into a
`CitationNexus` [1] object, and to serialize a `CitationNexus` back to a
validated CITATION.cff file. The module uses `cffconvert` [2] for parsing
and validation, and `ruamel.yaml` [3] for YAML serialization.

Contents
--------
Functions
	addCitation
		Populate a `CitationNexus` with field from an existing CITATION.cff file.
	getCitation
		Parse a CITATION.cff file and return the raw dictionary.
	writeCitation
		Serialize a `CitationNexus` to a validated CITATION.cff file.

References
----------
[1] updateCitation.variables.CitationNexus
	Internal package reference
[2] cffconvert - Citation File Format converter
	https://github.com/citation-file-format/cffconvert
[3] ruamel.yaml - YAML parser and emitter
	https://yaml.readthedocs.io/en/latest/

"""
from cffconvert.cli.create_citation import create_citation
from operator import truth
from typing import Any, TYPE_CHECKING
from updateCitation import CitationNexus
import attrs
import pathlib
import ruamel.yaml

if TYPE_CHECKING:
	import cffconvert

def getCitation(pathFilenameCitationSSOT: pathlib.Path) -> dict[str, Any]:
	"""Parse a CITATION.cff file and return the raw dictionary.

	(AI generated docstring)

	You can use `getCitation` to read and parse a CITATION.cff file into a
	raw dictionary using the `cffconvert` [1] parser. The function delegates
	parsing to `cffconvert.cli.create_citation.create_citation` [1] and
	`ruamel.yaml` [2] internally.

	Parameters
	----------
	pathFilenameCitationSSOT : pathlib.Path
		The full path to the CITATION.cff file to parse.

	Returns
	-------
	cffobj : dict[str, Any]
		The parsed citation data as a dictionary with CFF field name as key.

	References
	----------
	[1] cffconvert - Citation File Format converter
		https://github.com/citation-file-format/cffconvert
	[2] ruamel.yaml - YAML parser and emitter
		https://yaml.readthedocs.io/en/latest/

	"""
	# Try to converge with cffconvert when possible.
	citationObject: cffconvert.Citation = create_citation(infile=str(pathFilenameCitationSSOT), url=None)
# NOTE `._parse()` is `ruamel.yaml.YAML` loader
	return citationObject._parse()  # noqa: SLF001

def addCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path) -> CitationNexus:
	"""Populate a `CitationNexus` with field from an existing CITATION.cff file.

	(AI generated docstring)

	You can use `addCitation` to read an existing CITATION.cff file and
	merge the field value into `nexusCitation`. The function iterates over
	all `attrs` [1] field of `CitationNexus` [2], looks up the corresponding
	CFF key, and sets the value if the CFF file contains a truthy value for
	that key. After populating, the function calls
	`nexusCitation.setInStone("Citation")` [3] to freeze the Citation-owned field.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object to populate.
	pathFilenameCitationSSOT : pathlib.Path
		The full path to the CITATION.cff file to read.

	Returns
	-------
	nexusCitationPopulated : CitationNexus
		The `nexusCitation` object with CITATION.cff field value merged in.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		nexusCitation = addCitation(nexusCitation, pathFilenameCitationSSOT)

	Real usage from test suite:

		nexusCitation = addCitation(nexusCitationTesting, citationAlphaDOTcff)
		assert isinstance(nexusCitation, CitationNexus)

	References
	----------
	[1] attrs - Classes Without Boilerplate
		https://www.attrs.org/en/stable/
	[2] updateCitation.variables.CitationNexus
		Internal package reference
	[3] updateCitation.variables.CitationNexus.setInStone
		Internal package reference

	"""
	cffobj: dict[str, Any] = getCitation(pathFilenameCitationSSOT)

	# This step is designed to prevent deleting fields that are populated in the current CFF file,
	# but for whatever reason do not get added to the CitationNexus object.

	for nexusCitationField in iter(attrs.fields(type(nexusCitation))):
		cffobjKeyName: str = nexusCitationField.name.replace("DASH", "-")
		cffobjValue = cffobj.get(cffobjKeyName)
		if cffobjValue: # An empty list will be False
			nexusCitation.__setattr__(nexusCitationField.name, cffobjValue, warn=False)

	nexusCitation.setInStone("Citation")
	return nexusCitation

def writeCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path, pathFilenameCitationDOTcffRepo: pathlib.Path | None = None) -> bool:
	"""Serialize a `CitationNexus` to a validated CITATION.cff file.

	(AI generated docstring)

	You can use `writeCitation` to convert a `CitationNexus` [1] object into
	a YAML file conforming to the Citation File Format specification [2].
	The function writes a temporary validation file, validates the file
	using `cffconvert` [3], and if validation succeeds, writes the final
	CITATION.cff file. The function optionally writes a second copy to a
	different path.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object to serialize.
	pathFilenameCitationSSOT : pathlib.Path
		The full path for the primary CITATION.cff output file.
	pathFilenameCitationDOTcffRepo : pathlib.Path | None = None
		The full path for an optional second copy of the CITATION.cff file.

	Returns
	-------
	validationSucceeded : bool
		`True` if `cffconvert` validation succeeds and the file is written,
		`False` if validation fails.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		validationStatus: bool = writeCitation(
			nexusCitation, truth.pathFilenameCitationSSOT,
			truth.pathFilenameCitationDOTcffRepository)

	References
	----------
	[1] updateCitation.variables.CitationNexus
		Internal package reference
	[2] Citation File Format (CFF) specification
		https://citation-file-format.github.io/
	[3] cffconvert - Citation File Format converter
		https://github.com/citation-file-format/cffconvert

	"""
	# NOTE embarrassingly hacky process to follow

	# TODO format the output
	# parameterIndent: int = 2  # noqa: ERA001
	# parameterLineWidth: int = 60  # noqa: ERA001

	# use `ruamel.yaml` because using the same packages and identifiers as `cffconvert` and other CFF ecosystem tools has benefits
	yamlWorkhorse: ruamel.yaml.YAML = ruamel.yaml.YAML()

	def fieldValueIsTruthy(_Z0Z_field: Any, Z0Z_value: Any) -> bool:
		return truth(Z0Z_value)  # empty lists and empty strings will be False

	# Convert the attrs object to a dictionary.
	dictionaryCitation: dict[str, Any] = attrs.asdict(nexusCitation, filter=fieldValueIsTruthy)

	# Rename the keys to match the CFF format.
	for keyName in list(dictionaryCitation.keys()):
		dictionaryCitation[keyName.replace("DASH", "-")] = dictionaryCitation.pop(keyName)

	# This function and this context manager only exist to work around the fact that `ruamel.yaml` does not support `pathlib.Path` objects.
	def writeStream(pathFilename: pathlib.Path) -> None:
		pathFilename = pathlib.Path(pathFilename)
		pathFilename.parent.mkdir(parents=True, exist_ok=True)
		with open(pathFilename, 'w') as pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith:  # noqa: PTH123
			yamlWorkhorse.dump(dictionaryCitation, pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith) # pyright: ignore[reportUnknownMemberType]

	# Write the validation file because I haven't figured out how to validate it as a stream yet.
	pathFilenameForValidation: pathlib.Path = pathlib.Path(pathFilenameCitationSSOT).with_stem('validation')
	writeStream(pathFilenameForValidation)
	citationObject: cffconvert.Citation = create_citation(infile=str(pathFilenameForValidation), url=None)
	pathFilenameForValidation.unlink()

	# If the validation succeeds, write the CFF file and the CFF repo file.
	if citationObject.validate() is None:
		writeStream(pathFilenameCitationSSOT)
		if pathFilenameCitationDOTcffRepo is not None and pathFilenameCitationDOTcffRepo != pathFilenameCitationSSOT:
			writeStream(pathFilenameCitationDOTcffRepo)
		return True

	return False
