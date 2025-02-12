import os
import pytest
from conftest import (
	addGitHubRelease,
	addGitHubSettings,
	CitationNexus,
	getGitHubRelease,
	SettingsPackage,
	standardizedEqualTo,
)

def test_addGitHubSettings_preservesGitUserEmail(settingsPackageTesting):
	emailBefore = settingsPackageTesting.gitUserEmail
	updatedPackage = addGitHubSettings(settingsPackageTesting)
	assert updatedPackage.gitUserEmail == emailBefore, (
		f"Expected email to remain {emailBefore}, "
		f"but got {updatedPackage.gitUserEmail}"
	)

def test_getGitHubRelease_noRepository(nexusCitationTesting, settingsPackageTesting):
	nexusCitationTesting.repository = None
	dictionaryOutcome = getGitHubRelease(nexusCitationTesting, settingsPackageTesting)
	assert dictionaryOutcome == {}, "Expected empty dictionary when repository is None"

def test_addGitHubRelease_hypotheticalVersion(nexusCitationTesting, settingsPackageTesting):
	nexusCitationTesting.repository = "dummyRepo"
	nexusCitationTesting.version = "9.9.9"
	updatedCitation = addGitHubRelease(nexusCitationTesting, settingsPackageTesting)
	# For now, we only check that it did not throw, and returns a CitationNexus.
	assert isinstance(updatedCitation, CitationNexus), (
		"Expected addGitHubRelease to return a CitationNexus"
	)
