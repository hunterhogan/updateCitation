"""Integrate GitHub API data into citation metadata.

(AI generated docstring)

You can use this module to authenticate with the GitHub API [1], retrieve
release information from a repository, populate `CitationNexus` [2] with
GitHub-sourced field, and commit and push updated CITATION.cff file from
a GitHub Actions environment.

Contents
--------
Functions
	addGitHubRelease
		Populate a `CitationNexus` with GitHub release metadata.
	addGitHubSettings
		Configure GitHub authentication and git user email on a `SettingsPackage`.
	getGitHubRelease
		Retrieve the latest release information from a GitHub repository.
	GitHubClient
		Create an authenticated GitHub API client as a context manager.
	GitHubRepository
		Create a GitHub repository instance as a context manager.
	gittyUpGitAmendGitHub
		Commit and push citation file from a GitHub Actions environment.

References
----------
[1] PyGithub - GitHub API client
	https://pygithub.readthedocs.io/en/stable/
[2] updateCitation.variables.CitationNexus
	Internal package reference

"""
from __future__ import annotations

from contextlib import contextmanager
from github import GithubException
from pathlib import Path
from typing import TYPE_CHECKING
from updateCitation import (
	CitationNexus, comparandPrecedesComparator, compareVersions, formatDateCFF, FREAKOUT, gitUserEmailFALLBACK, Identifier, SettingsPackage)
import datetime
import github
import os
import warnings

if TYPE_CHECKING:
	from collections.abc import Generator
	from github.AuthenticatedUser import AuthenticatedUser as GitHubAuthenticatedUser
	from github.Branch import Branch
	from github.GitObject import GitObject
	from github.GitRelease import GitRelease
	from github.NamedUser import NamedUser as GitHubNamedUser
	from github.Repository import Repository
	from updateCitation import GitHubReleaseData

@contextmanager
def GitHubClient(tokenAsStr: str | None) -> Generator[github.Github]:
	"""Create an authenticated GitHub API client as a context manager.

	(AI generated docstring)

	You can use `GitHubClient` to obtain a `github.Github` [1] instance
	that is automatically closed when the context manager exits. If
	`tokenAsStr` is provided, the client authenticates with
	`github.Auth.Token` [1]. If `tokenAsStr` is `None`, the client
	connects without authentication.

	Parameters
	----------
	tokenAsStr : str | None
		A GitHub authentication token string, or `None` for unauthenticated
		access.

	Yields
	------
	gitHubClient : github.Github
		An authenticated (or unauthenticated) GitHub API client.

	References
	----------
	[1] PyGithub - GitHub API client
		https://pygithub.readthedocs.io/en/stable/

	"""
	gitHubAuthToken: github.Auth.Token | None = github.Auth.Token(tokenAsStr) if tokenAsStr else None
	gitHubClient: github.Github = github.Github(auth=gitHubAuthToken)
	try:
		yield gitHubClient
	finally:
		gitHubClient.close()

def addGitHubSettings(truth: SettingsPackage) -> SettingsPackage:
	"""Configure GitHub authentication and git user email on a `SettingsPackage`.

	(AI generated docstring)

	You can use `addGitHubSettings` to populate `truth.GITHUB_TOKEN` from
	environment variable `GITHUB_TOKEN` or `GH_TOKEN` if the token is not
	already set. The function also resolves `truth.gitUserEmail` by querying
	the GitHub API [1] for the authenticated user, falling back to the
	`GITHUB_ACTOR` environment variable, and finally to
	`gitUserEmailFALLBACK` [2].

	Parameters
	----------
	truth : SettingsPackage
		The settings object to configure.

	Returns
	-------
	truthConfigured : SettingsPackage
		The `truth` object with `GITHUB_TOKEN` and `gitUserEmail` populated.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		truth = addGitHubSettings(truth)

	Real usage from test suite:

		updatedPackage = addGitHubSettings(settingsPackageTesting)

	References
	----------
	[1] PyGithub - GitHub API client
		https://pygithub.readthedocs.io/en/stable/
	[2] updateCitation.variables.gitUserEmailFALLBACK
		Internal package reference

	"""
	truth.GITHUB_TOKEN = truth.GITHUB_TOKEN or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

	if not truth.gitUserEmail:
		with GitHubClient(truth.GITHUB_TOKEN) as gitHubClient:
			try:
				userGitHub: GitHubAuthenticatedUser | GitHubNamedUser = gitHubClient.get_user()
				gitUserEmailFromGitHubUser: str | None = f"{userGitHub.id}+{userGitHub.login}@users.noreply.github.com"
			except GithubException:
				gitUserEmailFromGitHubUser = None

		gitHubActor: str | None = os.environ.get("GITHUB_ACTOR")
		gitUserEmailGitHubActor: str | None = f"{gitHubActor}@users.noreply.github.com" if gitHubActor else None
		truth.gitUserEmail = gitUserEmailFromGitHubUser or gitUserEmailGitHubActor or gitUserEmailFALLBACK

	return truth

