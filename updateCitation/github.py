from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from updateCitation import (
	CitationNexus,
	compareVersions,
	formatDateCFF,
	FREAKOUT,
	gitUserEmailFALLBACK,
	SettingsPackage,
)
import datetime
import github
import github.Repository
import os
import warnings

@contextmanager
def GithubClient(tokenAsStr: str | None) -> Generator[github.Github, Any, None]:
	"""Creates a GitHub client with authentication if a token is available.

	Parameters:
		tokenAsStr: A GitHub authentication token as a string.

	Returns:
		A GitHub client instance that will be automatically closed.
	"""
	# Don't do the following because: 1) not DRY, 2) it's "sneaky" to use environment variables without the user's knowledge.
	# tokenAsStr = tokenAsStr or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
	githubAuthToken = github.Auth.Token(tokenAsStr) if tokenAsStr else None
	githubClient = github.Github(auth=githubAuthToken)
	try:
		yield githubClient
	finally:
		githubClient.close()

def addGitHubSettings(truth: SettingsPackage) -> SettingsPackage:
	# TODO low priority: make "load token from environment variable" optional
	truth.GITHUB_TOKEN = truth.GITHUB_TOKEN or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

	if not truth.gitUserEmail:
		with GithubClient(truth.GITHUB_TOKEN) as githubClient:
			try:
				userGitHub = githubClient.get_user()
				ImaGitUserEmail = f"{userGitHub.id}+{userGitHub.login}@users.noreply.github.com"
			except github.GithubException:
				ImaGitUserEmail = None

		githubActor = os.environ.get("GITHUB_ACTOR")
		gitUserEmailGithubActor = f"{githubActor}@users.noreply.github.com" if githubActor else None
		truth.gitUserEmail = ImaGitUserEmail or gitUserEmailGithubActor or gitUserEmailFALLBACK

	return truth

@contextmanager
def GitHubRepository(nexusCitation: CitationNexus, truth: SettingsPackage) -> Generator[github.Repository.Repository, Any, None]:
	"""Creates a GitHub repository instance for the given citation.

	Parameters:
		nexusCitation: Citation object containing repository information.
		truth: Settings package containing GitHub authentication token.

	Returns:
		A GitHub repository instance.

	Raises:
		FREAKOUT: If repository information is missing.
	"""
	if not nexusCitation.repository:
		raise FREAKOUT

	with GithubClient(truth.GITHUB_TOKEN) as githubClient:
		full_name_or_id: str = nexusCitation.repository.replace("https://github.com/", "").replace(".git", "")
		githubRepository = githubClient.get_repo(full_name_or_id)
		yield githubRepository

def gittyUpGitAmendGitHub(truth: SettingsPackage, nexusCitation: CitationNexus, pathFilenameCitationSSOT: Path, pathFilenameCitationDOTcffRepository: Path):
	environmentIsGitHubAction = bool(os.environ.get("GITHUB_ACTIONS") and os.environ.get("GITHUB_WORKFLOW"))
	if not environmentIsGitHubAction or not nexusCitation.repository:
		return

	import subprocess
	# TODO I don't like that this flow assumes `git` is installed and available in the environment.
	# Can I use `GitHubRepository` instead of `subprocess`?

	subprocess.run(["git", "config", "user.name", truth.gitUserName])
	subprocess.run(["git", "config", "user.email", truth.gitUserEmail])

	# Stage the citation files
	subprocess.run(["git", "add", str(pathFilenameCitationSSOT), str(pathFilenameCitationDOTcffRepository)])

	commitResult = subprocess.run(["git", "commit", "-m", truth.gitCommitMessage])
	if commitResult.returncode == 0:
		subprocess.run(["git", "push", "origin", "HEAD"])

def getGitHubRelease(nexusCitation: CitationNexus, truth: SettingsPackage) -> dict[str, Any] | None:
	"""Retrieves the latest release information from a GitHub repository.
		Parameters:
			nexusCitation: A CitationNexus object containing citation metadata, including the repository URL.
		Returns:
			dictionaryRelease: A dictionary containing release information or an empty dictionary.
		Raises:
			NEVER: `Exception` is caught and converted to a warning. (So, don't filter all warnings, you know?)
		"""
	if not nexusCitation.repository:
		return None

	try:
		# NOTE latestRelease.tag_name == nexusCitation.version
		if not nexusCitation.version:
			raise FREAKOUT

		with GitHubRepository(nexusCitation, truth) as githubRepository:
			latestRelease = githubRepository.get_latest_release()
			tagObject = githubRepository.get_git_ref(f'tags/{latestRelease.tag_name}').object
			# TODO `commitLatestRelease` should be fixed but it's not
			commitLatestRelease = tagObject.sha if tagObject.type == 'tag' else tagObject.sha
			commitLatestCommit = githubRepository.get_commit(githubRepository.default_branch).sha

		urlRelease = latestRelease.html_url

		dictionaryRelease = {
			"commit": commitLatestRelease,
			"dateDASHreleased": latestRelease.published_at.strftime(formatDateCFF),
			"identifiers": [{
				"type": "url",
				"value": urlRelease,
				"description": f"The URL for {nexusCitation.title} {latestRelease.tag_name}."
			}] if urlRelease else [],
			"repositoryDASHcode": urlRelease,
		}

		if compareVersions(latestRelease.tag_name, nexusCitation.version) == -1:
			dictionaryReleaseHypothetical = {
				"commit": commitLatestCommit,
				"dateDASHreleased": datetime.datetime.now().strftime(formatDateCFF),
				"identifiers": [{
					"type": "url",
					"value": urlRelease.replace(latestRelease.tag_name, nexusCitation.version),
					"description": f"The URL for {nexusCitation.title} {nexusCitation.version}."
				}] if urlRelease else [],
				"repositoryDASHcode": urlRelease.replace(latestRelease.tag_name, nexusCitation.version),
			}
			dictionaryRelease.update(dictionaryReleaseHypothetical)

		return dictionaryRelease

	except Exception as ERRORmessage:
		warnings.warn(f"Failed to get GitHub release information. {ERRORmessage}", UserWarning)
		return None

def addGitHubRelease(nexusCitation: CitationNexus, truth: SettingsPackage) -> CitationNexus:
	"""Adds GitHub release information to a CitationNexus object.
		Parameters:
			nexusCitation: The CitationNexus object to update.
		Returns:
			CitationNexus: The updated CitationNexus object with GitHub release information.
	"""

	gitHubReleaseData = getGitHubRelease(nexusCitation, truth)

	if gitHubReleaseData:
		commitSherpa = gitHubReleaseData.get("commit")
		if commitSherpa:
			nexusCitation.commit = commitSherpa

		dateDASHreleasedSherpa = gitHubReleaseData.get("dateDASHreleased")
		if dateDASHreleasedSherpa:
			nexusCitation.dateDASHreleased = dateDASHreleasedSherpa

		identifiersSherpa = gitHubReleaseData.get("identifiers")
		if identifiersSherpa:
			nexusCitation.identifiers = identifiersSherpa

		repositoryDASHcodeSherpa = gitHubReleaseData.get("repositoryDASHcode")
		if repositoryDASHcodeSherpa:
			nexusCitation.repositoryDASHcode = repositoryDASHcodeSherpa

	nexusCitation.setInStone("GitHub")
	return nexusCitation
