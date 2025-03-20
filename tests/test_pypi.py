import pytest
from tests.conftest import standardizedEqualTo
from updateCitation.pypi import getPyPIrelease

@pytest.mark.parametrize("nexusCitationTesting, expected", [
({"title": "numpy", "version": "1.23.5"}, {"repositoryDASHartifact": "https://pypi.org/project/numpy/1.23.5/"}),
({"title": "scikit-learn", "version": "1.2.2"}, {"repositoryDASHartifact": "https://pypi.org/project/scikit-learn/1.2.2/"}),
({"title": "Requests", "version": "2.28.2"}, {"repositoryDASHartifact": "https://pypi.org/project/requests/2.28.2/"}),
({"title": "Orion", "version": "5.7.11"}, {"repositoryDASHartifact": "https://pypi.org/project/orion/5.7.11/"}),
({"title": "Taurus", "version": "11.13.17"}, {"repositoryDASHartifact": "https://pypi.org/project/taurus/11.13.17/"}),
({"version": "1.0.0"}, ValueError),
({"title": "pandas"}, ValueError),
({}, ValueError), ], indirect=["nexusCitationTesting"] )
def test_getPyPIrelease(nexusCitationTesting: dict[str, str], expected: dict[str, str] | type[ValueError]) -> None:
	"""Test PyPI release info retrieval with various package names and versions."""
	standardizedEqualTo(expected, getPyPIrelease, nexusCitationTesting)
