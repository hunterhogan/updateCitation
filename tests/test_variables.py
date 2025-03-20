from pathlib import Path
from updateCitation import CitationNexus, SettingsPackage
from updateCitation.variables import cffDASHversionDefaultHARDCODED, messageDefaultHARDCODED

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
