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
	# `._parse()` is a yaml loader
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

def writeCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path, pathFilenameCitationDOTcffRepo: pathlib.Path) -> bool:
	# NOTE embarrassingly hacky process to follow
	parameterIndent: int = 2
	parameterLineWidth: int = 60
	yamlWorkhorse = ruamel.yaml.YAML()

	def srsly(Z0Z_field: Any, Z0Z_value: Any) -> bool:
		if Z0Z_value: # empty lists
			return True
		else:
			return False

	dictionaryCitation = attrs.asdict(nexusCitation, filter=srsly)
	for keyName in list(dictionaryCitation.keys()):
		dictionaryCitation[keyName.replace("DASH", "-")] = dictionaryCitation.pop(keyName)

	pathFilenameForValidation = pathlib.Path(pathFilenameCitationSSOT).with_stem('validation')

	def writeStream(pathFilename: pathlib.Path):
		pathFilename = pathlib.Path(pathFilename)
		pathFilename.parent.mkdir(parents=True, exist_ok=True)
		with open(pathFilename, 'w') as pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith:
			yamlWorkhorse.dump(dictionaryCitation, pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith)

	writeStream(pathFilenameForValidation)

	citationObject: cffconvert.Citation = create_citation(infile=str(pathFilenameForValidation), url=None)

	pathFilenameForValidation.unlink()

	if citationObject.validate() is None:
		writeStream(pathFilenameCitationSSOT)
		writeStream(pathFilenameCitationDOTcffRepo)
		return True

	return False
