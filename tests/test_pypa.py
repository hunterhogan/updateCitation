import pytest
from tests.conftest import standardizedEqualTo
from updateCitation import addPyPAMetadata, CitationNexus
from updateCitation.pypa import getPyPAMetadata

def test_getPyPAMetadata_missingName() -> None:
	dictionaryPackageData = {
		"version": "17.19.23",
	}
	with pytest.raises(Exception):
		getPyPAMetadata(dictionaryPackageData)