@contextmanager
def GitHubRepository(nexusCitation: CitationNexus, truth: SettingsPackage) -> Generator[Repository]:
	"""Create a GitHub repository instance as a context manager.

	(AI generated docstring)

	You can use `GitHubRepository` to obtain a `github.Repository.Repository` [1]
	instance for the repository URL stored in `nexusCitation.repository`. The
	function extracts the owner and repository name from the URL and uses
	`GitHubClient` [2] to authenticate.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object containing the `repository` URL.
	truth : SettingsPackage
		The settings object containing the GitHub authentication token.

	Yields
	------
	gitHubRepository : github.Repository.Repository
		A GitHub repository instance.

	Raises
	------
	FREAKOUT
		If `nexusCitation.repository` is falsy.

	References
	----------
	[1] PyGithub - GitHub API client
		https://pygithub.readthedocs.io/en/stable/
	[2] updateCitation.github.GitHubClient
		Internal package reference

	"""
	if not nexusCitation.repository:
		raise FREAKOUT

	with GitHubClient(truth.GITHUB_TOKEN) as gitHubClient:
		full_name_or_id: str = nexusCitation.repository.replace("https://github.com/", "").replace(".git", "")
		yield gitHubClient.get_repo(full_name_or_id)

def gittyUpGitAmendGitHub(truth: SettingsPackage, nexusCitation: CitationNexus, pathFilenameCitationSSOT: Path, pathFilenameCitationDOTcffRepository: Path) -> None:
	"""Commit and push citation file from a GitHub Actions environment.

	(AI generated docstring)

	You can use `gittyUpGitAmendGitHub` to stage, commit, and push the updated
	CITATION.cff file when running inside a GitHub Actions workflow. The
	function checks for the `GITHUB_ACTIONS` and `GITHUB_WORKFLOW` environment
	variable and returns immediately if the environment is not a GitHub Actions
	runner or if `nexusCitation.repository` is falsy. The function appends
	"Update CITATION.cff" to the previous commit message unless the message
	already contains that text.

	Parameters
	----------
	truth : SettingsPackage
		The settings object containing git user name and email.
	nexusCitation : CitationNexus
		The citation object containing the `repository` URL.
	pathFilenameCitationSSOT : Path
		The full path to the authoritative CITATION.cff file to stage.
	pathFilenameCitationDOTcffRepository : Path
		The full path to the repository-root CITATION.cff file to stage.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		gittyUpGitAmendGitHub(
			truth, nexusCitation, truth.pathFilenameCitationSSOT,
			truth.pathFilenameCitationDOTcffRepository)

	"""  # noqa: DOC501
	environmentIsGitHubAction: bool = bool(os.environ.get("GITHUB_ACTIONS") and os.environ.get("GITHUB_WORKFLOW"))
	if environmentIsGitHubAction and nexusCitation.repository:

		with GitHubRepository(nexusCitation, truth) as gitHubRepository:
			branchName: str = os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_REF_NAME") or gitHubRepository.default_branch
			branch: Branch = gitHubRepository.get_branch(branchName)
			previousCommitMessageLines: list[str] = branch.commit.commit.message.strip().splitlines()
			if previousCommitMessageLines:
				previousCommitMessage: str = previousCommitMessageLines[0].strip()
			else:
				previousCommitMessage = ""
			gitAuthor: github.InputGitAuthor = github.InputGitAuthor(truth.gitUserName, truth.gitUserEmail)
			dictionaryPathsCitation: dict[str, Path] = {
				Path(pathFilename).relative_to(truth.pathRepository).as_posix(): Path(pathFilename)
				for pathFilename in (pathFilenameCitationSSOT, pathFilenameCitationDOTcffRepository)
			}

			if previousCommitMessage:
				# Only append if the previous message doesn't already contain citation update text
				if "Update CITATION.cff" not in previousCommitMessage:
					combinedCommitMessage: str = f"{previousCommitMessage} + Update CITATION.cff [skip ci]"
				else:
					combinedCommitMessage = truth.gitCommitMessage
			else:
				combinedCommitMessage = truth.gitCommitMessage

			for pathCitationRepository, pathFilenameCitation in dictionaryPathsCitation.items():
				contentCitation: str = pathFilenameCitation.read_text(encoding="utf-8")
				try:
					contentFile = gitHubRepository.get_contents(pathCitationRepository, ref=branchName)
				except github.GithubException as exception:
					if exception.status != 404:
						raise
					gitHubRepository.create_file(
						pathCitationRepository
						, combinedCommitMessage
						, contentCitation
						, branch=branchName
						, author=gitAuthor
						, committer=gitAuthor
					)
				else:
					if isinstance(contentFile, list):
						raise FREAKOUT
					if contentFile.decoded_content.decode("utf-8") != contentCitation:
						gitHubRepository.update_file(
							pathCitationRepository
							, combinedCommitMessage
							, contentCitation
							, contentFile.sha
							, branch=branchName
							, author=gitAuthor
							, committer=gitAuthor
						)

