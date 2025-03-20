import pathlib
import pytest
from tests.conftest import standardizedEqualTo
from updateCitation.citationFileFormat import addCitation
from updateCitation.variables import CitationNexus

def test_addCitation(nexusCitationTesting: CitationNexus, citationAlphaDOTcff: pathlib.Path):
	"""Test that addCitation() returns a CitationNexus object."""
	nexusCitation = addCitation(nexusCitationTesting, citationAlphaDOTcff)
	assert isinstance(nexusCitation, CitationNexus), "addCitation() should return a CitationNexus object."

@pytest.mark.parametrize("fieldName, expectedValue", [
	("cffDASHversion", "1.2.0"),
	("message", "If you use this software, you can cite it using the metadata from this file."),
	("authors", [{'given-names': 'Hunter', 'family-names': 'Hogan', 'email': 'HunterHogan@pm.me'}]),
	("commit", "0d70eb67ffbab9563208ec06294887fb7fa6768a"),
	("dateDASHreleased", "2025-02-07"),
	("identifiers", [{'type': 'url', 'value': 'https://github.com/hunterhogan/mapFolding/releases/tag/0.3.9', 'description': 'The URL for mapFolding 0.3.9.'}]),
	("keywords", ['A001415', 'A001416', 'A001417', 'A001418', 'A195646', 'folding', 'map folding', 'OEIS', 'stamp folding']),
	("license", "CC-BY-NC-4.0"),
	("repository", "https://github.com/hunterhogan/mapFolding.git"),
	("repositoryDASHartifact", "https://pypi.org/project/mapfolding/0.3.9/"),
	("repositoryDASHcode", "https://github.com/hunterhogan/mapFolding/releases/tag/0.3.9"),
	("title", "mapFolding"),
	("type", "software"),
	("url", "https://github.com/hunterhogan/mapFolding"),
	("version", "0.3.9"),
])
def test_addCitation_fields(nexusCitationTesting: CitationNexus, citationAlphaDOTcff: pathlib.Path, fieldName: str, expectedValue: str):
	"""Test that addCitation() correctly sets each field in the CitationNexus object."""
	nexusCitation = addCitation(nexusCitationTesting, citationAlphaDOTcff)
	# actual = getattr(nexusCitation, fieldName)
	standardizedEqualTo(expectedValue, getattr, nexusCitation, fieldName)
