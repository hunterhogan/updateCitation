from __future__ import annotations

from typing import NotRequired, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
	from updateCitation import Identifier

class GitHubReleaseData(TypedDict):
	"""GitHub release metadata returned by `getGitHubRelease`."""

	commit: NotRequired[str]
	dateDASHreleased: str
	identifiers: list[Identifier]
	repositoryDASHcode: str
