from pathlib import Path
import pytest
from conftest import standardizedEqualTo, cffDASHversionDEFAULT, messageDEFAULT, CitationNexus, SettingsPackage

def test_CitationNexus_requiredFields(nexusCitationTesting: CitationNexus) -> None:
    assert nexusCitationTesting.cffDASHversion == cffDASHversionDEFAULT
    assert nexusCitationTesting.message == messageDEFAULT
    assert nexusCitationTesting.authors == []
    assert nexusCitationTesting.title is None

def test_CitationNexus_setInStone_failsOnMissingRequired(nexusCitationTesting: CitationNexus) -> None:
    nexusCitation = CitationNexus()
    with pytest.raises(ValueError, match="Field title is required but not provided"):
        nexusCitation.setInStone("pyprojectDOTtoml")

def test_CitationNexus_setInStone_freezesFields(nexusCitationTesting: CitationNexus) -> None:
    nexusCitationTesting.title = "SolarSystem"
    nexusCitationTesting.authors = [{"given-names": "Mercury", "family-names": "Venus"}]
    nexusCitationTesting.setInStone("pyprojectDOTtoml")

    nexusCitationTesting.title = "GalacticCore"
    assert nexusCitationTesting.title == "SolarSystem"

def test_CitationNexus_setInStone_multipleContexts(nexusCitationTesting: CitationNexus) -> None:
    nexusCitationTesting.title = "Jupiter"
    nexusCitationTesting.authors = [{"given-names": "Saturn", "family-names": "Uranus"}]
    nexusCitationTesting.version = "3.5.7"
    nexusCitationTesting.keywords = ["Neptune", "Pluto"]
    nexusCitationTesting.setInStone("pyprojectDOTtoml")
    nexusCitationTesting.setInStone("PyPA")

    # Should not change fields frozen by either context
    nexusCitationTesting.title = "NewTitle"
    nexusCitationTesting.version = "3.5.8"
    assert nexusCitationTesting.title == "Jupiter"
    assert nexusCitationTesting.version == "3.5.7"

def test_SettingsPackage_initialization(pathFilenameTmpTesting: Path) -> None:
    settings = SettingsPackage(pathFilenamePackageSSOT=pathFilenameTmpTesting)
    assert settings.pathFilenamePackageSSOT == pathFilenameTmpTesting
    assert settings.filenameCitationDOTcff == "CITATION.cff"
    assert isinstance(settings.tomlPackageData, dict)
