from github import Auth, Github
from typing import Any, Dict
from updateCitation import CitationNexus
import os
import warnings

def getGitHubRelease(nexusCitation: CitationNexus) -> Dict[str, Any]:
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

    githubClient = None
    try:
        # Initialize GitHub client with optional authentication
        token = os.environ.get("GITHUB_TOKEN")
        githubClient = Github(auth=Auth.Token(token)) if token else Github()

        repoFullName = nexusCitation.repository.replace("https://github.com/", "").replace(".git", "")
        repo = githubClient.get_repo(repoFullName)

        latestRelease = repo.get_latest_release()

        return {
            "dateDASHreleased": latestRelease.published_at.strftime("%Y-%m-%d"),
            "identifiers": [{
                "type": "url",
                "value": latestRelease.html_url,
                "description": f"The URL for {nexusCitation.title} {nexusCitation.version}."
            }] if latestRelease.html_url else [],
            "repositoryDASHcode": latestRelease.html_url,
        }

    except Exception as ERRORmessage:
        warnings.warn(f"Failed to get GitHub release info: {ERRORmessage}")
        return {}
    finally:
        if githubClient:
            githubClient.close()

def addGitHubRelease(nexusCitation: CitationNexus) -> CitationNexus:
    """Adds GitHub release information to a CitationNexus object.
        Parameters:
            nexusCitation (CitationNexus): The CitationNexus object to update.
        Returns:
            CitationNexus: The updated CitationNexus object with GitHub release information.
    """

    gitHubReleaseData = getGitHubRelease(nexusCitation)

    commitValue = gitHubReleaseData.get("commit")
    if commitValue:
        nexusCitation.commit = commitValue

    dateDASHreleasedValue = gitHubReleaseData.get("dateDASHreleased")
    if dateDASHreleasedValue:
        nexusCitation.dateDASHreleased = dateDASHreleasedValue

    identifiersValue = gitHubReleaseData.get("identifiers")
    if identifiersValue:
        nexusCitation.identifiers = identifiersValue

    repositoryDASHcodeValue = gitHubReleaseData.get("repositoryDASHcode")
    if repositoryDASHcodeValue:
        nexusCitation.repositoryDASHcode = repositoryDASHcodeValue

    # nexusCitation.setInStone("GitHub")
    return nexusCitation
