import pytest
from conftest import standardizedEqualTo, getPyPAMetadata, addPyPAMetadata, CitationNexus

def test_getPyPAMetadata_missingName() -> None:
	dictionaryPackageData = {
		"version": "17.19.23",
	}
	with pytest.raises(Exception):
		getPyPAMetadata(dictionaryPackageData)

def test_addPyPAMetadata_missingName(nexusCitationTesting: CitationNexus) -> None:
	dictionaryPackageData = {
		"urls": {
			"homepage": "https://gemini.stars.cosmos"
		}
	}
	with pytest.raises(Exception):
		addPyPAMetadata(nexusCitationTesting, dictionaryPackageData)
