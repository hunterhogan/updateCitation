from contextlib import contextmanager
from typing import Any, Generator
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
import pathlib
import warnings

def addGitHubSettings(truth: SettingsPackage) -> SettingsPackage:
	truth.GITHUB_TOKEN = truth.GITHUB_TOKEN or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

	if not truth.gitUserEmail:
		githubAuth = github.Auth.Token(truth.GITHUB_TOKEN) if truth.GITHUB_TOKEN else None
		githubClient = github.Github(auth=githubAuth)

		try:
			userGitHub = githubClient.get_user()
			ImaGitUserEmail = f"{userGitHub.id}+{userGitHub.login}@users.noreply.github.com"
		except github.GithubException:
			ImaGitUserEmail = None

		githubActor = os.environ.get("GITHUB_ACTOR")
		Z0Z_email = f"{githubActor}@users.noreply.github.com" if githubActor else None
		truth.gitUserEmail = ImaGitUserEmail or Z0Z_email or gitUserEmailFALLBACK

		githubClient.close()

	return truth

@contextmanager
def GitHubRepository(nexusCitation: CitationNexus, truth: SettingsPackage) -> Generator[github.Repository.Repository, Any, None]:
	if not nexusCitation.repository:
		raise FREAKOUT

	githubAuth = github.Auth.Token(truth.GITHUB_TOKEN) if truth.GITHUB_TOKEN else None
	githubClient = github.Github(auth=githubAuth)

	full_name_or_id: str = nexusCitation.repository.replace("https://github.com/", "").replace(".git", "")
	githubRepository = githubClient.get_repo(full_name_or_id)
	try:
		yield githubRepository
	finally:
		githubClient.close()

def gittyUpGitPushGitHub(truth: SettingsPackage, nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path, pathFilenameCitationDOTcffRepository: pathlib.Path):
	environmentIsGitHubAction = bool(os.environ.get("GITHUB_ACTIONS") and os.environ.get("GITHUB_WORKFLOW"))
	if not environmentIsGitHubAction or not nexusCitation.repository:
		return

	import subprocess

	subprocess.run(["git", "config", "user.name", truth.gitUserName])
	subprocess.run(["git", "config", "user.email", truth.gitUserEmail])

	subprocess.run(["git", "add", str(pathFilenameCitationSSOT), str(pathFilenameCitationDOTcffRepository)])
	commitResult = subprocess.run(["git", "commit", "-m", truth.gitCommitMessage])
	if commitResult.returncode == 0:
		subprocess.run(["git", "push", "origin", "HEAD"])

def getGitHubRelease(nexusCitation: CitationNexus, truth: SettingsPackage):
	"""Retrieves the latest release information from a GitHub repository.
		Parameters:
			nexusCitation (CitationNexus): A CitationNexus object containing
				citation metadata, including the repository URL.
		Returns:
			Dict[str, Any]: A dictionary containing the release date,
				identifiers (release URL), and repository code URL.
				Returns an empty dictionary if the repository URL is missing
				or if an error occurs while fetching the release information.
		"""
	if not nexusCitation.repository:
		return {}

	try:
		# latestRelease.tag_name == nexusCitation.version
		if not nexusCitation.version:
			raise FREAKOUT

		# Using context management to ensure the client closes automatically.
		with GitHubRepository(nexusCitation, truth) as githubRepository:
			latestRelease = githubRepository.get_latest_release()
			commitLatestRelease = githubRepository.get_commit(latestRelease.target_commitish).sha
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

	except Exception:
		warnings.warn(f"Failed to get GitHub release information. {str(Exception)}", UserWarning)
		return {}

def addGitHubRelease(nexusCitation: CitationNexus, truth: SettingsPackage) -> CitationNexus:
	"""Adds GitHub release information to a CitationNexus object.
		Parameters:
			nexusCitation (CitationNexus): The CitationNexus object to update.
		Returns:
			CitationNexus: The updated CitationNexus object with GitHub release information.
	"""

	gitHubReleaseData = getGitHubRelease(nexusCitation, truth)

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

	# nexusCitation.setInStone("GitHub")
	return nexusCitation
