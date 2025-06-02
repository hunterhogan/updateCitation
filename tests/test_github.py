from tests.conftest import standardizedEqualTo
from typing import Any
from unittest.mock import MagicMock, patch
from updateCitation import addGitHubRelease, addGitHubSettings, CitationNexus, SettingsPackage
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

	with patch('updateCitation.github.getGitHubRelease') as mockGetRelease:
		mockGetRelease.return_value = None
		updatedCitation = addGitHubRelease(nexusCitationTesting, settingsPackageTesting)

	# For now, we only check that it did not throw, and returns a CitationNexus.
	assert isinstance(updatedCitation, CitationNexus), (
		"Expected addGitHubRelease to return a CitationNexus"
	)

@patch('updateCitation.github.GitHubRepository')
def test_getGitHubRelease_successfulResponse(mockGitHubRepo: MagicMock, nexusCitationTesting: CitationNexus, settingsPackageTesting: SettingsPackage) -> None:
	nexusCitationTesting.repository = "owner/repo"
	nexusCitationTesting.version = "1.0.0"

	# Mock the GitHub repository and release objects
	mockRelease = MagicMock()
	mockRelease.tag_name = "1.0.0"
	mockRelease.html_url = "https://github.com/owner/repo/releases/tag/1.0.0"
	mockRelease.published_at.strftime.return_value = "2025-06-02"

	mockRepo = MagicMock()
	mockRepo.get_latest_release.return_value = mockRelease

	mockTagRef = MagicMock()
	mockTagRef.object.sha = "abc123"
	mockTagRef.object.type = "commit"
	mockRepo.get_git_ref.return_value = mockTagRef

	mockGitHubRepo.return_value.__enter__.return_value = mockRepo

	releaseData = getGitHubRelease(nexusCitationTesting, settingsPackageTesting)

	assert releaseData is not None
	assert releaseData["commit"] == "abc123"
	assert releaseData["dateDASHreleased"] == "2025-06-02"
	assert len(releaseData["identifiers"]) == 1
	assert releaseData["identifiers"][0]["value"] == "https://github.com/owner/repo/releases/tag/1.0.0"

@patch('updateCitation.github.getGitHubRelease')
def test_addGitHubRelease_withValidReleaseData(mockGetRelease: MagicMock, nexusCitationTesting: CitationNexus, settingsPackageTesting: SettingsPackage) -> None:
	nexusCitationTesting.repository = "owner/repo"
	nexusCitationTesting.version = "1.0.0"

	mockReleaseData: dict[str, Any] = {
		"commit": "abc123",
		"dateDASHreleased": "2025-06-02",
		"identifiers": [{"type": "url", "value": "https://github.com/owner/repo/releases/tag/1.0.0"}],
		"repositoryDASHcode": "https://github.com/owner/repo/releases/tag/1.0.0"
	}
	mockGetRelease.return_value = mockReleaseData

	updatedCitation = addGitHubRelease(nexusCitationTesting, settingsPackageTesting)

	assert updatedCitation.commit == "abc123"
	assert updatedCitation.dateDASHreleased == "2025-06-02"
	assert updatedCitation.identifiers == mockReleaseData["identifiers"]
	assert updatedCitation.repositoryDASHcode == "https://github.com/owner/repo/releases/tag/1.0.0"
