import pathlib
from updateCitation import CitationNexus
import bibtex2cff
import bibtex2cff.convert_cff

def getBibtex(pathFilename: pathlib.Path):
	"""Convert a BibTeX file into a CFF reference entry.

	Args:
		pathFilename: Path to a BibTeX file.

	Returns:
		A dictionary containing the CFF reference data.
	"""
	return bibtex2cff.convert_cff.CFFDefinitionUpdate(str(pathFilename)).get_definition

def addReferences(nexusCitation: CitationNexus) -> CitationNexus:
	pathFilenameExampleBibTeX = pathlib.Path('/apps/mapFolding/citations/Lunnon.bibtex')
	"""
bibtex2cff:
KeyError: 'article'
srsly?
	"""
	# pathFilenameExampleBibTeX = pathlib.Path('/apps/mapFolding/citations/jOEIS.bibtex')
	"""
CFF schema:
"required": [
	"authors",
	"title",
	"type"
],

But, bibtex2cff:
pydantic.error_wrappers.ValidationError: 3 validation errors for BibTeXDefinition
month
  field required (type=value_error.missing)
publisher
  field required (type=value_error.missing)
doi
  field required (type=value_error.missing)
	"""
	nexusCitation.references.append(getBibtex(pathFilenameExampleBibTeX))
	return nexusCitation
