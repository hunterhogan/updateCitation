from pathlib import Path
import pytest
from conftest import standardizedEqualTo, cffDASHversionDEFAULT, messageDEFAULT, CitationNexus, SettingsPackage

def test_CitationNexus_requiredFields(nexusCitationTesting: CitationNexus) -> None:
	assert nexusCitationTesting.cffDASHversion == cffDASHversionDEFAULT
	assert nexusCitationTesting.message == messageDEFAULT
	assert nexusCitationTesting.authors == []
	assert nexusCitationTesting.title is None

def test_SettingsPackage_initialization(pathFilenameTmpTesting: Path) -> None:
	settings = SettingsPackage(pathFilenamePackageSSOT=pathFilenameTmpTesting)
	assert settings.pathFilenamePackageSSOT == pathFilenameTmpTesting
	assert settings.filenameCitationDOTcff == "CITATION.cff"
	assert isinstance(settings.tomlPackageData, dict)
