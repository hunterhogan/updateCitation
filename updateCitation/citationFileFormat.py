from cffconvert.cli.create_citation import create_citation
from typing import Any
from updateCitation import CitationNexus
import attrs
import cffconvert
import pathlib
import ruamel.yaml

def getCitation(pathFilenameCitationSSOT: pathlib.Path) -> dict[str, Any]:
	# Try to converge with cffconvert when possible.
	citationObject: cffconvert.Citation = create_citation(infile=str(pathFilenameCitationSSOT), url=None)
	# `._parse()` is `ruamel.yaml.YAML` loader
	return citationObject._parse()

def addCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path) -> CitationNexus:
	cffobj = getCitation(pathFilenameCitationSSOT)

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
	# NOTE embarrassingly hacky process to follow

	# TODO format the output
	# parameterIndent: int = 2
	# parameterLineWidth: int = 60

	# use `ruamel.yaml` because using the same packages and identifiers as `cffconvert` and other CFF ecosystem tools has benefits
	yamlWorkhorse = ruamel.yaml.YAML()

	def srsly(Z0Z_field: Any, Z0Z_value: Any) -> bool:
		if Z0Z_value: # empty lists
			return True
		else:
			return False

	# Convert the attrs object to a dictionary.
	dictionaryCitation = attrs.asdict(nexusCitation, filter=srsly)

	# Rename the keys to match the CFF format.
	for keyName in list(dictionaryCitation.keys()):
		dictionaryCitation[keyName.replace("DASH", "-")] = dictionaryCitation.pop(keyName)

	# This function and this context manager only exist to work around the fact that `ruamel.yaml` does not support `pathlib.Path` objects.
	def writeStream(pathFilename: pathlib.Path) -> None:
		pathFilename = pathlib.Path(pathFilename)
		pathFilename.parent.mkdir(parents=True, exist_ok=True)
		with open(pathFilename, 'w') as pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith:
			yamlWorkhorse.dump(dictionaryCitation, pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith)

	# Write the validation file because I haven't figured out how to validate it as a stream yet.
	pathFilenameForValidation = pathlib.Path(pathFilenameCitationSSOT).with_stem('validation')
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
