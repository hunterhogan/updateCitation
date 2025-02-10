"""SSOT for Pytest."""
from typing import Generator, Any, Type, Callable
import pathlib
from updateCitation import (
    add_pyprojectDOTtoml,
    addCitation,
    addGitHubRelease,
    addPyPAMetadata,
    addPyPIrelease,
    CitationNexus,
    flowControl,
    getSettingsPackage,
    SettingsPackage,
)
from updateCitation.github import getGitHubRelease
from updateCitation.pypa import getPyPAMetadata
from updateCitation.pypi import getPyPIrelease
from updateCitation.pyprojectDOTtoml import get_pyprojectDOTtoml
from updateCitation.variables import cffDASHversionDEFAULT, CitationNexusFieldsRequired, messageDEFAULT
import pytest
import shutil
import uuid

# SSOT for test data paths and filenames
pathDataSamples = pathlib.Path("tests/dataSamples")
pathFilenameCitationAlphaDOTcff = pathDataSamples / "citationAlpha.cff"
pathTmpRoot = pathDataSamples / "tmp"

@pytest.fixture(scope="session", autouse=True)
def setupTeardownTestSession() -> Generator[None, None, None]:
    pathDataSamples.mkdir(exist_ok=True)
    pathTmpRoot.mkdir(exist_ok=True)
    yield
    shutil.rmtree(pathTmpRoot, ignore_errors=True)

@pytest.fixture
def pathTmpTesting(request: pytest.FixtureRequest) -> pathlib.Path:
    """'path' means directory or folder, not file."""
    pathTmp = pathTmpRoot / uuid.uuid4().hex
    pathTmp.mkdir(parents=True, exist_ok=False)
    return pathTmp

@pytest.fixture
def pathFilenameTmpTesting(request: pytest.FixtureRequest) -> pathlib.Path:
    """'filename' means file; 'pathFilename' means the full path and filename."""
    try:
        extension = request.param
    except AttributeError:
        extension = ".txt"

    uuidString = uuid.uuid4().hex
    pathFilenameTmp = pathlib.Path(pathTmpRoot, uuidString[0:-8], uuidString[-8:None] + extension)
    pathFilenameTmp.parent.mkdir(parents=True, exist_ok=False)
    return pathFilenameTmp

@pytest.fixture
def nexusCitationTesting(request: pytest.FixtureRequest) -> CitationNexus:
    """Return a CitationNexus object with the specified attributes."""
    try:
        attributes = request.param
    except AttributeError:
        attributes = {}

    return CitationNexus(**attributes)

@pytest.fixture
def citationAlphaDOTcff() -> pathlib.Path:
    return pathFilenameCitationAlphaDOTcff

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

def standardizedEqualTo(expected: Any, functionTarget: Callable, *arguments: Any, **keywordArguments: Any) -> None:
    """Template for most tests to compare the actual outcome with the expected outcome, including expected errors."""
    if type(expected) == Type[Exception]:
        messageExpected = expected.__name__
    else:
        messageExpected = expected

    try:
        messageActual = actual = functionTarget(*arguments, **keywordArguments)
    except Exception as actualError:
        messageActual = type(actualError).__name__
        actual = type(actualError)

    assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
