import pytest
from tests.conftest import standardizedEqualTo, getPyPAMetadata, addPyPAMetadata, CitationNexus

def test_getPyPAMetadata_missingName() -> None:
	dictionaryPackageData = {
		"version": "17.19.23",
	}
	with pytest.raises(Exception):
		getPyPAMetadata(dictionaryPackageData)
