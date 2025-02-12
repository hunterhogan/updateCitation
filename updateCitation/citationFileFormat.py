from cffconvert.cli.create_citation import create_citation
from typing import Any, Dict, List
from updateCitation import CitationNexus, CitationNexusFieldsFrozen
import attrs
import cffconvert
import pathlib
import ruamel.yaml

def addCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path) -> CitationNexus:
	"""Given a path to a citation file, return a CitationNexus object.
		The citation file is expected to be in a format that can be parsed by
		`cffconvert.cli.create_citation.create_citation()`. This function
		ensures convergence with the CFF ecosystem by using `create_citation`
		and its internal `_parse()` method.
		Parameters:
			pathFilenameCitationSSOT (pathlib.Path): Path to the citation file.
		Returns:
			CitationNexus: A CitationNexus object populated with data from the
				citation file.
		"""

	# `cffconvert.cli.create_citation.create_citation()` is PAINFULLY mundane, but a major problem
	# in the CFF ecosystem is divergence. Therefore, I will use this function so that my code
	# converges with the CFF ecosystem.
	citationObject: cffconvert.Citation = create_citation(infile=pathFilenameCitationSSOT, url=None)
	# `._parse()` is a yaml loader: use it for convergence
	cffobj: Dict[Any, Any] = citationObject._parse()

	# This step is designed to prevent deleting fields that are populated in the current CFF file,
	# but for whatever reason do not get added to the CitationNexus object.
	Z0Z_list: List[attrs.Attribute] = list(attrs.fields(type(nexusCitation)))
	for Z0Z_field in Z0Z_list:
		if Z0Z_field.name in CitationNexusFieldsFrozen:
			continue
		cffobjKeyName: str = Z0Z_field.name.replace("DASH", "-")
		cffobjValue = cffobj.get(cffobjKeyName)
		if cffobjValue: # An empty list will be False
			setattr(nexusCitation, Z0Z_field.name, cffobjValue)

	# nexusCitation.setInStone("Citation")
	return nexusCitation

def writeCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path, pathFilenameCitationDOTcffRepo: pathlib.Path) -> bool:
	# NOTE embarrassingly hacky process to follow
	parameterIndent= 2
	parameterLineWidth = 60
	yamlWorkhorse = ruamel.yaml.YAML()

	def srsly(Z0Z_filed, Z0Z_value):
		if Z0Z_value: # empty lists
			return True
		else:
			return False

	dictionaryCitation = attrs.asdict(nexusCitation, filter=srsly)
	for keyName in list(dictionaryCitation.keys()):
		dictionaryCitation[keyName.replace("DASH", "-")] = dictionaryCitation.pop(keyName)

	pathFilenameForValidation = pathFilenameCitationSSOT.with_stem('validation')

	def writeStream(pathFilename):
		with open(pathFilename, 'w') as pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith:
			yamlWorkhorse.dump(dictionaryCitation, pathlibIsAStealthContextManagerThatRuamelCannotDetectAndRefusesToWorkWith)

	writeStream(pathFilenameForValidation)

	citationObject: cffconvert.Citation = create_citation(infile=pathFilenameForValidation, url=None)

	pathFilenameForValidation.unlink()

	if citationObject.validate() is None:
		writeStream(pathFilenameCitationSSOT)
		writeStream(pathFilenameCitationDOTcffRepo)
		return True

	return False
