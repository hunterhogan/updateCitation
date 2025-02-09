import pathlib
from updateCitation.citationFileFormat import addCitation
from updateCitation.variables import CitationNexus
from tests.conftest import citationAlphaDOTcff, standardizedEqualTo

# Redesigning the flow invalidated all of the tests in this file.
# def test_getNexusCitation(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns a CitationNexus object."""
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     assert isinstance(nexusCitation, CitationNexus), "getNexusCitation() should return a CitationNexus object."

# def test_getNexusCitation_cffVersion(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct cffversion."""
#     expected = "1.2.0"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.cffDASHversion
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_message(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct message."""
#     expected = "If you use this software, you can cite it using the metadata from this file."
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.message
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_authors(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct authors."""
#     expected = [{'given-names': 'Hunter', 'family-names': 'Hogan', 'email': 'HunterHogan@pm.me'}]
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.authors
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_commit(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct commit."""
#     expected = "0d70eb67ffbab9563208ec06294887fb7fa6768a"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.commit
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_dateReleased(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct dateReleased."""
#     expected = "2025-02-07"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.dateDASHreleased
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_identifiers(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct identifiers."""
#     expected = [{'type': 'url', 'value': 'https://github.com/hunterhogan/mapFolding/releases/tag/0.3.9', 'description': 'The URL for mapFolding 0.3.9.'}]
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.identifiers
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_keywords(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct keywords."""
#     expected = ['A001415', 'A001416', 'A001417', 'A001418', 'A195646', 'folding', 'map folding', 'OEIS', 'stamp folding']
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.keywords
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_license(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct license."""
#     expected = "CC-BY-NC-4.0"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.license
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_repository(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct repository."""
#     expected = "https://github.com/hunterhogan/mapFolding.git"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.repository
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_repositoryArtifact(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct repositoryArtifact."""
#     expected = "https://pypi.org/project/mapfolding/0.3.9/"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.repositoryDASHartifact
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_repositoryCode(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct repositoryCode."""
#     expected = "https://github.com/hunterhogan/mapFolding/releases/tag/0.3.9"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.repositoryDASHcode
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_title(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct title."""
#     expected = "mapFolding"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.title
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_type(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct type."""
#     expected = "software"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.type
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_url(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct url."""
#     expected = "https://github.com/hunterhogan/mapFolding"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.url
#     standardizedEqualTo(expected, lambda: actual)

# def test_getNexusCitation_version(citationAlphaDOTcff: pathlib.Path):
#     """Test that getNexusCitation() returns the correct version."""
#     expected = "0.3.9"
#     nexusCitation = addCitation(citationAlphaDOTcff)
#     actual = nexusCitation.version
#     standardizedEqualTo(expected, lambda: actual)
