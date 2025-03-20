"""SSOT for Pytest."""
from collections.abc import Generator, Callable
from typing import Any
from updateCitation import CitationNexus, CitationNexusFieldsProtected, filename_pyprojectDOTtomlDEFAULT, SettingsPackage
from pathlib import Path
import pytest
import shutil
import uuid

# SSOT for test data paths and filenames
pathDataSamples = Path("tests/dataSamples")
pathFilenameCitationAlphaDOTcff = pathDataSamples / "citationAlpha.cff"
pathTmpRoot = pathDataSamples / "tmp"

@pytest.fixture(scope="session", autouse=True)
def setupTeardownTestSession() -> Generator[None]:
	pathDataSamples.mkdir(exist_ok=True)
	pathTmpRoot.mkdir(exist_ok=True)
	yield
	shutil.rmtree(pathTmpRoot, ignore_errors=True)

@pytest.fixture(autouse=True)
def resetCitationNexusProtectedFields() -> None:
	"""Reset the protected fields set before each test to prevent test interference."""
	CitationNexusFieldsProtected.clear()

@pytest.fixture
def pathTmpTesting(request: pytest.FixtureRequest) -> Path:
	"""'path' means directory or folder, not file."""
	pathTmp = pathTmpRoot / uuid.uuid4().hex
	pathTmp.mkdir(parents=True, exist_ok=False)
	return pathTmp

@pytest.fixture
def pathFilenameTmpTesting(request: pytest.FixtureRequest) -> Path:
	"""'filename' means file; 'pathFilename' means the full path and filename."""
	try:
		extension = request.param
	except AttributeError:
		extension = ".txt"

	uuidString = uuid.uuid4().hex
	pathFilenameTmp = Path(pathTmpRoot, uuidString[0:-8], uuidString[-8:None] + extension)
	pathFilenameTmp.parent.mkdir(parents=True, exist_ok=False)
	return pathFilenameTmp

@pytest.fixture
def nexusCitationTesting(request: pytest.FixtureRequest) -> CitationNexus:
	"""Return a CitationNexus object with the specified attributes."""
	try:
		attributes: dict[str, Any] = request.param
	except AttributeError:
		attributes = {}

	return CitationNexus(**attributes)

@pytest.fixture
def citationAlphaDOTcff() -> Path:
	return pathFilenameCitationAlphaDOTcff

"""
Section: Pytest fixtures for testing the updateCitation package"""

@pytest.fixture
def settingsPackageTesting() -> SettingsPackage:
	return SettingsPackage(
		pathFilenamePackageSSOT= pathDataSamples / filename_pyprojectDOTtomlDEFAULT,
		GITHUB_TOKEN="FAKE_TOKEN",
		gitUserEmail="test@example.com",
		gitUserName="TestUserName",
		gitCommitMessage="TestCommitMessage",
	)

"""
Section: Standardized assert statements and failure messages"""

def uniformTestFailureMessage(expected: Any, actual: Any, functionName: str, *arguments: Any, **keywordArguments: Any) -> str:
	"""Format assertion message for any test comparison."""
	listArgumentComponents = [str(parameter) for parameter in arguments]
	listKeywordComponents = [f"{key}={value}" for key, value in keywordArguments.items()]
	joinedArguments = ', '.join(listArgumentComponents + listKeywordComponents)

	return (f"\nTesting: `{functionName}({joinedArguments})`\n"
			f"Expected: {expected}\n"
			f"Got: {actual}")

def standardizedEqualTo(expected: Any, functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
	"""Template for most tests to compare the actual outcome with the expected outcome, including expected errors."""
	if type(expected) == type[Exception]:
		messageExpected = expected.__name__
	else:
		messageExpected = expected

	try:
		messageActual = actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual = type(actualError).__name__
		actual = type(actualError)

	assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
