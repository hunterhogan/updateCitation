from __future__ import annotations

from tests.conftest import standardizedEqualTo
from typing import Any
from updateCitation import addPyPAMetadata, CitationNexus
from updateCitation.pypa import getPyPAMetadata
import pytest

def test_getPyPAMetadata_missingName() -> None:
	dictionaryPackageData = {
		"version": "17.19.23",
	}
	with pytest.raises(Exception):
		getPyPAMetadata(dictionaryPackageData)

@pytest.mark.parametrize("dictionaryPackageData, nameExpected, projectURLsExpected", [
	(
		{
			"name": "Citation-Diamond",
			"version": "2.3.5",
			"keywords": ["citation", "metadata"],
			"license": "MIT",
			"urls": {
				"Homepage": "https://example.test/citation-diamond",
				"Repository": "https://github.com/hunterhogan/citation-diamond",
			},
		},
		"citation-diamond",
		{
			"homepage": "https://example.test/citation-diamond",
			"repository": "https://github.com/hunterhogan/citation-diamond",
		},
	),
	(
		{
			"name": "Citation-Emerald",
			"version": "3.5.8",
			"keywords": ["citation", "metadata"],
			"urls": {
				"Homepage": "https://example.test/citation-emerald",
				"Repository": "https://github.com/hunterhogan/citation-emerald",
			},
		},
		"citation-emerald",
		{
			"homepage": "https://example.test/citation-emerald",
			"repository": "https://github.com/hunterhogan/citation-emerald",
		},
	),
])
def test_getPyPAMetadata_validPackageData(
	dictionaryPackageData: dict[str, Any],
	nameExpected: str,
	projectURLsExpected: dict[str, str],
) -> None:
	pypaMetadata = getPyPAMetadata(dictionaryPackageData)
	assert pypaMetadata.name == nameExpected, (
		f"getPyPAMetadata returned name {pypaMetadata.name}, expected {nameExpected}."
	)
	assert pypaMetadata.project_urls == projectURLsExpected, (
		f"getPyPAMetadata returned project URLs {pypaMetadata.project_urls}, expected {projectURLsExpected}."
	)
