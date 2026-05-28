from __future__ import annotations

from typing import TYPE_CHECKING
from updateCitation import CitationNexus, SettingsPackage
from updateCitation.variables import cffDASHversionDefaultHARDCODED, messageDefaultHARDCODED

if TYPE_CHECKING:
	from pathlib import Path

def test_CitationNexus_requiredFields(nexusCitationTesting: CitationNexus) -> None:
	assert nexusCitationTesting.cffDASHversion == cffDASHversionDefaultHARDCODED
	assert nexusCitationTesting.message == messageDefaultHARDCODED
	assert nexusCitationTesting.authors == []
	assert nexusCitationTesting.title is None

def test_SettingsPackage_initialization(pathFilenameTmpTesting: Path) -> None:
	settings = SettingsPackage(pathFilenamePackageSSOT=pathFilenameTmpTesting)
	assert settings.pathFilenamePackageSSOT == pathFilenameTmpTesting
	assert settings.filenameCitationDOTcff == "CITATION.cff"
	assert isinstance(settings.tomlPackageData, dict)
