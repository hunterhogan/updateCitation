from __future__ import annotations

from tests.conftest import standardizedEqualTo
from updateCitation import addPyPAMetadata, CitationNexus
from updateCitation.pypa import getPyPAMetadata
import pytest

def test_getPyPAMetadata_missingName() -> None:
	dictionaryPackageData = {
		"version": "17.19.23",
	}
	with pytest.raises(Exception):
		getPyPAMetadata(dictionaryPackageData)
