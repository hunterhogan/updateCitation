# import os
# from updateCitation import flowControl
# import pathlib
# import pytest
# from tests.conftest import standardizedEqualTo, cffDASHversionDefaultHARDCODED, messageDefaultHARDCODED, CitationNexus, SettingsPackage, get_pyprojectDOTtoml

# # Dummy implementations to record call order.
# def dummy_add_pyprojectDOTtoml(nexusCitation: CitationNexus, truth: SettingsPackage) -> tuple[CitationNexus, SettingsPackage]:
# 	callOrder.append("add_pyprojectDOTtoml")
# 	truth = get_pyprojectDOTtoml(truth)  # Populate truth.tomlPackageData from the pyproject.toml file.
# 	# Set required fields to avoid ValueError from setInStone.
# 	nexusCitation.title = truth.tomlPackageData.get("name")
# 	nexusCitation.authors = truth.tomlPackageData.get("authors", [])
# 	# Supply a dummy contact if absent.
# 	contactData = truth.tomlPackageData.get("contact")
# 	if not contactData:
# 		nexusCitation.contact = [{"name": "Dummy", "email": "dummy@example.com"}]
# 	else:
# 		nexusCitation.contact = contactData
# 	return nexusCitation, truth

# def dummy_addCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT) -> CitationNexus:
# 	callOrder.append("addCitation")
# 	return nexusCitation

# def dummy_addPyPAMetadata(nexusCitation: CitationNexus, tomlPackageData: dict) -> CitationNexus:
# 	callOrder.append("addPyPAMetadata")
# 	return nexusCitation

# def dummy_addGitHubSettings(truth: SettingsPackage) -> SettingsPackage:
# 	callOrder.append("addGitHubSettings")
# 	return truth

# def dummy_addGitHubRelease(nexusCitation: CitationNexus, truth: SettingsPackage) -> CitationNexus:
# 	callOrder.append("addGitHubRelease")
# 	return nexusCitation

# def dummy_addPyPIrelease(nexusCitation: CitationNexus) -> CitationNexus:
# 	callOrder.append("addPyPIrelease")
# 	return nexusCitation

# def dummy_writeCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT, pathFilenameCitationDOTcffRepository) -> bool:
# 	callOrder.append("writeCitation")
# 	return True

# def dummy_gittyUpGitPushGitHub(truth: SettingsPackage, nexusCitation: CitationNexus, pathFilenameCitationSSOT, pathFilenameCitationDOTcffRepository) -> bool:
# 	callOrder.append("gittyUpGitPushGitHub")
# 	return True

# @pytest.fixture
# def validTomlTmpFile(tmp_path: pathlib.Path) -> pathlib.Path:
# 	pathFilename = tmp_path / "pyproject.toml"
# 	tomlContent = """
# [project]
# name = "ValidTitle"
# authors = [{name = "John Doe", email = "john@example.com"}]
# contact = [{name = "Contact Name", email = "contact@example.com"}]
# """
# 	pathFilename.write_text(tomlContent)
# 	return pathFilename

# @pytest.fixture
# def missingTitleTomlTmpFile(tmp_path: pathlib.Path) -> pathlib.Path:
# 	pathFilename = tmp_path / "pyproject.toml"
# 	# Missing the "name" key.
# 	tomlContent = """
# [project]
# authors = [{name = "John Doe", email = "john@example.com"}]
# contact = [{name = "Contact Name", email = "contact@example.com"}]
# """
# 	pathFilename.write_text(tomlContent)
# 	return pathFilename

# def restore_flowControl(monkeypatch) -> None:
# 	# Restore original functions (if needed in further tests) by deleting our attributes.
# 	for name in ["add_pyprojectDOTtoml", "addCitation", "addPyPAMetadata", "addGitHubRelease", "addPyPIrelease", "writeCitation"]:
# 		if hasattr(flowControl, name):
# 			monkeypatch.undo()

# def test_here_valid(validTomlTmpFile: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
# 	global callOrder
# 	callOrder = []  # type: list[str]

# 	# Override functions in flowControl, recording call order.
# 	monkeypatch.setattr(flowControl, "add_pyprojectDOTtoml", dummy_add_pyprojectDOTtoml)
# 	monkeypatch.setattr(flowControl, "addCitation", dummy_addCitation)
# 	monkeypatch.setattr(flowControl, "addPyPAMetadata", dummy_addPyPAMetadata)
# 	monkeypatch.setattr(flowControl, "addGitHubSettings", dummy_addGitHubSettings)
# 	monkeypatch.setattr(flowControl, "addGitHubRelease", dummy_addGitHubRelease)
# 	monkeypatch.setattr(flowControl, "addPyPIrelease", dummy_addPyPIrelease)
# 	monkeypatch.setattr(flowControl, "writeCitation", dummy_writeCitation)
# 	monkeypatch.setattr(flowControl, "gittyUpGitPushGitHub", dummy_gittyUpGitPushGitHub)

# 	# Call here() with our valid temporary pyproject.toml.
# 	flowControl.here(validTomlTmpFile)

# 	# Verify call order.
# 	expectedOrder = [
# 		"add_pyprojectDOTtoml",
# 		"addCitation",
# 		"addPyPAMetadata",
# 		"addGitHubSettings",
# 		"addGitHubRelease",
# 		"addPyPIrelease",
# 		"writeCitation",
# 		"gittyUpGitPushGitHub"
# 	]
# 	assert callOrder == expectedOrder

# def test_here_missingTitle(missingTitleTomlTmpFile: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
# 	# Override add_pyprojectDOTtoml to mimic its normal behavior so that title remains None.
# 	def dummy_noTitle(nexusCitation: CitationNexus, truth: SettingsPackage) -> tuple[CitationNexus, SettingsPackage]:
# 		# Do not set title.
# 		nexusCitation.authors = truth.tomlPackageData.get("authors", [])
# 		nexusCitation.contact = truth.tomlPackageData.get("contact", [])
# 		# This will cause setInStone to raise ValueError.
# 		nexusCitation.setInStone("pyprojectDOTtoml")
# 		return nexusCitation, truth

# 	monkeypatch.setattr(flowControl, "add_pyprojectDOTtoml", dummy_noTitle)

# 	with pytest.raises(ValueError):
# 		flowControl.here(missingTitleTomlTmpFile)