def getGitHubRelease(nexusCitation: CitationNexus, truth: SettingsPackage) -> GitHubReleaseData | None:
	"""Retrieve the latest release information from a GitHub repository.

	(AI generated docstring)

	You can use `getGitHubRelease` to query the GitHub API [1] for the latest
	release of the repository specified in `nexusCitation.repository`. The
	function returns a dictionary containing `commit`, `dateDASHreleased`,
	`identifiers`, and `repositoryDASHcode` field. If the latest release tag
	is older than `nexusCitation.version` (compared via `compareVersions` [2]),
	the function produces hypothetical release data for the upcoming version.
	If any `Exception` occurs, the function emits a `UserWarning` and returns
	`None`.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object containing `repository` URL and `version`.
	truth : SettingsPackage
		The settings object containing the GitHub authentication token.

	Returns
	-------
	dictionaryRelease : dict[str, Any] | None
		A dictionary of release metadata field, or `None` if the repository
		is not set or retrieval fails.

	Examples
	--------
	Real usage from test suite:

		standardizedEqualTo(None, getGitHubRelease, nexusCitationTesting,
			settingsPackageTesting)

	References
	----------
	[1] PyGithub - GitHub API client
		https://pygithub.readthedocs.io/en/stable/
	[2] updateCitation.pypa.compareVersions
		Internal package reference

	"""  # noqa: DOC501
	if nexusCitation.repository:

		# TODO I think my goal here is to get the information, but carry on if there is an exception. I
		# suspect I should use contextlib instead.
		try:  # NOTE releaseLatest.tag_name == nexusCitation.version  # noqa: PLW0717
			if not nexusCitation.version:
				raise FREAKOUT  # noqa: TRY301

			with GitHubRepository(nexusCitation, truth) as gitHubRepository:
				releaseLatest: GitRelease = gitHubRepository.get_latest_release()
				tagObject: GitObject = gitHubRepository.get_git_ref(f'tags/{releaseLatest.tag_name}').object
				if tagObject.type == 'tag':
					commitReleaseLatest: str = gitHubRepository.get_git_tag(tagObject.sha).object.sha
				else:
					commitReleaseLatest: str = tagObject.sha

			urlRelease: str = releaseLatest.html_url

			dictionaryRelease: GitHubReleaseData = {
				"commit": commitReleaseLatest,
				"dateDASHreleased": releaseLatest.published_at.strftime(formatDateCFF),
				"identifiers": [{
					"type": "url",
					"value": urlRelease,
					"description": f"The URL for {nexusCitation.title} {releaseLatest.tag_name}."
				}] if urlRelease else [],
				"repositoryDASHcode": urlRelease,
			}

			if compareVersions(releaseLatest.tag_name, nexusCitation.version) == comparandPrecedesComparator:
				dictionaryReleaseHypothetical: GitHubReleaseData = {
					"dateDASHreleased": datetime.datetime.now(datetime.UTC).strftime(formatDateCFF),
					"identifiers": [{
						"type": "url",
						"value": urlRelease.replace(releaseLatest.tag_name, nexusCitation.version),
						"description": f"The URL for {nexusCitation.title} {nexusCitation.version}."
					}] if urlRelease else [],
					"repositoryDASHcode": urlRelease.replace(releaseLatest.tag_name, nexusCitation.version),
				}
				dictionaryRelease.update(dictionaryReleaseHypothetical)

			return dictionaryRelease

		except Exception as ERRORmessage:
			warnings.warn(f"Failed to get GitHub release information. {ERRORmessage}", UserWarning, stacklevel=2)
			return None
	return None

