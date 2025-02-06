from updateCitation import GITHUB_API_VERSION_HEADER
from updateCitation import CitationNexus
from typing import Any, Dict
import os
import requests

def getGitHubRelease(nexusCitation: CitationNexus) -> Dict[str, Any]:
    """Return a dictionary with GitHub release data.

    The dictionary contains the following keys:
        commit: The commit hash (using the API field 'target_commitish').
        date-released: The published date (in YYYY-MM-DD format).
        identifiers: A list with one identifier object, whose description is
            'The URL for {nexusCitation.title} {nexusCitation.version}.'
        repository-code: A URL for the commit in the repository.

    Raises:
        ValueError: If the nexusCitation.repository is not set or cannot be parsed.
        RuntimeError: If the HTTP request to GitHub fails.
    """
    if not nexusCitation.repository:
        raise ValueError("Repository URL is required to get GitHub release info.")
    # To try to converge with the CFF ecosystem, much of the following logic is copy pasta from
    # cffconvert.cli.rawify_url.rawify_url()
    urlparts = nexusCitation.repository.replace("https://github.com", "", 1).strip("/").split("/") + [None] * 5
    ownername, reponame, _2, refvalue, *_filename_parts = urlparts
    reponame = reponame.replace(".git", "") # type: ignore # Remove .git from the repository name, if present.
    assert ownername is not None, "URL should include the name of the owner/organization."
    assert reponame is not None, "URL should include the name of the repository."
    if refvalue is None:
        repos_api = f"https://api.github.com/repos/{ownername}/{reponame}/releases/latest"
        headers = GITHUB_API_VERSION_HEADER
        headers.update({"Accept": "application/vnd.github+json"})
        token = os.environ.get("GITHUB_TOKEN")
        headers.update({"Authorization": f"Bearer { token }"})
        response = requests.get(repos_api, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to get GitHub release info: {response.status_code}")

    releaseData = response.json()
    # commitHash = releaseData.get("target_commitish")
    publishedAt = releaseData.get("published_at")
    if publishedAt:
        # Convert ISO timestamp (e.g., "2020-12-31T12:34:56Z") to "YYYY-MM-DD".
        publishedAt = publishedAt.split("T")[0]

    releaseHtmlUrl = releaseData.get("html_url")
    identifierDescription = f"The URL for {nexusCitation.title} {nexusCitation.version}."
    return {
        # "commit": commitHash,
        "dateDASHreleased": publishedAt,
        "identifiers": [{
            "type": "url",
            "value": releaseHtmlUrl,
            "description": identifierDescription,
        }],
        "repositoryDASHcode": releaseHtmlUrl,
    }

def addGitHubRelease(nexusCitation: CitationNexus) -> CitationNexus:
    """
    Update the nexusCitation with GitHub release information.

    This function populates the following fields on the nexusCitation:
        - commit: using the commit hash from GitHub.
        - dateDASHreleased: the release date.
        - identifiers: appends a GitHub-specific identifier.
        - repositoryDASHcode: the URL to view the commit in the repository.

    Returns:
        The updated CitationNexus instance.

    Raises:
        Any exception raised by getGitHubRelease.
    """
    gitHubReleaseData = getGitHubRelease(nexusCitation)
    nexusCitation.commit = gitHubReleaseData.get("commit")
    nexusCitation.dateDASHreleased = gitHubReleaseData.get("dateDASHreleased")
    # Overwrite the existing list of identifiers. This could be better
    nexusCitation.identifiers = gitHubReleaseData.get("identifiers", [])
    nexusCitation.repositoryDASHcode = gitHubReleaseData.get("repositoryDASHcode")
    return nexusCitation
