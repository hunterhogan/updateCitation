from __future__ import annotations

from ruamel.yaml import YAML
from tests.conftest import standardizedEqualTo
from typing import Any, TYPE_CHECKING
from unittest.mock import MagicMock, patch
from updateCitation import addGitHubRelease, addGitHubSettings, CitationNexus, SettingsPackage
from updateCitation.github import getGitHubRelease
import pytest

if TYPE_CHECKING:
	from pathlib import Path

def test_addGitHubSettings_preservesGitUserEmail(settingsPackageTesting: SettingsPackage) -> None:
	emailBefore = settingsPackageTesting.gitUserEmail
	updatedPackage = addGitHubSettings(settingsPackageTesting)
	assert updatedPackage.gitUserEmail == emailBefore, (
		f"Expected email to remain {emailBefore}, "
		f"but got {updatedPackage.gitUserEmail}"
	)

@pytest.mark.parametrize("environmentVariableName, tokenExpected", [
	("GITHUB_TOKEN", "tokenFibonacci13"),
])
def test_addGitHubSettings_readsGitHubTokenEnvironment(
	environmentVariableName: str,
	tokenExpected: str,
	monkeypatch: pytest.MonkeyPatch,
	settingsPackageTesting: SettingsPackage,
) -> None:
	settingsPackageTesting.GITHUB_TOKEN = None
	monkeypatch.setenv(environmentVariableName, tokenExpected)
	updatedPackage = addGitHubSettings(settingsPackageTesting)
	assert updatedPackage.GITHUB_TOKEN == tokenExpected, (
		f"addGitHubSettings returned {updatedPackage.GITHUB_TOKEN}, expected {tokenExpected} "
		f"from {environmentVariableName}."
	)

@pytest.mark.parametrize("pathFilenameWorkflowFixtureName", [
	"pathFilenameWorkflowUpdateCitation",
	"pathFilenameWorkflowUpdateCitationPackaged",
])
def test_updateCitationWorkflow_runsUpdateCitationAndExposesGitHubToken(
	pathFilenameWorkflowFixtureName: str,
	request: pytest.FixtureRequest,
) -> None:
	pathFilenameWorkflow: Path = request.getfixturevalue(pathFilenameWorkflowFixtureName)
	if not pathFilenameWorkflow.exists():
		pytest.skip(f"{pathFilenameWorkflow} is not present in this checkout.")

	workflowData: dict[str, Any] = YAML(typ="safe").load(pathFilenameWorkflow.read_text(encoding="utf-8"))  # pyright: ignore[reportUnknownMemberType]
	dictionaryStepRun: dict[str, Any] = next(
		dictionaryStep
		for dictionaryStep in workflowData["jobs"]["updateCitation"]["steps"]
		if dictionaryStep.get("name") == "Run updateCitation"
	)
	assert dictionaryStepRun["env"]["GITHUB_TOKEN"] == "${{ github.token }}", (  # noqa: S105
		f"{pathFilenameWorkflow} did not expose github.token as GITHUB_TOKEN for updateCitation."
	)
	assert dictionaryStepRun["run"].strip() == "pipx run updateCitation", (
		f"{pathFilenameWorkflow} does not run updateCitation with pipx."
	)
	assert "python -m pip install ." not in dictionaryStepRun["run"], (
		f"{pathFilenameWorkflow} installs from the local checkout instead of the reusable updateCitation package."
	)
	assert workflowData["permissions"]["contents"] == "write", (
		f"{pathFilenameWorkflow} grants {workflowData['permissions']['contents']}, expected contents write."
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
	assert releaseData["commit"] == "abc123"  # pyright: ignore[reportTypedDictNotRequiredAccess]
	assert releaseData["dateDASHreleased"] == "2025-06-02"
	assert len(releaseData["identifiers"]) == 1
	assert releaseData["identifiers"][0]["value"] == "https://github.com/owner/repo/releases/tag/1.0.0"  # pyright: ignore[reportTypedDictNotRequiredAccess]

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