def addGitHubRelease(nexusCitation: CitationNexus, truth: SettingsPackage) -> CitationNexus:
	"""Populate a `CitationNexus` with GitHub release metadata.

	(AI generated docstring)

	You can use `addGitHubRelease` to merge GitHub release data into
	`nexusCitation`. The function calls `getGitHubRelease` [1] to retrieve
	release information, then sets `commit`, `dateDASHreleased`, `identifiers`,
	and `repositoryDASHcode` on `nexusCitation`. After populating, the function
	calls `nexusCitation.setInStone("GitHub")` [2] to freeze the
	GitHub-owned field.

	Parameters
	----------
	nexusCitation : CitationNexus
		The citation object to populate with GitHub release data.
	truth : SettingsPackage
		The settings object containing the GitHub authentication token.

	Returns
	-------
	nexusCitationPopulated : CitationNexus
		The `nexusCitation` object with GitHub release field populated.

	Examples
	--------
	Real usage from updateCitation.flowControl module:

		nexusCitation = addGitHubRelease(nexusCitation, truth)

	Real usage from test suite:

		updatedCitation = addGitHubRelease(nexusCitationTesting, settingsPackageTesting)

	References
	----------
	[1] updateCitation.github.getGitHubRelease
		Internal package reference
	[2] updateCitation.variables.CitationNexus.setInStone
		Internal package reference

	"""
	gitHubReleaseData: GitHubReleaseData | None = getGitHubRelease(nexusCitation, truth)

	if gitHubReleaseData:
		commitSherpa: str | None = gitHubReleaseData.get("commit")
		if commitSherpa:
			nexusCitation.commit = commitSherpa

		dateDASHreleasedSherpa: str | None = gitHubReleaseData.get("dateDASHreleased")
		if dateDASHreleasedSherpa:
			nexusCitation.dateDASHreleased = dateDASHreleasedSherpa

		identifiersSherpa: list[Identifier] | None = gitHubReleaseData.get("identifiers")
		if identifiersSherpa:
			nexusCitation.identifiers = identifiersSherpa

		repositoryDASHcodeSherpa: str | None = gitHubReleaseData.get("repositoryDASHcode")
		if repositoryDASHcodeSherpa:
			nexusCitation.repositoryDASHcode = repositoryDASHcodeSherpa

	nexusCitation.setInStone("GitHub")
	return nexusCitation
