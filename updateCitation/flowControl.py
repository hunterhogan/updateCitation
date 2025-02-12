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

	nexusCitation, truth = add_pyprojectDOTtoml(nexusCitation, truth)

	if not nexusCitation.title:
		# TODO learn how to change the field from `str | None` to `str` after the field is populated
		# especially for a required field
		raise ValueError("Package name is required.")

	nexusCitation = addCitation(nexusCitation, truth.pathFilenameCitationSSOT)
	nexusCitation = addPyPAMetadata(nexusCitation, truth.tomlPackageData)
	truth = addGitHubSettings(truth)
	nexusCitation = addGitHubRelease(nexusCitation, truth)
	nexusCitation = addPyPIrelease(nexusCitation)

	validationStatus = writeCitation(nexusCitation, truth.pathFilenameCitationSSOT, truth.pathFilenameCitationDOTcffRepository)

	if validationStatus and truth.gitPushFromGitHubAction:
		gitStatus = gittyUpGitPushGitHub(truth, nexusCitation, truth.pathFilenameCitationSSOT, truth.pathFilenameCitationDOTcffRepository)
