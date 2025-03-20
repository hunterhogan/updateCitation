import os
import pytest
from updateCitation import (
	addGitHubRelease,
	addGitHubSettings,
	CitationNexus,
	SettingsPackage,
)
from tests.conftest import standardizedEqualTo
from updateCitation.github import getGitHubRelease

def test_addGitHubSettings_preservesGitUserEmail(settingsPackageTesting: SettingsPackage) -> None:
	emailBefore = settingsPackageTesting.gitUserEmail
	updatedPackage = addGitHubSettings(settingsPackageTesting)
	assert updatedPackage.gitUserEmail == emailBefore, (
		f"Expected email to remain {emailBefore}, "
		f"but got {updatedPackage.gitUserEmail}"
	)

def test_getGitHubRelease_noRepository(nexusCitationTesting: CitationNexus, settingsPackageTesting: SettingsPackage) -> None:
	nexusCitationTesting.repository = None
	standardizedEqualTo(None, getGitHubRelease, nexusCitationTesting, settingsPackageTesting)

def test_addGitHubRelease_hypotheticalVersion(nexusCitationTesting: CitationNexus, settingsPackageTesting: SettingsPackage) -> None:
	nexusCitationTesting.repository = "dummyRepo"
	nexusCitationTesting.version = "9.9.9"
	updatedCitation = addGitHubRelease(nexusCitationTesting, settingsPackageTesting)
	# For now, we only check that it did not throw, and returns a CitationNexus.
	assert isinstance(updatedCitation, CitationNexus), (
		"Expected addGitHubRelease to return a CitationNexus"
	)
