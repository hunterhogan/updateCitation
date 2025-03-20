from os import PathLike
from pathlib import Path
from typing import Any
from updateCitation import (
	add_pyprojectDOTtoml,
	addCitation,
	addGitHubRelease,
	addGitHubSettings,
	addPyPAMetadata,
	addPyPIrelease,
	CitationNexus,
	filename_pyprojectDOTtomlDEFAULT,
	gittyUpGitAmendGitHub,
	getSettingsPackage,
	SettingsPackage,
	writeCitation,
)

def here(pathFilename_pyprojectDOTtoml: str | PathLike[Any] | None = None) -> None:
	pathFilenameSettingsSSOT = Path(pathFilename_pyprojectDOTtoml) if pathFilename_pyprojectDOTtoml else Path.cwd() / filename_pyprojectDOTtomlDEFAULT
	truth: SettingsPackage = getSettingsPackage(pathFilenameSettingsSSOT)

	nexusCitation = CitationNexus()

	nexusCitation = add_pyprojectDOTtoml(nexusCitation, truth)

	if not nexusCitation.title:
		# TODO learn how to change the field from `str | None` to `str` after the field is populated
		# especially for a required field
		raise ValueError("Package name is required.")

	if Path(truth.pathFilenameCitationSSOT).exists():
		pathFilenameCitationSSOT = truth.pathFilenameCitationSSOT
	elif Path(truth.pathFilenameCitationDOTcffRepository).exists():
		pathFilenameCitationSSOT = truth.pathFilenameCitationDOTcffRepository
	else:
		truth.pathFilenameCitationSSOT.parent.mkdir(parents=True, exist_ok=True)
		truth.pathFilenameCitationSSOT.write_text(f"cff-version: {nexusCitation.cffDASHversion}\n")
		pathFilenameCitationSSOT = truth.pathFilenameCitationSSOT

	nexusCitation = addCitation(nexusCitation, pathFilenameCitationSSOT)
	nexusCitation = addPyPAMetadata(nexusCitation, truth.tomlPackageData, truth.projectURLTargets)
	truth = addGitHubSettings(truth)
	if truth.Z0Z_addGitHubRelease:
		nexusCitation = addGitHubRelease(nexusCitation, truth)
	if truth.Z0Z_addPyPIrelease:
		nexusCitation = addPyPIrelease(nexusCitation)

	validationStatus = writeCitation(nexusCitation, truth.pathFilenameCitationSSOT, truth.pathFilenameCitationDOTcffRepository)

	"""TODO remove the second push
	TODO figure out the sha paradox
	TODO possibly related: fix the `commitLatestRelease` value in `getGitHubRelease`
	- allegedly, `commitInProgress = os.environ.get("GITHUB_SHA")`
	- so the citation could 1) have the correct commit hash in the same file as the release,
	and 2) the up-to-date citation file could be in the release it references.

	During some commits, I intentionally make both `dictionaryRelease` and `dictionaryReleaseHypothetical`.
	But I don't know how to conditionally use `dictionaryReleaseHypothetical` only if the Python Tests pass
	(and the release actions are successful).

	I guess I could wait to see the outcome of the tests,
	then choose the correct dictionary. I don't want to prevent the commit: I just want to put accurate information
	in the citation file.

	"""

	if validationStatus and truth.gitAmendFromGitHubAction:
		gittyUpGitAmendGitHub(truth, nexusCitation, truth.pathFilenameCitationSSOT, truth.pathFilenameCitationDOTcffRepository)
