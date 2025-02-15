from typing import Any, Union
from updateCitation import (
	add_pyprojectDOTtoml,
	addCitation,
	addGitHubRelease,
	addGitHubSettings,
	addPyPAMetadata,
	addPyPIrelease,
	CitationNexus,
	filename_pyprojectDOTtomlDEFAULT,
	gittyUpGitPushGitHub,
	getSettingsPackage,
	SettingsPackage,
	writeCitation,
)
import os
import pathlib

def here(pathFilename_pyprojectDOTtoml: Union[str, os.PathLike[Any], None] = None) -> None:
	pathFilenameSettingsSSOT = pathlib.Path(pathFilename_pyprojectDOTtoml) if pathFilename_pyprojectDOTtoml else pathlib.Path.cwd() / filename_pyprojectDOTtomlDEFAULT
	truth: SettingsPackage = getSettingsPackage(pathFilenameSettingsSSOT)

	nexusCitation = CitationNexus()

	nexusCitation = add_pyprojectDOTtoml(nexusCitation, truth)

	if not nexusCitation.title:
		# TODO learn how to change the field from `str | None` to `str` after the field is populated
		# especially for a required field
		raise ValueError("Package name is required.")

	# TODO consider whether or not my system will be intuitive for other people
	# I'm beginning to suspect it will be confusing for others and that the
	# default should be to have pathFilenameCitationSSOT = pathFilenameCitationDOTcffRepository
	# and I customize my personal settings to put pathFilenameCitationSSOT in a different place.
	if truth.pathFilenameCitationSSOT.exists():
		pathFilenameCitationSSOT = truth.pathFilenameCitationSSOT
	elif truth.pathFilenameCitationDOTcffRepository.exists():
		pathFilenameCitationSSOT = truth.pathFilenameCitationDOTcffRepository
	else:
		truth.pathFilenameCitationSSOT.parent.mkdir(parents=True, exist_ok=True)
		truth.pathFilenameCitationSSOT.write_text(f"cff-version: {nexusCitation.cffDASHversion}\n")
		pathFilenameCitationSSOT = truth.pathFilenameCitationSSOT

	nexusCitation = addCitation(nexusCitation, pathFilenameCitationSSOT)
	nexusCitation = addPyPAMetadata(nexusCitation, truth.tomlPackageData)
	truth = addGitHubSettings(truth)
	nexusCitation = addGitHubRelease(nexusCitation, truth)
	nexusCitation = addPyPIrelease(nexusCitation)

	validationStatus = writeCitation(nexusCitation, truth.pathFilenameCitationSSOT, truth.pathFilenameCitationDOTcffRepository)

	"""TODO change from
on:
	push:

to

on:
    pre-receive:

	- This will allow me to avoid making two commits.
	- allegedly, `commitInProgress = os.environ.get("GITHUB_SHA")`
	- so the citation could 1) have the correct commit hash in the same file as the release,
	and 2) the up-to-date citation file could be in the release it references.

	During some commits, I intentionally make both `dictionaryRelease` and `dictionaryReleaseHypothetical`.
	But I don't know how to conditionally use `dictionaryReleaseHypothetical` only if the Python Tests pass
	(and the release actions are successful).

	I guess if the tests were `pre-receive`, for example, I could wait to see the outcome of the tests,
	then choose the correct dictionary. I don't want to prevent the commit: I just want to put accurate information
	in the citation file.

	"""

	if validationStatus and truth.gitPushFromGitHubAction:
		gitStatus = gittyUpGitPushGitHub(truth, nexusCitation, truth.pathFilenameCitationSSOT, truth.pathFilenameCitationDOTcffRepository)
