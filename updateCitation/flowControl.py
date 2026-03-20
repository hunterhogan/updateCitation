"""Orchestrate the full citation update workflow.

(AI generated docstring)

You can use this module to run the complete citation update process. The
module reads settings from `pyproject.toml` [1], aggregates citation metadata
from the existing CITATION.cff file, PyPA metadata, GitHub release data,
and PyPI release data, then writes a validated CITATION.cff file and
optionally commits and pushes the result.

Contents
--------
Functions
	here
		Run the full citation update workflow from `pyproject.toml` to CITATION.cff.

References
----------
[1] pyproject.toml specification - Python Packaging User Guide
	https://packaging.python.org/en/latest/specifications/pyproject-toml/

"""
from os import PathLike
from pathlib import Path
from typing import Any
from updateCitation import (
	add_pyprojectDOTtoml, addCitation, addGitHubRelease, addGitHubSettings, addPyPAMetadata, addPyPIrelease, CitationNexus,
	filename_pyprojectDOTtomlDEFAULT, getSettingsPackage, gittyUpGitAmendGitHub, SettingsPackage, writeCitation)

def here(pathFilename_pyprojectDOTtoml: str | PathLike[Any] | None = None) -> None:
	"""Run the full citation update workflow from `pyproject.toml` to CITATION.cff.

	(AI generated docstring)

	You can call `here` to execute the complete citation update pipeline.
	The function reads package settings via `getSettingsPackage` [1], populates
	a `CitationNexus` [2] from `pyproject.toml` [3] author data, the existing
	CITATION.cff file, PyPA metadata, GitHub release information, and PyPI
	release data. The function then writes a validated CITATION.cff file using
	`writeCitation` [4] and optionally commits and pushes the changes via
	`gittyUpGitAmendGitHub` [5].

	Parameters
	----------
	pathFilename_pyprojectDOTtoml : str | PathLike[Any] | None = None
		The full path to the `pyproject.toml` file. If `None`, the function
		uses the current working directory with the default filename.

	Raises
	------
	ValueError
		If the package name (`nexusCitation.title`) is `None` after reading
		`pyproject.toml`.

	Examples
	--------
	Real usage from Z0Z_runUpdateCitation.py:

		import updateCitation
		updateCitation.here()

	References
	----------
	[1] updateCitation.pyprojectDOTtoml.getSettingsPackage
		Internal package reference
	[2] updateCitation.variables.CitationNexus
		Internal package reference
	[3] pyproject.toml specification - Python Packaging User Guide
		https://packaging.python.org/en/latest/specifications/pyproject-toml/
	[4] updateCitation.citationFileFormat.writeCitation
		Internal package reference
	[5] updateCitation.github.gittyUpGitAmendGitHub
		Internal package reference

	"""
	pathFilenameSettingsSSOT: Path = Path(pathFilename_pyprojectDOTtoml) if pathFilename_pyprojectDOTtoml else Path.cwd() / filename_pyprojectDOTtomlDEFAULT
	truth: SettingsPackage = getSettingsPackage(pathFilenameSettingsSSOT)

	nexusCitation: CitationNexus = CitationNexus()

	nexusCitation = add_pyprojectDOTtoml(nexusCitation, truth)

	if not nexusCitation.title:
		# TODO learn how to change the field from `str | None` to `str` after the field is populated
		# especially for a required field
		message = "Package name is required."
		raise ValueError(message)

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

	validationStatus: bool = writeCitation(nexusCitation, truth.pathFilenameCitationSSOT, truth.pathFilenameCitationDOTcffRepository)

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
